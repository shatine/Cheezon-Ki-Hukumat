"""Record the existing Flow source asset corresponding to each chosen reference.

The selected clean PNG remains the edit/video source. Its original Flow revision
identity is retained even when a different allowed project is used for new work.
This measures file correspondence, not project-media availability, actual UI
attachment, transfer, or visual quality. Observe the exact input before submission.
"""
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from record_review import (flow_project_id, load_flow_project_policy,
                           load_revision_observations, resolve_source_revision)

HERE = Path(__file__).resolve().parent
PC = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
project_policy = load_flow_project_policy()
prompts = json.loads((HERE / "prompts_v1.json").read_text(encoding="utf-8-sig"))
ledger = json.loads((HERE / "picks_v1.json").read_text(encoding="utf-8-sig"))
picks = ledger["picks"]
revision_observations = load_revision_observations(HERE / "source_revision_observations_v1.json")
refs = set()
for prompt in prompts:
    value = prompt.get("ref")
    if value:
        refs.update(value.split("+") if isinstance(value, str) else value)
entries = {}
for ref in sorted(refs):
    if ref not in picks:
        entries[ref] = {"status": "not_chosen"}
        continue
    pick = picks[ref]
    raw = PC / "img_raw" / pick["raw_file"]
    clean = PC / "img" / pick["file"]
    raw_bytes, clean_bytes = raw.read_bytes(), clean.read_bytes()
    raw_sha = hashlib.sha256(raw_bytes).hexdigest()
    clean_sha = hashlib.sha256(clean_bytes).hexdigest()
    if clean_sha != pick["sha256"]:
        raise ValueError(f"{ref}: clean PNG changed since the explicit chosen review")
    source_reviews = [row for row in ledger.get("review_log", [])
                      if row["input"]["id"] == ref and row["input"]["attempt"] == pick["attempt"]
                      and row["input"]["decision"] == "chosen"]
    if (len(source_reviews) != 1 or raw_sha != source_reviews[0]["measurements"]["raw"]["sha256"]
            or source_reviews[0]["input"]["flow_url"] != pick["flow_url"]):
        raise ValueError(f"{ref}: original bytes/Flow source do not match the explicit chosen review")
    # Decode the same bytes that were hashed; also supports Unicode PC paths.
    a = cv2.imdecode(np.frombuffer(raw_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    b = cv2.imdecode(np.frombuffer(clean_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    if a is None or b is None or a.shape != b.shape:
        raise ValueError(f"{ref}: raw/clean pixels unavailable or dimensions differ")
    height, width = a.shape[:2]
    changed = np.any(a != b, axis=2)
    yy, xx = np.where(changed)
    bbox = [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1] if len(xx) else None
    fraction = float(changed.mean())
    corner_only = bbox is None or (bbox[0] >= width * 0.75 and bbox[1] >= height * 0.7 and fraction <= 0.03)
    url = pick["flow_url"]
    source_project = flow_project_id(url, role="source")
    if source_project is None:
        raise ValueError(f"{ref}: source asset is outside the explicitly allowed episode projects")
    revision = resolve_source_revision(ref, pick["attempt"], ledger.get("review_log", []), revision_observations, PC / "img_raw")
    entries[ref] = {
        "status": ("requires_review_before_use" if not corner_only else
                   "source_correspondence_verified" if revision is not None else "revision_unresolved_do_not_use"),
        "transport": "not_determined_by_file_correspondence_observe_exact_input_before_submit",
        "flow_source_url": url, "flow_container_id": url.rsplit("/", 1)[-1],
        "flow_source_project_id": source_project,
        "current_generation_project_id": project_policy["current_generation_project_id"],
        "same_project_as_current_generation": source_project == project_policy["current_generation_project_id"],
        "availability_by_project": {pid: {"status": "not_checked_in_current_ui",
            "actual_ui_availability_observation_recorded": False}
            for pid in project_policy["allowed_source_project_ids"]},
        "source_media_url": revision["media_url"] if revision is not None else None,
        "source_revision_resolution": revision,
        "selected_attempt": pick["attempt"], "original_file": str(raw), "selected_clean_file": str(clean),
        "original_sha256": raw_sha,
        "selected_clean_sha256": clean_sha,
        "dimensions": [width, height], "changed_pixel_fraction": fraction,
        "changed_pixel_bbox_xyxy": bbox, "changes_confined_to_lower_right_processing_area": corner_only,
        "clean_png_reuploaded": None, "clean_png_upload_performed_by_this_script": False,
        "actual_ui_reference_attachment_verified_by_this_script": False,
        "note": "The editor URL is a mutable container, not an image revision. Use only the resolved source_media_url of this chosen attempt and observe the actual editor input before every submission. A later legacy observation retains its own real observation time; it does not backfill an earlier observation. Local dewm processing changes only the measured lower-right area."
    }
report = {
    "scope": "measured raw/clean correspondence and explicitly recorded image revision identity; not visual approval or actual UI attachment verification",
    "reason": "Chosen original revision identity remains bound to the reviewed files and original project. Project-media availability and transport in the current generation project have not been checked by this script; do not claim cross-project attachment, transfer or re-upload without an actual recorded UI observation.",
    "flow_project_policy": "images/flow_project_policy_v1.json",
    "current_generation_project_id": project_policy["current_generation_project_id"],
    "project_media_availability_verified_by_this_script": False,
    "edit_and_video_sources_remain_selected_clean_png": True,
    "references": entries
}
(HERE / "reference_assets_v1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({key: value["status"] for key, value in entries.items()}, ensure_ascii=False))
