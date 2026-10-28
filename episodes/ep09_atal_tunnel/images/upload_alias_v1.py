"""Strict, offline identity proof for explicitly approved master PNG uploads.

Check only (default): python upload_alias_v1.py --proof <proof.json>
Record AFTER root collected real evidence: add --record.
Optional --episode-root and --media-root are for isolated fixtures.
This program never uploads, browses, selects images or grants authorization.

Proof JSON (all fields required, no extra fields):
  schema_version: 1; alias_id: safe ASCII identifier; id: one approved master;
  selected_attempt, selected_file, selected_sha256, input_file, input_sha256;
  destination_project_id, destination_profile_label, approval_file_sha256;
  upload: {observed_by:"root", observed_at_utc, evidence,
    root_observed_upload_submission:true, root_observed_new_server_revision:true,
    flow_url:<cb1 edit URL>, media_url:<actual new image revision URL>};
  download: {observed_by:"root", observed_at_utc, evidence,
    root_observed_server_download:true, from_media_url:<same new revision>,
    file:<media-root>/img_upload_server/<new image UUID>.png|jpg|jpeg, sha256}.

The legacy/default path requires exact pixels. A separate, explicit
proof_kind="root_reviewed_service_representation" requires all legacy proof
fields plus batch_receipt_file/batch_receipt_sha256 and
comparison_file/comparison_sha256. It is NOT a fallback, pixel tolerance,
lossless claim or deterministic JPEG claim. It requires a separately hashed
root comparison decision, not an automatic similarity pass.

Manual receipt JSON in images/upload_receipts_v1/: schema_version, receipt_id,
destination_project_id, destination_profile_label, observed_by="root",
transfer_started_at_utc, transfer_completed_at_utc (observed completion, not
an invented network timestamp), completed_tiles_observed_at_utc, evidence,
root_observed_exact_six_input_files=true,
root_observed_upload_completed_six_tiles=true, assets (exactly six rows of
id, selected_attempt, selected_filename, input_file, input_sha256).
Manual upload observation additionally needs
root_opened_corresponding_filename_tile=true and observed_input_filename.
Comparison JSON in images/upload_comparisons_v1/: schema_version, id,
selected_attempt, selected_file, selected_sha256, selected_png_file,
server_download_file, server_sha256, dimensions, observed_by="root",
observed_at_utc, root_opened_selected_png_original=true,
root_opened_server_jpeg_original=true, same_shape=true, same_composition=true,
same_content=true, pass=true, notes (specific direct comparison observations).

The server file must be a separately observed original download, never the local
selected PNG re-designated as a download. On the strict path, same dimensions,
full decoded RGB and alpha bytes are required; no lossy exception. The manual
path explicitly records nonidentical JPEG pixels and the separate root decision;
pixel-error measurements never generate that decision. Neither path permits
an unobserved input, resize or rotation.
Root observations are explicit declarations, not automatically proved UI facts.
The original source URL/revision and reviewed raw-byte identity remain checked.
An authorization-scope hash is rechecked at use; unrelated later confirmation
metadata in the approval JSON does not silently change the approved scope.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import sys

from PIL import Image, ImageChops

EP = Path(__file__).resolve().parent.parent
MEDIA = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
DEST = "cb1e7ac3-1d61-4206-ac72-3444f121843c"
PROFILE = "artbuilder883"
MASTERS = {"AT_S", "AT_N", "AT_C", "AT_INT", "G3D_EXC", "G3D_DEEP"}
PROOF_FIELDS = {"schema_version", "alias_id", "id", "selected_attempt", "selected_file",
                "selected_sha256", "input_file", "input_sha256", "destination_project_id",
                "destination_profile_label", "approval_file_sha256", "upload", "download"}
UPLOAD_FIELDS = {"observed_by", "observed_at_utc", "evidence", "root_observed_upload_submission",
                 "root_observed_new_server_revision", "flow_url", "media_url"}
DOWNLOAD_FIELDS = {"observed_by", "observed_at_utc", "evidence", "root_observed_server_download",
                   "from_media_url", "file", "sha256"}
MANUAL_KIND = "root_reviewed_service_representation"
MANUAL_PROOF_FIELDS = PROOF_FIELDS | {"proof_kind", "batch_receipt_file", "batch_receipt_sha256",
                                    "comparison_file", "comparison_sha256"}
MANUAL_UPLOAD_FIELDS = UPLOAD_FIELDS | {"root_opened_corresponding_filename_tile", "observed_input_filename"}
RECEIPT_FIELDS = {"schema_version", "receipt_id", "destination_project_id", "destination_profile_label",
                  "observed_by", "transfer_started_at_utc", "transfer_completed_at_utc",
                  "completed_tiles_observed_at_utc", "evidence", "root_observed_exact_six_input_files",
                  "root_observed_upload_completed_six_tiles", "assets"}
RECEIPT_ASSET_FIELDS = {"id", "selected_attempt", "selected_filename", "input_file", "input_sha256"}
COMPARISON_FIELDS = {"schema_version", "id", "selected_attempt", "selected_file", "selected_sha256",
                     "selected_png_file", "server_download_file", "server_sha256", "dimensions",
                     "observed_by", "observed_at_utc", "root_opened_selected_png_original",
                     "root_opened_server_jpeg_original", "same_shape", "same_composition",
                     "same_content", "pass", "notes"}


def read_json(path):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError(f"Duplicate JSON key: {key}")
            out[key] = value
        return out
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_sha(value):
    return digest(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exact_object(value, keys, name):
    require(isinstance(value, dict) and set(value) == keys, f"{name} needs exactly {sorted(keys)}")


def observation(value, flag_fields):
    require(value["observed_by"] == "root", "Observation must explicitly identify root")
    require(isinstance(value["evidence"], str) and bool(value["evidence"].strip()), "Observation evidence missing")
    stamp = value["observed_at_utc"]
    require(isinstance(stamp, str), "Observation timestamp missing")
    parsed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Observation timestamp needs a timezone")
    require(all(value[key] is True for key in flag_fields), "Explicit root observation flags must be true")
    return parsed


def decode(path):
    data = Path(path).read_bytes()
    with Image.open(io.BytesIO(data)) as image:
        require(getattr(image, "n_frames", 1) == 1, "Animated/multiple-frame images are forbidden")
        require(image.getexif().get(274, 1) == 1, "EXIF orientation transformations are forbidden")
        require(image.format in {"PNG", "JPEG"}, "Unsupported downloaded image format")
        require(image.mode in {"RGB", "RGBA"}, "Only native RGB/RGBA images are supported; no colour-mode conversion")
        if image.format == "PNG":
            require(len(data) > 25 and data[24] == 8, "Only 8-bit PNG is supported; no implicit bit-depth reduction")
        fmt, dims, native_mode = image.format, list(image.size), image.mode
        image.load()
        rgba = image.convert("RGBA")
        rgb, alpha = rgba.convert("RGB").tobytes(), rgba.getchannel("A").tobytes()
    return dict(sha256=digest(data), dimensions=dims, format=fmt, native_mode=native_mode, rgb=rgb, alpha=alpha)


def proof_shape(proof):
    manual = isinstance(proof, dict) and proof.get("proof_kind") == MANUAL_KIND
    exact_object(proof, MANUAL_PROOF_FIELDS if manual else PROOF_FIELDS, "Upload proof")
    return manual


def evidence_json(ep, proof, file_key, sha_key, folder):
    path = Path(proof[file_key]).resolve()
    require(path.parent == (ep / "images" / folder).resolve() and path.suffix.lower() == ".json",
            f"{file_key} must be an explicit episode {folder} JSON")
    data = path.read_bytes()
    require(isinstance(proof[sha_key], str) and digest(data) == proof[sha_key], f"{file_key} SHA changed/missing")
    return read_json(path)


def timestamp(value):
    require(isinstance(value, str), "Explicit observation time missing")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Observation time needs timezone")
    return parsed


def pixel_error_report(source, server):
    # Measurements only. No threshold here produces a manual comparison pass.
    dims = tuple(source["dimensions"])
    diff = ImageChops.difference(Image.frombytes("RGB", dims, source["rgb"]),
                                Image.frombytes("RGB", dims, server["rgb"]))
    histogram = diff.histogram()
    counts = [sum(histogram[i + channel * 256] for channel in range(3)) for i in range(256)]
    pixels = dims[0] * dims[1]
    channels = pixels * 3
    maximum_band = ImageChops.lighter(ImageChops.lighter(*diff.split()[:2]), diff.split()[2])
    changed_pixels = pixels - maximum_band.histogram()[0]
    mse = sum(i * i * count for i, count in enumerate(counts)) / channels
    return dict(exact_pixel_equal=False, total_pixels=pixels, changed_pixels=changed_pixels,
                changed_pixel_fraction=changed_pixels / pixels,
                changed_channel_values=channels - counts[0], total_channel_values=channels,
                mean_absolute_channel_error=sum(i * count for i, count in enumerate(counts)) / channels,
                maximum_channel_error=max(i for i, count in enumerate(counts) if count),
                rmse=math.sqrt(mse), psnr_db=10 * math.log10(255 * 255 / mse) if mse else None,
                automatic_visual_pass=False)


def manual_representation_evidence(proof, ep, media, pick, source, server, upload_time, download_time):
    require(server["format"] == "JPEG" and server["native_mode"] == "RGB"
            and server["dimensions"] == source["dimensions"] == [1376, 768],
            "Manual service representation requires native RGB JPEG at the exact 1376x768 dimensions")
    require(source["alpha"] == server["alpha"] == b"\xff" * (1376 * 768), "Manual service representation must be opaque")
    require(source["rgb"] != server["rgb"], "Exact pixels must use the existing strict path, not a manual representation")
    receipt = evidence_json(ep, proof, "batch_receipt_file", "batch_receipt_sha256", "upload_receipts_v1")
    exact_object(receipt, RECEIPT_FIELDS, "Six-master receipt")
    require(receipt["schema_version"] == 1 and isinstance(receipt["receipt_id"], str) and receipt["receipt_id"].strip()
            and receipt["destination_project_id"] == DEST and receipt["destination_profile_label"] == PROFILE
            and receipt["observed_by"] == "root" and isinstance(receipt["evidence"], str) and receipt["evidence"].strip()
            and receipt["root_observed_exact_six_input_files"] is True
            and receipt["root_observed_upload_completed_six_tiles"] is True, "Incomplete receipt/root destination/completion declaration")
    times = [timestamp(receipt[key]) for key in ("transfer_started_at_utc", "transfer_completed_at_utc", "completed_tiles_observed_at_utc")]
    require(times[0] <= times[1] <= times[2] <= upload_time <= download_time, "Receipt/upload/download observation chronology is inconsistent")
    assets = receipt["assets"]
    require(isinstance(assets, list) and len(assets) == 6, "Receipt must enumerate exactly six inputs")
    for row in assets:
        exact_object(row, RECEIPT_ASSET_FIELDS, "Receipt asset")
    require({row["id"] for row in assets} == MASTERS, "Receipt duplicates or substitutes a master ID")
    approved = {row["id"]: row for row in read_json(ep / "images/upload_approval_v1.json")["assets"]}
    for row in assets:
        chosen = approved[row["id"]]
        require(type(row["selected_attempt"]) is int and row["selected_attempt"] == chosen["selected_attempt"]
                and row["selected_filename"] == chosen["selected_filename"]
                and row["input_sha256"] == chosen["sha256"]
                and Path(row["input_file"]).resolve() == Path(chosen["proposed_upload_file"]).resolve(),
                "Receipt input identity differs from the current approved chosen master")
        require(digest(Path(row["input_file"]).read_bytes()) == row["input_sha256"]
                and digest(Path(chosen["selected_copy_file"]).read_bytes()) == row["input_sha256"],
                "Receipt input/selected copy bytes have changed")
    require(proof["upload"]["root_opened_corresponding_filename_tile"] is True
            and proof["upload"]["observed_input_filename"] == pick["file"], "Root did not explicitly open the corresponding exact filename tile")
    comparison = evidence_json(ep, proof, "comparison_file", "comparison_sha256", "upload_comparisons_v1")
    exact_object(comparison, COMPARISON_FIELDS, "Root service comparison")
    require(comparison["schema_version"] == 1 and comparison["id"] == proof["id"]
            and type(comparison["selected_attempt"]) is int and comparison["selected_attempt"] == pick["attempt"]
            and comparison["selected_file"] == pick["file"] and comparison["selected_sha256"] == pick["sha256"]
            and comparison["server_sha256"] == server["sha256"] and comparison["dimensions"] == [1376, 768],
            "Comparison identifies the wrong chosen master/server bytes")
    source_paths = {Path(proof["input_file"]).resolve(), Path(approved[proof["id"]]["selected_copy_file"]).resolve()}
    require(Path(comparison["selected_png_file"]).resolve() in source_paths
            and digest(Path(comparison["selected_png_file"]).read_bytes()) == pick["sha256"]
            and Path(comparison["server_download_file"]).resolve() == Path(proof["download"]["file"]).resolve(),
            "Comparison does not bind the actual selected/server files")
    require(comparison["observed_by"] == "root" and isinstance(comparison["notes"], str) and comparison["notes"].strip()
            and all(comparison[key] is True for key in ("root_opened_selected_png_original", "root_opened_server_jpeg_original",
                                                       "same_shape", "same_composition", "same_content", "pass")),
            "Separate explicit root original-size comparison/pass/notes missing")
    require(timestamp(comparison["observed_at_utc"]) >= download_time, "Comparison predates the observed server download")
    return dict(proof_kind=MANUAL_KIND, exact_pixel_equal=False, lossless=False,
                deterministic_transform_proven=False, manual_comparison_pass=True,
                batch_receipt_sha256=proof["batch_receipt_sha256"], comparison_sha256=proof["comparison_sha256"],
                selected_rgb_sha256=digest(source["rgb"]), server_rgb_sha256=digest(server["rgb"]),
                selected_alpha_sha256=digest(source["alpha"]), server_alpha_sha256=digest(server["alpha"]),
                pixel_error_measurements=pixel_error_report(source, server))


def review_helpers(ep, media):
    path = ep / "images/record_review.py"
    spec = importlib.util.spec_from_file_location("_upload_alias_review_helpers", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.HERE = ep / "images"
    module.MEDIA = media
    module.RAW, module.CLEAN, module.SELECTED = (media / x for x in ("img_raw", "img", "img_selected"))
    return module


def approved_context(ep, media, sid):
    rr = review_helpers(ep, media)
    policy = rr.load_flow_project_policy()
    require(policy["current_generation_project_id"] == DEST, "Current generation project is not the approved cb1 destination")
    prompts = rr.load_json(ep / "images/prompts_v1.json")
    manifest = {row["id"]: row for row in prompts}
    require(len(manifest) == len(prompts) and sid in MASTERS and manifest.get(sid, {}).get("kind") == "master", "Only the exact six chosen master IDs are eligible")
    ledger = rr.load_json(ep / "images/picks_v1.json")
    picks = rr.rebuild_picks(ledger["review_log"])
    require(picks == ledger["picks"], "Stored picks differ from explicit review history")
    require(sid in picks, "Required chosen master is missing")
    pick = picks[sid]
    require(pick.get("root_opened_clean_original") is True or pick.get("raw_and_cleaned_opened_at_original_size") is True, "Chosen clean original review missing")
    actual = rr.measure(media / "img_selected" / pick["file"])
    require(actual["sha256"] == pick["sha256"] and actual["dimensions"] == pick["dimensions"], "Selected master bytes/dimensions changed")
    require(rr.valid_flow_url(pick.get("flow_url")), "Original source URL is not allowed")
    observations = rr.load_revision_observations(ep / "images/source_revision_observations_v1.json")
    revision = rr.resolve_source_revision(sid, pick["attempt"], ledger["review_log"], observations, media / "img_raw")
    require(revision is not None, "Original raw/source revision identity remains unresolved")
    origin = dict(attempt=pick["attempt"], file=pick["file"], sha256=actual["sha256"],
                  flow_url=pick["flow_url"], source_media_url=revision["media_url"])
    approval_path = ep / "images/upload_approval_v1.json"
    approval = rr.load_json(approval_path)
    require(approval.get("authorized") is True, "Specific six-master transfer approval is absent")
    dest = approval.get("destination", {})
    require(dest.get("service") == "Google Flow" and dest.get("project_id") == DEST
            and dest.get("project_url") == f"https://flow.google.com/project/{DEST}"
            and dest.get("browser_profile_label") == PROFILE, "Approval destination/profile mismatch")
    authorization = approval.get("authorization", {})
    require(authorization.get("user_answer_verbatim") == "기준 그림 6장 업로드 승인"
            and authorization.get("destination") == dest
            and set(authorization.get("specific_assets", [])) == MASTERS
            and len(authorization.get("specific_assets", [])) == 6, "Direct six-asset user authorization evidence missing")
    transfer = approval.get("proposed_transfer", {})
    require(set(transfer.get("asset_ids", [])) == MASTERS and len(transfer.get("asset_ids", [])) == 6
            and transfer.get("asset_count") == 6, "Approval does not cover exactly the six master assets")
    assets = approval.get("assets", [])
    require(isinstance(assets, list) and len(assets) == 6 and {x.get("id") for x in assets} == MASTERS, "Approval asset rows are missing/duplicated/unknown")
    scope_assets = []
    for asset in assets:
        chosen = picks.get(asset["id"], {})
        require(asset.get("authorized") is True and asset.get("selected_attempt") == chosen.get("attempt")
                and asset.get("selected_filename") == chosen.get("file") and asset.get("sha256") == chosen.get("sha256")
                and asset.get("dimensions") == chosen.get("dimensions")
                and asset.get("original_flow_source_url") == chosen.get("flow_url"), "Approved master selection changed or is not individually authorized")
        require(Path(asset["proposed_upload_file"]).resolve() == (media / "img" / chosen["file"]).resolve()
                and Path(asset["selected_copy_file"]).resolve() == (media / "img_selected" / chosen["file"]).resolve(), "Approved file path is not the exact selected master file")
        scope_assets.append({key: asset[key] for key in ("id", "selected_attempt", "selected_filename", "proposed_upload_file", "selected_copy_file", "sha256", "dimensions", "authorized", "original_flow_source_url")})
    scope = dict(authorized=True, destination=dest, authorization=authorization,
                 proposed_transfer=transfer, assets=sorted(scope_assets, key=lambda x: x["id"]))
    return rr, pick, origin, next(x for x in assets if x["id"] == sid), digest(approval_path.read_bytes()), canonical_sha(scope)


def validate_proof(proof, ep=EP, media=MEDIA, expected_scope=None):
    ep, media = Path(ep).resolve(), Path(media).resolve()
    manual = proof_shape(proof)
    require(proof["schema_version"] == 1 and isinstance(proof["alias_id"], str)
            and re.fullmatch(r"[A-Za-z0-9_-]{1,120}", proof["alias_id"]), "Invalid upload alias identity/version")
    sid = proof["id"]
    rr, pick, origin, asset, approval_sha, scope_sha = approved_context(ep, media, sid)
    require(type(proof["selected_attempt"]) is int and proof["selected_attempt"] == pick["attempt"]
            and proof["selected_file"] == pick["file"] and proof["selected_sha256"] == pick["sha256"], "Proof does not identify the current exact chosen master")
    require(proof["destination_project_id"] == DEST and proof["destination_profile_label"] == PROFILE, "Proof destination mismatch")
    require(isinstance(proof["approval_file_sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", proof["approval_file_sha256"]), "Proof approval-file SHA missing")
    if expected_scope is None:
        require(proof["approval_file_sha256"] == approval_sha, "Approval file changed before registration")
    else:
        require(scope_sha == expected_scope, "Authorization scope changed since alias registration")
    input_path = Path(proof["input_file"]).resolve()
    require(input_path == Path(asset["proposed_upload_file"]).resolve(), "Upload input is not the exact approved PNG path")
    source = decode(input_path)
    require(source["format"] == "PNG" and source["sha256"] == proof["input_sha256"] == pick["sha256"]
            and source["dimensions"] == pick["dimensions"], "Input PNG SHA/dimensions differ from the chosen master")
    upload, download = proof["upload"], proof["download"]
    exact_object(upload, MANUAL_UPLOAD_FIELDS if manual else UPLOAD_FIELDS, "Upload observation")
    exact_object(download, DOWNLOAD_FIELDS, "Server download observation")
    upload_time = observation(upload, ["root_observed_upload_submission", "root_observed_new_server_revision"])
    download_time = observation(download, ["root_observed_server_download"])
    require(rr.flow_project_id(upload["flow_url"], role="source") == DEST and rr.valid_media_url(upload["media_url"]), "New uploaded editor/revision is invalid or in another project")
    require(upload["media_url"] != origin["source_media_url"], "An upload alias must identify the observed new server revision")
    require(download["from_media_url"] == upload["media_url"], "Download is not bound to the observed new revision")
    server_path = Path(download["file"]).resolve()
    require(server_path.parent == (media / "img_upload_server").resolve()
            and server_path.stem == upload["media_url"].rsplit("/", 1)[-1]
            and server_path.suffix.lower() in {".png", ".jpg", ".jpeg"}
            and server_path != input_path and server_path != (media / "img_selected" / pick["file"]).resolve(), "Server evidence must be a separate revision-named original download in img_upload_server")
    server = decode(server_path)
    require(server["sha256"] == download["sha256"], "Server download bytes changed or its declared SHA is wrong")
    require((server_path.suffix.lower() == ".png") == (server["format"] == "PNG"), "Server extension/actual image format mismatch")
    if not manual:
        require(server["dimensions"] == source["dimensions"] and server["rgb"] == source["rgb"]
                and server["alpha"] == source["alpha"], "Server dimensions/RGB/alpha differ; no tolerance or lossy exception is allowed")
    result = dict(id=sid, selected_attempt=pick["attempt"], selected_file=pick["file"],
                selected_sha256=pick["sha256"], origin=origin, destination_project_id=DEST,
                flow_url=upload["flow_url"], source_media_url=upload["media_url"],
                server_download_sha256=server["sha256"], dimensions=source["dimensions"],
                rgb_sha256=digest(source["rgb"]), alpha_sha256=digest(source["alpha"]),
                approval_scope_sha256=scope_sha)
    if manual:
        result.pop("rgb_sha256")
        result.pop("alpha_sha256")
        result.update(manual_representation_evidence(proof, ep, media, pick, source, server, upload_time, download_time))
    return result


def validate_registered_alias(alias_id, sid, destination_project, expected_origin, ep=EP, media=MEDIA):
    require(destination_project == DEST, "Child result project differs from the approved upload destination")
    ledger = read_json(Path(ep) / "images/upload_aliases_v1.json")
    require(ledger.get("schema_version") == 1 and isinstance(ledger.get("aliases"), dict), "Invalid upload alias ledger")
    require(alias_id in ledger["aliases"], "Explicit upload alias is missing/unproved")
    record = ledger["aliases"][alias_id]
    manual = record.get("proof", {}).get("proof_kind") == MANUAL_KIND
    require(record.get("status") == (MANUAL_KIND if manual else "verified_upload_identity_only") and record["proof"]["alias_id"] == alias_id
            and record["proof"]["id"] == sid and canonical_sha(record["proof"]) == record.get("proof_sha256"), "Alias proof identity/hash/status mismatch")
    actual = validate_proof(record["proof"], ep, media, record["validation"]["approval_scope_sha256"])
    require(actual == record["validation"] and actual["origin"] == expected_origin, "Alias no longer matches the current selected original source")
    result = dict(upload_alias_id=alias_id, flow_url=actual["flow_url"], source_media_url=actual["source_media_url"],
                selected_sha256=actual["selected_sha256"], approval_scope_sha256=actual["approval_scope_sha256"],
                alias_record_sha256=canonical_sha(record))
    if manual:
        result.update(proof_kind=MANUAL_KIND, exact_pixel_equal=False, lossless=False,
                      deterministic_transform_proven=False, manual_comparison_pass=True,
                      batch_receipt_sha256=actual["batch_receipt_sha256"], comparison_sha256=actual["comparison_sha256"])
    return result


def register_proof(proof, ep=EP, media=MEDIA):
    ep = Path(ep).resolve()
    manual = proof_shape(proof)
    require(isinstance(proof["alias_id"], str), "Upload alias ID must be explicit text")
    lock = ep / "images/.upload_aliases.lock"
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(proof.get("alias_id", ""))
    try:
        validation = validate_proof(proof, ep, media)
        path = ep / "images/upload_aliases_v1.json"
        ledger = read_json(path) if path.exists() else dict(schema_version=1, aliases={})
        require(ledger.get("schema_version") == 1 and isinstance(ledger.get("aliases"), dict), "Invalid upload alias ledger")
        ledger["scope"] = "Typed strict pixel identity or separately declared root-reviewed service representation; never automatic visual or per-generation UI approval"
        aid = proof["alias_id"]
        if aid in ledger["aliases"]:
            prior = ledger["aliases"][aid]
            require(prior["proof"] == proof and prior["validation"] == validation, "Refusing to overwrite a different existing alias")
            return prior
        require(not any(x["validation"]["source_media_url"] == validation["source_media_url"] for x in ledger["aliases"].values()), "Server revision is already registered to an alias")
        record = dict(status=MANUAL_KIND if manual else "verified_upload_identity_only", proof=proof, proof_sha256=canonical_sha(proof),
                      validation=validation, recorded_at_utc=datetime.now(timezone.utc).isoformat())
        ledger["aliases"][aid] = record
        temp = path.with_suffix(".json.upload_alias.tmp")
        with temp.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        temp.replace(path)
        return record
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--proof", required=True, type=Path)
    parser.add_argument("--record", action="store_true", help="Record this explicit, fully verified proof; default checks only")
    parser.add_argument("--episode-root", type=Path, default=EP)
    parser.add_argument("--media-root", type=Path, default=MEDIA)
    args = parser.parse_args()
    proof = read_json(args.proof)
    result = register_proof(proof, args.episode_root, args.media_root)["validation"] if args.record else validate_proof(proof, args.episode_root, args.media_root)
    print(json.dumps(dict(status=MANUAL_KIND if proof.get("proof_kind") == MANUAL_KIND else "verified_upload_identity_only", record_written=args.record,
                         alias_id=proof["alias_id"], validation=result,
                         visual_or_actual_attachment_approval=False), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        raise SystemExit(f"ERROR: {exc}")
