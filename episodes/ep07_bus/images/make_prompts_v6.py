"""EP7 v6 추가 이미지 프롬프트 (Flow, 한 장씩 검수). 계획: plan/shot_plan_v7.md
- 문체·색 규칙은 make_prompts_v5.py와 같다. ref = Flow에 붙일 기준 그림 id (picks_v5.txt의 파일).
- m2~m5: Muse 텍스트 생성본의 버스가 달라서 PB를 붙여 다시 만든다. v5 원래 내용 기록이 저장소에 없으므로
  아래 내용은 대본 기준 추정이다. PC의 v5_m2~m5 그림과 맞으면 그대로, 다르면 그림 쪽 내용에 맞춰 문장만 고친다.
- 실존 인물(E Bull Jet 형제, 판데이 부부)은 재현하지 않는다: 차·장소·멀리 있는 일반 성인만.
결과: images/prompts_v6.json"""
import json
from pathlib import Path
P=("Photorealistic cinematic still, bright clear Indian daylight, vivid natural Bollywood colours, sharp focus, 16:9. "
   "No text, no letters, no logos, no watermark. Adults only, people small or medium distance, faces not close-up.")
D=("Clean bright 3D educational diorama render, soft studio light, white-grey background, saturated clear colours, "
   "16:9, no text, no labels, no letters. Colour code: heat = red-orange glow arrows, cold = icy blue, clean water = bright blue, "
   "waste water = brown-grey, electricity = thick cable with glowing yellow core, moisture = small white droplets.")
BUS=("the SAME retired Kerala KSRTC ordinary bus as the reference image: classic red-maroon body with one yellow band, "
     "rounded front, flat roof, long row of side windows, faded paint, no readable text")
