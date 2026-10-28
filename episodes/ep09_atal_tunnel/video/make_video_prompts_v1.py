"""ep09 영상 프롬프트 준비 전용. Muse에 접속하거나 생성 요청을 보내지 않는다.

--draft: 미선택 첫 프레임을 null로 둔 초안만 저장한다.
--ready: 50개 실제 선택 파일과 파일별 동작 적합성 검토가 모두 확인될 때만
         vprompts_v1.json을 쓴다. 첫 프레임 준비와 Muse 실행 승인은 별개다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
EP = HERE.parent
DEFAULT_MEDIA_ROOT = Path(r"D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel")
LIGHT = "The lighting stays the same bright light for the whole shot, no darkening, no fade."
IDENTITY = (
    "Use exactly the selected first-frame image. Preserve its camera, single-bore identity, construction stage, "
    "material colours, object count and relative layout. No new objects, tools, supports, emitters, arrows, "
    "text, labels, logos or watermarks. Only the bounded physical motion described below is allowed. "
    "No shape morphing, teleportation, instant excavation, dissolving rock, self-growing supports or material creation. "
    "Fluid may enter or leave only through an inlet, hose or outlet already visible in the first frame. "
    "Tools and components must remain visibly supported or guided; never levitate. "
    "Never turn an upper-heading stage into a completed road tunnel or mix temporary and final inverts. "
    "No reverse playback, repeated action cycle, time lapse, slow motion or frozen-frame extension."
)
STRICT_PRINCIPLE_STILL = (
    "Every solid object stays completely still and keeps its exact shape and position for the whole shot: "
    "nothing slides, lifts, tilts, melts, disappears or leaks. Only light, colour and glowing arrows change."
)
PRINCIPLE_IDENTITY = (
    "Use exactly the selected first-frame image. Preserve its camera, single-bore identity, construction stage, "
    "base material colours, object count and relative layout. No new objects, tools, supports, emitters, arrows, "
    "text, labels, logos or watermarks. "
    + STRICT_PRINCIPLE_STILL + " "
    "All particles, pipes, buckets, cars, ribs, ground, observation targets and concrete retain their exact "
    "first-frame shape and position without any exception. Water and grout also retain their exact shape, "
    "level, quantity and location: no actual fluid flow, spraying, pouring, filling, ripples or leakage. "
    "Show direction only by a shallow moving colour-intensity highlight confined to an already visible material "
    "surface or existing diagram path; never extend it into a new path or across a physical gap. "
    "Any arrows already present keep their exact geometry, count and position; only their existing colour or "
    "glow may pulse. If no arrow exists in the first frame, no arrow appears. "
    "No excavation, seating, deformation, healing, rising water, new coating, stage morphing or material creation. "
    "Never turn an upper-heading stage into a completed road tunnel or mix temporary and final inverts. "
    "No reversed or repeated source playback, time lapse, slow motion or frozen-frame extension."
)
REAL = (
    "Photorealistic historical or place reconstruction, not documentary footage. Keep the exact same portal or "
    "interior finish as the selected image. Only existing Indian adults, no new people, no children; faces stay small. "
    "For an underground scene keep the existing neutral-white work-light exposure; no sunlight through rock. "
    "Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
)
D3 = (
    "Clean bright 3D educational render, white-grey studio background. Keep the exact same simplified model, "
    "single bore, left-to-right construction axis, shape, material identity and explanatory colours as the first frame. "
    "Every component and every material is physically motionless; there are no guided-component or ground-response exceptions. "
    "Only restrained surface illumination, colour intensity and the glow of arrows already present may change. "
    "Any arrows already present remain exactly where they are and do not multiply. No new arrows or labels. "
    "Water, injected grout and loose material remain distinct; the traffic road and any escape passage remain dry. "
    "Ambient sound only. No dialogue, no music, no watermark."
)

# 원리 43개는 첫 프레임의 실제 도형 위 빛·색만 변화한다. 실사 7개 동작은 별도 유지한다.
# tuple = (영어 강조/동작, 실제 첫 프레임에서 확인할 강조 대상, 종료 상태).
ACTION = {
    "o001": (
        "Existing muddy water continues from the visible face cracks down the same rough face into the already wet shallow collecting area immediately below. "
        "Only local splash and small ripples move within that established receiving area; the clear supported working strip and machinery stay in place. "
        "Do not route water into a hose, invent a drainage system, raise the water level or flood the workers.",
        ["face cracks and existing downward muddy inflow visible", "already wet shallow receiving area below the flow", "supported dry side working strip remains clear"],
        "The same controlled inflow continues; no growing flood or new fracture."),
    "o002": (
        "The water already at the face carries a few existing small loose stones and soil grains a short distance downward onto the same muddy pile. "
        "The pile changes only slightly and the protected side space stays open. No slab failure or falling large boulder.",
        ["water and small loose fragments at face", "existing muddy receiving pile", "clear protected side space"],
        "A few grains have settled on the existing pile; the same modest flow continues."),
    "o003": (
        "Only the two small cars already visible advance normally in their own existing lanes: the rear-view car in the incoming left-hand lane moves toward the same rectangular south-portal opening, "
        "while the farther car in the outgoing right-hand lane continues away from that opening. Neither car reverses or changes lane. "
        "Preserve exactly two lanes total and one central lane-separating line; no physical median or barrier, new cars, lane changes or road widening.",
        ["selected south portal geometry", "two existing small cars", "single two-way two-lane carriageway"],
        "The incoming car continues toward the same bore or is naturally occluded by its mouth; the outgoing car continues along its lane away from the bore. No vehicle reappears or respawns."),
    "o004": (
        "In the existing distant mountain view, only already visible pine branches move very slightly in a natural breeze. "
        "Keep the south portal, road, mountain and any existing cloud shapes fixed; do not invent a car, route line or mountain cut-away.",
        ["distant south portal within mountain landscape", "existing visible tree branches"],
        "The same wide landscape remains, with only a small continuing branch movement."),
    "p001": (
        "Use a shallow blue colour-intensity trace only on the existing connected pore-water shapes toward the exposed heading. Then softly illuminate the actual fractured block edges and clay pockets, distinguishing their existing textures without shifting any grain or liquid boundary.",
        ["existing connected blue pore-water shapes", "visible fractured rock and clay textures", "exposed heading on left"],
        "The same fractured-ground composition and pore-water geometry remain, with a restrained blue sheen on the existing path."),
    "p002": (
        "A restrained blue sheen progresses along only the water already visible at the right-hand face. Soft neutral-grey illumination then picks out the existing loose-fragment edges and the boundary of the short left-hand void. No particle trajectory, falling material or newly opened space is drawn.",
        ["existing blue water at the right-hand face", "visible loose-fragment edges", "existing short left-hand void"],
        "Water, fragments and void keep exactly their first-frame geometry; only their surface illumination differs."),
    "p003": (
        "Sequence a shallow blue highlight over the existing sump water and the already visible hose route. Separately illuminate the unchanged weak crown and side-wall cracks with a restrained neutral-grey sheen. The pump, equipment, grains and water surface remain motionless; no lower water level or healed ground is shown.",
        ["existing sump and visible hose route", "weak crown and side-wall cracks", "existing supported working space"],
        "The original sump level, hose, cracked ground and working space remain unchanged under the surface highlights."),
    "p004": (
        "First trace the already visible drainage route with a shallow blue intensity change. Then softly highlight the actual grey ribs and shotcrete around the protected workspace. Keep any face fragments and all drainage material fixed, showing the two existing systems by illumination alone.",
        ["existing drainage route", "installed ribs and shotcrete", "protected workspace"],
        "The same supported workspace and drainage geometry remain, without settling particles or additional support."),
    "p005": (
        "Pass a soft blue highlight along the existing separate side-drain material toward its already visible outlet. A restrained neutral-grey sheen then follows the existing crown and wall supports bordering the dry workspace. Do not alter liquid boundaries or the opening.",
        ["existing side-drain path and visible outlet", "existing crown and wall supports", "dry clear workspace"],
        "The drain, supports and clear workspace retain their exact first-frame shapes and positions."),
    "p006": (
        "A shallow teal highlight progresses along the actual straight pipe surface on its existing left-to-right axis, then along the already embedded crown pipes. Softly illuminate the still-solid next patch beneath them. The additional pipe and its guide remain in their original positions; nothing is inserted.",
        ["visible straight teal pipe and crown-level insertion point", "existing embedded crown pipes", "still-solid next patch"],
        "The exact original pipe insertion state and solid next patch remain, with only axial surface highlights."),
    "p007": (
        "Softly illuminate the existing arch-shaped row of pipe mouths one after another, then trace teal intensity along the actual straight longitudinal pipe bodies. Give the distinct grey transverse rib a separate restrained sheen. Preserve the partly inserted tube and solid next patch exactly as pictured.",
        ["arch-shaped row of existing pipe mouths", "straight longitudinal teal pipe surfaces", "separate transverse rib and solid next patch"],
        "All pipe mouths, axial bodies and transverse ribs retain their exact original geometry and insertion state."),
    "p008": (
        "Highlight the actual embedded teal canopy along its forward reach, then softly illuminate the still-solid short patch directly beneath it and the boundary of the previously supported opening at left. Any excavator, bucket and receiver remain completely still; no bite or removed material appears.",
        ["embedded straight canopy above the next patch", "still-solid short patch beneath the canopy", "previously supported opening at left"],
        "The canopy, solid next patch and supported opening remain exactly as in the first frame; only their existing surfaces carry light."),
    "p009": (
        "Use alternating shallow teal illumination on the two existing rows of straight canopy pipes, including their actual arch-shaped end arrangement. Then softly highlight the separate grey transverse rib and the existing short supported opening. No water animation or loose-grain movement is needed.",
        ["two existing rows of straight teal canopy pipes with arch-shaped ends", "separate grey transverse rib", "existing short supported opening"],
        "The same double-row canopy and supported opening remain physically unchanged, with their separate roles distinguished by light."),
    "p010": (
        "Sequence a restrained teal sheen over the two existing pipe rows, a neutral-grey highlight on the actual short exposed edge, and a soft highlight on the existing local support. Preserve every real gap and the support original seating position; the bucket, positioning arm and all material stay still.",
        ["existing double-row canopy", "short face edge and still-solid next patch", "existing local support and its actual connection surfaces"],
        "The same short edge, partly positioned support, lower bench and forward ground remain unchanged."),
    "p011": (
        "Softly distinguish the existing short solid patch from the previously open supported area using restrained surface illumination. Then illuminate only the existing exposed edge and nearby grey support in sequence. No bucket stroke, support seating or new cavity occurs.",
        ["short solid next patch", "previously supported upper-heading opening", "existing exposed edge and nearby grey support"],
        "The original short opening and solid next patch remain, with no physical excavation or support installation."),
    "p012": (
        "Gently vary the intensity of the soft yellow highlight already covering the narrow axial patch, confined to its exact existing boundaries. Then give the previous grey support a restrained sheen for comparison. All ground and equipment remain fixed; no numeral or apparent ten-second excavation is introduced.",
        ["existing narrow highlighted solid axial patch", "previously installed ribs and shotcrete"],
        "The narrow patch remains wholly in its first-frame state; only its existing highlight intensity changes."),
    "p013": (
        "Illuminate the already supported previous strip, then the actual next adjacent solid strip, then the existing nearby grey support. Each highlight stays on its own visible surface and stops at any real gap. Keep the machinery, staged support and ground completely fixed without starting another construction cycle.",
        ["previously supported strip", "next adjacent solid strip", "existing nearby support surfaces"],
        "The two original adjacent regions and all support components remain in their original construction state."),
    "p014": (
        "Use a restrained neutral-grey sheen to distinguish the shotcrete, mesh, ribs and bolts already present in the previous section. Briefly illuminate the existing texture of the rough target patch without turning it into a new coating. The nozzle, hose and any concrete remain fixed, with no spray or material growth.",
        ["existing shotcrete and mesh or rib surfaces in the previous section", "existing bolt surfaces", "rough uncoated target patch"],
        "The existing coated section and rough target retain their original textures and boundaries; no concrete is deposited."),
    "p015": (
        "A soft neutral-grey surface highlight follows the actual existing bolt shaft across the visible fracture locations, then the existing bearing plate. Do not extend the highlight beyond the real shaft or close a crack. The bolt, plate and bore remain exactly in their first-frame positions.",
        ["visible existing bolt shaft crossing cracks", "existing bearing plate and fracture edges"],
        "The bolt retains its original insertion depth and the cracks retain their original geometry."),
    "p016": (
        "Alternate restrained neutral-grey illumination between the two existing support zones, emphasizing their actual shotcrete thickness edges and different rib density. Keep the ground, support types and every material boundary fixed; no water or loose-grain animation is required.",
        ["two existing support zones with different density", "actual shotcrete thickness edges", "continuous original bore geometry"],
        "The two original ground-dependent support arrangements remain unchanged and readable side by side."),
    "p017": (
        "Apply a shallow muted-orange light emphasis only at the actual support-foot contact surfaces, then softly illuminate the existing weak footing texture underneath. The grains, feet, supports and lower bench remain exactly still; this general principle is indicated without settlement, heave or collapse.",
        ["clearly visible support feet and their contact surfaces", "weak footing texture", "solid lower bench"],
        "The support keeps its original upright geometry and the footing keeps its exact first-frame shape."),
    "p018": (
        "Softly illuminate the existing weak footing, the actual firm base material at the feet and the existing contact surfaces in sequence. Retain the support original slight distortion and every grain position; no material is placed, compacted or used to straighten the support.",
        ["existing weak footing and slightly distorted support", "firm base material already at the feet", "actual foot-to-base contact surfaces"],
        "The same base arrangement and initial support distortion remain, with only restrained contact-surface highlights."),
    "p019": (
        "Pass a shallow neutral-grey sheen along the actual continuous earlier-stage crown and side supports, down both feet and across the shallow temporary invert already joining them. Follow only the existing connected support surface above the solid lower bench. No component is installed or moved, and no deep final bottom or traffic road appears.",
        ["earlier upper heading above the solid lower bench", "shallow temporary invert already joined to both support feet", "continuous existing crown-side-foot-temporary-bottom connection"],
        "The already connected shallow temporary closure remains exact above the solid lower bench, with surface illumination alone."),
    "p020": (
        "Pass a restrained neutral-grey sheen along the actual continuous later-stage crown and side walls into the deep curved permanent bottom already connected to both sides. Emphasize the existing deep curve and its continuous structural path only. The lower bench is already completely removed; no temporary upper floor, incomplete joint or closing form appears, and no construction action occurs.",
        ["later stage with the lower bench completely removed", "continuous deep curved permanent bottom already connected to both sides", "existing connected crown-side-wall-deep-bottom path"],
        "The already connected later deep final structure retains its exact first-frame shape, with no temporary upper floor or construction transition."),
    "p021": (
        "Begin with restrained orange illumination at the actual ground-to-lining contact surfaces, then pass a shallow neutral-grey sheen along the existing continuous crown, sides and deep bottom. Follow only the genuinely connected lining surface around the closed ring. No new force arrows, elastic response or change of the flat dry road occurs.",
        ["fully connected later deep ring", "actual ground-to-lining contact surfaces", "dry flat internal road slab"],
        "The closed ring and its original contact geometry remain exact, with only a restrained highlight along the existing structural path."),
    "p022": (
        "Sequentially highlight the earlier embedded pipes in teal, the actual ribs and shotcrete in neutral grey, and the existing shallow temporary closure. Then trace blue intensity only on the already visible crack-water and collection-channel shapes. Keep the solid lower bench and all material boundaries fixed; do not replay construction.",
        ["earlier heading with solid lower bench and temporary closure", "existing pipes, ribs and shotcrete", "existing blue crack-water and collection channel"],
        "The earlier temporary-closure stage and its separate water geometry remain unchanged."),
    "p023": (
        "Give the existing grey support a restrained sheen, then pass a shallow blue colour-intensity highlight along the already visible crack-water into the existing lower channel. The liquid itself does not travel, change level or vanish, and the support does not seal any additional crack.",
        ["existing water-bearing crack shapes", "existing controlled collection channel", "unchanged grey structural support"],
        "The original support and separate blue water route remain physically unchanged around the clear workspace."),
    "p024": (
        "Trace a shallow blue highlight along the existing side collection point and continuous pipe to its visible left outlet. Separately pulse a restrained purple sheen only on the grout already occupying selected fine cracks. Preserve both material shapes, the open outlet and every crack boundary.",
        ["existing side collection point and continuous open outlet", "separate purple-treated fine cracks"],
        "The same open main outlet and locally treated fine cracks remain, without liquid or grout movement."),
    "p025": (
        "Alternate a soft purple highlight on the already treated fine-crack material with a blue intensity trace on the separate existing larger water route and open collection pipe. Keep the treated crack geometry and water volume fixed; no plug, grout or new flow path appears.",
        ["fine cracks already treated with purple grout", "separate existing blue route to an open collection pipe"],
        "The two original treated and draining routes retain exactly their first-frame boundaries and arrangement."),
    "p026": (
        "Gently pulse blue intensity inside the exact existing water pocket behind the closed plug, then softly illuminate its actual contact with the surrounding grey shell. The pocket boundary, level and quantity remain fixed throughout. No new pressure arrow or higher water shape appears in this hypothetical risk diagram.",
        ["existing closed plug and blue pocket", "actual water-pocket boundary and adjacent grey shell"],
        "The hypothetical risk model retains its original pocket level, plug and stable shell, with illumination changes only."),
    "p027": (
        "Pulse only the colour intensity of the short orange pressure arrows already visible, one after another, while retaining their exact length, shape, number and position. A shallow blue sheen may vary within the existing water shape and a restrained grey sheen on the adjacent lining. The water level, plug and lining remain fixed.",
        ["existing short orange pressure arrows", "fixed blue water shape behind the plug", "adjacent grey lining surface"],
        "The same water level and intact shell remain, with the existing pressure markers unchanged except for their glow."),
    "p028": (
        "Pass a shallow blue colour-intensity trace along the existing ground-side water shapes behind the waterproof layer, down their actual connected drain and toward its visible outlet. Briefly highlight the separate barrier surface. Water, barrier, lining and deep invert remain fixed; no blue highlight enters the traffic space or an escape passage.",
        ["continuous existing ground-side water path", "waterproof layer distinct from lining", "separate drain and visible open outlet"],
        "The original separated waterproofing and drainage geometry remains, with the road dry and every liquid boundary fixed."),
    "p029": (
        "Highlight the existing purple-treated cracks and thin barrier separately, then trace shallow blue intensity on the actual behind-barrier water route toward its existing outlet. Do not extend a highlight through a sealed crack or across the road; all grout, water and structural geometry remain motionless.",
        ["existing purple-treated cracks", "thin barrier behind the lining", "continuous existing water route to outlet"],
        "The original treated cracks, barrier and independent draining route remain unchanged around the dry road."),
    "p030": (
        "Use a restrained purple sheen on the existing local sealing, a soft neutral sheen on the thin barrier, and a shallow blue intensity trace on the separate open drain. Confine every highlight to its actual first-frame surface; no sealing spreads and no water shape or final-ring geometry changes.",
        ["existing purple sealing and thin barrier", "existing open blue drain path", "dry road within the later ring"],
        "The same combined sealing and drainage arrangement remains exact, with only distinct surface highlights."),
    "p031": (
        "Softly illuminate the existing crown target, side-wall targets and passive previous-position outlines in sequence, then their actual neighbouring support surfaces. All targets, outlines, ground and support retain their exact first-frame positions. Do not add a laser, measurement digit, movement or automatic stabilizing response.",
        ["existing crown and side-wall observation targets", "existing passive previous-position outlines", "actual adjacent support surfaces"],
        "The original target positions and observed geometry remain unchanged, distinguished only by restrained illumination."),
    "p032": (
        "First illuminate the existing observed position difference and passive outlines, then the already present local support and its actual connection surfaces. Any staged support, guide and positioning arm remain exactly where they were. No component seats, no gap closes and no sensor repairs the ground.",
        ["existing observation difference and passive outlines", "existing local support and actual connection surfaces", "still-solid next excavation patch"],
        "The original observed difference and support arrangement remain, with no installation or automatic response."),
    "p033": (
        "Alternate restrained illumination over the two existing ground patches and then their different local support densities. Emphasize only actual fracture edges and support surfaces. No ground, grain, fluid or lining changes geometry and neither support arrangement transforms into the other.",
        ["two existing adjacent ground patches", "different local support densities and visible fracture edges"],
        "The two original ground-dependent arrangements remain physically distinct and unchanged."),
    "p034": (
        "Softly highlight the actual strained rib surface in neutral grey and the existing loose-material face pocket with restrained muted-amber illumination. Keep the rib distortion, every fragment and all ground exactly as pictured. No fall, additional strain, receiver movement or new accident event is animated.",
        ["existing locally strained rib", "existing loose-material pocket at the face", "empty protected hazard area"],
        "The original simplified historical condition remains unchanged, with no new collapse or displacement."),
    "p035": (
        "Highlight the three existing systems separately: blue intensity along the open drainage path, restrained purple light along the actual injection-hose surface to its visible fine-crack contact, and a shallow teal sheen along the straight crown pipe axis. Stop every highlight at the existing geometry; do not extend purple material into an empty crack. No grout flows and no pipe is inserted.",
        ["existing separate blue drainage path", "injection hose contacting visible selected fine cracks", "existing straight teal crown pipe and its axial surface"],
        "The three original systems remain separate and fixed, with their roles shown only by existing-surface colour highlights."),
    "p036": (
        "Softly illuminate the existing observation target, then the locally denser grey support and the boundary of the still-solid next ground patch. Keep all three in their exact original positions. No new water route, moving grain, measurement beam or added support is needed.",
        ["existing observation target", "locally denser grey support", "still-solid next ground patch"],
        "The original local observation and support arrangement remains exact, without material movement or reinforcement growth."),
    "p037": (
        "Trace a shallow blue highlight on the existing open drainage route, then a restrained neutral-grey sheen on the strengthened support and a soft light emphasis on the already stabilized loose-material edge. Preserve every fragment position and the forward excavation face; no finished road or new cavity appears.",
        ["existing open drainage route", "already stabilized loose-material edge", "existing strengthened support and forward face"],
        "The same difficult short zone and its support and water geometry remain, with surface illumination alone."),
    "p038": (
        "In this already open later lower stage, softly illuminate the existing deep permanent-bottom concrete, the supported closing-form edges and the actual side-wall connection surfaces. Stop at each real joint gap. Keep the feed hose, fresh material, retained upper support and bottom geometry fixed without pouring or closure.",
        ["later lower-stage excavation already open", "existing deep-bottom material and supported closing-form edges", "actual final-invert connection surfaces"],
        "The later lower-stage joint and deep-bottom structure retain their exact original construction state and gaps."),
    "a001": (
        "The compact machine already present uses its existing face-contact tool to remove a few small fragments from the thin partition beside the pilot opening. "
        "Fragments fall into the existing receiving space and the same work light beyond becomes slightly more visible. "
        "Do not dissolve the whole wall, blast, create a wide opening instantly or add a ceremony. Distant workers stay safely behind the existing barrier.",
        ["thin partition and small pilot hole", "existing supported machine tool contacting partition", "existing fragment receiving space and safety barrier"],
        "The pilot opening is a little wider through physical removal; the remaining partition and scene remain coherent."),
    "p039": (
        "A restrained grey sheen follows the existing connected final ring around the dry road space. Then pass a shallow blue colour-intensity trace along the separate existing groundwater route outside the lining. The small car, road, water and membrane remain exactly in their first-frame positions and shapes.",
        ["later connected ring and dry road space", "separate existing groundwater route outside the lining", "existing small car on the road"],
        "The same stationary car and protected road space remain inside the unchanged ring, with water geometry fixed outside it."),
    "a002": (
        "Only the already visible droplets at the lining joint detach one at a time, fall by gravity and reach the existing side drain. "
        "Keep the damp patch small and the road dry; existing distant cars may continue normally. Do not add an inspector, handheld torch, flood or emergency.",
        ["small damp lining joint with existing droplets", "separate side drain", "dry road"],
        "The same small local leak continues into the side drain without spreading."),
    "a003": (
        "In the selected closer view, follow the existing small droplets from the same lining joint to the already visible side-drain edge with a fixed camera. "
        "Water makes only small contact ripples in the drain; no wet area expands across the road and no new person or tool enters.",
        ["closer view of existing droplets and joint", "visible side-drain contact point", "dry road"],
        "The same localized droplets and small drain ripples remain, with unchanged interior geometry."),
    "p040": (
        "Trace shallow blue intensity only along the existing unobstructed behind-lining route to its visible outlet, then softly highlight the actual lining surface. The water shape and level, road and any inspection tool stay fixed. No tool operates and no repair, blockage or opening appears.",
        ["unobstructed existing behind-lining route", "visible outlet", "dry completed road and lining"],
        "The original open water route and completed structure remain exact, without physical flow or automatic maintenance."),
    "p041": (
        "Sequence shallow teal highlights along the already embedded straight pipes and neutral-grey highlights on the existing short opened strip and immediate support. Then vary blue intensity only within the water shapes actually visible in the existing cracks. Keep the solid lower bench and every particle fixed; do not enact construction stages.",
        ["earlier heading with solid lower bench", "already embedded straight pipes and immediate support", "existing short opened strip and visible blue crack-water"],
        "The same earlier-stage protected space remains, without excavation, temporary-closure changes or a later road."),
    "p042": (
        "Trace a restrained neutral-grey sheen around the actual connected later crown, sides and deep bottom, then shallow blue intensity along the separate behind-lining drain to its visible outlet. The car and every solid and liquid boundary remain fixed. No highlight crosses into the road or a below-road escape space.",
        ["later closed ring with connected deep bottom", "separate existing blue drain to a visible outlet", "dry flat road and existing small car"],
        "The original completed road space, stationary car and separate drainage geometry remain unchanged."),
    "p043": (
        "Softly illuminate the existing inner boundary of the protected single road space, then pass a shallow blue colour-intensity trace only on its existing separate outside drainage route. Keep the small car, road, water, supports and rock exactly as pictured. No closing transition or new object appears.",
        ["existing completed single road space", "separate existing outside drain", "existing small car"],
        "The same protected space, stationary car and outside water geometry remain, with restrained surface highlights only."),
}

# 원리의 강조 경로와 단계 구분은 실제 첫 프레임에서 확인한다. 실사 동작 검수는 그대로 유지한다.
CRITICAL_PREFLIGHT = {
    "p008": "Highlight only the actual embedded canopy, solid next patch and existing short opening; equipment stays motionless.",
    "p010": "Keep both pipe rows, existing short face edge and local support exactly as pictured; do not seat any component.",
    "p011": "The solid patch and existing support edge must be identifiable; no excavation or new unsupported cavity.",
    "p012": "The fixed narrow axial patch explains advance length only; no ten-second excavation or generated numeral.",
    "p013": "Highlight the two existing adjacent regions without a new construction cycle or stage transition.",
    "p019": "Earlier shallow temporary invert must already join both support feet above the solid lower bench; no gap, guide, ram or deep final bottom.",
    "p020": "Later deep final structure must already form a continuous connection to both sides and crown, with the lower bench removed; no partial form, joint gap or temporary upper floor.",
    "p021": "A genuinely connected deep ring must be present; trace its existing lining surface without new arrows or elastic motion.",
    "p027": "Existing orange pressure arrows may change glow only; their length, count and position and the water level stay fixed.",
    "p031": "Targets and previous-position outlines remain passive and fixed; only their existing surfaces change illumination.",
    "p032": "Highlight observed geometry and existing local support; staged components remain in their original positions.",
    "p035": "Blue drain, injection hose/fine-crack contact and straight teal pipe must remain distinct; no actual grout flow or pipe insertion.",
    "p038": "Later deep-invert material and actual joint edges remain fixed; no concrete pouring, closure or earlier temporary-floor transition.",
    "a001": "Physical face-contact tool and fragment receiver must exist; the partition cannot dissolve.",
    "a002": "The image prompt has no inspector; do not add the person mentioned in the broader screen note.",
    "a003": "Use only the existing localized leak, not a current emergency or invented inspector.",
}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_sha(path):
    return hashlib.sha256(path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode("utf-8")).hexdigest()


def png_size(path):
    data = path.read_bytes()[:24]
    if len(data) != 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("selected first frame must be the reviewed PNG, not an assumed or raw filename")
    return list(struct.unpack(">II", data[16:24]))


def schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Ep09 Muse prompt package; frame readiness is not generation permission",
        "type": "object", "required": ["status", "generation_authorized", "is_submission_file", "clips"],
        "properties": {
            "status": {"enum": ["draft_not_submit_ready", "first_frames_resolved_approval_pending"]},
            "generation_authorized": {"const": False},
            "is_submission_file": {"const": False},
            "clips": {"type": "array", "minItems": 50, "maxItems": 50, "items": {
                "type": "object", "required": ["id", "image", "source_ids", "role", "render", "action", "camera", "movement", "speed", "framing", "end", "required_existing_features", "motion_contract_sha256", "prompt", "save", "frame_readiness"],
                "properties": {
                    "id": {"type": "string", "pattern": "^(o00[1-4]|a00[1-3]|p0(?:0[1-9]|[1-3][0-9]|4[0-3]))$"},
                    "image": {"type": ["string", "null"], "description": "Resolved only from actual images/picks_v1.json, never inferred"},
                    "source_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                    "role": {"enum": ["도입", "원리", "동작"]},
                    "render": {"enum": ["real", "3d"]},
                    "camera": {"const": "locked-off static shot"},
                    "movement": {"type": "string"}, "speed": {"type": "string"},
                    "framing": {"type": "string"}, "end": {"type": "string"},
                    "required_existing_features": {"type": "array", "minItems": 2, "items": {"type": "string"}},
                    "motion_contract_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    "action": {"type": "string"}, "prompt": {"type": "string"}, "save": {"type": "string"},
                    "frame_readiness": {"enum": ["missing_pick", "picked_file_unavailable", "picked_action_review_pending", "confirmed"]},
                },
            }},
        },
        "allOf": [{"if": {"properties": {"status": {"const": "first_frames_resolved_approval_pending"}}},
                   "then": {"properties": {"clips": {"items": {"properties": {
                       "image": {"type": "string", "minLength": 1}, "frame_readiness": {"const": "confirmed"},
                       "image_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                   }, "required": ["image_sha256"]}}}}}],
        "$comment": "--ready additionally enforces all 50 frame_readiness=confirmed, unique IDs and exact source correspondence. No network submission exists in this script.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--ready", action="store_true")
    parser.add_argument("--clip-seconds", type=float, required=True, help="Explicit production requirement, not a verified Muse setting")
    parser.add_argument("--media-root", type=Path, default=DEFAULT_MEDIA_ROOT)
    args = parser.parse_args()
    if not math.isfinite(args.clip_seconds) or args.clip_seconds <= 0:
        parser.error("clip-seconds must be a finite positive requirement")
    plan_path = EP / "plan/shot_list_v1.json"
    catalog_path = EP / "plan/scene_catalog_v1.json"
    image_path = EP / "images/prompts_v1.json"
    picks_path = EP / "images/picks_v1.json"
    plan = read_json(plan_path)
    catalog = read_json(catalog_path)
    image_rows = read_json(image_path)
    picks_data = read_json(picks_path) if picks_path.exists() else {"picks": {}}
    picks = picks_data.get("picks", {})
    c_by_id = {x["source_id"]: x for x in catalog["assets"]}
    i_by_id = {x["id"]: x for x in image_rows}
    video_cuts = [x for x in plan["cuts"] if x["kind"] == "v"]
    vids = [x["src"] for x in video_cuts]
    errors, blockers = [], []
    if len(vids) != 50 or len(set(vids)) != 50 or set(vids) != set(ACTION):
        errors.append("Actual plan video IDs differ from the 50 action definitions")
    if sum(x["role"] == "원리" for x in video_cuts) != 43 or sum(x["role"] == "도입" for x in video_cuts) != 4 or sum(x["role"] == "동작" for x in video_cuts) != 3:
        errors.append("Actual roles differ from 43 principle / 4 opening / 3 action")
    if abs(catalog.get("video_requirement_seconds", -1) - args.clip_seconds) > 1e-6:
        errors.append("Clip production requirement differs from measured shot-plan requirement")
    checks_path = HERE / "first_frame_action_checks_v1.json"
    # Existing manual confirmations are preserved. Missing rows remain pending, never auto-approved.
    action_checks = read_json(checks_path) if checks_path.exists() else {"scope": "manual visual compatibility of actual selected first frames", "clips": {}}
    for sid in vids:
        action_checks.setdefault("clips", {}).setdefault(sid, {
            "reviewed": False, "compatible": False, "required_features_present": False,
            "confirmed_pick_file": None, "confirmed_pick_sha256": None, "confirmed_motion_contract_sha256": None, "notes": "",
        })
        action_checks["clips"][sid].setdefault("confirmed_motion_contract_sha256", None)
    rows = []
    for cut in video_cuts:
        sid = cut["src"]
        if sid not in ACTION or sid not in i_by_id or sid not in c_by_id:
            errors.append(f"{sid}: missing action, actual image prompt or semantic catalog row")
            continue
        image_def, cat = i_by_id[sid], c_by_id[sid]
        if image_def.get("kind") != "frame" or image_def.get("source_ids") != cat.get("sentence_ids"):
            errors.append(f"{sid}: actual first-frame prompt and measured catalog source IDs differ")
        if cut["role"] == "원리" and image_def.get("render") != "3d":
            errors.append(f"{sid}: principle first frame is not 3D")
        action, required, end = ACTION[sid]
        camera = "locked-off static shot"
        principle = cut["role"] == "원리"
        speed = ("camera speed none; only slow restrained changes of light and colour intensity on fixed first-frame geometry; no physical motion"
                 if principle else "camera speed none; all physical motion at natural real-time speed, 1.0x, bounded and not exaggerated")
        movement = "Camera completely still, no zoom, no pan, no dolly, no rotation. " + action
        framing = "Exactly the composition and projection of the selected first-frame image; preserve scale, orientation, boundaries and subject size."
        prompt = (f"{action} [locked-off static shot]. Movement: {movement} Speed: {speed}. "
                  f"Framing: {framing} End: {end} The camera remains in the same composition, with no reset or fade. "
                  f"{PRINCIPLE_IDENTITY if principle else IDENTITY} {LIGHT} {D3 if image_def['render'] == '3d' else REAL}")
        motion_contract = dict(prompt=prompt, required_existing_features=required,
                               initial_state=image_def.get("initial_state"), source_image_prompt=image_def["prompt"],
                               source_reference=image_def.get("ref"), source_ids=image_def["source_ids"])
        motion_sha = hashlib.sha256(json.dumps(motion_contract, sort_keys=True, ensure_ascii=False,
                                               separators=(",", ":")).encode("utf-8")).hexdigest()
        selected, image_file, frame_sha, size = picks.get(sid), None, None, None
        readiness, reason = "missing_pick", "No actual chosen first frame exists for this source ID"
        if selected:
            name = selected.get("file")
            status = selected.get("visual_status", "")
            cleaned_reviewed = (selected.get("root_opened_clean_original") is True
                                or selected.get("raw_and_cleaned_opened_at_original_size") is True)
            if not isinstance(name, str) or Path(name).name != name or not status.startswith("chosen_") or not cleaned_reviewed:
                reason = "Pick is not an actual visually chosen, original-size reviewed PNG record"
            else:
                candidate = args.media_root / "img" / name
                if not candidate.is_file():
                    readiness, reason = "picked_file_unavailable", "Selected file is not available at the declared PC media root"
                else:
                    try:
                        size = png_size(candidate)
                    except (OSError, ValueError) as exc:
                        readiness, reason = "picked_file_unavailable", str(exc)
                    else:
                        if selected.get("dimensions") != size:
                            readiness, reason = "picked_file_unavailable", "PNG dimensions differ from the actual pick record"
                        else:
                            frame_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
                            if frame_sha != selected.get("sha256"):
                                readiness, reason = "picked_file_unavailable", "Selected PNG SHA256 differs from the pick ledger, or the ledger hash is missing"
                            else:
                                image_file = str(candidate.resolve())
                                review = action_checks["clips"].get(sid, {})
                                ok = (review.get("reviewed") is True and review.get("compatible") is True and
                                      review.get("required_features_present") is True and review.get("confirmed_pick_file") == name and
                                      review.get("confirmed_pick_sha256") == frame_sha and
                                      review.get("confirmed_motion_contract_sha256") == motion_sha)
                                readiness, reason = ("confirmed", "Actual selected frame and its physical-action compatibility confirmed") if ok else (
                                    "picked_action_review_pending", "Selected image exists, but bounded-motion compatibility is not confirmed for this exact file hash")
        if readiness != "confirmed":
            blockers.append({"id": sid, "frame_readiness": readiness, "reason": reason})
        rows.append(dict(
            id=sid, image=image_file, image_sha256=frame_sha, image_dimensions=size,
            first_frame_selection_source="images/picks_v1.json", pick_attempt=selected.get("attempt") if selected else None,
            source_ids=image_def["source_ids"], visual_source_ids=image_def.get("visual_source_ids", image_def["source_ids"]),
            role=cut["role"], render=image_def["render"], move="LOCK", camera=camera,
            script=" / ".join(cat["sentence_ko"]), screen_ko=cat["screen_ko"], initial_state=image_def.get("initial_state"),
            source_image_prompt=image_def["prompt"], source_reference_group=image_def.get("ref"),
            epistemic_boundary=image_def.get("boundary"), action=action, movement=movement, speed=speed, framing=framing, end=end,
            motion_contract_sha256=motion_sha,
            required_existing_features=required, critical_preflight=CRITICAL_PREFLIGHT.get(sid), prompt=prompt,
            production_requirement_sec=args.clip_seconds, current_muse_setting_verified=False,
            planned_out_f0=cut["out_f0"], planned_out_f1=cut["out_f1"], planned_use_sec=cut["dur"],
            actual_video_generated=False, actual_usable_range=None,
            save=str(args.media_root / "clips_v1" / f"{sid}.mp4"),
            frame_readiness=readiness, first_frame_readiness_reason=reason,
        ))
    for row in rows:
        if not all(tag in row["prompt"] for tag in ("Movement:", "Speed:", "Framing:", "End:", LIGHT, "No new objects")):
            errors.append(f"{row['id']}: required prompt sections/preservation rule missing")
        if row["camera"] != "locked-off static shot":
            errors.append(f"{row['id']}: unexpected camera movement")
        if row["role"] == "원리":
            if row["prompt"].count(STRICT_PRINCIPLE_STILL) != 1 or PRINCIPLE_IDENTITY not in row["prompt"]:
                errors.append(f"{row['id']}: fixed-geometry principle policy missing or duplicated")
            if IDENTITY in row["prompt"] or "except a component" in row["prompt"] or "elastic displacement is allowed" in row["prompt"]:
                errors.append(f"{row['id']}: physical-motion exception conflicts with principle policy")
        if row["planned_use_sec"] > args.clip_seconds - 0.05 + 1e-6:
            errors.append(f"{row['id']}: measured cut use exceeds production requirement minus end margin")
    if [x["id"] for x in rows] != vids:
        errors.append("Prompt order differs from actual measured shot-list order")
    if errors:
        print(json.dumps({"status": "invalid_definition", "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    HERE.mkdir(parents=True, exist_ok=True)
    write_json(HERE / "vprompts_v1_schema.json", schema())
    if not checks_path.exists() or action_checks != read_json(checks_path):
        write_json(checks_path, action_checks)
    status = "draft_not_submit_ready" if args.draft else "first_frames_resolved_approval_pending"
    package = dict(
        status=status, is_submission_file=False, generation_authorized=False,
        user_muse_approval_recorded=False, approval_record=None, actual_muse_submission_performed=False,
        purpose="preparation only; selecting all first frames does not authorize generation",
        production_requirement_seconds=args.clip_seconds, current_muse_setting_verified=False,
        expected_video_sources=50, principle_sources=43, opening_sources=4, action_sources=3,
        camera_move_count=0, ready_first_frames=sum(x["frame_readiness"] == "confirmed" for x in rows),
        selected_first_frames=sum(x["image"] is not None for x in rows),
        all_image_assets_actual_chosen=len(picks), all_image_assets_expected=picks_data.get("expected_ids", 85),
        input_hash_canonicalization="UTF-8 without BOM; LF line endings",
        inputs={str(p.relative_to(EP)).replace("\\", "/"): canonical_sha(p) for p in (plan_path, catalog_path, image_path)},
        physical_motion_policy=("principles p001-p043: every solid and all water/grout geometry, levels and quantities fixed; "
                                "only light/colour on existing surfaces and glow of existing arrows may change; "
                                "opening/action o001-o004/a001-a003: unchanged bounded physical actions; "
                                "all cameras fixed; no new arrows or stage morphing"),
        clips=rows,
    )
    report = dict(
        status="draft_valid_not_ready" if args.draft else ("ready_blocked" if blockers else "first_frames_resolved_approval_pending"),
        scope="prompt_definition_and_actual_first_frame_resolution_only", generation_authorized=False,
        actual_muse_submission_performed=False, actual_video_generated=False,
        expected=50, defined=len(rows), role_counts={role: sum(x["role"] == role for x in rows) for role in ("원리", "도입", "동작")},
        camera_move_count=0, selected_video_frames=package["selected_first_frames"], ready_video_frames=package["ready_first_frames"],
        actual_chosen_images=len(picks), expected_image_assets=package["all_image_assets_expected"],
        definition_errors=errors, readiness_blockers=blockers,
        current_muse_9227_settings_verified=False, user_muse_approval_recorded=False,
        warning="No actual frame or video quality review is performed by this generator. Manual checks are tied to exact selected file hashes.",
    )
    if args.draft:
        write_json(HERE / "vprompts_v1_draft.json", package)
    elif not blockers:
        write_json(HERE / "vprompts_v1.json", package)
    write_json(HERE / "video_prompt_validation_v1.json", report)
    print(json.dumps({k: report[k] for k in ("status", "expected", "defined", "role_counts", "camera_move_count", "selected_video_frames", "ready_video_frames", "actual_chosen_images", "definition_errors")}, ensure_ascii=False, indent=2))
    if args.ready and blockers:
        print(f"REFUSED: {len(blockers)} first frames are not actually confirmed for their defined physical actions; no ready JSON written.")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
