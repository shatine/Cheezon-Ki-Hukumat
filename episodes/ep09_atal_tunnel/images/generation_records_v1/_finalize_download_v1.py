"""Preserve an observed Flow download, run configured dewm, measure both files."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image

record_path = Path(sys.argv[1]).resolve(strict=True)
data = json.loads(record_path.read_text(encoding="utf-8"))
media_root = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
basename = f"v1_{data['id']}_{data['attempt']}"
raw = media_root / "img_raw" / (basename + ".jpg")
clean = media_root / "img" / (basename + ".png")
assert not raw.exists() and not clean.exists(), "Output exists; inspect before resuming"
assert hashlib.sha256(data["exact_submitted_prompt"].encode()).hexdigest() == data["prompt_sha256"]
shutil.copyfile(data["result"]["downloaded_original_path"], raw)
subprocess.run([sys.executable, r"D:\youtube\7. Cheezon Ki Hukumat\tools\lama\dewm.py", str(raw), str(clean)], check=True)
for kind, path in (("raw", raw), ("clean", clean)):
    with Image.open(path) as image:
        data["result"][kind] = {"path": str(path), "format": image.format, "width": image.width, "height": image.height, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}
data["status"] = "generated; awaiting root strict review"
record_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"id": data["id"], "attempt": data["attempt"], "raw": data["result"]["raw"], "clean": data["result"]["clean"]}))