B3=("the SAME stylised 3D bus as the reference image (same shape, colours, window count, cut-away left side)")
WALL="EXACTLY the same bus wall cross-section as the reference image (red outer steel sheet, pale-yellow insulation, inner wood panel, grey steel rib), same camera"
VAN="the SAME white Force Traveller high-roof camper van as the reference image"
EBJ="the SAME brightly custom-painted camper van as the reference image (colourful wild graphics, extra roof lights and LED bar)"
S=[
# id, ref, 문단, prompt
# --- 도입 비참 장면 재생성 (같은 버스) ---
("m2","PB","S02 한 달 뒤: 더위", f"{P} Using the reference image: {BUS}, converted into a home one month later on a blazing afternoon. Through the open door an Indian adult man is seen inside, drenched in sweat, fanning himself with a plain hand fan beside a small table fan; heat shimmer above the metal roof. Medium-wide shot from outside."),
("m3s","PB","S02 한 달 뒤: 오수 (M3와 이름 겹침 방지)", f"{P} Using the reference image: {BUS}, converted into a home one month later, parked on a dusty plot. Behind the bus an Indian adult man holds his nose and carries two heavy covered plastic buckets away from a small grey puddle of waste water under the rear of the bus. Medium-wide shot, bright day."),
("m4","PB","S02 한 달 뒤: 곰팡이·물방울", f"{P} Inside the reference bus converted into a home one month later: the windows are fogged with condensation droplets, dark mould patches on the ceiling corner above the bed, a bucket on the floor catching drips; an Indian adult man stands at a distance looking up at the ceiling. Bright morning light."),
("m5","PB","S02 한 달 뒤: 쫓겨남", f"{P} Using the reference image: {BUS}, converted into a home, parked at a city roadside one month later. A traffic police officer in khaki at medium distance points away while an Indian adult man stands beside the bus door with a rolled mattress, shoulders slumped. Wide shot, bright day."),
# --- 길이 부족 보충 (v6 계획) ---
("s03b","PB","S03c 2라크에 팔림", f"{P} Using the reference image: {BUS}, at a KSRTC depot auction: a few Indian adult men in shirts stand at a simple folding table beside the bus, one hands over a bundle of rupee notes to an official, others raise their hands to bid. Medium-wide shot, faces small, no readable text."),
("s06c","PB","S06 창으로 쏟아지는 햇빛", f"{P} Interior of the reference bus converted into a home at noon: harsh direct sunbeams pour through the long row of side windows onto the bed and floor, bright hot patches of light, dust floating in the beams, no people. Wide interior shot along the bus."),
("s08b","PB","S08 단열재 시공", f"{P} Interior of the reference bus during conversion: an Indian adult worker presses thick pale-yellow insulation panels between the exposed steel ribs of the side wall, rolls of insulation and plywood sheets on the floor, bright work lights and window light. Medium-wide shot, worker's face small."),
("s08c","PB","S08 낮아진 천장", f"{P} Interior of the reference bus after insulation and wood panelling: the ceiling is visibly low, an Indian adult man stands under it and has to bend his neck, his head almost touching the panelled ceiling, narrow room. Medium-wide side shot, face small."),
("s09b","PB","S09 드러난 강철 뼈대", f"{P} Interior of the reference bus stripped to the shell: the inner panels removed, a regular row of grey steel ribs and rails directly joined to the red outer metal skin, sunlight coming through the windows, no people. Close-medium shot along the wall."),
("s09z","s09","S09 열교 확대", f"{D} Using the reference image: {WALL}, zoomed in closer on the point where the steel rib touches the outer sheet. A bright red heat stream enters the rib at the outer sheet and travels along the rib to the inner wood panel, while the insulation beside it stays pale and cool."),
("s10b",None,"S10 냉장고에서 병 꺼내기", f"{P} A bright Indian home kitchen: an adult's hand takes a steel water bottle out of an open fridge door, cold mist at the shelf, sunlit window behind. Close-medium shot, only the hand and arm visible."),
("s11c","PB","S11 젖은 뼈대 만지는 손", f"{P} Inside the reference converted bus at night under a warm lamp: an adult's hand touches an exposed steel rib behind a pulled-back wall panel, the cold metal is covered with water droplets and a thin line of water runs down. Close shot, only hand visible."),
("s12b","PB","S12 뼈대 덮는 폼 단열", f"{P} Interior of the reference bus during conversion: an Indian adult worker sprays pale-yellow spray foam insulation that fully covers the steel ribs and the outer metal skin between them, wearing a mask and gloves, bright work light. Medium-wide shot, face covered and small."),
("s12c","PB","S12 틈새 막기·환풍기", f"{P} Inside the reference converted bus: an adult's hands seal a window frame gap with a sealant gun, and above, a small roof vent fan spins in the ceiling. Close-medium shot, bright daylight."),
("s13b","PB","S13 아침에 깨서 화장실로", f"{P} Early morning inside the reference converted bus home, finished cosy interior with clean wood panels: an Indian adult man sits up in bed and stretches, then looks toward the tiny toilet door at the rear, soft bright sun. Medium-wide shot, face small."),
("s14c","PB","S14 좁은 싱크대 설거지", f"{P} Inside the reference converted bus home: an Indian adult woman washes a steel plate at a tiny kitchen sink, a thin trickle from the tap, a few dishes waiting, window light. Medium shot from the side, face small."),
("s15c","s24","S15 서비스 기둥에 연결", f"{P} Close-medium shot of a short grey service pedestal at a caravan site: adult hands connect a blue water hose and plug a thick power cable into it, a grey drain hose already attached, green grass around. Bright day, only hands visible, no readable text."),
("s16c",None,"S16 수도·하수·전기 있는 땅", f"{P} An empty fenced plot of land at the edge of an Indian town: a water tap stand, a concrete sewer manhole cover and an electric pole with a meter box at the corner, bare level ground ready for a vehicle. Wide shot, bright day, no people."),
("s16d",None,"S16 계산서 보는 남자", f"{P} An Indian adult man sits on plastic chair outside a small house holding a sheet of paper bill and a pen, frowning, a calculator on a stool beside him. Medium shot, face small and side-on, no readable text on the paper."),
("s18b",None,"S18 관청 서류 도장", f"{P} Inside an Indian government office: an official's hand presses a rubber stamp onto a thick file of papers on a cluttered wooden desk, files stacked, ceiling fan. Close shot, only hands, no readable text."),
("s19b",None,"S19 차를 집 삼아 사는 다른 사람", f"{P} A small converted camper van parked at a roadside highway dhaba at dusk, an Indian adult man cooking on a small stove beside its open side door, warm lights of the dhaba behind. Wide shot, figure small."),
("s20b","s19","S20 정비소 개조·에어컨", f"{P} Using the reference image: {VAN}, inside an Indian vehicle workshop with its side door open, two adult mechanics fitting a split AC unit and wood panels inside, tools on the floor. Medium-wide shot, faces small."),
("s22b","s19","S22 주 경계 고속도로", f"{P} Using the reference image: {VAN}, driving along an empty Indian national highway past a state border checkpost arch (no readable text), dry hills on both sides. Wide shot, bright day."),
("s22c","s22","S22 등록 완료", f"{P} Using the reference image: the same busy Indian RTO office: an Indian adult man at the counter receives back a file with a nod from the clerk, holding it with both hands. Medium-wide shot, faces small, no readable text."),
("s23b","s23","S23 유튜브 촬영 장비 옆 캠핑카", f"{P} Using the reference image: {EBJ}, parked on a Kerala roadside, a camera on a tripod and a ring light set up in front of it, no people. Wide shot, bright day, no readable text."),
("s23c","s23","S23 RTO 사무실 앞 소동", f"{P} Outside a Kerala government transport office gate: a crowd of young adults pressing at the gate seen from behind at a distance, police officers in khaki holding them back, the custom-painted van visible behind. Wide shot, bright day, faces not visible."),
("s23d","s23","S23 압수 차량 보관소", f"{P} Using the reference image: {EBJ}, parked behind a closed and padlocked iron gate in a police vehicle yard among other seized vehicles, a police jeep beside it. Wide shot, bright day, no people close."),
("s24b","s24","S24 파크 입구·경비", f"{P} Using the reference image: the same Kerala caravan park: the entrance gate in the fence with a small security cabin and a guard in uniform at a distance, a white caravan driving in. Wide shot, misty green hills."),
("s24c","s24","S24 서비스 기둥 확대", f"{P} Using the reference image: the same Kerala caravan park, close shot of one service pedestal beside a white caravan with a blue water hose, a grey drain hose and a power cable connected, wet grass. Close-medium shot, no readable text."),
("s24d","s24","S24 3색 쓰레기통·화장실동", f"{P} Using the reference image: the same Kerala caravan park, a clean toilet block building and a row of three colour-coded waste bins (green, blue, red) beside a paved path. Medium-wide shot, no readable text."),
("s26b","s19","S26 24시간 주차장의 캠핑카", f"{P} Using the reference image: {VAN}, parked in a crowded 24-hour city car park at night under sodium lights, other cars around, curtains drawn on its windows. Wide shot."),
("s26c",None,"S26 돈 세는 부부", f"{P} An Indian adult couple sitting at a small table counting rupee notes and looking at a thick bill, seen from the side at medium distance, faces small. Bright window light."),
("s26d","PB","S26 안의 물방울, 밖의 호스", f"{P} Using the reference image: {BUS}, converted into a home: inside, fogged windows with condensation; outside, a blue water hose, a grey drain hose and a power cable run from the bus to a ground connection post. Wide side shot, bright day."),
("s27b","PB","S27 위에서 본 버스 집과 땅 경계", f"{P} High aerial view looking down on {BUS}, converted into a home on its own small fenced plot with a garden, water pipe, drain and power line connected, neighbouring plots around. Bright golden hour."),
("s28b","PB","S28 해질녘 버스 집", f"{P} Using the reference image: {BUS}, converted into a cosy home on its fenced plot at dusk, warm lights glowing in all the windows, a clothesline outside, no people. Wide shot from ground level."),
]
OUT = Path(__file__).resolve().parent / "prompts_v6.json"
json.dump([dict(id=a,ref=b,line=c,prompt=d) for a,b,c,d in S],open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(S))
