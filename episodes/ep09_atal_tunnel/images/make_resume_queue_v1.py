"""Prepare an image-only resume queue from current picks and exact prompt bytes.

No network/browser/generation calls and no visual approval. A service block is
not cleared by running this script. Selected IDs are never submitted again.
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = json.loads((HERE / 'prompts_v1.json').read_text(encoding='utf-8-sig'))
ledger = json.loads((HERE / 'picks_v1.json').read_text(encoding='utf-8-sig'))
picks = ledger['picks']
attempts = {}
for item in ledger['review_log']:
    source = item['input']
    attempts[source['id']] = max(attempts.get(source['id'], 0), source['attempt'])
for path in (HERE / 'generation_records_v1').glob('*.json'):
    item = json.loads(path.read_text(encoding='utf-8-sig'))
    if isinstance(item, dict) and isinstance(item.get('id'), str) and type(item.get('attempt')) is int:
        attempts[item['id']] = max(attempts.get(item['id'], 0), item['attempt'])
queue = []
for row in rows:
    if row['id'] in picks:
        continue
    refs = (row['ref'].split('+') if isinstance(row.get('ref'), str) else row.get('ref') or [])
    missing = [ref for ref in refs if ref not in picks]
    queue.append(dict(id=row['id'], kind=row['kind'], ref=row.get('ref'),
                      next_attempt=attempts.get(row['id'], 0) + 1,
                      latest_prompt_sha256=hashlib.sha256(row['prompt'].encode('utf-8')).hexdigest(),
                      missing_selected_references=missing,
                      reference_state='await_prior_root_pick' if missing else 'references_selected_service_still_blocked'))
report = dict(status='preparation_only_service_blocked', actual_submission_performed=False,
              actual_video_generation_authorized=False, expected_images=len(rows), selected_images=len(picks),
              remaining_images=len(queue),
              blocker='Flow abnormal activity and reCAPTCHA connection error recurred on o003 attempt 1; see generation_records_v1/o003_1.json',
              resume_gate='Human confirms service issue resolved, then inspect current UI before any further submit. No repeated refresh, CAPTCHA solving, extension changes or local upload.',
              ordering='Current image manifest order; selected IDs omitted. Each input revision must match the exact selected source. One image at a time.',
              queue=queue)
(HERE / 'resume_queue_v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(status=report['status'], selected=len(picks), remaining=len(queue),
                      first_five=[dict(id=x['id'], attempt=x['next_attempt']) for x in queue[:5]],
                      dependency_waiting=[x['id'] for x in queue if x['missing_selected_references']],
                      submissions=0), ensure_ascii=False, indent=2))
