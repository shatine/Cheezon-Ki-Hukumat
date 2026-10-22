"""EP7 도입부 0~30초 새로 만들기 (사용자 2026-10-22: h·m은 로컬 확인 없이 새로, PB 영상은 10초 전부 쓰게 다시).
도입 구성 (영상만, 자연스럽게 길게):
  o1 0.0~5.4 화려한 버스 집 → o2 5.4~10.5 한 달 뒤 → PB 10.5~20.5 (10초 전부) → s03 20.5~23.0 (기존 0~2.5초) → s04a 23.0~30.0 (기존 0~7초)
이미지: Flow, 한 장씩, 기준 그림 PB(v5_PB_1) 첨부. 저장 BUS\\img3d\\v8_{id}_{n}.png
영상: Muse, 한 개씩. 저장 BUS\\clips_v8\\{id}.mp4
결과: images/prompts_opening_v8.json, video/vprompts_opening_v8.json"""
import json, runpy
from pathlib import Path
HERE = Path(__file__).resolve().parent
g = runpy.run_path(str(HERE / "make_prompts_v6.py")); P, BUS = g["P"], g["BUS"]
IMG = [
 ("o1", "PB", "S01~S02a 앞: 화려한 버스 생활",
  f"{P} Using the reference image: {BUS}, now beautifully converted into a dreamy tiny home in a green Kerala garden at golden morning light: fresh cream curtains in the windows, warm string lights along the roof edge, a small wooden deck with potted plants and two cane chairs at the open door, an Indian adult couple at medium distance sipping chai on the deck, smiling. Inviting, glamorous, bright. Wide three-quarter shot, whole bus visible."),
 ("o2", "PB", "S02a 뒤~S02b: 한 달 뒤",
  f"{P} Using the reference image: {BUS}, converted into a home one month later on a scorching afternoon, parked on a bare dusty plot: curtains drooping, string lights hanging loose, plants dead and dry, a plastic bucket and water cans scattered, a small grey waste-water puddle under the rear, an Indian adult man at medium distance sitting on the door step, sweating, head in his hands. Harsh bright sun, wide three-quarter shot, whole bus visible."),
]
SUF = " Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
VID = [
 ("o1", "v8_o1.png", "S01~S02a", "slow dolly in",
  "The couple on the deck sip chai and laugh softly; string lights glow; curtains move in a light breeze; leaves sway. [slow dolly in]. Movement: move the camera physically forward in a straight line toward the bus. Speed: very slow, barely noticeable. Framing: the whole bus stays in frame, people stay small. End: settle on a slightly closer wide shot of the bus home."),
 ("o2", "v8_o2.png", "S02a~S02b", "locked",
  "The sweating man slowly lifts his head and wipes his face; dry leaves blow across the dusty ground; a loose string light swings. [locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame."),
 ("PB", "v5_PB_1.png", "S03a~S03b (10초 전부)", "slow dolly in",
  "The retired red-maroon KSRTC bus stands still in the sunny depot yard; palm leaves sway gently, light dust drifts. The lighting stays the same bright midday sun for the whole shot, no darkening, no fade, no clouds. [slow dolly in]. Movement: move the camera physically forward in a straight line toward the bus. Speed: very slow and even for the full 10 seconds. Framing: the whole bus stays in frame from start to end, never closer than the full bus. End: finish on a slightly closer wide shot with the whole bus visible."),
]
json.dump([dict(id=a, ref=b, line=c, prompt=d) for a, b, c, d in IMG], open(HERE / "prompts_opening_v8.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump([dict(id=a, image=b, script=c, move=d, prompt=e + SUF, save=f"BUS\\clips_v8\\{a}.mp4") for a, b, c, d, e in VID],
          open(HERE.parent / "video" / "vprompts_opening_v8.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(IMG), len(VID))
