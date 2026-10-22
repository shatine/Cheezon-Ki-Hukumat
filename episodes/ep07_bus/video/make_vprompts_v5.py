import json
SUF=" Photorealistic, bright midday daylight, vivid colours. Only adults, no children. Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
SUF3D=" Clean bright 3D educational render, white-grey studio background. Keep the exact same bus shape, colours and layout as the image. No new objects, no arrows, no text, no labels. Ambient sound only. No dialogue, no music, no watermark."
LOCK="[locked-off static shot]. Movement: camera completely still, no zoom, no pan. Speed: none. Framing: exactly the composition of the image. End: same frame."
MOV={
"slow dolly in":"Movement: move the camera physically forward in a straight line toward the main subject. Speed: smooth controlled push. Framing: keep camera height, lens direction and subject position consistent while distance closes. End: finish in a tighter composition.",
"slider right":"Movement: slide smoothly sideways to the right parallel to the subject. Speed: slow and even. Framing: keep the row of subjects readable and level. End: finish on a new section of the row.",
"push past":"Movement: move forward past a visible foreground object, edge or opening. Speed: smooth forward glide. Framing: let the foreground pass close to the lens while the space beyond becomes clearer, people stay small in the distance. End: arrive inside or beyond the foreground layer.",
"macro slow zoom in":"Movement: slowly increase lens focal length toward a tighter frame. Speed: gradual and even. Framing: keep the main visual target readable as it becomes larger in frame. End: finish on a stable tighter composition.",
"drone push in":"Movement: fly smoothly forward toward the subject. Speed: controlled aerial approach. Framing: keep the building centred and level. End: finish closer on the central dome.",
"drone pull back":"Movement: fly smoothly backward away from the subject or destination. Speed: controlled aerial retreat. Framing: keep the subject readable as more landscape appears. End: finish on a wider aerial composition.",
"zoom in 3D":"Movement: camera stays locked, only a slow straight optical zoom in toward the hose connection at the service post. Speed: gradual and even. Framing: the connection stays centred. End: finish on the close-up of the connection.",
}
# id: (image, narration S#, move or None, scene motion, is3d)
S=[
("PB","v5_PB_1","S01","slow dolly in","The retired red-maroon KSRTC bus stands still in the sunny scrapyard; palm leaves sway gently, light dust drifts.",0),
("s01","v5_s01_1","S01b",None,"Clothes on the line beside the bus flutter in a light breeze; palm leaves sway.",0),
("s02","v5_s02_1","S01c",None,"The adult man sitting beside his bags slowly lowers his head and sighs; a light breeze moves the trees.",0),
("s03","v5_s03_2","S02","slider right","Retired KSRTC buses stand in a row; inspectors in the distance walk slowly along them.",0),
("s04a","v5_s04a2_1","S03",None,"The yellow outline lines around the bus floor glow softly and pulse once; nothing else changes.",1),
("s04b","v5_s04b_2","S03b","push past","Empty bus interior with seats removed; sunlight patches lie still on the floor, dust drifts in the light.",0),
("s04c","v5_s04c_1","S04",None,"On the crowded rental balcony the landlord and tenant talk with small gestures; washing on the line moves in the breeze.",0),
("M3","v5_M3_1","S04b",None,"The cut-away bus home stays still; soft light shifts slightly across the bed and kitchen.",1),
("s05","v5_s05_1","S05",None,"The man in front of the bus home scratches his head and looks around; clothes flutter, leaves sway.",0),
("s06a","v5_s06a_2","S06",None,"The hand touches the hot car door handle and snaps back quickly; heat shimmer rises from the metal.",0),
("s06b","v5_s06b_2","S06b",None,"Orange heat glow flows from the sun into the roof and walls of the bus and spreads inside; the bus does not move.",1),
("s07a","v5_s07a_1","S07",None,"The man lying in the hot bus fans himself slowly and wipes sweat; a small table fan turns.",0),
("s07b","v5_s07b_1","S07b",None,"The outdoor AC unit fan spins and a yellow glow pulses along the power cable from the pole into the bus; orange heat keeps entering the roof.",1),
("s08","v5_s08r_2","S08",None,"The thick insulation layers in walls, ceiling and floor glow softly; the blue arrows of shrinking space move slightly inward and stop.",1),
("s09","v5_s09r_2","S09",None,"Orange heat travels from the hot outer sheet along the steel beam through the insulation and glows at the inner wood; the insulation stays pale.",1),
("s10","v5_s10_1","S10","macro slow zoom in","Water droplets slowly form and grow on the cold metal bottle; a few slide down.",0),
("s11a","v5_s11ar_2","S11",None,"Cold blue spreads along the steel beam; water droplets form on it, grow, merge and drip into the small puddle.",1),
("s11b","v5_s11b_1","S11b",None,"Mould on the damp bus wall stays still; a drip of water slowly runs down the panel.",0),
("s12","v5_s12_1","S12",None,"The green seals glow softly around the covered beam and fresh air flows out of the roof vent as a gentle shimmer.",1),
("s13","v5_s13_1","S13",None,"In the finished bright bus room a curtain moves softly in the breeze; the adult in the distance walks slowly.",0),
("s14a","v5_s14z_1","S14",None,"Blue water level in the fresh tank slowly drops while the brown level in the waste tank slowly rises.",1),
("s14b","v5_s14b_1","S14b",None,"The empty blue tank stays empty and the brimming brown tank bubbles slightly at the top.",1),
("s15a","v5_s15a_1","S15","zoom in 3D","Blue water flows in, brown waste flows out and a yellow glow travels along the cable between the bus and the service post.",1),
("s15b","v5_s15b_2","S15b",None,"Sun rays hit the roof solar panels and a thin yellow glow runs to the bus, then a stronger yellow glow comes from the outside power post.",1),
("s16a","v5_s16a_1","S16",None,"Blue, brown and yellow lines under the ground glow and flow between the plot and the bus; the fence and bus stay still.",1),
("s16b","v5_s16b_2","S17",None,"Traffic passes in the background; a scooter rides by slowly behind the parked bus.",0),
("s17a","v5_s17a_2","S17b",None,"The traffic police officer walks toward the bus; clothes on the bus side flutter; autos pass.",0),
("s17b","v5_s17b_1","S17c","drone push in","The fountain plays, small figures walk on the paths, flags move gently.",0),
("s18","v5_s18_2","S18",None,"The floating document with red stamp sways slightly and the padlock on the gate glints; nothing else moves.",1),
("s19","v5_s19_2","S19","drone pull back","The couple set up folding chairs beside the white camper van; trees move in the wind.",0),
("s20","v5_s20_1","S20",None,"Inside the camper the woman cooks at the small sink and the man sorts bags; curtains move slightly.",0),
("s21a","v5_s21a_2","S21",None,"The man pumps the hand pump and water pours into the plastic can.",0),
("s21b","v5_s21b_2","S21b",None,"The white camper van rolls slowly into the hotel parking while the guard waves it in.",0),
("s22","v5_s22_1","S22",None,"The clerk shakes his head and pushes the file back; the queue shuffles, ceiling fans turn.",0),
("s23","v5_s23_2","S23",None,"Police officers stand around the painted van; one walks around it writing; the crowd at the gate murmurs and shifts.",0),
("s24","v5_s24_1","S24","drone pull back","Caravans parked on pads with hoses connected; a person walks to the toilet block; mist drifts on the hills.",0),
("s25","v5_s25_2","S25",None,"The man stands looking at the bus, then tilts his head thinking; palm leaves sway.",0),
("s26","v5_s26_1","S26",None,"Blue water, brown waste and yellow power flow along the lines between the bus and the service post; the garden leaves sway slightly.",1),
("s27","v5_s27_2","S27",None,"The family sitting outside the bus home talk and laugh; clothes on the line flutter; warm light in the windows.",0),
("s28","v5_s28_2","S28","drone pull back","The family outside the bus home wave up; clothes flutter, palms sway.",0),
]
out=[]
for k,img,line,mv,motion,is3d in S:
    cam = f"[{mv}]. "+MOV[mv] if mv else LOCK
    out.append(dict(id=k,image=img+".png",script=line,move=mv or "locked",
        prompt=motion+" "+cam+(SUF3D if is3d else SUF),save=f"BUS\\clips_v5\\{k}.mp4"))
json.dump(out,open("vprompts_v5.json","w"),ensure_ascii=False,indent=1)
print(len(out), sum(1 for o in out if o["move"]!="locked"))
