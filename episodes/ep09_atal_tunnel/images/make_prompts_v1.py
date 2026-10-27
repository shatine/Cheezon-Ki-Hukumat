"""9편 실측 장면 계획 → Flow 이미지/영상 첫 프레임 프롬프트.

실행: python images/make_prompts_v1.py
입력: ../plan/scene_catalog_v1.json, ../script/source_ko_sentences.json
출력: prompts_v1.json, prompt_validation_v1.json
아직 미생성/미검수. 승인 내레이션 파일은 읽기만 한다.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P = ('Photorealistic cinematic still, bright clear Indian daylight, vivid natural Bollywood colours, sharp focus, 16:9. '
     'No text, no letters, no logos, no watermark. Adults only, people small or medium distance, faces not close-up.')
D3 = ('Clean bright 3D educational diorama render, soft studio light, white-grey background, saturated clear colours, 16:9, '
      'no text, no labels, no letters. Colour code: heat = red-orange glow arrows, cold = icy blue, clean water = bright blue, '
      'waste water = brown-grey, electricity = thick cable with glowing yellow core, moisture = small white droplets. '
      'Force code: push = orange arrows, pull = blue arrows, heat = red glow, wind = white flow lines. '
      'For this engineering model only: rock = grey-brown, steel ribs and shotcrete = neutral grey, straight advance pipes = teal, '
      'injected grout = purple, water itself = blue, water-pressure PUSH arrows = orange. These are explanatory colours, not a claim about the site materials.')
NOTXT = ('No readable text, letters, numerals, logos, brand marks, number plates, signs, prayer flags, shrines or watermarks. '
         'Leave all figures, dates and narration labels for editing.')
NOCOPY = ('Use the reference only for the subject design, identity and orientation; '
          'use a clearly different camera position, subject size and framing from the reference image.')
EXC = ('the SAME simplified tunnel excavation model as the reference: a single tunnel void in a grey-brown rock block, '
       'already excavated space on screen left and unexcavated ground on screen right, advancing from left to right. '
       'A cut-away side reveals the upper heading. Long straight teal pipes lie parallel to the advance axis above the crown '
       'and extend ahead into the ground; in a transverse section their circular ends form an arch. '
       'Separate neutral-grey steel support ribs run transversely across the excavated section. '
       'Do not bend the advance pipes into arches. Do not turn the tunnel into twin vehicle bores')
DEEP = ('the SAME later-stage weak-ground tunnel model as the reference, in the same left-to-right coordinate system: '
        'one tunnel with a deep curved final invert below the flat roadway, the crown, side walls and bottom connected into '
        'a closed structural ring. The lower ground has already been excavated. This is the later final structure, '
        'not the earlier temporary closure of the upper heading and not a claim about every normal section')
SOUTH = ('the SAME south-portal reconstruction as the reference: a rectangular dark road opening beneath a brown sloping awning, '
         'yellow-orange vertical facade cladding, a forested Himalayan valley and a grey reinforced slope beside the portal. '
         'The road is one single two-way carriageway, exactly two lanes total, one lane each direction, exactly one central '
         'lane-separating line; no second dashed lane divider, no widening or road fork; the lane arrangement is clearly visible '
         'all the way to the dark rectangular mouth. '
         'No traditional ceremonial gate merged with the actual tunnel mouth; no green gabled north-portal facade')
NORTH = ('the SAME north-portal reconstruction as the reference: a large dark-green gable with a smaller red-brown front gable, '
         'yellow wall panels, a rectangular main road opening on screen right, small service space on the left, '
         'one single two-way carriageway, exactly two lanes total, one lane each direction, exactly one central '
         'lane-separating line; no extra lane divider or road fork; the small left service recess is not a second traffic bore. '
         'grey retaining walls and steep bare snowy Himalayan terrain. No south-portal forest facade or ceremonial gate')
CONST = ('the SAME construction reconstruction as the reference: one upper-heading excavation in weak fractured grey-brown ground, '
         'grey steel support ribs and rough shotcrete behind the working face, a compact yellow tracked machine and small Indian adult '
         'workers seen from behind or the side. Bright neutral-white work lamps give even daylight-balanced exposure underground; '
         'no sunlight through solid rock. No identifiable real worker or archival-photograph claim')
INTERIOR = ('the SAME completed-tunnel interior concept as the reference: a single bore carrying two-way traffic on two lanes, '
            'a flat road within a curved tunnel shell, neutral-grey walls, bright neutral-white illumination and clear separated side drains. '
            'No parallel vehicle bore, no central dividing wall, and no claim that the neutral illustrative finish is a measured site colour')

# 기준 그림의 ref=None은 관찰 요약에 근거한 최초 생성이다. 외부 사진을 받은 것처럼 표기하지 않는다.
MASTERS = {
    'AT_S': (None, 'south portal, observation-derived reconstruction', f'{P} Create an observation-derived reconstruction of the Atal Tunnel south portal: {SOUTH.split(": ", 1)[1]}. Wide three-quarter view from the approach-road shoulder, the entire facade visible, bright clear daylight, no cars, no people. Completely empty road and surroundings: no pedestrians, no workers, no human silhouettes, no people anywhere. This is a new illustrative reconstruction, not an archival photo. {NOTXT}'),
    'AT_N': (None, 'north portal, observation-derived reconstruction', f'{P} Create an observation-derived reconstruction of the Atal Tunnel north portal: {NORTH.split(": ", 1)[1]}. Wide three-quarter view, facade clearly visible in bright snowy daylight, no cars, no people. This is a new illustrative reconstruction, not an archival photo. {NOTXT}'),
    'AT_C': (None, 'construction reconstruction, upper heading', f'{P} Create a historical engineering reconstruction, not an archival photograph: {CONST.split(": ", 1)[1]}. Three-quarter view from safely inside the supported excavation toward the face, a little muddy water contained at the bottom, no catastrophe spectacle. Long straight crown advance pipes point ahead into the ground, grey transverse ribs remain distinct. {NOTXT}'),
    'AT_INT': (None, 'completed interior, neutral illustrative finish', f'{P} Create a neutral-finish interior concept, not a survey photograph: {INTERIOR.split(": ", 1)[1]}. Clear long view down the road from a side shoulder; no people, no cars. Keep side drainage separate from the road. {NOTXT}'),
    'G3D_EXC': (None, 'excavation engineering model', f'{D3} Create a physically coherent simplified cut-away excavation block: {EXC.split(": ", 1)[1]}. A stable wide three-quarter side view, the whole short block visible. One short upper heading only, solid lower bench still present, no flat finished road. Leave a clear dry working space beneath the supported crown, a little blue groundwater in cracks ahead, no arrows yet, no temporary invert yet. {NOTXT}'),
    'G3D_DEEP': ('G3D_EXC', 'later final deep-invert model', f'{D3} Using the reference only for the model style, material colours, single-bore identity and left-to-right axis: build a clearly LATER construction stage. {DEEP}. Remove the former lower bench and any temporary upper-heading invert; replace them with the deep curved permanent bottom connected to both sides. Show a flat grey road slab inside the ring and small separate drainage channels behind the lining, never through the road. Same stable three-quarter side view, no arrows yet. {NOTXT}'),
}

# 승인 문장마다 직접 읽히는 상태를 정한다. 문장을 바꾸거나 새 수치를 발명하지 않는다.
# (reference, render type, scene, epistemic boundary)
SCENE = {
    'S01a': ('AT_C', 'real', 'At the weak-ground face, bright blue-grey water and muddy rock fragments emerge from cracks toward the protected working space. A compact machine is small at left; the supported tunnel and the difficult ground dominate.', 'historical reconstruction'),
    'S01b': ('AT_C', 'real', 'A strong inflow of muddy water emerges at the excavated face and gathers in a low sump with a pipe leading away; the supported upper-heading cavity is still readable. Show abundant inflow without a measurement scale or a flood covering workers.', 'contractor-reported maximum; quantity added in edit'),
    'S01c': ('AT_C', 'real', 'Close-medium view of the emerging wet material: fractured grey stones and brown soil visible in the water, with part of a supported wall behind.', 'historical reconstruction'),
    'S01d': ('AT_C', 'real', 'Water carries loose soil and small broken rock onto a muddy pile at the edge of the working face, seen obliquely with a clear protected working space to the side.', 'historical reconstruction'),
    'S02a': ('AT_S', 'real', 'The completed south portal and its approach road, with two small unbranded passenger cars seen from behind entering the rectangular opening. The forested valley surrounds the identifiable facade.', 'observation-derived exterior reconstruction'),
    'S02b': ('AT_S', 'real', 'A distant high view of the real-shaped south portal very small within tall Himalayan ridges, the approach road leading into the mountain. Snowy high peaks behind and forest lower down; no cut-through mountain or route line.', 'altitude and length added in edit'),
    'S02c': ('AT_S', 'real', 'The completed south portal beneath the vast mountain, a closer road-shoulder view with the rectangular opening framed by its yellow-orange facade. Leave uncluttered sky and mountain area for later editing labels; no cut-through mountain or invented location of the difficult zone.', 'the under-600-metre upper-heading crossing period is attributed in edit, not final completion'),
    'S03a': ('AT_S', 'real', 'From a distant forested slope, a small approach road enters the south portal beneath a vast Himalayan ridge; the mountain overwhelms the small road.', 'illustrative context'),
    'S03b': (None, 'real', 'A winding Rohtang mountain-pass road climbing through steep Himalayan terrain, a few unbranded cars small and seen from behind or the side. No readable road signs, flags, shrines or identifiable landmarks invented.', 'illustrative old over-pass route; not exact survey'),
    'S03c': (None, 'real', 'A Himalayan mountain-pass road completely blocked by deep snow and an avalanche mound, stopped trucks tiny and seen from behind. Bright white snow, clear daylight; no trapped people or emergency victims.', 'historical seasonal isolation, not a current closure report'),
    'S03d': ('AT_S', 'real', 'An approach road disappears through the rectangular south-portal opening into the mountain while the ridgeline rises far above it, an oblique low-medium view from the road shoulder.', 'observation-derived portal reconstruction'),
    'S04a': (None, 'real', 'A high aerial view of a Himalayan road making many tight hairpin bends up a steep mountain slope; no drawn line, map text, or invented exact tunnel trajectory.', 'illustrative over-pass road'),
    'S04b': ('AT_INT', 'real', 'A clear long straight view inside the completed single two-way road tunnel, small unbranded cars seen from behind, clean road and light grey interior. The geometry makes the direct mountain passage readable.', 'government distance/time savings added in edit'),
    'S04c': ('AT_C', 'real', 'A view from the supported excavation toward a rough solid rock-and-mud face, with the machine stopped before it; the material barrier fills most of the picture and the working space is small.', 'historical reconstruction, no literal map-to-tunnel composite'),
    'S05a': ('G3D_EXC', '3d', 'Expose a close section of the ground above and ahead of the heading: irregular fractured blocks, muddy pockets and cracks, visibly different from one solid rock mass. The excavated void remains on the left.', 'simplified geology principle'),
    'S05b': ('G3D_EXC', '3d', 'Zoomed model crop of the weak zone ahead of the heading: loose small grey rock fragments in brown clay with blue water in connected pores, embedded in the same block. Keep components clearly separate and supported space visible at left.', 'simplified weak-ground composition'),
    'S05c': ('G3D_EXC', '3d', 'Show blue water and grey-brown loose fragments entering the left-hand excavated void from the right-hand face. A short open area lies immediately behind the face; no finished road.', 'simplified inflow principle'),
    'S06a': ('G3D_EXC', '3d', 'A small schematic pump and thick hose remove blue water from a sump at the lower edge of the supported upper heading. Weak cracked ground remains at the crown and sides above; no operator or numeric gauge.', 'pump question within the engineering model'),
    'S06b': ('G3D_EXC', '3d', 'Water is led away at floor level but loose cracked ground still remains above the crown and at the sides. Separate the visible drainage hose from the structural supports, with a few loose fragments poised above the opening.', 'general principle; pumping does not strengthen ground'),
    'S06c': ('G3D_EXC', '3d', 'Loose soil and rock intrude at the face and reduce the clear space around a small yellow machine in the upper heading. Show only a modest schematic intrusion, no crushed people or invented accident geometry.', 'general principle'),
    'S06d': ('G3D_EXC', '3d', 'In one coherent model, a side drainage pipe carries blue water away while grey ribs and shotcrete hold the crown and walls. Keep the clear workspace visible between these separate systems.', 'support and water handling together'),
    'S07a': ('G3D_EXC', '3d', 'A closer cut-away shows the crown edge at the face, the next patch of weak ground still solid ahead of the open void, and the straight advance pipes positioned to reinforce it. Keep the forward ground distinct from the excavated space.', 'sets up advance support in the engineering model'),
    'S07b': ('G3D_EXC', '3d', 'Reveal long straight teal steel tubes installed from above the heading face and extending horizontally rightward into the not-yet-excavated ground. The front portions stay embedded in solid material, never floating.', 'advance pipes run along the tunnel axis'),
    'S07c': ('G3D_EXC', '3d', 'Keep the same pipes straight along the advance axis, but remove a narrow transverse slice of the foreground ground so their circular ends are readable as an arch-shaped row above the crown. Distinct grey ribs are behind the face.', 'arch arrangement of pipe ends, not bent pipes'),
    'S07d': ('G3D_EXC', '3d', 'The teal crown tubes extend ahead of the face into the ground to protect the next short upper-heading advance; the upcoming excavation volume is a faint transparent cut-away below those pipes.', 'short advance protection, not full-tunnel roof'),
    'S08a': ('G3D_EXC', '3d', 'A clear cut-away detail of the pipe roof: straight teal pipe bodies extend ahead into ground while their mouths trace an arch above the crown; distinct grey transverse support ribs are behind the face.', 'pipe-roof name added in edit'),
    'S08b': ('G3D_EXC', '3d', 'Two parallel arch-shaped rows of teal pipe ends are visible above the crown in a cut-away weak-ground area; every tube extends straight forward along the axis. Grey transverse supports remain a separate element.', 'double row only where required in weak ground'),
    'S08c': ('G3D_EXC', '3d', 'Show a very short new heading opening under the advanced teal pipe canopy, immediately followed by a grey rib and shotcrete. The forward ground remains largely unexcavated.', 'advance reinforcement assists short excavation and support'),
    'S09a': ('G3D_EXC', '3d', 'A short supported upper-heading opening stops at a nearby face, with the remainder of the right-hand ground still solid. No long unsupported roof cavity.', 'short unsupported span principle'),
    'S09b': ('G3D_EXC', '3d', 'Expose only one short upper-heading advance beneath the teal pipes; the newest grey rib and fresh light-grey shotcrete sit immediately behind the new face. The lower bench remains solid.', 'upper heading first, immediate support'),
    'S09c': ('G3D_EXC', '3d', 'A narrow newly excavated axial strip is highlighted soft yellow immediately behind the face, with supporting grey ribs close behind and solid ground ahead. No ruler or numeral.', 'about one metre in some sections; added in edit'),
    'S09d': ('G3D_EXC', '3d', 'The next short advance is newly exposed on the right while the previous short section on the left already has its grey rib and shotcrete; solid lower bench remains underneath.', 'repeated excavation-support cycle, no time stretching'),
    'S10a': ('G3D_EXC', '3d', 'A small nozzle sprays light-grey shotcrete onto newly exposed rough crown and side ground, leaving a continuous supported surface immediately behind the face. The nozzle is schematic, no worker close-up.', 'shotcrete supports exposed ground'),
    'S10b': ('G3D_EXC', '3d', 'A detail of the fresh support system shows grey steel mesh against rough ground beneath shotcrete and a separate transverse steel rib seated at its feet. Keep advance pipes teal and axial.', 'combination where needed, not universal installation'),
    'S10c': ('G3D_EXC', '3d', 'A close cut-away through a cracked rock side wall shows long straight grey rock bolts passing through several fractured blocks into the surrounding rock. Their outer ends connect to bearing plates at the supported surface.', 'rock bolts in suitable fractured rock, not loose soil everywhere'),
    'S10d': ('G3D_EXC', '3d', 'Two adjacent short support zones in the same continuous heading show visibly different shotcrete thickness and support density appropriate to different ground patches. Keep the bore geometry continuous; no dimension labels.', 'schematic variation by ground conditions'),
    'S11a': ('G3D_EXC', '3d', 'A closer cut-away includes the two feet of a grey support rib meeting the upper-heading floor, with the curved crown support above and the lower bench still solid. No deformation claimed yet.', 'sets up the support-foot question'),
    'S11b': ('G3D_EXC', '3d', 'A general-principle model detail shows the feet of a roof-and-side support resting on visibly soft loose ground, with short orange load arrows directed into that weak base. Very slight schematic side distortion, no bottom heave and no invented field event.', 'general weak-footing principle, not observed bottom heave'),
    'S11c': ('G3D_EXC', '3d', 'Show firm support seating beneath both rib feet and a clear connected path for force toward the base. Keep the temporary upper-heading stage and solid lower bench, no finished road yet.', 'support needs a sound base'),
    'S12a': ('G3D_EXC', '3d', 'At the upper-heading stage, join the left and right support feet by a shallow temporary grey invert across the heading floor above the still-solid lower bench. The upper support loop is closed; no deep final invert or flat traffic road yet.', 'EARLIER temporary closure only'),
    'S12b': ('G3D_DEEP', '3d', 'Show the LATER lower excavation completed and a deep curved permanent final invert joining both side walls below the future flat road level. The earlier solid bench and temporary upper-heading floor are gone.', 'LATER final deep invert, separate from temporary stage'),
    'S12c': ('G3D_DEEP', '3d', 'The connected crown, both side walls and deep curved bottom form one closed ring around the road space. Orange load arrows follow the connected support path around the ring and into surrounding ground, without crossing the empty traffic space.', 'schematic connected structural support'),
    'S12d': ('G3D_DEEP', '3d', 'A flat grey road slab lies horizontally inside the deep closed structural ring, clearly above its lowest curved bottom. A small unbranded car gives scale; only one vehicle bore.', 'road inside later final structure'),
    'S13a': ('AT_C', 'real', 'A new camera view of the same wet weak-ground heading from beside a rib foot, with the protected working space framed by the rib and the rough face beyond. Do not copy the opening camera.', 'new callback composition'),
    'S13b': ('AT_C', 'real', 'A wide oblique view of water emerging from the rough face of the same supported upper heading, while the strengthened clear workspace remains visible to one side. A different camera angle and distance from the opening.', 'callback question, new source image'),
    'S13c': ('G3D_EXC', '3d', 'Show the EARLIER upper-heading stage only: straight advance pipes into the ground, one short freshly excavated patch, immediate ribs and shotcrete, and a shallow temporary closure linking support feet over the solid lower bench.', 'summary of support sequence; later final stage shown in its own shot'),
    'S13d': ('G3D_EXC', '3d', 'Grey structural support holds the heading shape, while blue water is still visible in cracks in the surrounding ground and entering a controlled lower collection channel. Support and water remain separate problems.', 'support does not remove groundwater'),
    'S14a': ('G3D_EXC', '3d', 'A closer cut-away view of blue water entering a collection point at the side of the supported excavation, with a clear continuous pipe leading toward an open outlet at the left edge. Keep the water away from the working floor.', 'question about drainage destination'),
    'S14b': ('G3D_EXC', '3d', 'Within the same cut-away block, purple grout occupies selected small cracks ahead and above the supported opening while a separate blue inflow route is collected into a pipe and taken leftward out of the working area. The main water outlet stays open.', 'grouting and collection used together'),
    'S14c': ('G3D_EXC', '3d', 'Show two different water paths in the same ground: fine cracks locally treated with purple grout and a larger blue inflow route deliberately connected to an open collection pipe. Keep them visibly separate.', 'different inflows need different handling'),
    'S15a': ('G3D_EXC', '3d', 'A clearly hypothetical principle model has a blue water-bearing channel in rock behind the supported lining, temporarily blocked by a small grey plug. A modest blue pocket accumulates behind it. No workers or site-specific incident.', 'HYPOTHETICAL blocked-path risk, not an actual construction action'),
    'S15b': ('G3D_EXC', '3d', 'In the hypothetical blocked water path, a larger blue water pocket stands behind the plug, with short orange PUSH arrows pointing from the retained blue water toward the tunnel lining. No water-pressure arrow points out of the lining into the water.', 'general water-pressure principle'),
    'S15c': ('G3D_EXC', '3d', 'Close view of blue water behind a grey tunnel lining pushing toward it with orange PUSH arrows; the grey shell carries the added load, a faint orange reaction path within the shell. Do not show catastrophic failure.', 'general load principle'),
    'S15d': (None, 'real', 'Indian adult engineer seen only from behind in a bright work room, studying an entirely blank diagram sheet beside a small unlabelled tunnel-ring model. No legible book, portrait, screen interface, signature or source document replica.', 'booklet attribution added in edit; no fabricated document contents'),
    'S16a': ('G3D_DEEP', '3d', 'In this drainage concept section, keep the main blue inflow path OPEN and collect it into a clearly continuous pipe and separate drain running leftward away from the road space. The pipe has a visible open outlet at the model edge, so the route is not a dead end.', 'collection and controlled drainage concept'),
    'S16b': ('G3D_DEEP', '3d', 'In a simplified drainage-equipped section, show a thin separate waterproofing layer behind the inner lining and a connected drainage route on its ground side leading down to an open pipe outlet outside the model. Blue water stays behind the barrier and away from the traffic road. No water inside an escape passage.', 'applies to equipped sections, not every section'),
    'S16c': ('G3D_DEEP', '3d', 'A coherent section shows selected cracks reduced with purple grout, a thin barrier behind the lining, and blue water still allowed into an open separate drain and out of the model. The flat traffic road stays dry.', 'water reduction and drainage combined by conditions'),
    'S17a': ('G3D_EXC', '3d', 'A newly supported upper heading remains within slowly responding fractured ground, shown with a very small schematic inward shift of the crown and sides. Do not show the sensor causing or preventing movement.', 'ground response continues after support'),
    'S17b': ('G3D_EXC', '3d', 'Small simple measurement targets at the crown and side walls are linked by faint straight blue observation lines to a small survey instrument on a stable floor point. No scale, digits, beam weapon or automatic ground control.', 'monitoring observes convergence'),
    'S17c': ('G3D_EXC', '3d', 'The measured crown and side positions are shown by faint previous-position outlines; beside the affected short zone, additional grey support is prepared while the excavation face stays close. Measurement lines observe only.', 'review and adaptation; no automatic stabilization'),
    'S17d': ('G3D_EXC', '3d', 'Two adjacent patches within one mountain block have different rock fracture and water conditions, with different local support density. One continuous single heading connects them; no identical universal cure.', 'ground-dependent support'),
    'S18a': ('G3D_EXC', '3d', 'A clearly simplified reconstruction of the difficult weak zone shows a local inward-deformed grey rib and a small fallen-material pile behind a protected barrier, with no people in danger. Preserve the single heading and surrounding weak ground.', 'documented additional collapse/deformation, no exact incident reconstruction'),
    'S18b': ('G3D_EXC', '3d', 'At the difficult face show additional straight teal advance pipes, selected purple grouted cracks and a separate open blue drainage pipe, while the already supported workspace remains behind. All three treatments are readable as different parts.', 'added measures during advance'),
    'S18c': ('G3D_EXC', '3d', 'The same weak-ground block has a small observation target by the face and a locally denser support zone, while the next short ground patch remains visible ahead. No magic sensor beam.', 'inspect ground then adapt reinforcement'),
    'S19a': ('AT_C', 'real', 'A construction bay in the short supported upper heading holds a drainage hose, extra grey ribs and compact machine waiting behind the wet face. No calendar, clock or final traffic road.', 'about four years was upper-heading crossing with associated work'),
    'S19b': ('G3D_EXC', '3d', 'Show one coherent difficult short zone with an open drainage route, stabilized loose material at the edge, and locally strengthened grey support. There is still an excavation face ahead and no finished road.', 'water handling, stabilization and support alongside excavation'),
    'S19c': ('G3D_DEEP', '3d', 'Show the LATER stage of the difficult zone after upper-heading passage: lower excavation has been opened and the deep final curved bottom is being connected to the side walls. No earlier temporary upper floor remains, and no completed traffic is shown.', 'later lower excavation and final invert'),
    'S20a': ('AT_C', 'real', 'Historical construction reconstruction of the final thin rock partition opened between two aligned excavation headings, a small irregular breakthrough hole with bright work light beyond, small adult workers distant and seen from behind. No real-person likeness, no flags or ceremony text.', '2017 breakthrough, not 2020 opening'),
    'S20b': ('AT_S', 'real', 'Completed south portal in clear daylight with a few small ordinary cars entering its rectangular opening, the grey side slope and forest visible. No ribbon ceremony, real public figure or date signage.', 'opening date added in edit'),
    'S21a': ('G3D_DEEP', '3d', 'A small car travels on the flat road within the completed closed ring, while blue groundwater remains visible outside the lining and drains through a separate open route. The road stays dry in this explanatory model.', 'groundwater remains after opening'),
    'S21b': ('AT_INT', 'real', 'Illustrative completed interior seen from a safe side shoulder, a small localized damp patch and droplets at one lining joint near a separate side drain; normal small cars far away. No widespread flooded road or current emergency.', 'historical post-opening leakage description in 2024, not current inspection footage'),
    'S21c': ('G3D_DEEP', '3d', 'The completed lining and flat dry road remain in place while an unobstructed blue drainage path behind the lining connects to a visible outlet. A small inspection tool at the outer pipe is secondary; no automatic repair.', 'ongoing drainage and structural maintenance principle'),
    'S22a': ('AT_N', 'real', 'A fresh wide three-quarter view of the north portal with its dark-green large gable, red-brown small front gable and yellow facade panels. The rectangular traffic opening stays on screen right, with grey retaining walls and bare snowy mountains.', 'new callback composition; north portal kept separate'),
    'S22b': ('AT_C', 'real', 'Another fresh view of the wet weak-ground face seen through the edge of an intact grey support rib, water and small loose fragments beyond, clear protected workspace in the foreground. No master composition copy.', 'callback question, new source image'),
    'S23a': ('G3D_EXC', '3d', 'EARLIER upper-heading model with blue water paths in cracks, straight teal pipes already embedded ahead, one short freshly opened heading strip, and immediate grey support behind. Solid lower bench remains.', 'first part of construction sequence'),
    'S23b': ('G3D_DEEP', '3d', 'LATER final closed ring with the deep curved bottom connected to both sides; blue water behind the lining has a separate open drain to the model edge. A flat grey road sits inside, not in the drain.', 'later bottom connection and separate water route'),
    'S23c': ('G3D_DEEP', '3d', 'Wide clear view of the completed single road space protected within the grey-brown mountain block: connected structural ring, flat two-way road inside and an open separate blue drainage route behind the lining. A very small unbranded car gives scale.', 'summary of protected empty space'),
    'S24a': ('AT_N', 'real', 'A bright, calm final view from a higher approach-road side toward the identifiable north portal and bare Himalayan ridge; one small car enters the rectangular opening on screen right. Use a different camera distance from the prior north-portal cut and leave open sky space for later editing graphics.', 'CTA text added in edit only'),
}

# 실제 영상의 첫 프레임은 동작이 끝난 화면과 구분한다. 바뀔 부재는 미리 물리적으로
# 지지된 자리에 놓는다. 이 표는 대본이 아니라 그림의 초기 물리 상태만 정의한다.
FRAME_INITIAL = {
    'S07a': 'INITIAL STATE: the next upper-heading patch is still solid ground. Existing crown pipes are embedded above the supported space; one additional straight teal pipe lies on a short supported drilling guide with its tip at the crown-level ground face, ready to advance rightward. No suspended unsupported pipe.',
    'S07b': 'INITIAL STATE: straight crown pipes already form an arch-shaped row of mouths in transverse view; one additional teal tube is partly inserted along the left-to-right advance axis, held by a short drilling guide behind the face. The next excavation patch beneath it is still solid.',
    'S07d': 'INITIAL STATE: straight teal pipes are already embedded ahead of the face. Directly beneath their forward reach, the next short upper-heading patch is still unexcavated; only the previous short space at left is open and supported.',
    'S08c': 'INITIAL STATE: two arch-shaped rows of straight teal crown pipes protect the next short upper-heading patch, which is still solid. Existing grey ribs support the previous left-hand excavation and the lower bench remains solid.',
    'S09a': 'INITIAL STATE: show only a short previously supported upper-heading opening at left and the next short unexcavated patch immediately ahead under the straight pipes. Grey support material is neatly staged on firm ground behind, not floating in the future opening.',
    'S09c': 'INITIAL STATE: a narrow axial patch immediately ahead of the heading is highlighted soft yellow but remains solid, ready for one short excavation advance. Previously installed ribs and shotcrete stand behind; no ruler or numeral.',
    'S09d': 'INITIAL STATE: the last short section already has its grey rib and shotcrete. The next adjacent short strip at right remains solid beneath the advance pipes, ready for a new excavation-support cycle.',
    'S10a': 'INITIAL STATE: a small newly exposed crown-and-side patch is still rough rock. A schematic shotcrete nozzle is held beside it, ready to spray. Mesh, transverse support and bolts already present in the previous left-hand section remain in place; do not coat the new patch before the action.',
    'S10c': 'INITIAL STATE: a close cut-away of the fractured side rock shows one long grey bolt partly inserted into a prepared bore crossing several cracks, its outer bearing plate aligned at the surface. Other installed bolts remain in the prior supported section.',
    'S11a': 'INITIAL STATE, GENERAL PRINCIPLE: a roof-and-side support sits on two small weak loose-ground footing patches over the still-solid lower bench. It is initially upright and very slightly stressed; no bottom heave or invented observed field collapse. Include the support feet clearly.',
    'S11b': 'INITIAL STATE, GENERAL PRINCIPLE: the support feet rest on weak loose ground and the side support is slightly distorted, with no bottom heave. Firm base material is positioned at the feet ready for local support improvement; it is a schematic principle rather than an observed Atal event.',
    'S12a': 'INITIAL STATE, EARLIER UPPER-HEADING STAGE: crown and side support stand above the still-solid lower bench. A shallow temporary invert lies between the two feet with one final small end connection not yet closed, supported by the ground beneath it. No deep final invert and no traffic road.',
    'S12b': 'INITIAL STATE, LATER STAGE ONLY: the remaining lower excavation has already been opened below the upper heading. The deep curved permanent bottom is partly formed on the ground and almost joins the two side walls, with one small closing section still incomplete. No temporary upper-heading floor or solid lower bench remains. No traffic yet.',
    'S12c': 'INITIAL STATE: the later permanent crown, side walls and deep curved bottom are fully joined into a closed ring, with the flat road slab inside. No force arrows are lit yet; the clear connected structural path is ready for the later force-flow explanation.',
    'S15a': 'INITIAL STATE, HYPOTHETICAL RISK MODEL: a larger water-bearing crack behind the tunnel shell has a small closed plug. A modest blue pocket has just begun to collect behind it. Keep the scene structurally stable; no pressure arrows, flood or catastrophic failure yet.',
    'S15b': 'INITIAL STATE, HYPOTHETICAL RISK MODEL: blue water stands behind a closed plug and reaches partway up a connected crack behind the grey lining. A few short orange PUSH arrows already point from water toward the structure, ready to grow in the later explanation. No explosion.',
    'S17a': 'INITIAL STATE: an already supported upper heading lies in fractured weak ground. Small observation targets are fixed on the crown and side walls, with faint previous-position outlines just outside them. Geometry is nearly undeformed at this start; no sensor stabilizes the ground.',
    'S17c': 'INITIAL STATE: faint previous-position outlines show a small observed inward movement of one short supported zone. Additional support is staged nearby on solid ground but not yet attached; the next excavation patch ahead is still solid. Observation lines remain passive.',
    'S18a': 'INITIAL STATE OF A SIMPLIFIED HISTORICAL RECONSTRUCTION: the difficult heading has a locally strained grey rib and a small loose-material pocket at the face, before the further intrusion described in the video. All people are absent from the hazard zone; no exact accident reconstruction.',
    'S18b': 'INITIAL STATE: an open drainage pipe is already connected and carrying a little blue water. An injection hose touches selected fine cracks and one additional straight teal crown tube is supported on its drilling guide, ready for the next reinforcement step. Keep these three systems separate.',
    'S19c': 'INITIAL STATE, LATER LOWER-STAGE CONSTRUCTION: the lower bench has been removed below the retained upper support. A deep curved permanent bottom is partly formed on the stable excavation base, with one short closing gap below, ready to connect to both side walls. No temporary upper floor or moving traffic.',
    'S20a': 'INITIAL STATE OF A HISTORICAL RECONSTRUCTION: a thin rough rock partition still separates two aligned headings, with only a small pilot opening revealing work light beyond. Small adult workers stand far back behind a safe barrier. No final wide breakthrough opening yet; no ceremony or flags.',
}

# 정지 이미지 분할은 실제 컷수만큼 서로 다른 촬영 거리·관심점을 지정한다.
REAL_VARIANTS = (
    'Wide three-quarter establishing composition, the whole relevant subject and its immediate surroundings visible.',
    'Closer oblique side composition, focus on the foreground physical detail that carries this sentence; the full scene stays identifiable behind it.',
    'Low medium-distance composition from a different side of the safe working space, foreground and background clearly separated.',
    'Higher oblique composition with a distinctly different subject size and foreground from adjacent shots; no near-duplicate crop.',
)
MODEL_VARIANTS = (
    'Stable three-quarter model view, whole relevant mechanism readable.',
    'Stable closer cut-away view centred on the physical connection described in this sentence; keep the same model axes.',
    'Stable wider cut-away view with the active part foregrounded and the protected working space behind it; keep the same axes.',
)
REPEAT_NULL_SUBJECT = {
    'S03c': 'the SAME snow-blocked mountain-pass road, deep snowbanks and small stopped unbranded trucks as the first reference shot; keep their design and winter terrain consistent but change the safe camera position',
    'S15d': 'the SAME small plain grey tunnel-ring model, entirely blank diagram sheets and generic Indian adult engineer seen from behind as the first reference shot; no document print or real-person likeness',
}


def read_catalog(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if isinstance(data, list):
        return data
    for key in ('assets', 'scenes', 'catalog'):
        if isinstance(data.get(key), list):
            return data[key]
    raise ValueError('scene_catalog_v1.json must contain an asset list')


def source_ids(row):
    value = row.get('source_ids', row.get('sentence_ids', row.get('sent_ids', row.get('sentences', row.get('source_id', row.get('sentence_id'))))))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    raise ValueError(f"{row.get('id')}: source sentence IDs missing")


def main():
    catalog_path = ROOT / 'plan' / 'scene_catalog_v1.json'
    if not catalog_path.exists():
        raise SystemExit('실측 plan/scene_catalog_v1.json 미작성. 최종 프롬프트는 아직 생성하지 않습니다.')
    catalog = read_catalog(catalog_path)
    sources = json.loads((ROOT / 'script' / 'source_ko_sentences.json').read_text(encoding='utf-8-sig'))
    source = {x['id']: x['ko_source'] for x in sources}
    errors = []
    rows = []
    needed = set()
    first_null_subject = {}
    for item in catalog:
        sid = item.get('id', item.get('asset_id', item.get('source_id')))
        if not sid:
            errors.append('asset has no ID')
            continue
        ids = source_ids(item)
        if any(x not in SCENE or x not in source for x in ids):
            errors.append(f'{sid}: unknown source IDs {ids}')
            continue
        # 실사 컷이 문장 경계를 걸쳐도 서로 다른 장소를 모핑·합성하지 않는다.
        # source_ids는 실제 겹치는 발화 전체, visual_source_ids는 이 한 장에서 보여 주는 의미다.
        dominant = item.get('dominant_sentence_id', ids[0])
        all_specs = [SCENE[x] for x in ids]
        visual_ids = [dominant] if all(x[1] == 'real' for x in all_specs) else ids
        specs = [SCENE[x] for x in visual_ids]
        render_types = {x[1] for x in specs}
        if len(render_types) != 1:
            errors.append(f'{sid}: real/3D source mixture {ids}; split the asset')
            continue
        kind = item.get('kind', item.get('type'))
        kind = {'IMG': 'image', 'VID': 'frame', 'i': 'image', 'v': 'frame', 'video': 'frame'}.get(kind, kind)
        if kind not in ('image', 'frame'):
            errors.append(f'{sid}: unknown kind {kind}')
            continue
        refs = list(dict.fromkeys(x[0] for x in specs if x[0]))
        if len(refs) > 1:
            errors.append(f'{sid}: construction-stage/reference mixture {refs}; split the asset')
            continue
        ref = refs[0] if refs else None
        if not ref and dominant in REPEAT_NULL_SUBJECT:
            if dominant in first_null_subject:
                ref = first_null_subject[dominant]
            else:
                first_null_subject[dominant] = sid
        if ref in MASTERS:
            needed.add(ref)
        render = specs[0][1]
        if item.get('master_id_override') and item['master_id_override'] != ref:
            errors.append(f"{sid}: required master {item['master_id_override']} differs from prompt ref {ref}")
        if item.get('principle') and (render != '3d' or kind != 'frame'):
            errors.append(f'{sid}: principle asset must be a 3D video first frame')
        variant = max(0, int(item.get('variant_index', item.get('variant', 1))) - 1)
        scene = ' '.join(x[2] for x in specs)
        initial_state = FRAME_INITIAL.get(visual_ids[0]) if kind == 'frame' else None
        if initial_state:
            scene = initial_state
        if isinstance(item.get('visual_detail'), str):
            scene += ' ' + item['visual_detail']
        same = {'AT_S': SOUTH, 'AT_N': NORTH, 'AT_C': CONST, 'AT_INT': INTERIOR, 'G3D_EXC': EXC, 'G3D_DEEP': DEEP}.get(ref, '')
        if ref and not same and dominant in REPEAT_NULL_SUBJECT:
            same = REPEAT_NULL_SUBJECT[dominant]
        if initial_state and ref == 'G3D_DEEP' and visual_ids[0] in ('S12b', 'S19c'):
            same = ('the SAME later-stage weak-ground tunnel model, material colours and left-to-right axis as the reference. '
                    'For this initial construction state the lower ground has been removed but the deep permanent bottom is still '
                    'partly formed as specified below, so the ring is not fully closed yet. No earlier temporary upper-heading floor '
                    'and no solid lower bench. Preserve the single-bore identity')
        head = P if render == 'real' else D3
        fixed = f' Using the reference image: {same}. ' if ref else ' '
        composition = (REAL_VARIANTS if render == 'real' else MODEL_VARIANTS)[variant % (len(REAL_VARIANTS) if render == 'real' else len(MODEL_VARIANTS))]
        if kind == 'frame' and render == '3d':
            composition += ' Locked-off static first frame, no camera movement; show the coherent initial physical state for the later mechanism animation.'
        prompt = f'{head}{fixed}{scene} {composition} {NOCOPY if render == "real" and ref else ""} {NOTXT}'
        rows.append(dict(id=sid, ref=ref, kind=kind, line=' / '.join(f'{x} {source[x]}' for x in ids),
                         script=' / '.join(source[x] for x in ids), source_ids=ids, visual_source_ids=visual_ids, prompt=prompt,
                         initial_state=initial_state,
                         render=render, representation='generated reconstruction' if render == 'real' else 'simplified engineering model',
                         boundary='; '.join(dict.fromkeys(x[3] for x in specs)), review_status='not evaluated by prompt generator; see images/picks_v1.md'))

    def add_parent(ref):
        parent = MASTERS[ref][0]
        if parent and parent not in needed:
            needed.add(parent)
            add_parent(parent)
    for ref in list(needed):
        add_parent(ref)
    master_rows = [dict(id=key, ref=ref, kind='master', line=label, script=label, source_ids=[], prompt=prompt,
                        representation='generated reference reconstruction; no external photo file attached',
                        review_status='not evaluated by prompt generator; see images/picks_v1.md')
                   for key, (ref, label, prompt) in MASTERS.items() if key in needed]
    result = master_rows + rows
    seen = set()
    for row in result:
        if row['id'] in seen:
            errors.append(f"duplicate ID {row['id']}")
        for ref in (row['ref'] or '').split('+'):
            if ref and ref not in seen:
                errors.append(f"{row['id']}: missing/forward reference {ref}")
        if not row['prompt'].endswith(NOTXT):
            errors.append(f"{row['id']}: missing no-text ending")
        seen.add(row['id'])
    if {x['id'] for x in rows} != {x.get('id', x.get('asset_id', x.get('source_id'))) for x in catalog}:
        errors.append('catalog asset IDs and prompt IDs differ')
    if len({x['id'].casefold() for x in result}) != len(result):
        errors.append('Windows case-insensitive asset-ID collision')
    if set(source) != set(SCENE):
        errors.append('approved sentence IDs and scene-specification IDs differ')
    report = dict(status='pass' if not errors else 'fail', errors=errors, asset_count=len(rows), master_count=len(master_rows),
                  total_prompts=len(result), measured_plan_source=catalog_path.relative_to(ROOT).as_posix(),
                  input_catalog_sha256=hashlib.sha256(catalog_path.read_bytes()).hexdigest(),
                  approved_sentence_specs=len(source),
                  asset_kind_counts={k: sum(x['kind'] == k for x in rows) for k in ('image', 'frame')},
                  check_scope='schema, source IDs, asset coverage, kind, real/3D separation, reference dependency order and no-text endings only',
                  visual_review='not performed by this generator; see images/picks_v1.md',
                  generation='not evaluated by this generator; see images/picks_v1.md')
    (HERE / 'prompt_validation_v1.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if errors:
        raise SystemExit('\n'.join(errors))
    (HERE / 'masters_v1.json').write_text(json.dumps(master_rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (HERE / 'prompts_v1.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
