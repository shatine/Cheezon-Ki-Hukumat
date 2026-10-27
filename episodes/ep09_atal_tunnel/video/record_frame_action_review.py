"""실제 첫 프레임을 본 root의 명시적 결정을 기계 검증한 뒤 검토 원장 한 행만 기록한다.

이 도구는 그림을 보거나 시각 판정을 만들지 않는다. Muse 생성 승인도 기록하지 않는다.
예: root가 선택 PNG 원본과 현재 영어 동작을 직접 확인한 뒤 결정 JSON을 작성한다.

{
  "id": "p001",
  "reviewed": true,
  "compatible": true,
  "required_features_present": true,
  "root_opened_selected_png_original": true,
  "expected_pick_file": "<actual picks entry file>",
  "expected_pick_sha256": "<actual picks entry sha256>",
  "expected_motion_contract_sha256": "<current draft row motion_contract_sha256>",
  "notes": "<what root actually checked in this PNG against this action>"
}

PowerShell:
python 'D:\\youtube\\Cheezon-Ki-Hukumat\\episodes\\ep09_atal_tunnel\\video\\record_frame_action_review.py' --decision 'D:\\youtube\\7. Cheezon Ki Hukumat\\episodes\\09_atal_tunnel\\review_edit\\frame_action_decisions\\p001.json'

선택 파일은 picks 실제 항목에서만 찾는다. 파일명/원장 SHA/실제 PNG SHA/현재 동작 계약이
모두 일치해야 한다. --episode-root/--media-root는 다른 체크아웃 또는 격리 fixture용이다.
명시 결정이 없거나 false/누락/불일치가 있으면 원장을 쓰지 않고 종료 코드 2로 거부한다.
원장 쓰기는 한 번에 한 프로세스만 직렬 실행한다. 이 CLI 또는 영상 생성기의
--draft/--ready가 끝나기 전에 다른 원장 쓰기 명령을 동시에 시작하지 않는다.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import hashlib
import json
import os
import re
import struct
import sys
import tempfile
from pathlib import Path

EP = Path(__file__).resolve().parent.parent
MEDIA = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
INPUTS = ("plan/shot_list_v1.json", "plan/scene_catalog_v1.json", "images/prompts_v1.json")


class Rejected(ValueError):
    pass


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(path):
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode("utf-8")).hexdigest()


def require(condition, message):
    if not condition:
        raise Rejected(message)


def hex_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def record_review(episode_root, media_root, decision_path):
    decision_bytes = decision_path.read_bytes()
    decision_sha = hashlib.sha256(decision_bytes).hexdigest()
    decision = json.loads(decision_bytes.decode("utf-8-sig"))
    require(isinstance(decision, dict), "Decision must be an explicit JSON object")
    sid = decision.get("id")
    require(isinstance(sid, str) and sid, "Missing explicit source id")
    for field in ("reviewed", "compatible", "required_features_present", "root_opened_selected_png_original"):
        require(decision.get(field) is True, f"Explicit {field}=true is required; no automatic visual judgment is made")
    require(isinstance(decision.get("notes"), str) and bool(decision["notes"].strip()), "Explicit review notes are required")
    expected_file = decision.get("expected_pick_file")
    require(isinstance(expected_file, str) and Path(expected_file).name == expected_file and expected_file.lower().endswith(".png"), "Expected pick must be an explicit PNG basename")
    for field in ("expected_pick_sha256", "expected_motion_contract_sha256"):
        require(hex_sha(decision.get(field)), f"Missing or invalid explicit {field}")

    picks_path = episode_root / "images/picks_v1.json"
    draft_path = episode_root / "video/vprompts_v1_draft.json"
    checks_path = episode_root / "video/first_frame_action_checks_v1.json"
    hashes_before = {p: sha_file(p) for p in (picks_path, draft_path, checks_path,
                                             *(episode_root / rel for rel in INPUTS))}
    hashes_before[decision_path] = decision_sha
    picks, draft, checks = load(picks_path), load(draft_path), load(checks_path)
    image_rows = load(episode_root / "images/prompts_v1.json")
    image_defs = [x for x in image_rows if x.get("id") == sid]
    require(len(image_defs) == 1 and image_defs[0].get("kind") == "frame", "ID is not exactly one current video first-frame definition; masters/images are not accepted")
    image_def = image_defs[0]
    require(isinstance(draft, dict) and isinstance(draft.get("clips"), list), "Current video draft is unavailable")
    for rel in INPUTS:
        require(draft.get("inputs", {}).get(rel) == canonical_sha(episode_root / rel), f"Video draft input is stale: {rel}; regenerate --draft before reviewing")
    rows = [x for x in draft["clips"] if x.get("id") == sid]
    require(len(rows) == 1, "ID is missing or duplicated in the current draft")
    row = rows[0]
    require(row.get("source_ids") == image_def.get("source_ids") and row.get("source_image_prompt") == image_def.get("prompt")
            and row.get("initial_state") == image_def.get("initial_state") and row.get("source_reference_group") == image_def.get("ref"),
            "Draft frame definition differs from the current image prompt")
    contract = dict(prompt=row["prompt"], required_existing_features=row["required_existing_features"],
                    initial_state=row.get("initial_state"), source_image_prompt=row["source_image_prompt"],
                    source_reference=row.get("source_reference_group"), source_ids=row["source_ids"])
    contract_sha = hashlib.sha256(json.dumps(contract, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    require(row.get("motion_contract_sha256") == contract_sha == decision["expected_motion_contract_sha256"], "Current motion contract SHA differs from the explicit decision")

    selected = picks.get("picks", {}).get(sid)
    require(isinstance(selected, dict), "No actual selected PNG exists in the pick ledger for this frame ID")
    require(str(selected.get("visual_status", "")).startswith("chosen_"), "Pick ledger has no chosen visual decision")
    require(selected.get("root_opened_clean_original") is True or selected.get("raw_and_cleaned_opened_at_original_size") is True,
            "Pick ledger lacks explicit original-size review of the selected clean PNG")
    require(selected.get("file") == expected_file, "Expected PNG filename differs from the actual pick ledger")
    require(selected.get("sha256") == decision["expected_pick_sha256"], "Expected PNG SHA differs from the actual pick ledger")
    image_dir = (media_root / "img").resolve(strict=True)
    actual_path = (image_dir / selected["file"]).resolve(strict=True)
    require(actual_path.parent == image_dir, "Selected PNG resolves outside the declared actual image directory")
    actual_sha = sha_file(actual_path)
    require(actual_sha == selected["sha256"], "Actual selected PNG SHA differs from the pick ledger")
    header = actual_path.read_bytes()[:24]
    require(len(header) == 24 and header[:8] == b"\x89PNG\r\n\x1a\n", "Selected file is not a PNG")
    require(list(struct.unpack(">II", header[16:24])) == selected.get("dimensions"), "Actual PNG dimensions differ from the pick ledger")
    require(isinstance(checks.get("clips"), dict) and isinstance(checks["clips"].get(sid), dict), "Target row is missing from the existing action-check manifest")
    updated = copy.deepcopy(checks)
    updated["clips"][sid].update(
        reviewed=True, compatible=True, required_features_present=True,
        root_opened_selected_png_original=True,
        confirmed_pick_file=selected["file"], confirmed_pick_sha256=actual_sha,
        confirmed_motion_contract_sha256=contract_sha, notes=decision["notes"].strip(),
        decision_source_file=str(decision_path.resolve()), decision_source_sha256=decision_sha,
        declaration_basis="explicit root decision JSON; helper performed no visual review",
        recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    )
    for path, old_sha in hashes_before.items():
        require(sha_file(path) == old_sha, f"Input changed during validation; retry with a current decision: {path.name}")
    # Atomic replacement only after every condition passed; unrelated rows and metadata are preserved.
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=checks_path.parent,
                                         prefix=".frame_review_", suffix=".tmp", delete=False) as handle:
            temp_path = Path(handle.name)
            handle.write(json.dumps(updated, ensure_ascii=False, indent=2) + "\n")
        os.replace(temp_path, checks_path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()
    return dict(status="explicit_root_declaration_recorded_mechanical_checks_passed", id=sid,
                updated_manifest=str(checks_path), updated_rows=1, selected_file=str(actual_path),
                selected_sha256=actual_sha, motion_contract_sha256=contract_sha,
                visual_review_performed_by_helper=False, muse_submission_performed=False,
                claim_source="the explicit root decision; this output is not an automatic visual pass")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--decision", required=True, type=Path)
    parser.add_argument("--episode-root", type=Path, default=EP)
    parser.add_argument("--media-root", type=Path, default=MEDIA)
    args = parser.parse_args()
    try:
        report = record_review(args.episode_root, args.media_root, args.decision)
    except (Rejected, OSError, KeyError, TypeError, ValueError) as exc:
        print(json.dumps(dict(status="rejected_no_manifest_update", reason=str(exc),
                              visual_review_performed_by_helper=False), ensure_ascii=False, indent=2))
        raise SystemExit(2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
