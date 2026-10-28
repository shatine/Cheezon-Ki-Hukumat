"""Prepare an offline image queue from current picks, records and upload policy.

Recorded failures remain history, not a current service-block claim. Recorded
output is not a visual pass. This script makes no browser/upload/generation,
selection or approval calls. Pending outputs must receive a root decision first.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def project_id(url):
    match = re.match(r'https://flow\.google\.com/project/([0-9a-f-]+)(?:/|$)', url or '')
    return match[1] if match else None


def refs(row):
    value = row.get('ref')
    return value.split('+') if isinstance(value, str) else value or []


def main():
    rows = read_json(HERE / 'prompts_v1.json')
    manifest = {row['id']: row for row in rows}
    if len(manifest) != len(rows):
        raise ValueError('Duplicate manifest IDs')
    ledger_bytes = (HERE / 'picks_v1.json').read_bytes()
    ledger = json.loads(ledger_bytes.decode('utf-8-sig'))
    picks = ledger['picks']
    policy = read_json(HERE / 'flow_project_policy_v1.json')
    current_id = policy['current_generation_project_id']
    if current_id not in policy['allowed_result_project_ids']:
        raise ValueError('Current generation project must be explicitly allowed')
    approval = read_json(HERE / 'upload_approval_v1.json')
    matches = approval['destination']['project_id'] == current_id
    authorized = approval.get('authorized') is True and matches
    confirmed = approval.get('confirmed_upload') is True and matches
    alias_confirmed = approval.get('confirmed_upload_identity_alias') is True and matches
    progress_path = HERE / 'generation_progress.json'
    progress = read_json(progress_path) if progress_path.exists() else {}
    attempts, decisions, failures, successes, pending = {}, {}, [], [], {}
    for review in ledger['review_log']:
        item = review['input']
        attempts[item['id']] = max(attempts.get(item['id'], 0), item['attempt'])
        decisions[(item['id'], item['attempt'])] = item['decision']
    for path in sorted((HERE / 'generation_records_v1').glob('*.json')):
        item = read_json(path)
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or type(item.get('attempt')) is not int:
            continue
        sid, attempt = item['id'], item['attempt']
        attempts[sid] = max(attempts.get(sid, 0), attempt)
        result = item.get('result', {})
        media = result.get('result_media_source_url')
        pid = item.get('flow_project_id') or project_id(result.get('container_editor_url'))
        record = path.relative_to(HERE).as_posix()
        if str(item.get('status', '')).startswith('failed'):
            failures.append(dict(id=sid, attempt=attempt, record=record,
                reported_status=item['status'], project_id=pid,
                observed_at_utc=result.get('observed_at_utc'), result_media_source_url=media,
                treated_as_current_service_blocker=False))
        if isinstance(media, str) and re.fullmatch(r'https://flow-content\.google/image/[0-9a-f-]+', media):
            decision = decisions.get((sid, attempt))
            if pid == current_id:
                successes.append(dict(id=sid, attempt=attempt, record=record,
                    result_media_source_url=media, observed_at_utc=result.get('observed_at_utc'),
                    root_decision=decision or 'not_recorded_in_pick_ledger',
                    currently_selected=picks.get(sid, {}).get('attempt') == attempt))
            if decision is None:
                pending.setdefault(sid, []).append(dict(attempt=attempt, record=record))

    def masters(sid, trail=()):
        if sid in trail or sid not in manifest:
            raise ValueError(f'Unknown/cyclic reference dependency: {trail + (sid,)}')
        if manifest[sid]['kind'] == 'master':
            return {sid}
        return set().union(*(masters(ref, trail + (sid,)) for ref in refs(manifest[sid])))

    queue = []
    for row in rows:
        sid = row['id']
        if sid in picks:
            continue
        required = refs(row)
        missing = [ref for ref in required if ref not in picks]
        master_ids = sorted(masters(sid))
        external_masters = [ref for ref in master_ids if ref in picks and project_id(picks[ref].get('flow_url')) != current_id]
        external_other = [ref for ref in required if ref in picks and manifest[ref]['kind'] != 'master'
                          and project_id(picks[ref].get('flow_url')) != current_id]
        gates = []
        if sid in pending:
            gates.append('await_existing_output_root_decision_do_not_resubmit')
        if missing:
            gates.append('await_prior_root_pick')
        if external_masters:
            gates.append('await_explicit_six_master_upload_approval' if not authorized else
                         'await_verified_master_upload_identity_and_live_UI_reference' if not (confirmed and alias_confirmed) else
                         'verify_exact_master_alias_and_live_UI_reference_before_submit')
        if external_other:
            gates.append('cross_project_nonmaster_reference_needs_observed_availability_or_separate_transfer_approval')
        state = gates[0] if gates else ('selected_server_references_need_live_exact_revision_check'
                                       if required else 'no_reference_required_live_UI_check')
        queue.append(dict(id=sid, kind=row['kind'], ref=row.get('ref'),
            next_attempt=attempts.get(sid, 0) + 1,
            latest_prompt_sha256=hashlib.sha256(row['prompt'].encode('utf-8')).hexdigest(),
            missing_selected_references=missing, master_dependencies=master_ids,
            cross_project_selected_masters=external_masters,
            cross_project_selected_nonmasters=external_other,
            existing_unreviewed_outputs=pending.get(sid, []),
            blocking_conditions=gates, reference_state=state))
    report = dict(status='preparation_only_master_upload_approval_pending' if not authorized else 'preparation_only_live_reference_checks_required',
        scope='Offline queue only; no claim of current live service availability or visual approval',
        actual_submission_performed=False, actual_video_generation_authorized=False,
        expected_images=len(rows), selected_images=len(picks), remaining_images=len(queue),
        selected_video_frames=sum(row['kind'] == 'frame' and row['id'] in picks for row in rows),
        reviewed_attempts=len(ledger['review_log']), picks_snapshot_sha256=hashlib.sha256(ledger_bytes).hexdigest(),
        current_project=f'https://flow.google.com/project/{current_id}',
        current_project_source='flow_project_policy_v1.json, not the historical progress snapshot',
        service_status='current_project_outputs_recorded_live_UI_check_still_required' if successes else 'no_current_project_success_record_available_live_UI_check_required',
        recorded_current_project_outputs=successes,
        selected_current_project_output_count=sum(x['currently_selected'] for x in successes),
        historical_failed_attempts=failures,
        historical_progress_snapshot=dict(file='generation_progress.json', recorded_at=progress.get('recorded_at'),
            project=progress.get('project'), latest_failure_record=progress.get('latest_failure_record'),
            used_as_current_service_or_operator_state=False),
        blocker='Specific transfer of the six selected local master PNGs to the current Google Flow account awaits explicit user approval. Unaffected server-reference/ref-null work remains separately eligible for live UI checks.' if not authorized else 'Approval alone does not verify upload identity or actual per-submission input.',
        local_master_upload=dict(approval_file='upload_approval_v1.json', authorized=authorized,
            confirmed_upload=confirmed, confirmed_upload_identity_alias=alias_confirmed,
            approval_matches_current_project=matches,
            actual_upload_count='unknown; an earlier connection failure does not prove zero transfers',
            automatic_review_rejection=approval.get('automatic_review_rejection'),
            prior_attempt_uncertainty=approval.get('prior_attempt_uncertainty')),
        resume_gate='Honor pending root decisions and specific local-transfer approval. Inspect live UI and exact input revisions before each one-image submission. No upload/video approval is granted by this script.',
        ordering='Manifest order; selected IDs omitted; existing unreviewed outputs need a root decision before retry.',
        state_counts=dict(Counter(x['reference_state'] for x in queue)),
        without_local_transfer_candidates_for_root_live_UI_check=[x['id'] for x in queue if not x['blocking_conditions']], queue=queue)
    (HERE / 'resume_queue_v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], selected=len(picks), remaining=len(queue),
        current_project_recorded_outputs=len(successes),
        without_local_transfer_candidates=report['without_local_transfer_candidates_for_root_live_UI_check'],
        pending_root_decisions=[x['id'] for x in queue if x['existing_unreviewed_outputs']],
        states=report['state_counts'], submissions_by_this_script=0), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
