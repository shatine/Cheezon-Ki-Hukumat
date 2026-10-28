"""Isolated identity/gate fixtures only. Never registers a production upload.

Run: python -B test_upload_alias_v1.py
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from PIL import Image, PngImagePlugin

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fixture_alias_module", HERE / "upload_alias_v1.py")
alias = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alias)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class AliasTests(unittest.TestCase):
    def setUp(self):
        self.workspace = HERE.parent.parent.resolve()
        self.temp = tempfile.TemporaryDirectory(prefix="ep09_alias_fixture_", dir=self.workspace)
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(self.workspace) and self.root != self.workspace
        self.ep, self.media = self.root / "episode", self.root / "media"
        images = self.ep / "images"
        images.mkdir(parents=True)
        for name in ("img", "img_raw", "img_selected", "img_upload_server"):
            (self.media / name).mkdir(parents=True)
        for name in ("record_review.py", "upload_alias_v1.py", "flow_project_policy_v1.json"):
            shutil.copy2(HERE / name, images / name)
        self.rr = alias.review_helpers(self.ep, self.media)
        self.rows = [dict(id=sid, kind="master", ref=None) for sid in sorted(alias.MASTERS)]
        self.rows += [dict(id="fixture_frame", kind="frame", ref="AT_C")]
        self.manifest = {x["id"]: x for x in self.rows}
        records = []
        for number, sid in enumerate(sorted(alias.MASTERS), 1):
            filename = f"v1_{sid}_1.png"
            image = Image.new("RGB", (16, 12))
            image.putdata([((x * 17 + number) % 256, (y * 21 + number) % 256, (x * y + number) % 256) for y in range(12) for x in range(16)])
            for folder in ("img_raw", "img", "img_selected"):
                image.save(self.media / folder / filename)
            item = dict(id=sid, attempt=1, decision="chosen", reason="ISOLATED FIXTURE ONLY",
                flow_url=f"https://flow.google.com/project/{self.rr.PROJECT}/edit/{number:08x}-0000-4000-8000-000000000000",
                result_media_url=f"https://flow-content.google/image/{number:08x}-0000-4000-8000-000000000000",
                raw_file=filename, clean_file=filename, root_opened_raw_original=True,
                root_opened_clean_original=True, actual_retake_reference_file=None, actual_ui_references=[])
            metrics = dict(raw=self.rr.measure(self.media / "img_raw" / filename),
                clean=self.rr.measure(self.media / "img" / filename), actual_retake_reference=None)
            records.append(dict(input=item, measurements=metrics, planned_ref=None, reference_picks={}))
        self.ledger = dict(schema_version=2, expected_ids=len(self.rows), review_log=records,
                           picks=self.rr.rebuild_picks(records))
        write(images / "prompts_v1.json", self.rows)
        write(images / "picks_v1.json", self.ledger)
        write(images / "source_revision_observations_v1.json", {"observations": []})
        dest = dict(service="Google Flow", project_id=alias.DEST,
                    project_url=f"https://flow.google.com/project/{alias.DEST}", browser_profile_label=alias.PROFILE)
        self.approval = dict(authorized=True, destination=dest,
            authorization=dict(user_answer_verbatim="기준 그림 6장 업로드 승인", destination=dest,
                               specific_assets=sorted(alias.MASTERS), recorded_at_utc="2026-10-28T00:00:00Z"),
            proposed_transfer=dict(asset_ids=sorted(alias.MASTERS), asset_count=6), assets=[])
        for sid in sorted(alias.MASTERS):
            pick = self.ledger["picks"][sid]
            self.approval["assets"].append(dict(id=sid, authorized=True, selected_attempt=1,
                selected_filename=pick["file"], sha256=pick["sha256"], dimensions=pick["dimensions"],
                original_flow_source_url=pick["flow_url"],
                proposed_upload_file=str(self.media / "img" / pick["file"]),
                selected_copy_file=str(self.media / "img_selected" / pick["file"])))
        write(images / "upload_approval_v1.json", self.approval)
        self.revision = "dddddddd-dddd-4ddd-8ddd-dddddddddddd"
        self.server = self.media / "img_upload_server" / f"{self.revision}.png"
        with Image.open(self.media / "img/v1_AT_C_1.png") as image:
            metadata = PngImagePlugin.PngInfo()
            metadata.add_text("fixture", "separate lossless server encoding")
            image.save(self.server, pnginfo=metadata)
        pick = self.ledger["picks"]["AT_C"]
        self.proof = dict(schema_version=1, alias_id="AT_C_fixture_upload", id="AT_C", selected_attempt=1,
            selected_file=pick["file"], selected_sha256=pick["sha256"],
            input_file=str(self.media / "img" / pick["file"]), input_sha256=pick["sha256"],
            destination_project_id=alias.DEST, destination_profile_label=alias.PROFILE,
            approval_file_sha256=sha(images / "upload_approval_v1.json"),
            upload=dict(observed_by="root", observed_at_utc="2026-10-28T00:01:00Z", evidence="ISOLATED fixture upload/revision observation",
                root_observed_upload_submission=True, root_observed_new_server_revision=True,
                flow_url=f"https://flow.google.com/project/{alias.DEST}/edit/eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
                media_url=f"https://flow-content.google/image/{self.revision}"),
            download=dict(observed_by="root", observed_at_utc="2026-10-28T00:02:00Z", evidence="ISOLATED fixture server-download observation",
                root_observed_server_download=True, from_media_url=f"https://flow-content.google/image/{self.revision}",
                file=str(self.server), sha256=sha(self.server)))

    def tearDown(self):
        assert self.root.resolve().is_relative_to(self.workspace) and self.root.resolve() != self.workspace
        self.temp.cleanup()

    def verify(self, proof=None):
        return alias.validate_proof(self.proof if proof is None else proof, self.ep, self.media)

    def child(self, alias_id="AT_C_fixture_upload", project=None):
        ref = dict(id="AT_C", flow_url=self.proof["upload"]["flow_url"],
            source_media_url=self.proof["upload"]["media_url"], upload_alias_id=alias_id)
        return dict(id="fixture_frame", attempt=1, actual_retake_reference_file=None,
            flow_url=f"https://flow.google.com/project/{project or alias.DEST}/edit/ffffffff-ffff-4fff-8fff-ffffffffffff",
            actual_ui_references=[ref])

    def refs(self):
        return self.rr.reference_picks("fixture_frame", self.manifest, self.ledger["picks"], self.ledger["review_log"], [])

    def manual_proof(self):
        """Explicit simulated root decisions in a private fixture, never real proof."""
        row = bytes(value for x in range(1376) for value in (x % 256, (x * 3) % 256, (x * 7) % 256))
        image = Image.frombytes("RGB", (1376, 768), row * 768)
        name = "v1_AT_C_1.png"
        for folder in ("img_raw", "img", "img_selected"):
            image.save(self.media / folder / name)
        review = next(x for x in self.ledger["review_log"] if x["input"]["id"] == "AT_C")
        review["measurements"]["raw"] = self.rr.measure(self.media / "img_raw" / name)
        review["measurements"]["clean"] = self.rr.measure(self.media / "img" / name)
        self.ledger["picks"] = self.rr.rebuild_picks(self.ledger["review_log"])
        write(self.ep / "images/picks_v1.json", self.ledger)
        pick = self.ledger["picks"]["AT_C"]
        asset = next(x for x in self.approval["assets"] if x["id"] == "AT_C")
        asset.update(sha256=pick["sha256"], dimensions=[1376, 768])
        write(self.ep / "images/upload_approval_v1.json", self.approval)
        server = self.server.with_suffix(".jpg")
        image.save(server, quality=85, subsampling=2)
        proof = copy.deepcopy(self.proof)
        proof.update(proof_kind=alias.MANUAL_KIND, selected_sha256=pick["sha256"], input_sha256=pick["sha256"],
                     approval_file_sha256=sha(self.ep / "images/upload_approval_v1.json"))
        proof["download"].update(file=str(server), sha256=sha(server))
        proof["upload"].update(root_opened_corresponding_filename_tile=True, observed_input_filename=name)
        receipt = dict(schema_version=1, receipt_id="ISOLATED_BATCH", destination_project_id=alias.DEST,
            destination_profile_label=alias.PROFILE, observed_by="root", evidence="ISOLATED six completed input tiles fixture",
            transfer_started_at_utc="2026-10-28T00:00:00Z", transfer_completed_at_utc="2026-10-28T00:00:10Z",
            completed_tiles_observed_at_utc="2026-10-28T00:00:10Z", root_observed_exact_six_input_files=True,
            root_observed_upload_completed_six_tiles=True,
            assets=[dict(id=x["id"], selected_attempt=x["selected_attempt"], selected_filename=x["selected_filename"],
                         input_file=x["proposed_upload_file"], input_sha256=x["sha256"]) for x in self.approval["assets"]])
        comparison = dict(schema_version=1, id="AT_C", selected_attempt=1, selected_file=name,
            selected_sha256=pick["sha256"], selected_png_file=proof["input_file"], server_download_file=str(server),
            server_sha256=sha(server), dimensions=[1376, 768], observed_by="root", observed_at_utc="2026-10-28T00:03:00Z",
            root_opened_selected_png_original=True, root_opened_server_jpeg_original=True,
            same_shape=True, same_composition=True, same_content=True, notes="ISOLATED explicit visual comparison fixture; not automatic or production review")
        comparison["pass"] = True
        for folder in ("upload_receipts_v1", "upload_comparisons_v1"):
            (self.ep / "images" / folder).mkdir()
        rp = self.ep / "images/upload_receipts_v1/fixture.json"
        cp = self.ep / "images/upload_comparisons_v1/fixture.json"
        write(rp, receipt); write(cp, comparison)
        proof.update(batch_receipt_file=str(rp), batch_receipt_sha256=sha(rp), comparison_file=str(cp), comparison_sha256=sha(cp))
        return proof

    def test_manual_representation_is_separate_and_persists_flags(self):
        proof = self.manual_proof()
        strict = {key: proof[key] for key in alias.PROOF_FIELDS}
        strict["upload"] = {key: proof["upload"][key] for key in alias.UPLOAD_FIELDS}
        with self.assertRaises(ValueError): self.verify(strict)
        validation = self.verify(proof)
        self.assertFalse(validation["exact_pixel_equal"])
        self.assertFalse(validation["lossless"])
        self.assertFalse(validation["deterministic_transform_proven"])
        self.assertFalse(validation["pixel_error_measurements"]["automatic_visual_pass"])
        self.assertGreater(validation["pixel_error_measurements"]["changed_channel_values"], 0)
        record = alias.register_proof(proof, self.ep, self.media)
        self.assertEqual(record["status"], alias.MANUAL_KIND)
        refs = self.refs()
        self.rr.validate_ui_references(self.child(), {}, refs, self.ledger["review_log"], [])
        self.assertEqual(refs["AT_C"]["input_upload_alias"]["proof_kind"], alias.MANUAL_KIND)
        self.assertFalse(refs["AT_C"]["input_upload_alias"]["exact_pixel_equal"])
        self.assertEqual(refs["AT_C"]["flow_url"], validation["origin"]["flow_url"])

    def test_manual_missing_receipt_or_comparison_or_open_flag_rejected(self):
        proof = self.manual_proof()
        for field in ("batch_receipt_file", "comparison_file"):
            bad = copy.deepcopy(proof); bad[field] = str(self.ep / "images/unknown.json")
            with self.assertRaises((ValueError, OSError)): self.verify(bad)
        comparison = alias.read_json(proof["comparison_file"])
        comparison["root_opened_server_jpeg_original"] = False
        write(proof["comparison_file"], comparison); proof["comparison_sha256"] = sha(proof["comparison_file"])
        with self.assertRaises(ValueError): self.verify(proof)

    def test_manual_receipt_wrong_id_sha_or_duplicate_rejected(self):
        proof = self.manual_proof(); original = alias.read_json(proof["batch_receipt_file"])
        for change in (lambda r: r["assets"][0].update(input_sha256="0" * 64),
                       lambda r: r["assets"][0].update(id="fixture_frame"),
                       lambda r: r["assets"].__setitem__(0, r["assets"][1])):
            receipt = copy.deepcopy(original); change(receipt)
            write(proof["batch_receipt_file"], receipt); proof["batch_receipt_sha256"] = sha(proof["batch_receipt_file"])
            with self.assertRaises(ValueError): self.verify(proof)

    def test_manual_wrong_master_changed_server_or_evidence_rejected_on_use(self):
        proof = self.manual_proof()
        comparison = alias.read_json(proof["comparison_file"]); comparison["id"] = "AT_N"
        write(proof["comparison_file"], comparison); proof["comparison_sha256"] = sha(proof["comparison_file"])
        with self.assertRaises(ValueError): self.verify(proof)
        comparison["id"] = "AT_C"; write(proof["comparison_file"], comparison); proof["comparison_sha256"] = sha(proof["comparison_file"])
        validation = self.verify(proof); alias.register_proof(proof, self.ep, self.media)
        path = Path(proof["download"]["file"]); path.write_bytes(path.read_bytes() + b"tampered")
        with self.assertRaises(ValueError):
            alias.validate_registered_alias(proof["alias_id"], "AT_C", alias.DEST, validation["origin"], self.ep, self.media)

    def test_manual_receipt_chronology_and_filename_tile_required(self):
        proof = self.manual_proof()
        bad = copy.deepcopy(proof); bad["upload"]["observed_input_filename"] = "v1_AT_N_1.png"
        with self.assertRaises(ValueError): self.verify(bad)
        receipt = alias.read_json(proof["batch_receipt_file"])
        receipt["completed_tiles_observed_at_utc"] = "2026-10-28T01:00:00Z"
        write(proof["batch_receipt_file"], receipt); proof["batch_receipt_sha256"] = sha(proof["batch_receipt_file"])
        with self.assertRaises(ValueError): self.verify(proof)

    def test_lossless_identity_register_and_child_preserves_origin(self):
        self.assertNotEqual(sha(self.server), self.proof["input_sha256"])
        validation = self.verify()
        alias.register_proof(self.proof, self.ep, self.media)
        path = self.ep / "images/upload_aliases_v1.json"
        original = path.read_bytes()
        alias.register_proof(self.proof, self.ep, self.media)
        self.assertEqual(path.read_bytes(), original)
        refs = self.refs()
        self.rr.validate_ui_references(self.child(), {}, refs, self.ledger["review_log"], [])
        self.assertEqual(refs["AT_C"]["flow_url"], validation["origin"]["flow_url"])
        self.assertEqual(refs["AT_C"]["input_upload_alias"]["source_media_url"], self.proof["upload"]["media_url"])

    def test_missing_alias_or_missing_alias_selector_rejected(self):
        with self.assertRaises((ValueError, OSError)):
            self.rr.validate_ui_references(self.child(), {}, self.refs(), self.ledger["review_log"], [])
        alias.register_proof(self.proof, self.ep, self.media)
        item = self.child()
        del item["actual_ui_references"][0]["upload_alias_id"]
        with self.assertRaises(ValueError):
            self.rr.validate_ui_references(item, {}, self.refs(), self.ledger["review_log"], [])

    def test_wrong_project_and_other_id_rejected(self):
        alias.register_proof(self.proof, self.ep, self.media)
        with self.assertRaises(ValueError):
            self.rr.validate_ui_references(self.child(project="22cd5ad1-3dbb-4183-a36b-48c7bc3e5144"), {}, self.refs(), self.ledger["review_log"], [])
        proof = copy.deepcopy(self.proof); proof["id"] = "fixture_frame"
        with self.assertRaises(ValueError): self.verify(proof)

    def test_partial_or_false_observation_rejected(self):
        for key in ("root_observed_upload_submission", "root_observed_new_server_revision"):
            proof = copy.deepcopy(self.proof); proof["upload"][key] = False
            with self.assertRaises(ValueError): self.verify(proof)
        proof = copy.deepcopy(self.proof); del proof["download"]["evidence"]
        with self.assertRaises(ValueError): self.verify(proof)

    def test_input_sha_and_disguised_local_download_rejected(self):
        proof = copy.deepcopy(self.proof); proof["input_sha256"] = "0" * 64
        with self.assertRaises(ValueError): self.verify(proof)
        proof = copy.deepcopy(self.proof); proof["download"]["file"] = proof["input_file"]
        with self.assertRaises(ValueError): self.verify(proof)

    def test_single_rgb_or_alpha_difference_rejected(self):
        for alpha_change in (False, True):
            with Image.open(self.proof["input_file"]) as image:
                image = image.convert("RGBA"); pixel = image.getpixel((0, 0))
                image.putpixel((0, 0), (pixel[0] ^ 1, *pixel[1:]) if not alpha_change else (*pixel[:3], 254))
                image.save(self.server)
            proof = copy.deepcopy(self.proof); proof["download"]["sha256"] = sha(self.server)
            with self.assertRaises(ValueError): self.verify(proof)

    def test_lossy_and_dimension_difference_rejected(self):
        jpeg = self.server.with_suffix(".jpg")
        with Image.open(self.proof["input_file"]) as image:
            image.save(jpeg, quality=70)
        proof = copy.deepcopy(self.proof); proof["download"].update(file=str(jpeg), sha256=sha(jpeg))
        with self.assertRaises(ValueError): self.verify(proof)

    def test_implicit_colour_or_bit_depth_conversion_rejected(self):
        for mode in ("I;16", "L"):
            Image.new(mode, (16, 12)).save(self.server)
            proof = copy.deepcopy(self.proof); proof["download"]["sha256"] = sha(self.server)
            with self.assertRaises(ValueError): self.verify(proof)
        Image.new("RGB", (17, 12)).save(self.server)
        proof = copy.deepcopy(self.proof); proof["download"]["sha256"] = sha(self.server)
        with self.assertRaises(ValueError): self.verify(proof)

    def test_revoked_approval_and_stale_selection_rejected(self):
        alias.register_proof(self.proof, self.ep, self.media)
        self.approval["authorized"] = False; write(self.ep / "images/upload_approval_v1.json", self.approval)
        with self.assertRaises(ValueError): alias.validate_registered_alias(self.proof["alias_id"], "AT_C", alias.DEST, self.refs()["AT_C"], self.ep, self.media)
        self.approval["authorized"] = True; write(self.ep / "images/upload_approval_v1.json", self.approval)
        self.ledger["picks"]["AT_C"]["sha256"] = "0" * 64; write(self.ep / "images/picks_v1.json", self.ledger)
        with self.assertRaises(ValueError): self.verify()

    def test_original_raw_and_source_revision_still_required(self):
        raw = self.media / "img_raw/v1_AT_C_1.png"
        raw.write_bytes(raw.read_bytes() + b"changed")
        with self.assertRaises(ValueError): self.verify()

    def test_confirmation_metadata_does_not_change_authorization_scope(self):
        validation = self.verify(); alias.register_proof(self.proof, self.ep, self.media)
        self.approval["confirmed_upload"] = True; write(self.ep / "images/upload_approval_v1.json", self.approval)
        found = alias.validate_registered_alias(self.proof["alias_id"], "AT_C", alias.DEST, validation["origin"], self.ep, self.media)
        self.assertEqual(found["source_media_url"], self.proof["upload"]["media_url"])

    def test_source_order_and_retake_alias_not_relaxed(self):
        alias.register_proof(self.proof, self.ep, self.media)
        self.manifest["fixture_frame"]["ref"] = "AT_C+AT_N"
        refs = self.refs(); item = self.child()
        item["actual_ui_references"].insert(0, dict(id="AT_N", flow_url=refs["AT_N"]["flow_url"], source_media_url=refs["AT_N"]["source_media_url"]))
        with self.assertRaises(ValueError): self.rr.validate_ui_references(item, {}, refs, self.ledger["review_log"], [])
        item = self.child(); item.update(id="AT_C", attempt=2, actual_retake_reference_file=str(self.media / "img_raw/v1_AT_C_1.png"))
        with self.assertRaises(ValueError): self.rr.validate_ui_references(item, {}, {}, self.ledger["review_log"], [])


if __name__ == "__main__":
    protected = {name: (HERE / name).read_bytes() if (HERE / name).exists() else None
                 for name in ("picks_v1.json", "upload_approval_v1.json", "upload_aliases_v1.json")}
    result = unittest.main(exit=False)
    for name, before in protected.items():
        path = HERE / name
        assert (path.read_bytes() if path.exists() else None) == before, f"Production file changed: {name}"
    raise SystemExit(0 if result.result.wasSuccessful() else 1)
