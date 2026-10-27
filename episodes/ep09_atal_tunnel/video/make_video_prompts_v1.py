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
REAL = (
    "Photorealistic historical or place reconstruction, not documentary footage. Keep the exact same portal or "
    "interior finish as the selected image. Only existing Indian adults, no new people, no children; faces stay small. "
    "For an underground scene keep the existing neutral-white work-light exposure; no sunlight through rock. "
    "Ambient sound only. No dialogue, no speech, no music, no text, no logos, no watermark."
)
D3 = (
    "Clean bright 3D educational render, white-grey studio background. Keep the exact same simplified model, "
    "single bore, left-to-right construction axis, shape, material identity and explanatory colours as the first frame. "
    "All rigid structures stay still except a component explicitly being guided into its existing connection. "
    "For the tiny ground-response examples only the described small elastic displacement is allowed, no buckling or collapse. "
    "Any arrows already present remain exactly where they are and do not multiply. No new arrows or labels. "
    "Water, injected grout and loose material remain distinct; the traffic road and any escape passage remain dry. "
    "Ambient sound only. No dialogue, no music, no watermark."
)

# ID별 실제 영상 동작. 아래의 물질/도구는 선택된 첫 프레임에 이미 있어야 한다.
# tuple = (영어 동작, 실제 첫 프레임에서 확인할 요소, 종료 상태).
ACTION = {
    "o001": (
        "Existing muddy water continues from the visible face cracks into the same low sump and existing drainage pipe. "
        "Small ripples travel along that route; the supported working space and machinery stay in place. The level does not flood the workers or road.",
        ["face inflow and sump visible", "continuous existing drainage route", "supported workspace remains clear"],
        "The same controlled inflow continues; no growing flood or new fracture."),
    "o002": (
        "The water already at the face carries a few existing small loose stones and soil grains a short distance downward onto the same muddy pile. "
        "The pile changes only slightly and the protected side space stays open. No slab failure or falling large boulder.",
        ["water and small loose fragments at face", "existing muddy receiving pile", "clear protected side space"],
        "A few grains have settled on the existing pile; the same modest flow continues."),
    "o003": (
        "Only the two small cars already visible advance normally along their existing lane into the same rectangular south-portal opening. "
        "Preserve exactly two lanes total and one central lane-separating line; no physical median or barrier, new cars, lane changes or road widening.",
        ["selected south portal geometry", "two existing small cars", "single two-way two-lane carriageway"],
        "The visible cars continue into the same bore or are naturally occluded by its mouth; no vehicle reappears."),
    "o004": (
        "In the existing distant mountain view, only already visible pine branches move very slightly in a natural breeze. "
        "Keep the south portal, road, mountain and any existing cloud shapes fixed; do not invent a car, route line or mountain cut-away.",
        ["distant south portal within mountain landscape", "existing visible tree branches"],
        "The same wide landscape remains, with only a small continuing branch movement."),
    "p001": (
        "Blue water already visible in connected pores creeps through those same pores toward the exposed heading. "
        "A few existing loose grains settle locally; large fractured blocks and all supports stay exactly in place.",
        ["connected blue pore water", "small loose grains distinguishable from solid blocks", "exposed heading on left"],
        "Water remains within the same connected pores and the weak-ground composition stays readable."),
    "p002": (
        "Existing blue water and a few existing grey-brown loose particles move from the right-hand face into the short left-hand void. "
        "Particles fall and settle by gravity in the existing receiving area; no bulk block disappears and the open length does not grow.",
        ["blue face inflow", "existing loose fragments", "left receiving area separate from structural support"],
        "A small amount has settled while the same modest inflow remains."),
    "p003": (
        "Water already collected in the sump travels through the existing pump hose. The level lowers only slightly while a few existing loose grains at the face still settle inward. "
        "The pump, machine and rigid supports stay fixed, and the weak roof does not heal or become solid rock.",
        ["existing pump, hose and sump", "water route in hose", "loose grains at weak face"],
        "A slightly lower sump level coexists with the same weak roof and walls."),
    "p004": (
        "Continue the small existing face inflow and drainage flow while a few already loose particles settle at the face edge. "
        "The already installed ribs and shotcrete retain the protected workspace; no support is newly spawned or grown.",
        ["existing face fragments and drainage route", "installed ribs and shotcrete", "protected workspace"],
        "The support geometry remains unchanged and water is still led away."),
    "p005": (
        "Only the existing blue water travels steadily through the separate side drain to its already open outlet. "
        "The existing grey crown and wall supports remain physically steady, preserving the same empty workspace.",
        ["open drainage path with visible outlet", "existing crown/wall support", "dry clear workspace"],
        "The established support and controlled drain continue without extra construction."),
    "p006": (
        "The single additional straight teal pipe already resting on its supported drilling guide advances a short distance rightward into the existing crown-level bore. "
        "Keep the pipe straight, its diameter unchanged and its rear supported; previously embedded pipes and all ground stay fixed.",
        ["one additional straight pipe on supported guide", "visible crown-level insertion point", "next patch still solid"],
        "The same pipe is partly farther inserted, with its visible rear still on the guide; excavation has not begun."),
    "p007": (
        "Advance only the already partly inserted teal tube slightly farther along the left-to-right axis using the existing guide. "
        "The existing arch-shaped arrangement of pipe mouths does not rotate or bend; every tube remains longitudinal and distinct from transverse ribs.",
        ["partly inserted tube and supported guide", "arch-shaped row of pipe mouths", "solid next patch"],
        "The pipe remains straight and partly visible on the guide; the arch arrangement is unchanged."),
    "p008": (
        "With the embedded canopy completely still, the already present supported excavator arm makes one small bucket stroke against the next short patch below the pipes. "
        "Only a few contacted particles move into the existing left-hand muck receiving area. Do not remove the entire patch or finish a whole advance.",
        ["embedded straight canopy", "supported excavator arm and bucket contacting face", "existing muck receiver/removal path"],
        "A shallow local bite is visible under the same canopy; most of the next patch remains solid."),
    "p009": (
        "Keep both rows of straight canopy pipes and the already installed transverse rib exactly still. "
        "Only blue water already in the surrounding cracks passes through its existing collection route and a few small exposed grains settle beneath the canopy. "
        "Do not add a third pipe row, new rib or a larger excavation.",
        ["two arch-shaped rows of straight pipe mouths", "existing blue water collection route", "small exposed grains below canopy"],
        "The double-row canopy and short supported opening retain their first-frame shape."),
    "p010": (
        "Under the still double-row canopy, the existing supported bucket makes one short local stroke and moves only contacted loose material toward the existing muck receiver. "
        "Then the already pre-positioned grey support makes only its small final seating movement on its visible positioning arm. No complete one-metre cycle or new support appears.",
        ["double-row canopy", "face-contact bucket and existing muck path", "nearly seated transverse support held by positioning arm"],
        "The short exposed edge remains supported; the lower bench and forward ground are still present."),
    "p011": (
        "Use the already visible bucket for one small controlled scoop at the edge of the short next patch. "
        "After the bucket clears, the support already held almost in position by its existing arm makes one small final seating movement. "
        "Previously installed support stays still; no large section is opened and no rib material grows from nothing.",
        ["small solid next patch", "supported bucket and receiving path", "pre-positioned support on visible positioning arm"],
        "A small newly exposed edge has immediate local support; no long unsupported cavity develops."),
    "p012": (
        "The existing bucket takes one shallow bite within the already highlighted narrow axial patch and transfers only that contacted material into the existing receiver. "
        "The highlighted remainder stays solid. This is one representative stroke, not an entire metre excavated in ten seconds.",
        ["narrow highlighted solid patch", "existing supported bucket at face", "existing material receiving route"],
        "Most of the highlighted patch remains solid with a small physical bite at its edge."),
    "p013": (
        "Perform one new small bucket stroke at the next adjacent solid strip while the previous rib and shotcrete remain stationary. "
        "Only the already held local support then finishes its small seating movement; do not replay, reset or duplicate the previous cycle.",
        ["previously supported strip", "next solid strip with bucket contact", "existing muck route and nearly seated support held by arm"],
        "The newly contacted short edge is locally supported and the remaining forward ground stays solid."),
    "p014": (
        "The existing shotcrete nozzle sprays a small continuous amount of grey concrete onto only the newly exposed rough patch. "
        "Material comes from the existing hose/nozzle and builds a thin bounded coating at contact. Existing mesh, ribs and bolts stay fixed; do not flood or bury the model.",
        ["rough uncoated patch", "shotcrete nozzle with existing feed hose", "prior mesh/ribs/bolts separate from target patch"],
        "A small thin coating covers only part of the target patch and the nozzle remains visible."),
    "p015": (
        "The one long bolt already partly in the prepared bore advances a short distance deeper across the same visible cracks. "
        "Its existing bearing plate approaches the rock surface without stretching the bolt or closing the cracks magically. All other installed bolts stay fixed.",
        ["partly inserted long bolt", "prepared bore across cracks", "aligned existing bearing plate"],
        "The same bolt sits slightly deeper and remains visibly distinct from rock and shotcrete."),
    "p016": (
        "Keep the two already different support zones and their shotcrete thicknesses completely unchanged. "
        "Only water already in the visible cracks follows each existing local route and a few already loose grains settle in the weaker patch. "
        "Do not transform one support type into the other or grow a new layer.",
        ["two existing different support zones", "visible local water routes and loose grains"],
        "Different ground and support conditions remain side by side without a stage transition."),
    "p017": (
        "Only the loose footing grains already under the two support feet compact slightly under the existing load. "
        "The feet and connected support follow an extremely small bounded settling movement, with no buckling, bottom heave or sudden collapse. "
        "The surrounding model remains fixed; this is a general schematic principle, not a recorded Atal incident.",
        ["support feet clearly visible", "loose footing grains over solid bench", "initially upright support"],
        "A barely perceptible settling is retained, without the support falling or returning to its initial position."),
    "p018": (
        "Existing firm base material immediately under the support feet compacts locally into the already prepared footing area. "
        "The previously slightly distorted support retains that shape; do not straighten or repair it magically. No material rises through the bench or appears from outside the frame.",
        ["weak footing and slightly distorted support", "firm base material already at feet", "clear supported placement path"],
        "The existing footing material is more firmly seated while the earlier small support distortion remains."),
    "p019": (
        "Only the existing ground-supported final connector at the shallow temporary invert moves a very short distance on its visible guide to close the already small end joint. "
        "Do not stretch or grow the invert. Keep the solid lower bench and upper-heading support unchanged; no deep final bottom or traffic road appears.",
        ["earlier upper heading with solid lower bench", "shallow temporary invert with small end joint", "existing supported connector/guide or short ram"],
        "The small temporary connection is seated; the lower bench still fills the lower stage."),
    "p020": (
        "At the already opened later lower stage, existing fresh grey concrete from the already visible feed hose moves a short distance into the existing supported closing form. "
        "Only the small local final-invert joint is progressively filled; the crown and side walls remain fixed. "
        "Do not excavate the lower bench in this clip, invent a precast method or complete a whole ring instantaneously.",
        ["later lower excavation already open", "deep final-invert closing form on stable base", "existing feed hose/nozzle and fresh grey concrete"],
        "The small closing joint is further filled with supplied concrete; no temporary upper floor appears."),
    "p021": (
        "At the existing ground-to-lining contacts, allow only a barely perceptible settling of the ground and a very small continuous elastic response of the connected lining. "
        "The crown, sides and deep bottom stay connected and preserve the same dry road space. Do not add loose grains or force arrows, open a joint, hinge a member or buckle the ring.",
        ["fully connected later deep ring", "dry flat internal road slab", "clear existing ground-to-lining contacts"],
        "The slightly settled load-bearing contact remains stable; the ring stays closed and the road stays flat and dry."),
    "p022": (
        "Keep the earlier embedded pipes, installed ribs, shotcrete and shallow temporary closure in their existing completed state. "
        "Only the already visible blue water moves through surrounding cracks into the existing lower collection channel. "
        "Do not replay all construction stages or replace the temporary invert with a deep final one.",
        ["earlier heading with solid lower bench and temporary closure", "existing blue cracks and collection channel"],
        "The supported space is unchanged but the separate water flow continues."),
    "p023": (
        "Blue water already visible in ground cracks travels into the same controlled lower channel. "
        "All grey support stays steady and the dry workspace stays open; supporting the roof does not erase the water or seal every crack.",
        ["existing water-bearing cracks", "controlled collection channel", "unchanged structural support"],
        "The water still follows its own route around the supported excavation."),
    "p024": (
        "Existing blue water enters the already visible side collection point and travels through the continuous pipe to the open left outlet. "
        "Purple grout already in selected small cracks stays exactly where it is; do not generate an injection hose that is absent from the frame.",
        ["side collection and continuous open outlet", "separate existing purple-treated fine cracks"],
        "The main outlet remains open while the treated fine cracks remain distinct."),
    "p025": (
        "Continue existing blue water through the larger open collection route while the already purple-grouted fine cracks remain blocked and unchanged. "
        "Keep the two paths visibly separate; no new grout, plug, barrier or pipe is created and water is not redirected into the working floor.",
        ["fine cracks already treated with purple grout", "separate larger water route to open pipe"],
        "Water still drains through the larger route without reopening the treated fine cracks."),
    "p026": (
        "Blue water already supplied by the visible connected crack slowly accumulates behind the existing closed plug. "
        "Its level rises by a modest bounded amount within the same crack; the plug and grey shell remain stable. "
        "No orange arrow is added, no rupture occurs and the water does not appear from nowhere.",
        ["closed plug", "modest blue pocket with visible connected supply crack", "stable surrounding shell"],
        "A modest higher water level remains behind the same plug, without a flood or failure."),
    "p027": (
        "Continue a small rise of the already present water behind the same plug, using only its visible supply route. "
        "The existing short orange pressure arrows stay in exactly the same locations, shape and number; do not grow or spawn them. "
        "The lining stays intact with no explosion, seepage through the road or dramatic structural motion.",
        ["part-filled water-bearing crack behind closed plug", "existing orange arrows", "visible supply route"],
        "The higher water pocket and original static pressure markers remain, with the shell intact."),
    "p028": (
        "Existing blue water follows the open ground-side route behind the waterproof layer, down into the separate continuous drain and out of the already visible outlet. "
        "The barrier, lining and deep invert remain fixed; no water crosses into the dry traffic space or an escape passage.",
        ["continuous ground-side water path", "waterproof layer distinct from lining", "separate open drain outlet"],
        "The same bounded drainage continues and the road remains dry."),
    "p029": (
        "Only the already present blue water moves behind the existing thin barrier toward the existing pipe outlet. "
        "Purple grout, membrane and lining stay still, preserving the separate treated and draining paths. Do not seal the main outlet or change the section type.",
        ["thin existing barrier", "purple-treated selected cracks", "continuous water route to outlet"],
        "Water drains behind the barrier while treated cracks and dry roadway stay unchanged."),
    "p030": (
        "Maintain a steady small flow of existing blue water through the visible open drain. "
        "The purple local sealing and the thin barrier stay fixed and do not spread over the model. No new pipe is drawn and the final ring does not change stage.",
        ["existing purple sealing and barrier", "open blue drain path", "dry flat road within later ring"],
        "The combined local sealing and separate drainage continue without a changing structure."),
    "p031": (
        "Let only the already fractured ground and attached crown/side observation targets undergo an extremely small inward displacement. "
        "Any existing previous-position outlines and survey instrument remain fixed and passive. "
        "Targets follow the surface; they do not pull the rock or stabilize it. No laser, digit or alarm appears.",
        ["nearly undeformed supported heading", "attached crown/side observation targets", "existing passive previous-position outlines"],
        "A tiny observed positional difference remains; no sensor-induced repair or collapse occurs."),
    "p032": (
        "The additional support component already staged on firm ground makes only a short guided seating movement into its existing prepared local connection. "
        "Use only the continuous supported placement route visible in the frame; the observed ground shape, passive targets and remaining excavation patch do not reset or transform.",
        ["existing local observation difference", "staged support with supported guide/positioning tool", "prepared local connection"],
        "The existing local support is seated without an automatic sensor response or new excavation stage."),
    "p033": (
        "Keep the already different local support densities unchanged. "
        "Existing water follows the visible cracks of each ground patch with a small natural flow; any already loose grains settle only locally. "
        "No universal new lining spreads from one zone into the other.",
        ["two different adjacent ground/support patches", "existing visible water routes or loose grains"],
        "The distinct ground-dependent support arrangements remain side by side."),
    "p034": (
        "A few existing loose particles at the face pocket descend locally into the existing receiving pile. "
        "The already strained rib shows at most a tiny additional elastic displacement, not a buckling wave or catastrophic collapse. "
        "Keep the protected area empty and do not invent an accident geometry or injured people.",
        ["existing locally strained rib", "small loose face pocket and receiving pile", "no people in hazard zone"],
        "A little additional material has settled; the wider model retains its original shape."),
    "p035": (
        "Keep the open drainage route flowing. Through the existing injection hose, a small amount of already supplied purple grout advances only along the selected visible fine cracks. "
        "The single additional straight teal tube on its existing guide may advance a short distance rightward. "
        "Keep all three systems separate and do not start a new excavation or spawn further tubes.",
        ["connected open drainage pipe", "existing injection hose and supplied grout", "one additional straight tube on supported guide"],
        "The small grouting and guided insertion increments remain, with the water outlet still open."),
    "p036": (
        "Only existing water in the newly revealed ground follows the already visible drainage path, and a few exposed grains settle locally. "
        "The small observation target and locally denser support remain passive and fixed. No magic measurement beam installs or multiplies support.",
        ["existing observation target and denser local support", "visible water or loose-grain path in forward patch"],
        "The existing local reinforcement remains in place as the small material response continues."),
    "p037": (
        "Maintain the visible existing water flow through the open drain while a few already loose grains settle at the stabilized edge. "
        "The locally strengthened support retains its geometry and no finished road, extra rib or sudden new cavity appears.",
        ["open drainage route", "stabilized loose-material edge", "existing strengthened support"],
        "The working space remains stable with controlled drainage and only minor grain settling."),
    "p038": (
        "In this already opened later lower stage, a small amount of existing fresh grey concrete from the visible feed hose enters the already supported final-invert closing form. "
        "Keep the retained upper support and deep bottom geometry fixed. No temporary upper floor, lower bench, traffic or new construction method appears.",
        ["later lower stage already open", "stable deep-invert closing form", "existing feed hose/nozzle and fresh grey concrete"],
        "Only the small final-bottom joint is further filled; the model remains in the same later stage."),
    "a001": (
        "The compact machine already present uses its existing face-contact tool to remove a few small fragments from the thin partition beside the pilot opening. "
        "Fragments fall into the existing receiving space and the same work light beyond becomes slightly more visible. "
        "Do not dissolve the whole wall, blast, create a wide opening instantly or add a ceremony. Distant workers stay safely behind the existing barrier.",
        ["thin partition and small pilot hole", "existing supported machine tool contacting partition", "existing fragment receiving space and safety barrier"],
        "The pilot opening is a little wider through physical removal; the remaining partition and scene remain coherent."),
    "p039": (
        "The single small car already in the model advances normally along the dry flat road while existing blue groundwater flows through the separate open drainage route outside the lining. "
        "The connected final ring, ground and membrane stay fixed; no other car or water path appears.",
        ["existing small car on dry road", "later connected ring", "separate visible groundwater route"],
        "The same car is farther along its lane and water remains outside the traffic space."),
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
        "Existing blue water continues through the unobstructed route behind the lining to its visible outlet. "
        "The road, structure and any existing inspection tool stay still. No tool operates autonomously and no automatic repair, blockage or new opening appears.",
        ["unobstructed behind-lining route", "visible outlet", "dry completed road"],
        "The existing water route remains open while the structure stays unchanged."),
    "p041": (
        "Keep the already embedded advance pipes, short opened strip, immediate support and solid lower bench exactly as in the earlier-stage frame. "
        "Only the existing water in the visible cracks moves toward the collection route and small exposed grains settle locally. "
        "Do not morph through excavation, temporary closure and final completion in this recap shot.",
        ["earlier heading with solid lower bench", "already embedded pipes and immediate support", "visible water/grain route"],
        "The same protected earlier-stage space is retained; no later-stage road appears."),
    "p042": (
        "Only the existing blue water moves behind the connected later ring into the open separate drain, while the already visible small car advances along the dry two-way road. "
        "Keep the deep curved bottom, crown and walls connected; never send water into the road or below-road escape space.",
        ["later closed ring and deep bottom", "separate open blue drain", "existing small car on dry road"],
        "The stable completed road space and its independent draining route remain readable."),
    "p043": (
        "The same very small car continues naturally along its existing lane inside the protected space. "
        "Existing water keeps draining along the already open outside route. All rock, supports and road retain their exact shape, with no new object or closing transition.",
        ["existing small car", "completed single road space", "separate existing open drain"],
        "The same supported empty space remains around the moving car and the water stays outside it."),
}

