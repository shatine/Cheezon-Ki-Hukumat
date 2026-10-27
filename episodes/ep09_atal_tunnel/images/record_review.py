"""Record the root reviewer's explicit decision; never infer a visual pass.

Usage: python record_review.py <decision.json>
Only picks_v1.json/md and a newly chosen img_selected copy are written.
Raw/clean images are measured, never edited or overwritten. Pillow is required.
"""
import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
MEDIA = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
RAW, CLEAN, SELECTED = (MEDIA / name for name in ("img_raw", "img", "img_selected"))
JSON_PATH, MD_PATH = HERE / "picks_v1.json", HERE / "picks_v1.md"
PROJECT = "baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd"
FIELDS = {"id", "attempt", "decision", "reason", "flow_url", "raw_file", "clean_file",
          "root_opened_raw_original", "root_opened_clean_original"}
OPTIONAL_FIELDS = {"actual_retake_reference_file"}
UI_REFERENCE_FIELDS = {"id", "flow_url", "source_media_url", "method", "observed_before_submit", "observed_by", "evidence"}
UI_REFERENCE_METHODS = {"project_media_attachment", "current_image_editor_input"}
REVISION_OBSERVATION_FIELDS = {"id", "attempt", "media_url", "raw_sha256", "observed_at", "observed_by", "evidence"}


def valid_flow_url(value):
    return isinstance(value, str) and re.fullmatch(
        rf"https://flow\.google\.com/project/{PROJECT}/edit/[0-9a-f-]+", value) is not None


