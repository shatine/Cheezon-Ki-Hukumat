"""Veo용 장면 첫 그림 생성 (Vertex Gemini 이미지). 기준 그림 + 첫 비트 → first/<장면>.png, 버킷 <slug>_<에피소드>/first/ 에도 올림.
사용: python first_frame.py H2 [H3 ...]   (이미 있는 그림은 건너뜀, 약 $0.04/장)
인증: 실행할 때 gcloud 로그인 토큰을 받는다(파일에 키를 저장하지 않음)."""
import base64, subprocess, sys, time, requests
from kit import HERE, CH, NAME, load

G = CH["gcp"]
MODEL = G.get("image_model", "gemini-2.5-flash-image")
URL = f"https://aiplatform.googleapis.com/v1/projects/{G['project']}/locations/global/publishers/google/models/{MODEL}:generateContent"
BUCKET = f"{G['bucket']}/{NAME}/first/"
OUT = HERE / "first"; OUT.mkdir(exist_ok=True)
gcloud = "gcloud.cmd" if sys.platform == "win32" else "gcloud"
token = lambda: subprocess.run([gcloud, "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
plan = {p["id"]: p for p in load("plan.json")}

for sid in sys.argv[1:]:
    out = OUT / f"{sid}.png"
    if out.exists():
        print(sid, "exists"); continue
    p = plan[sid]
    first_beat = p["image"] or p["prompt"].split("\n")[0].split("] ", 1)[1]
    style = CH["styles"][p["style"]]["suffix"]
    # 기준 그림은 그 장면 첫 비트에 해당 인물이 있을 때만 붙인다(아무 장면에나 붙이면 인물이 끼어든다)
    refs = p["refs"]
    parts = [{"inlineData": {"mimeType": "image/png" if r.endswith(".png") else "image/jpeg",
                             "data": base64.b64encode((HERE / "ref" / r).read_bytes()).decode()}} for r in refs]
    text = (" ".join(CH["refs"].get(r, "") for r in refs) + " Show only what is described below. Do not add extra characters."
            + ("" if refs or CH.get("people_allowed") else " No people or figures at all.")  # people_allowed: 실사 사람 허용 채널(Cheezon)
            + "\nCreate the opening frame of this scene as a single wide 16:9 image. Only adults, absolutely no children or babies anywhere. "
            + first_beat + "\n" + style + " Still frame, cinematic composition. No text, no letters, no numbers, no logos.")
    parts.append({"text": text})
    body = {"contents": [{"role": "user", "parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}}}
    for wait in (0, 30, 60, 90, 120):  # 429(분당 한도)는 결과·비용이 없으므로 기다렸다 다시 보냄
        time.sleep(wait)
        r = requests.post(URL, headers={"Authorization": f"Bearer {token()}"}, json=body, timeout=300)
        if r.status_code != 429:
            break
    if not r.ok:
        print(sid, "ERR", r.status_code, r.text[:500]); continue
    img = [x for c in r.json().get("candidates", []) for x in c["content"].get("parts", []) if "inlineData" in x]
    if not img:
        print(sid, "NO IMAGE", r.text[:500]); continue
    out.write_bytes(base64.b64decode(img[0]["inlineData"]["data"]))
    subprocess.run([gcloud, "storage", "cp", str(out), BUCKET], capture_output=True)
    print(sid, "ok", out.name, flush=True)
    time.sleep(8)