# 현재 초안 문구만으로 동작의 물리적 준비를 확정할 수 없어 실제 프레임 확인이 특히 필요한 항목.
CRITICAL_PREFLIGHT = {
    "p008": "Excavation tool and material receiver must actually be present; solid ground cannot disappear.",
    "p010": "Bucket, receiver and already held almost-seated support must be present.",
    "p011": "Bucket and physically held support must be visible before any excavation/seating action.",
    "p012": "One shallow representative stroke only; do not equate ten seconds with a one-metre advance.",
    "p013": "New cycle uses existing tool/support and never replays a prior source range.",
    "p019": "Closing connector must already exist and remain supported; no self-growing invert.",
    "p020": "Existing concrete supply and supported form are needed; no material creation or method claim.",
    "p021": "No arrows exist in the planned initial state; only existing ground/lining may show a tiny physical elastic response, no new arrows or grains.",
    "p032": "Any staged support must have a supported guide/positioning tool; no levitation.",
    "p035": "Injection supply and guided pipe must be present and remain separate from drainage.",
    "p038": "Later-stage concrete supply/form must be visible; no earlier temporary-floor transition.",
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
        speed = "camera speed none; all physical motion at natural real-time speed, 1.0x, bounded and not exaggerated"
        movement = "Camera completely still, no zoom, no pan, no dolly, no rotation. " + action
        framing = "Exactly the composition and projection of the selected first-frame image; preserve scale, orientation, boundaries and subject size."
        prompt = (f"{action} [locked-off static shot]. Movement: {movement} Speed: {speed}. "
                  f"Framing: {framing} End: {end} The camera remains in the same composition, with no reset or fade. "
                  f"{IDENTITY} {LIGHT} {D3 if image_def['render'] == '3d' else REAL}")
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
        if row["planned_use_sec"] > args.clip_seconds - 0.05 + 1e-6:
            errors.append(f"{row['id']}: measured cut use exceeds production requirement minus end margin")
    if [x["id"] for x in rows] != vids:
        errors.append("Prompt order differs from actual measured shot-list order")
    if errors:
        print(json.dumps({"status": "invalid_definition", "errors": errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    HERE.mkdir(parents=True, exist_ok=True)
    write_json(HERE / "vprompts_v1_schema.json", schema())
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
        physical_motion_policy="only actual first-frame materials/components; fixed camera; no new arrows; no stage morphing",
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
