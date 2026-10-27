"""Exact controlled master retake instructions. Never submits to a generation service."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA = Path(r'D:\youtube\7. Cheezon Ki Hukumat\episodes\09_atal_tunnel')
source = MEDIA / 'img_raw' / 'v1_AT_N_1.jpg'
prompt = (
    'Photorealistic cinematic still, bright clear snowy Himalayan daylight, sharp focus, 16:9. '
    'Using the currently supplied source image: keep this SAME north-portal reconstruction, '
    'the same exact building geometry, snowy mountains, retaining walls, camera position and empty two-lane road. '
    'Keep the large dark-green rear gable. Keep the much smaller red-brown front gable ONLY over the left service section, '
    'clearly narrower than half of the full facade. Keep the main rectangular dark road mouth on the RIGHT. '
    'The small left service recess is not a traffic bore. Exactly one central lane-separating line, two lanes total. '
    'Only correct the facade markings: remove every tiny white glyph-like mark or sign-like patch from the right red-brown '
    'vertical portal post and all other facade parts. Fill these small marked areas with continuous plain matching red-brown '
    'or yellow panel material. All posts and panels are completely blank and unmarked. '
    'Do not enlarge or move either roof; do not change the source building design. '
    'No cars, no people, no text, letters, numerals, plaques, signs, stickers, logos, flags or watermarks. '
    'This remains an illustrative reconstruction, not a survey photograph. No readable text.'
)
row = {
    'id': 'AT_N', 'attempt': 3, 'kind': 'master_retake',
    'reason': 'Keep attempt1 roof proportions while removing observed right-post glyph-like marks; attempt2 expanded the small red gable.',
    'actual_reference_required': True,
    'reference_source_url': 'https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/a10bade0-3cad-479d-93a8-5d68d9986821',
    'reference_original_file': str(source),
    'reference_original_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'prompt': prompt,
    'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(),
    'generation_performed_by_this_script': False,
    'actual_ui_reference_must_be_observed_and_recorded': True,
}
exc_source = MEDIA / 'img_raw' / 'v1_G3D_EXC_2.jpg'
exc_prompt = (
    'Clean bright 3D educational engineering diorama, soft studio light, white-grey background, sharp focus, 16:9. '
    'Using the supplied image as the actual input: preserve the SAME longitudinal side-cut rock block, camera, '
    'grey transverse support ribs, left open upper excavation, middle solid rough working face, right solid unexcavated ground '
    'and continuous solid lower bench. Keep the current clear left-to-right excavation axis. Do not make a dark open passage '
    'through the middle face. No road, no invert, no purple material. '
    'Correct ONLY the teal advance-pipe bank. Replace the small stacked bundle with many evenly spaced hollow teal steel '
    'tubes distributed around the WHOLE UPPER SEMICIRCULAR CROWN above the grey arch supports. Their circular LEFT mouths '
    'must form a visible broad arch-shaped row, continuing down both upper shoulders rather than clustering at the very top. '
    'Each individual tube body is perfectly STRAIGHT and rigid, parallel to the horizontal left-to-right tunnel axis. '
    'The tubes themselves never curve with the arch: only the arrangement of separate circular mouths forms an arch. '
    'Show the near longitudinal cut surface revealing several straight tube bodies and keep the other tubes visible at the left '
    'end section. All forward portions enter and remain embedded in the solid right-hand ground. Any exposed long lengths '
    'are visible solely because of the explanatory cut, not dangling outside the rock. No wavy, sagging or twisted tubes, '
    'no isolated unsupported poles, no transverse teal crossbars. Grey transverse ribs stay a distinct separate system. '
    'Do not change the source excavation geometry or advance stage. No arrows, people, text, labels, letters, numerals, '
    'symbols, logos or watermarks. No readable text.'
)
rows = [row, {
    'id': 'G3D_EXC', 'attempt': 3, 'kind': 'master_retake',
    'reason': 'Attempt2 fixes longitudinal face/solid separation but shows only a few clustered wavy tubes, not a crown-wide arch of straight advance pipes.',
    'actual_reference_required': True,
    'reference_source_url': 'https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d',
    'reference_media_url': 'https://flow-content.google/image/8f1d0888-32a8-40d3-900b-a9c67ff1110d',
    'reference_original_file': str(exc_source),
    'reference_original_sha256': hashlib.sha256(exc_source.read_bytes()).hexdigest(),
    'prompt': exc_prompt,
    'prompt_sha256': hashlib.sha256(exc_prompt.encode()).hexdigest(),
    'generation_performed_by_this_script': False,
    'actual_ui_reference_must_be_observed_and_recorded': True,
}]
exc3_source = MEDIA / 'img_raw' / 'v1_G3D_EXC_3.jpg'
exc4_prompt = (
    'Clean bright precise CAD-like 3D educational engineering diorama, soft studio light, white-grey background, 16:9. '
    'Using the supplied source image as actual input, preserve its camera, longitudinal cut rock block, lower solid bench, '
    'grey transverse ribs, open excavation on LEFT, rough solid working face in MIDDLE, and solid unexcavated rock on RIGHT. '
    'Preserve the broad arch-shaped arrangement of the circular teal pipe mouths at the LEFT end. '
    'Fix only the representation of the teal pipe bodies: each is a smooth rigid straight circular cylinder, with parallel '
    'left-to-right axes. No bends, waves, sagging, merged tubes or irregular diameters. '
    'Show the clean short straight lengths above the grey supported open excavation. As they cross the working face, '
    'they enter the solid right-hand ground and become OCCLUDED by opaque rock. The ground hides the forward pipe lengths '
    'and their buried tips; remove every long exposed teal line currently drawn across the outer right rock wall. '
    'Do not draw pipes along the outside surface of the right block, and do not trace its cracks with teal material. '
    'The support continues ahead INSIDE solid ground, not on its exterior. The visible pipe mouths still form an arch '
    'across both upper shoulders, and their visible short bodies stay straight. Keep a clear supported working space '
    'and the grey rib feet on the lower bench. No change of excavation stage, no open passage behind the solid face, '
    'no grout, no purple material, no temporary invert, no road. No arrows, people, labels, text, letters, numbers, logos '
    'or watermarks. No readable text.'
)
rows.append({
    'id': 'G3D_EXC', 'attempt': 4, 'kind': 'master_retake',
    'reason': 'Attempt3 restores the arch of pipe mouths but leaves wavy exposed forward lengths on the outer rock; hide buried lengths inside opaque ground and straighten only the short visible cylinders.',
    'actual_reference_required': True,
    'reference_source_url': 'https://flow.google.com/project/baa9c0e8-3cbd-454c-a5e4-afa8d4f469cd/edit/af07f2b6-3d44-46cb-86a1-4cd74df7414d',
    'reference_media_url': 'https://flow-content.google/image/76a3473e-8fb4-4f83-ae83-a15d459d1ee5',
    'reference_original_file': str(exc3_source),
    'reference_original_sha256': hashlib.sha256(exc3_source.read_bytes()).hexdigest(),
    'prompt': exc4_prompt,
    'prompt_sha256': hashlib.sha256(exc4_prompt.encode()).hexdigest(),
    'generation_performed_by_this_script': False,
    'actual_ui_reference_must_be_observed_and_recorded': True,
})
(HERE / 'retake_prompts_v1.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prepared 3 controlled master retakes; no generation submitted.')