def valid_media_url(value):
    # edit/<id> identifies a mutable editor container, not an image revision.
    return isinstance(value, str) and re.fullmatch(
        r"https://flow-content\.google/image/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", value) is not None


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def load_revision_observations(path):
    """Read explicit later observations; never synthesize an old UI observation."""
    if not path.exists():
        return []
    data = load_json(path)
    if (not isinstance(data, dict) or "observations" not in data or set(data) - {"observations", "scope"}
            or not isinstance(data["observations"], list)):
        raise ValueError("Revision observation JSON needs an observations list and optional scope text")
    if "scope" in data and (not isinstance(data["scope"], str) or not data["scope"].strip()):
        raise ValueError("Revision observation scope must be nonempty text when present")
    seen = set()
    for item in data["observations"]:
        if not isinstance(item, dict) or set(item) != REVISION_OBSERVATION_FIELDS:
            raise ValueError(f"Each revision observation needs exactly {sorted(REVISION_OBSERVATION_FIELDS)}")
        if any(not isinstance(item[key], str) or not item[key].strip()
               for key in ("id", "observed_at", "observed_by", "evidence")):
            raise ValueError("Revision observation identity, time, observer and evidence must be nonempty text")
        if type(item["attempt"]) is not int or item["attempt"] < 1:
            raise ValueError("Revision observation attempt must be a positive integer")
        if not valid_media_url(item["media_url"]) or not isinstance(item["raw_sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["raw_sha256"]):
            raise ValueError("Revision observation needs an actual media revision URL and raw SHA-256")
        key = (item["id"], item["attempt"])
        if key in seen:
            raise ValueError(f"Duplicate revision observation for {key}")
        seen.add(key)
    return data["observations"]


def resolve_source_revision(asset_id, attempt, records, observations, raw_root=None):
    """Resolve the revision bound to recorded original bytes, or return None.

    A later observation's own observed_at/evidence are preserved. It does not
    claim the revision URL was observed at the earlier submission time.
    """
    sources = [row for row in records if (row["input"]["id"], row["input"]["attempt"]) == (asset_id, attempt)]
    if len(sources) != 1:
        raise ValueError(f"{asset_id} #{attempt}: source requires exactly one review record")
    source = sources[0]
    source_input = source["input"]
    if not valid_flow_url(source_input.get("flow_url")):
        raise ValueError("Source review has no valid editor container URL")
    folder = RAW if raw_root is None else Path(raw_root)
    stem = f"v1_{asset_id}_{attempt}"
    raw = image_path(source_input["raw_file"], folder, stem, raw=True)
    raw_sha = digest(raw.read_bytes())
    if raw_sha != source["measurements"]["raw"]["sha256"]:
        raise ValueError(f"{asset_id} #{attempt}: original source bytes changed since review")
    direct = source_input.get("result_media_url")
    if direct is not None and not valid_media_url(direct):
        raise ValueError("Source result_media_url is not an image revision URL")
    observed = [item for item in observations if (item["id"], item["attempt"]) == (asset_id, attempt)]
    if len(observed) > 1:
        raise ValueError("Conflicting or duplicate source revision observations")
    if observed:
        observation = observed[0]
        if observation["raw_sha256"] != raw_sha or not valid_media_url(observation["media_url"]):
            raise ValueError(f"{asset_id} #{attempt}: revision observation does not match recorded original SHA")
        if direct is not None and direct != observation["media_url"]:
            raise ValueError("Revision observation conflicts with the recorded result revision")
    if direct is not None:
        return {"media_url": direct, "raw_sha256": raw_sha, "resolution_source": "recorded_result_media_url"}
    if observed:
        return {"media_url": observed[0]["media_url"], "raw_sha256": raw_sha,
                "resolution_source": "separate_explicit_legacy_revision_observation", "observation": observed[0]}
    return None


def image_path(value, folder, stem, raw=False):
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError("Image file must be a filename/full path, or null for absent clean")
    path = Path(value)
    path = path if path.is_absolute() else folder / path
    path = path.resolve()
    if path.parent != folder.resolve() or path.stem != stem:
        raise ValueError(f"Unexpected image path: {path}")
    if path.suffix.lower() not in ({".jpg", ".jpeg", ".png"} if raw else {".png"}):
        raise ValueError(f"Unexpected image extension: {path}")
    return path


def measure(path, optional=False):
    if path is None or not path.is_file():
        if optional:
            return None
        raise ValueError(f"Missing image: {path}")
    data = path.read_bytes()
    with Image.open(path) as image:
        size, fmt = list(image.size), image.format
        image.verify()
    expected = "PNG" if path.suffix.lower() == ".png" else "JPEG"
    if fmt != expected:
        raise ValueError(f"Extension/actual format mismatch: {path}: {fmt}")
    return {"path": str(path), "sha256": digest(data), "bytes": len(data),
            "dimensions": size, "format": fmt}


def normalize(payload, manifest, require_ui_references=True):
    required = FIELDS | ({"actual_ui_references", "result_media_url"} if require_ui_references else set())
    allowed = FIELDS | OPTIONAL_FIELDS | {"actual_ui_references", "result_media_url"}
    if not isinstance(payload, dict) or not required <= set(payload) or set(payload) - allowed:
        raise ValueError(f"Decision JSON needs {sorted(required)}; optional: {sorted(OPTIONAL_FIELDS)}")
    item = dict(payload)
    item.setdefault("actual_retake_reference_file", None)
    if "result_media_url" in item and not valid_media_url(item["result_media_url"]):
        raise ValueError("result_media_url must identify the actual downloaded image revision")
    if "actual_ui_references" in item:
        references = item["actual_ui_references"]
        if not isinstance(references, list):
            raise ValueError("actual_ui_references must be a list; use [] when no input image was present")
        for ref in references:
            allowed_shapes = [UI_REFERENCE_FIELDS] if require_ui_references else [UI_REFERENCE_FIELDS, UI_REFERENCE_FIELDS - {"source_media_url"}]
            if not isinstance(ref, dict) or set(ref) not in allowed_shapes:
                raise ValueError(f"Each actual_ui_references entry needs exactly {sorted(UI_REFERENCE_FIELDS)}")
            if any(not isinstance(ref[key], str) or not ref[key].strip()
                   for key in ("id", "observed_by", "evidence")):
                raise ValueError("UI reference id, observed_by and evidence must be nonempty text")
            if not valid_flow_url(ref["flow_url"]):
                raise ValueError("UI reference flow_url must identify a source in the fixed project")
            if "source_media_url" in ref and not valid_media_url(ref["source_media_url"]):
                raise ValueError("UI reference source_media_url must identify the actual input image revision")
            if ref["method"] not in UI_REFERENCE_METHODS:
                raise ValueError(f"UI reference method must be one of {sorted(UI_REFERENCE_METHODS)}")
            if ref["observed_before_submit"] is not True:
                raise ValueError("UI reference must have observed_before_submit: true")
        ids = [ref["id"] for ref in references]
        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate actual UI reference IDs are forbidden")
    if item["id"] not in manifest:
        raise ValueError(f"Unknown ID: {item['id']}")
    if type(item["attempt"]) is not int or item["attempt"] < 1:
        raise ValueError("attempt must be a positive integer")
    if item["decision"] not in {"chosen", "remake"}:
        raise ValueError("decision must be chosen or remake")
    for key in ("reason", "flow_url"):
        if not isinstance(item[key], str) or not item[key].strip():
            raise ValueError(f"{key} must be nonempty text")
    if not valid_flow_url(item["flow_url"]):
        raise ValueError("flow_url must identify a result in the fixed episode project")
    for key in ("root_opened_raw_original", "root_opened_clean_original"):
        if type(item[key]) is not bool:
            raise ValueError(f"{key} must be an explicit JSON boolean")
    if item["decision"] == "chosen" and not item["root_opened_clean_original"]:
        raise ValueError("chosen requires root_opened_clean_original: true")
    stem = f"v1_{item['id']}_{item['attempt']}"
    raw = image_path(item["raw_file"], RAW, stem, raw=True)
    clean = image_path(item["clean_file"], CLEAN, stem)
    if raw is None:
        raise ValueError("raw_file is required, including for remake")
    metrics = {"raw": measure(raw), "clean": measure(clean, optional=item["decision"] == "remake")}
    if metrics["clean"] is None and item["root_opened_clean_original"]:
        raise ValueError("Cannot report opening an absent clean image")
    retake = item["actual_retake_reference_file"]
    metrics["actual_retake_reference"] = None
    if retake is not None:
        if manifest[item["id"]].get("kind") != "master" or item["attempt"] <= 1:
            raise ValueError("A raw retake reference is allowed only for an explicit master retry")
        if not isinstance(retake, str):
            raise ValueError("actual_retake_reference_file must be a raw filename/full path or null")
        prior_stem = Path(retake).stem
        match = re.fullmatch(rf"v1_{re.escape(item['id'])}_([1-9][0-9]*)", prior_stem)
        if not match or int(match[1]) >= item["attempt"]:
            raise ValueError("Master retake reference must be an earlier attempt of the same ID")
        retake_path = image_path(retake, RAW, prior_stem, raw=True)
        metrics["actual_retake_reference"] = measure(retake_path)
        item["actual_retake_reference_file"] = str(retake_path)
    item["raw_file"] = raw.name
    item["clean_file"] = clean.name if clean is not None else None
    return item, metrics


def ref_ids(value):
    if value is None:
        return []
    return value.split("+") if isinstance(value, str) else list(value)


def reference_picks(asset_id, manifest, picks, records, observations):
    result = {}
    required = ref_ids(manifest[asset_id].get("ref"))
    if len(required) != len(set(required)):
        raise ValueError(f"{asset_id}: duplicate planned references")
    for ref in required:
        if ref == asset_id or ref not in picks:
            raise ValueError(f"{asset_id}: required prior chosen reference missing: {ref}")
        pick = picks[ref]
        actual = measure(SELECTED / pick["file"])
        if actual["sha256"] != pick["sha256"]:
            raise ValueError(f"Chosen reference file changed: {ref}")
        if not valid_flow_url(pick.get("flow_url")):
            raise ValueError(f"Chosen reference has no valid Flow source URL: {ref}")
        revision = resolve_source_revision(ref, pick["attempt"], records, observations)
        if revision is None:
            raise ValueError(f"{ref}: selected source revision is unresolved; do not use the editor container as an image identity")
        result[ref] = {"attempt": pick["attempt"], "file": pick["file"], "sha256": actual["sha256"],
                       "flow_url": pick["flow_url"], "source_media_url": revision["media_url"]}
    return result


def validate_ui_references(item, metrics, references, records, observations):
    """Check reported observation identity/order, never infer an actual UI attachment.

    Existing records without this field remain historical records. Every new
    decision, including ref=None, must explicitly supply actual_ui_references.
    A current_image_editor_input observation means the source was visibly the
    editor input before submission; merely visiting its URL is not evidence.
    """
    expected = [(ref, value["flow_url"], value["source_media_url"]) for ref, value in references.items()]
    retake = item["actual_retake_reference_file"]
    if retake is not None:
        prior = [row for row in records if row["input"]["id"] == item["id"]
                 and row["input"]["raw_file"] == Path(retake).name]
        if len(prior) != 1:
            raise ValueError("Master retake source must have exactly one earlier review ledger entry")
        source = prior[0]
        if source["input"]["attempt"] >= item["attempt"]:
            raise ValueError("Master retake source ledger entry is not an earlier attempt")
        if metrics["actual_retake_reference"]["sha256"] != source["measurements"]["raw"]["sha256"]:
            raise ValueError("Master retake raw source changed since its recorded review")
        source_url = source["input"]["flow_url"]
        if not valid_flow_url(source_url):
            raise ValueError("Master retake source ledger has no valid Flow URL")
        revision = resolve_source_revision(item["id"], source["input"]["attempt"], records, observations)
        if revision is None:
            raise ValueError("Master retake source revision is unresolved; a matching editor URL is insufficient")
        expected.append((item["id"], source_url, revision["media_url"]))
    observed = [(ref["id"], ref["flow_url"], ref["source_media_url"]) for ref in item["actual_ui_references"]]
    if observed != expected:
        raise ValueError("Actual UI reference IDs/editor URLs/image revision URLs must exactly match required sources in order; "
                         f"expected {expected}, reported {observed}")


def copy_chosen(record):
    clean = record["measurements"]["clean"]
    if clean is None:
        raise ValueError("chosen has no clean image")
    SELECTED.mkdir(parents=True, exist_ok=True)
    target = SELECTED / record["input"]["clean_file"]
    if target.exists():
        if measure(target)["sha256"] != clean["sha256"]:
            raise ValueError(f"Refusing to overwrite different selected image: {target}")
        return
    with Path(clean["path"]).open("rb") as source, target.open("xb") as output:
        shutil.copyfileobj(source, output)
    if measure(target)["sha256"] != clean["sha256"]:
        raise ValueError(f"Selected copy verification failed: {target}; inspect manually")


def rebuild_picks(records):
    picks = {}
    seen = set()
    for record in records:
        item = record["input"]
        key = (item["id"], item["attempt"])
        if key in seen:
            raise ValueError(f"Duplicate existing review entry: {key}")
        seen.add(key)
        if item["decision"] == "chosen":
            clean = record["measurements"]["clean"]
            picks[item["id"]] = {
                "attempt": item["attempt"], "file": item["clean_file"], "raw_file": item["raw_file"],
                "reference": record["planned_ref"], "planned_ref": record["planned_ref"],
                "reference_picks": record["reference_picks"],
                "actual_retake_reference_file": item["actual_retake_reference_file"],
                "ui_reference_provenance_status": ("reported_observation_revision_identity_checked"
                    if "actual_ui_references" in item and "result_media_url" in item else
                    "legacy_revision_identity_not_recorded"),
                "visual_status": "chosen_as_generated_reconstruction_reference",
                "root_opened_raw_original": item["root_opened_raw_original"],
                "root_opened_clean_original": item["root_opened_clean_original"],
                "raw_and_cleaned_opened_at_original_size": item["root_opened_raw_original"] and item["root_opened_clean_original"],
                "dimensions": clean["dimensions"], "sha256": clean["sha256"],
                "reason": item["reason"], "flow_url": item["flow_url"],
            }
            if "actual_ui_references" in item:
                picks[item["id"]]["actual_ui_references"] = item["actual_ui_references"]
            if "result_media_url" in item:
                picks[item["id"]]["result_media_url"] = item["result_media_url"]
    return picks


def migrate_legacy(legacy, markdown, manifest):
    """Migrate ONLY the two explicit historical AT_S reviews, never infer a new pass."""
    pick = legacy.get("picks", {}).get("AT_S", {})
    if (set(legacy.get("picks", {})) != {"AT_S"} or legacy.get("chosen_count") != 1
            or pick.get("attempt") != 2 or pick.get("file") != "v1_AT_S_2.png"
            or pick.get("raw_file") != "v1_AT_S_2.jpg"
            or pick.get("raw_and_cleaned_opened_at_original_size") is not True):
        raise ValueError("Unrecognized legacy ledger; refusing an automatic migration")
    rows = {}
    for line in markdown.splitlines():
        if line.startswith("| AT_S |"):
            cols = [part.strip() for part in line.strip().strip("|").split("|")]
            if len(cols) != 6:
                raise ValueError("Legacy AT_S markdown row changed")
            rows[int(cols[2])] = cols
    if (set(rows) != {1, 2} or "보류·재생성" not in rows[1][4] or "선택" not in rows[2][4]
            or any("원본과 처리본을 직접 확인" not in row[5] for row in rows.values())):
        raise ValueError("Legacy markdown lacks the two explicit raw/clean root reviews")
    urls = {
        1: f"https://flow.google.com/project/{PROJECT}/edit/d7501eaa-9047-474c-8302-ab06402c0ef2",
        2: pick.get("flow_url"),
    }
    records = []
    for attempt, decision in ((1, "remake"), (2, "chosen")):
        if not urls[attempt] or urls[attempt] not in markdown:
            raise ValueError("Missing explicit legacy Flow result URL")
        item, metrics = normalize({
            "id": "AT_S", "attempt": attempt, "decision": decision, "reason": rows[attempt][5],
            "flow_url": urls[attempt], "raw_file": f"v1_AT_S_{attempt}.jpg",
            "clean_file": f"v1_AT_S_{attempt}.png", "root_opened_raw_original": True,
            "root_opened_clean_original": True,
        }, manifest, require_ui_references=False)
        if any(metrics[key]["dimensions"] != [1376, 768] for key in ("raw", "clean")):
            raise ValueError("Legacy dimensions no longer match the explicit historical record")
        records.append({"input": item, "measurements": metrics, "planned_ref": None,
                        "reference_picks": {}, "recorded_at": "2026-10-27 (legacy explicit review)",
                        "review_source": "existing root-authored picks_v1.md/json; not a new visual review"})
    return {"schema_version": 2, "scope": "explicit root visual decisions; automatic file measurements are separate",
            "expected_ids": len(manifest), "review_log": records,
            "legacy_record": {"source_date": "2026-10-27", "json": legacy, "markdown": markdown}}


def markdown_report(ledger, manifest):
    def cell(value):
        return str(value).replace("|", "\\|").replace("\n", "<br>")
    records, picks = ledger["review_log"], ledger["picks"]
    reviewed = {row["input"]["id"] for row in records}
    lines = ["# 9편 이미지 선택·실제 시각 검토 기록 v1", "",
             f"갱신: {ledger['updated_at']}. 선택 **{len(picks)}/{len(manifest)} ID**, 기록 {len(reviewed)} ID / {len(records)}시도. 미선택 {len(manifest) - len(picks)} ID. 미기록 {len(manifest) - len(reviewed)} ID.", "",
             "2026-10-27 최초 생성 UI에서 지정 Flow 프로젝트, Nano Banana 2.1 / 16:9 / x1 / 0크레딧을 확인했다. 한 장씩 생성한다.", "",
             "이미지는 관찰한 형상·승인 대본으로 새로 생성한 설명용 재구성이다. 현장 기록 사진·측량 결과가 아니다. 도구는 시각 합격을 판단하지 않고 root가 명시한 선택·재생성 결정과 실제 원본 크기로 연 여부를 기록한다.", "",
             "자동 확인은 파일 존재·실제 형식·픽셀 크기·바이트 수·SHA-256·선행 선택 참조 파일에 한정된다. planned_ref와 master 재시도에서 명시한 미선택 원본 참조(actual_retake_reference_file)를 구분한다. 같은 프로젝트의 실제 첨부 원본 자산은 reference_assets_v1.json/생성 기록과 대조하며, 표의 선행 선택 PNG 파일은 그 원천을 구별하기 위한 선택 기록이다. PNG를 재업로드했다고 뜻하지 않는다. Flow에 실제 참조를 첨부했는지, 의미·형상·글자·사람·밝기·중복이 적절한지는 이 측정으로 검증하지 않는다. 오디오 받아쓰기 검사도 별개다.", "",
             "새 결정은 result_media_url에 실제 결과 이미지 revision을 기록하고, actual_ui_references에 제출 전 실제 입력으로 본 ID·편집기 URL·source_media_url·방법·관찰자·근거를 명시한다. ref가 없으면 []로 입력 이미지 부재를 신고한다. 편집기 URL은 수정되는 컨테이너이므로 이미지 revision 식별자가 아니다. 도구는 신고의 순서·정확한 원천 revision·기록된 파일 해시를 확인하며 서비스의 실제 첨부를 자동 입증하지 않는다.", "",
             "과거 결과 revision이 기록되지 않았으면 source_revision_observations_v1.json의 별도 관찰을 통해 원장·실제 원본과 raw SHA가 모두 같은 경우에만 해석한다. 별도 observed_at/evidence는 관찰한 실제 시점과 사후 확인 여부를 보존하며, 과거 입력 기록에 새 관찰을 소급해서 만들지 않는다. revision 미확인 상태에서는 후속 참조를 차단한다.", "",
             "## 생성·실제 검토", "",
             "| ID | 첨부 기준의 선행 선택 | 시도 | 원본 / 처리본 | 결정 | 원본 크기 직접 열기 raw / clean | 실제로 본 내용·조치(root 기록) |",
             "|---|---|---:|---|---|---|---|"]
    for row in records:
        item = row["input"]
        refs = ", ".join(f"{key}={value['file']}" for key, value in row["reference_picks"].items()) or "없음"
        if item["actual_retake_reference_file"]:
            refs += f"; master 재시도 raw: {Path(item['actual_retake_reference_file']).name} (첨부는 root 신고)"
        files = f"{item['raw_file']} / {item['clean_file'] or '없음'}"
        opened = " / ".join("예" if item[key] else "아니오" for key in ("root_opened_raw_original", "root_opened_clean_original"))
        lines.append("| " + " | ".join(cell(value) for value in (item["id"], refs, item["attempt"], files,
                     "선택" if item["decision"] == "chosen" else "보류·재생성", opened, item["reason"])) + " |")
    lines += ["", "## 현재 명시적 선택", "", "| ID | 선택 파일 | 처리본 픽셀 크기 | SHA-256 |", "|---|---|---|---|"]
    for asset_id in manifest:
        if asset_id in picks:
            pick = picks[asset_id]
            lines.append(f"| {asset_id} | `{pick['file']}` | {'×'.join(map(str, pick['dimensions']))} | `{pick['sha256']}` |")
    lines += ["", "## 출처·범위·PC 보관", "",
              "- AT_S 시도1은 부모와 독립 검토자가 각각 실제 파일을 열었다. 시도2는 root가 원본·처리본을 실제 원본 크기로 연 기존 명시 기록을 보존했다. 이 도구 실행은 새 시각 검수가 아니다.",
              "- Primary 본문의 단일 튜브·2차로 설명은 재확인했다. 독립 검토에서 남측 원사진 재열람이 실패했으므로 이 회차에 원사진과 나란히 직접 대조했다고 보고하지 않는다.",
              "- 기존 AT_S 시도1·2의 문장·날짜·Flow 출처와 당시 전체 JSON/Markdown은 JSON의 `legacy_record`에 원문 보존한다. 원본 JPEG와 워터마크 처리 PNG를 구별한다. 기존 `tools\\lama\\dewm.py` 처리를 기록하며 생성 글자를 흐려서 통과시키지 않는다.",
              f"- PC 원본: `{RAW}`. 처리본: `{CLEAN}`. 명시 선택 복사본: `{SELECTED}`. 원본은 보존하며 이 도구는 이미지를 편집·삭제하지 않는다.",
              "- 최신 번호를 자동 선택하지 않는다. 재생성 결정은 이전의 별도 선택을 자동 해제하지 않으며, 새 `chosen` 결정만 해당 ID 선택을 교체한다. 정규 planned_ref는 결정 당시 선행 선택의 파일·해시로 고정한다. master 재시도의 같은 ID 앞선 원본만 별도 raw 참조로 허용하며 정규 참조의 선행 선택 조건을 면제하지 않는다.", ""]
    for row in records:
        item = row["input"]
        raw, clean = row["measurements"]["raw"], row["measurements"]["clean"]
        lines.append(f"- {item['id']} 시도{item['attempt']} Flow: {item['flow_url']} · 자동 측정 raw {raw['format']} {raw['dimensions']} / clean {clean['format'] + ' ' + str(clean['dimensions']) if clean else '없음'}; 세부 SHA·바이트는 JSON.")
        lines.append(f"  - 결과 revision: {item.get('result_media_url', '기존 입력 기록에 없음; 별도 원본 해시 대조 관찰로 확인해야 함')}.")
        if "actual_ui_references" not in item:
            lines.append("  - UI 입력 관찰: 기존 기록에 없음. 새 관찰로 소급 표기하지 않는다.")
        elif not item["actual_ui_references"]:
            lines.append("  - UI 입력 관찰 신고: 참조 입력 없음([]). 자동 UI 검증은 아니다.")
        else:
            for ref in item["actual_ui_references"]:
                lines.append(f"  - UI 입력 관찰 신고: {ref['id']} / {ref['flow_url']} / {ref['method']} / "
                             f"revision {ref.get('source_media_url', '기존 기록에 없음')} / 제출 전 / "
                             f"관찰자 {cell(ref['observed_by'])} / 근거 {cell(ref['evidence'])}. 자동 UI 검증은 아니다.")
    return "\n".join(lines) + "\n"


def save_text(path, text):
    temporary = path.with_name(path.name + ".record_review.tmp")
    with temporary.open("x", encoding="utf-8", newline="\n") as output:
        output.write(text)
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("decision_json", type=Path)
    args = parser.parse_args()
    # One writer at a time. A leftover lock needs inspection, never auto-removal.
    lock = HERE / ".record_review.lock"
    with lock.open("x", encoding="utf-8") as output:
        output.write(str(args.decision_json.resolve()))
    try:
        rows = load_json(HERE / "prompts_v1.json")
        manifest = {row["id"]: row for row in rows}
        if len(manifest) != len(rows):
            raise ValueError("Duplicate IDs in prompt manifest")
        ledger = load_json(JSON_PATH)
        if "review_log" not in ledger:
            ledger = migrate_legacy(ledger, MD_PATH.read_text(encoding="utf-8-sig"), manifest)
        if ledger.get("schema_version") != 2 or ledger.get("expected_ids") != len(manifest):
            raise ValueError("Unexpected ledger version or manifest ID count")
        picks = rebuild_picks(ledger["review_log"])
        payload = load_json(args.decision_json)
        if not isinstance(payload, dict):
            raise ValueError("Decision JSON must be an object")
        duplicate = next((row for row in ledger["review_log"] if (row["input"]["id"], row["input"]["attempt"]) == (payload.get("id"), payload.get("attempt"))), None)
        item, metrics = normalize(payload, manifest, require_ui_references=duplicate is None)
        if duplicate:
            if duplicate["input"] != item or duplicate["measurements"] != metrics:
                raise ValueError("This ID/attempt is already recorded with different input or files")
            print(f"Identical existing decision verified; no duplicate: {item['id']} #{item['attempt']}")
            return
        else:
            observations = load_revision_observations(HERE / "source_revision_observations_v1.json")
            refs = reference_picks(item["id"], manifest, picks, ledger["review_log"], observations)
            validate_ui_references(item, metrics, refs, ledger["review_log"], observations)
            ledger["review_log"].append({"input": item, "measurements": metrics,
                "planned_ref": manifest[item["id"]].get("ref"), "reference_picks": refs,
                "recorded_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "review_source": "root explicit decision JSON; helper makes no visual judgment"})
        # Confirm every current selection's bytes; never choose the latest file automatically.
        current_records = {}
        for record in ledger["review_log"]:
            if record["input"]["decision"] == "chosen":
                current_records[record["input"]["id"]] = record
        for record in current_records.values():
            copy_chosen(record)
        ledger["picks"] = rebuild_picks(ledger["review_log"])
        ledger["chosen_count"] = len(ledger["picks"])
        ledger["updated_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
        save_text(JSON_PATH, json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        save_text(MD_PATH, markdown_report(ledger, manifest))
        print(f"Recorded {item['decision']}: {item['id']} #{item['attempt']}; chosen {ledger['chosen_count']}/{len(manifest)}")
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
