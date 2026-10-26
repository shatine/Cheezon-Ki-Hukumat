"""8편 영상 프롬프트 v1 (생성하지 않음). plan_v1 VID 24개, 첫 프레임은 images/prompts_v1.json의 같은 id 그림(v1_{id}_n).
규칙(cheezon-production references/prompts.md): [장면 동작]. [카메라 태그]. Movement / Speed / Framing / End + 접미사.
- 3D 원리는 locked-off static shot, 힘·흐름만 움직인다. "Keep the exact same shape … No new objects".
- 카메라 무빙은 약 2/10만(o02 tilt up, o03 drone, v12 slider, v23 drone pull back = 4/24), 사람 쪽 dolly in 없음, 같은 방향 연속 없음.
- 모든 클립에 밝기 고정 문장. "One single continuous camera movement" 문구 금지.
결과: video/vprompts_v1.json"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
LOCK = "[locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame."
LIGHT = "The lighting stays the same bright light for the whole shot, no darkening, no fade."
REAL = "Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
D3 = ("Clean bright 3D educational render, white-grey studio background. Keep the exact same bridge, gorge shape, colours and layout as the image. "
      "No new objects, no text, no labels. Ambient sound only. No dialogue, no music, no watermark.")
KEEP = "Keep the exact same bridge shape (two-rib steel truss arch, flat deck on slender piers, no piers in the river)."
S = [
 # id, 문장, 무빙, 동작, 카메라
 ("o01", "S01a~b", "locked", f"The ground shakes: rocks and dust tumble down both slopes of the gorge far below, while the train keeps rolling slowly across the deck and the bridge stays perfectly intact. {KEEP}", LOCK),
 ("o02", "S01c~S02a", "tilt up", f"The river flows gently below; the deck stays tiny and high in the sky. {KEEP}",
  "[slow tilt up]. Movement: tilt the camera slowly upward from the river to the bridge in the sky. Speed: very slow and even. Framing: the cliffs frame both sides, the bridge centred at the end. End: hold on the bridge high in the sky."),
 ("V02", "S02b~c", "locked", "The thin green bar grows slowly upward from the river until it touches the deck, then glows softly. The Eiffel Tower model, the red-and-white Qutub Minar tower, the bridge and the gorge stay exactly as in the image; nothing new appears.", LOCK),
 ("o03", "S02d", "drone", f"The passenger train glides across the deck; light clouds drift over the peaks. {KEEP}",
  "[drone slow push forward along the gorge]. Movement: fly slowly forward along the gorge toward the bridge. Speed: slow and even. Framing: the whole arch stays in frame. End: settle on a wide shot with the whole bridge and the train."),
 ("V04", "S04c", "locked", "The two steep rock slopes slowly highlight from bottom to top along their faces, showing how steep the V-shaped valley walls are; the river flows at the bottom. Keep the gorge shape exactly the same.", LOCK),
 ("V05", "S05c", "locked", "The tall pier on the steep slope slowly tilts and slides down the slope toward the valley floor as small rock pieces crumble from under its foot. The gorge stays exactly the same.", LOCK),
 ("V06", "S06b", "locked", "The two half-arches, standing on their cliff foundations, extend slowly toward each other and meet in the middle; then the orange push arrows pulse along each half-arch and flow down into the rock of both mountains.", LOCK),
 ("V07a", "S07b~c", "locked", "The hanging chain sways slightly and settles into its natural curve; blue pull arrows pulse along the chain toward both ends. The chain only hangs, it does not flip.", LOCK),
 ("V07b", "S07d", "locked", "The upside-down chain arch holds still; orange push arrows pulse along the arch from the top down into both cliffs.", LOCK),
 ("V09", "S09b", "locked", "Grey cement flows from the pipe only into the cracks inside the rock block: the cracks turn grey one by one, starting near the pipe and spreading outward, until every crack is filled and the rock reads as one solid mass. Nothing leaks out of the block and nothing drips onto the table; the block outline, the green top and the layered rock colours stay exactly the same.", LOCK),
 ("V10a", "S10a~b", "locked", "The drill hole is already made; the bright steel tendon slides deeper into the hole, then the yellow jack on the anchor block pulls the tendon tight.", LOCK),
 ("V10b", "S10c", "locked", "Blue pull arrows pulse along the taut tendon toward the anchor block, and orange push arrows from the block press into the slope, the cracks in the rock closing slightly.", LOCK),
 ("v12", "S12b~c", "slider", "The steel segment hangs from the cable crane and travels slowly across the gorge along the cable, swinging very slightly. The river far below is turquoise.",
  "[slider right]. Movement: glide the camera slowly to the right, following the segment. Speed: slow and even. Framing: the segment stays in the middle 70% of the frame. End: settle with the segment over the middle of the gorge."),
 ("V13", "S13b~c", "locked", "The two half-arches reach slightly further out over the gap; blue pull arrows pulse along the back-stay cables from the arch tips to the anchors in the rock.", LOCK),
 ("v14", "S14a", "locked", "The last steel segment is lowered slowly on its cable into the gap between the two half-arches until it fits in place; tiny workers guide it.", LOCK),
 ("V14", "S14b~c", "locked", "The yellow hydraulic jacks push and adjust until the gap between the two half-arch ends closes and they lock; then the back-stay cables slacken and fall away, and the arch stands by itself.", LOCK),
 ("V16a", "S16b~c", "locked", "The two deck girders slide only a few centimetres left and right on the flat black bearing pads, very gently, and the expansion joint gap between them narrows and widens slightly. The girders never lift and never separate from the pads, the pads stay flat, and the pier stays fixed.", LOCK),
 ("V16b", "S16d", "locked", "A gentle side-to-side shiver of the ground only: the whole diorama keeps exactly the same shape (one V-shaped gorge, the same slopes, the same river), the piers sway very slightly and the deck slides a tiny amount on its bearings. No new valleys, no change to the terrain, nothing falls.", LOCK),
 ("V17", "S17b", "locked", "The red damaged pier fades away; the deck above stays continuous and supported, and the small train crosses slowly over the gap.", LOCK),
 ("V18", "S18b~c", "locked", "White wind flow lines enter the wide valley mouth and squeeze into the narrow gorge, moving faster and closer together as they pass under the bridge.", LOCK),
 ("V20a", "S20b~c", "locked", "The left half of the arch slowly warms to a soft red glow and bends only very slightly, a barely visible change; the deck stays straight and level and the whole bridge stays intact. The shaded right half stays grey.", LOCK),
 ("V20b", "S20d", "locked", "Both rails stay on the deck the whole time and slide together a short distance along their fastenings toward the expansion joint, so the gap at the rail joint narrows slightly. The warm red area of the deck stays the same. No rail disappears or changes shape.", LOCK),
 ("V22", "S22a~b", "locked", "Orange push arrows flow down the arch into both reinforced cliffs, while the deck rocks gently on its bearing pads; the bridge stays intact.", LOCK),
 ("v23", "S23a", "drone pull back", f"No cuts and no scene changes. The white train crosses the bridge; clouds drift over the Himalayan ranges. {KEEP}", "[drone pull back]. Movement: fly very slowly backward and slightly up, away from the bridge. Speed: very slow and even. Framing: the whole bridge stays in the centre of the frame the whole time. End: a wide shot with the bridge still clearly visible in the centre among the mountains."),
]
# 클라우드 검수 v1~v4에서 확정한 첫 프레임 (PC img\ 폴더)
PICK = dict(o01="v1_o01_1", o02="v1_o02_1", V02="v1_V02_6", o03="v1_o03_2", V04="v1_V04_1", V05="v1_V05_1",
            V06="v1_V06_2", V07a="v1_V07a_2", V07b="v1_V07b_3", V09="v1_V09_1", V10a="v1_V10a_1", V10b="v1_V10b_3",
            v12="v1_v12_1", V13="v1_V13_3", v14="v1_v14_3", V14="v1_V14_1", V16a="v1_V16a_3", V16b="v1_V16b_4",
            V17="v1_V17_2", V18="v1_V18_2", V20a="v1_V20a_1", V20b="v1_V20b_2", V22="v1_V22_1", v23="v1_v23_2")
out = []
for i, sent, move, act, cam in S:
    suf = D3 if i.startswith("V") else REAL
    out.append(dict(id=i, image=PICK[i] + ".png", script=sent, move=move,
                    prompt=f"{act} {cam} {LIGHT} {suf}", save=f"CB\\clips_v1\\{i}.mp4"))
RETAKE = ["V09", "V16a", "V16b", "V20a", "V20b", "v23"]   # 클라우드 검수 v1 (2026-10-26) 다시 만들 것
for x in out: x["retake_v2"] = x["id"] in RETAKE
json.dump(out, open(HERE / "vprompts_v1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
moving = [x["id"] for x in out if x["move"] != "locked"]
print(len(out), "clips; camera moves:", moving, f"{len(moving)}/{len(out)}")
