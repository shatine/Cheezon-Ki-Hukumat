"""EP7 v6 추가 Muse 영상 프롬프트 (10초, 한 개씩). 이미지: images/prompts_v6.json을 Flow에서 검수 통과한 것.
- 문구 틀·접미사는 make_vprompts_v5.py와 같다. "One single continuous camera movement" 문구 금지(video-camera §0).
- 카메라: 기본 고정. 무빙은 s06c(slider right, 사람 없음), s26b(slider left, 차) 2개뿐 → 전체 신규 34 + 재생성 4 = 38개 중 무빙 2개. 편집 계획 v8 사용 클립 기준 비율은 shot_table_v8.md.
- 3D(is3d=1)는 고정, 열·물·냉기만 움직임.
결과: video/vprompts_v6.json"""
import json
from pathlib import Path
SUF=" Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
SUF3D=" Clean bright 3D educational render, white-grey studio background. Keep the exact same bus shape, colours and layout as the image. No new objects, no arrows, no text, no labels. Ambient sound only. No dialogue, no music, no watermark."
LOCK="[locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame."
MOV={
"slider right":"Movement: slide smoothly sideways to the right parallel to the subject. Speed: very slow, barely noticeable. Framing: keep the windows and light beams readable and level. End: settle on a still composition.",
"slider left":"Movement: slide smoothly sideways to the left parallel to the subject. Speed: very slow, barely noticeable. Framing: keep the camper van centred in the middle 70%. End: settle on a still composition with the van centred.",
}
# id, 문단, move or None, 움직임, is3d
S=[
("m2","S02",None,"The sweating man fans himself faster and wipes his forehead; the table fan turns; heat shimmer rises above the roof.",0),
("m3s","S02",None,"The man carrying the two buckets walks slowly away from the bus, turning his head aside; the small puddle stays under the bus.",0),
("m4","S02",None,"A drop falls from the mouldy ceiling into the bucket; condensation droplets slide down the fogged windows; the man looks up.",0),
("m5","S02",None,"The police officer keeps pointing away; the man lowers his head and lifts the rolled mattress.",0),
("s03b","S03",None,"The buyer hands the bundle of notes to the official, who takes it and nods; other men lower their raised hands.",0),
("s06c","S06","slider right","Sunbeams through the windows stay bright on the bed and floor; dust drifts slowly in the light.",0),
("s06d","S06",None,"The hand grabs the hot metal handrail and snaps back quickly; heat shimmer rises from the metal.",0),
("s08b","S08",None,"The worker presses one insulation panel into the gap between two steel ribs and smooths it with his palm.",0),
("s08c","S08",None,"The man straightens up slowly and his head nearly touches the low ceiling; he bends his neck again.",0),
("s09b","S09",None,"Sunlight from the windows slides very slightly across the bare steel ribs; dust floats; nothing else moves.",0),
("s09z","S09",None,"The red heat glow enters the steel rib from the outer sheet and travels along it to the inner panel; the insulation beside it stays pale.",1),
("s10b","S10",None,"The hand lifts the cold bottle out of the fridge; a thin cold mist drifts from the shelf.",0),
("s11c","S11",None,"The fingertips slide on the wet steel rib; water droplets gather and a thin line of water runs down.",0),
("s12b","S12",None,"The spray foam slowly covers the steel rib and the metal skin beside it, expanding and filling the gap.",0),
("s12c","S12",None,"The sealant bead runs along the window gap; the roof vent fan spins steadily above.",0),
("s13b","S13",None,"The man sits up in bed, stretches his arms and turns toward the toilet door at the rear.",0),
("s14c","S14",None,"The woman rinses the steel plate under the thin trickle of water and puts it aside.",0),
("s15c","S15",None,"The hands push the water hose onto the pedestal and plug in the power cable; the cable settles.",0),
("s16c","S16",None,"Grass at the edge of the plot moves in the wind; the tap stand, manhole and pole stay still.",0),
("s16d","S16",None,"The man runs his pen down the bill, stops, and rubs his forehead.",0),
("s18b","S18",None,"The hand presses the rubber stamp onto the file and lifts it; the ceiling fan turns.",0),
("s19b","S19",None,"The man stirs the pot on the small stove; steam rises; dhaba lights glow behind.",0),
("s20b","S20",None,"The two mechanics lift the AC unit into place inside the van and fix it to the wall.",0),
("s21c","S21",None,"The hand turns the tap; a few last drops fall and then nothing; the hand turns the tap again.",0),
("s22b","S22",None,"The white camper van drives through the frame from left to right past the checkpost arch.",0),
("s22c","S22",None,"The clerk slides the file back with a nod and the man takes it with both hands.",0),
("s23b","S23",None,"The ring light glows and the tripod stays still; leaves move behind the painted van.",0),
("s23c","S23",None,"The crowd at the gate pushes and shifts; the police officers hold their arms out to keep them back.",0),
("s23d","S23",None,"The padlocked gate stays shut; a police officer walks past slowly in the background.",0),
("s23e","S23",None,"The tow truck winch slowly pulls the painted van up onto the flatbed; the officer watches.",0),
("s24b","S24",None,"The white caravan drives slowly through the gate; the guard raises the barrier.",0),
("s24c","S24",None,"Water drips once from the hose connector; the cables stay still; grass moves slightly.",0),
("s24d","S24",None,"An adult walks along the path past the three bins toward the toilet block; mist drifts on the hills.",0),
("s26b","S26","slider left","Car headlights pass behind the parked camper van; the curtains on its windows stay drawn.",0),
("s26c","S26",None,"The couple count the notes and put them down on the bill; one rubs the neck.",0),
("s26d","S26",None,"Droplets slide down the fogged windows of the bus; the hoses outside stay connected; leaves sway.",0),
("s27b","S27",None,"Seen from high above, trees sway gently and a few leaves move; the bus home and the fence stay still.",0),
("s28b","S28",None,"The window lights glow steadily; the clothesline moves gently in the evening breeze.",0),
]
OUT = Path(__file__).resolve().parent / "vprompts_v6.json"
out=[]
for k,line,mv,motion,is3d in S:
    cam = f"[{mv}]. "+MOV[mv] if mv else LOCK
    out.append(dict(id=k,image=f"v6_{k}.png",script=line,move=mv or "locked",prompt=f"{motion} {cam}"+(SUF3D if is3d else SUF),save=f"BUS\\clips_v6\\{k}.mp4"))
json.dump(out,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out))
