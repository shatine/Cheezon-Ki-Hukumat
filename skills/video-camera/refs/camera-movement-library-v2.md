# Claude Code Skill: AI Video Camera Movement & Genre Prompt Generator (v2)

## Overview & Purpose
This skill provides a comprehensive cinematic camera movement library and structured prompt construction guidelines for AI video generation models (e.g., Kling, Runway Gen-2/Gen-3, Luma Dream Machine, Sora, Seedance, Higgsfield).
It enables Claude Code to construct precise, highly reusable AI video prompts by separating scene narrative from mechanical camera movement, with specialized genre-based camera movement patterns—including dedicated strategies for **Educational & Documentary** productions.

---

## Skill Instructions & Workflow for Claude Code

When the user asks for AI video prompts, script breakdown, genre-specific camera moves, or camera movement recommendations:

1. **Modular Prompt Architecture**: Always structure video prompts into two distinct modules:
   - **Module A (Scene Concept & Subject)**: Subject, environment, lighting, action, atmosphere.
   - **Module B (Camera Specification)**: Camera movement tag, Movement direction/path, Speed, Framing, End state.
   - **Combined Template**: `[Scene Description]. [Camera Movement Tag]. Movement: [Direction/Path]. Speed: [Pacing]. Framing: [Composition]. End: [Final Framing].`

2. **Selecting Camera Moves by Narrative Intent & Genre**:
   - **Educational / Documentary (교육 및 다큐멘터리)**: Slow zoom in (focused analysis), Pedestal up/down (structural reveal), Slider left/right (artifact observation), Locked-off static shot (archival/talking head), Macro push-in (scientific/detailed inspection), Crane up (landscape context).
   - **Action & Thriller (액션 및 스릴러)**: Chase shot, Whip pan, Low tracking shot, Crash zoom in, Handheld shake.
   - **Drama & Romance (드라마 및 로맨스)**: Slow dolly in, Arc around subject, Over-the-shoulder tracking, Slow tilt down.
   - **Horror & Suspense (공포 및 서스펜스)**: Creeping dolly out, Body-mounted Snorricam, Unstable handheld, Reverse tracking.
   - **Sci-Fi & Cyberpunk (SF 및 사이버펑크)**: FPV drone glide, Infinite zoom, Pass-through movement, High-altitude orbit.
   - **Commercial & Fashion (광고 및 패션)**: 360 Orbit, Slider parallax, Fast crash zoom, High-speed tracking.

3. **Output Format**: Provide both modular tags and copy-paste ready English/Korean prompt combinations for AI video generators.

---

## Part 1: Genre-Based Camera Movement Guide & Prompts (장르별 카메라 무브먼트 가이드)

### 1. Educational & Documentary (교육용 및 다큐멘터리) - Specialized Section
*Camera Philosophy*: High stability, clear subject isolation, smooth spatial context presentation, and neutral/observational pacing. Avoid erratic movements; prioritize visual clarity, educational depth, and authentic observational aesthetics.

#### A. Scientific & Biological Observation (과학 및 생물학적 탐구)
* **Recommended Movement**: `Macro Slow Push-in` / `Slider Right with Parallax`
* **Purpose**: Highlighting microscopic details, cell structures, or natural specimens without spatial distortion.
* **Tag**: `slow zoom in`, `slider right`
* **English AI Prompt**:
  `A high-resolution macro shot of a plant leaf cross-section showing chloroplasts absorbing sunlight. slow zoom in. Movement: slowly advance the lens straight into the cellular structure. Speed: extremely smooth and steady micro-glide. Framing: keep central cell organelles sharply in focus with shallow depth of field. End: settle on a detailed close-up of a single chloroplast.`
* **Korean Reference**: 식물 세포 구조나 미시 세계를 정밀하게 관찰하는 교육용 마크로 푸시인 샷.

#### B. Historical Artifact & Museum Display (역사 유물 및 전시물 관찰)
* **Recommended Movement**: `Smooth Arc Orbit` / `Slider Left with Soft Lighting Shift`
* **Purpose**: Revealing 3D texture, craftsmanship, and historic details of artifacts or museum exhibits.
* **Tag**: `arc right`, `slider left`
* **English AI Prompt**:
  `An ancient Bronze Age artifact resting on a dark museum velvet pedestal, illuminated by directional spotlight. arc right. Movement: orbit slowly in a 45-degree arc around the artifact. Speed: slow, reverent, and museum-guide pacing. Framing: maintain medium close-up, keeping engraving details crisp against a softly blurred background. End: land on a striking profile view of the artifact.`
* **Korean Reference**: 고대 유물이나 전시품의 입체 질감을 보여주는 박물관 다큐멘터리 스타일 아크 샷.

#### C. Nature & Wildlife Observation (자연 및 야생동물 다큐멘터리)
* **Recommended Movement**: `Telephoto Tracking Shot` / `Slow Drone Elevation`
* **Purpose**: Observing animals in their natural habitat from a respectful distance without human disturbance.
* **Tag**: `tracking shot`, `drone push in`
* **English AI Prompt**:
  `A majestic snow leopard walking across a ridge in the snow-capped Himalayan mountains at dusk. tracking shot. Movement: travel parallel to the snow leopard using a long telephoto lens perspective. Speed: calm, deliberate, matching the animal's slow gait. Framing: environmental wide shot keeping the leopard centered while expansive mountain peaks surround it. End: preserve stable telephoto tracking as the leopard pauses.`
* **Korean Reference**: 텔레포토 렌즈를 활용해 자연 속 동물의 이동을 고요하게 추적하는 자연 다큐멘터리 샷.

#### D. Architectural & Urban History (건축 및 도시사 다큐멘터리)
* **Recommended Movement**: `Pedestal Up` / `Crane Up & Tilt Down`
* **Purpose**: Showcasing structural scale, historical facade evolution, and spatial geometry.
* **Tag**: `pedestal up`, `crane up`
* **English AI Prompt**:
  `A historic Gothic cathedral exterior at golden hour, detailed stone gargoyles and stained glass windows visible. pedestal up. Movement: lift the camera vertically straight up along the front facade. Speed: slow, majestic elevation. Framing: start at ground entrance, rising past ornate arches toward the spires. End: settle on the top spire against the dramatic sky.`
* **Korean Reference**: 건축물의 수직적 장엄함과 구조적 상세를 보여주는 크레인/페더스털 하이라이트 샷.

#### E. Expert Interview & Archival Narration (전문가 인터뷰 및 사료 설명)
* **Recommended Movement**: `Locked-off Static Shot` / `Subtle Push-In`
* **Purpose**: Enhancing authority and focus on key commentary or historical document examination.
* **Tag**: `locked-off static shot`, `slow zoom in`
* **English AI Prompt**:
  `An elderly historian sitting in a dimly lit library filled with leather-bound books, talking to camera. slow zoom in. Movement: barely perceptible forward zoom toward the subject's face. Speed: ultra-slow, respectful pacing. Framing: medium shot slightly off-center, maintaining eye-level perspective. End: finish in a slightly tighter medium close-up as key insight is delivered.`
* **Korean Reference**: 신뢰감을 높이고 진술에 집중하게 만드는 다큐멘터리 인터뷰 서서히 다가가는 샷.

---

### 2. Action & Thriller (액션 및 스릴러)
*Camera Philosophy*: Dynamic energy, high velocity, close proximity to conflict, sharp direction changes.

#### A. High-Speed Kinetic Pursuit (고속 추격전)
* **Tag**: `chase shot`, `whip pan right`
* **English AI Prompt**:
  `A motorcycle speeding through a rain-drenched neon city alleyway at midnight. chase shot. Movement: follow closely behind the rear wheel through tight turns. Speed: fast, aggressive, low-to-the-ground motion. Framing: keep low center of gravity with motion blur along the wet pavement. End: maintain high velocity right behind the vehicle.`

#### B. Visceral Combat & Tension (근접 격투 및 긴장감)
* **Tag**: `handheld shot`, `crash zoom in`
* **English AI Prompt**:
  `Two martial artists exchanging rapid blows on a dusty rooftop. handheld shot. Movement: reactive handheld tracking that sways with force impact. Speed: sudden, kinetic, organic operator motion. Framing: medium-tight profile catching visceral movement and dust physics. End: snap close on the blocking stance.`

---

### 3. Drama & Romance (드라마 및 로맨스)
*Camera Philosophy*: Emotional connection, intimate pacing, soft focus shifts, character-driven movement.

#### A. Emotional Encounter / Reunion (감정적 재회 및 서사)
* **Tag**: `dolly in`, `clockwise orbit`
* **English AI Prompt**:
  `Two lovers reuniting at a foggy train station as golden sunlight breaks through the mist. clockwise orbit. Movement: slow 360-degree orbit circling around the couple as they embrace. Speed: soft, sweeping, emotional cadence. Framing: close-up couple centered while blurry station lights spin gently in background. End: land on a warm profile silhouette.`

#### B. Solitude & Reflection (고독과 내면 성찰)
* **Tag**: `slow zoom out`, `dolly out`
* **English AI Prompt**:
  `A lonely woman sitting at a diner counter looking out at a rain-streaked window. dolly out. Movement: move physically backward through the dimly lit diner interior. Speed: steady, contemplative retreat. Framing: start on close face reflection, retreating to reveal the vast empty diner around her. End: finish on a wide isolated room composition.`

---

### 4. Horror & Suspense (공포 및 서스펜스)
*Camera Philosophy*: Spatial disorientation, impending threat, claustrophobia, uncanny observation.

#### A. Psychological Dread & Stalking (심리적 공포 및 추적)
* **Tag**: `body-mounted Snorricam`, `slow zoom in`
* **English AI Prompt**:
  `A terrified man running through a dark foggy forest at night, looking back over his shoulder. body-mounted Snorricam. Movement: lock camera to actor's chest while background disorients around him. Speed: erratic, frantic human movement. Framing: hyper-intense face close-up locked in frame while trees blur violently. End: remain locked on subject's panic-stricken face.`

---

### 5. Sci-Fi & Commercial (SF, 사이버펑크 및 광고/패션)
*Camera Philosophy*: Futuristic geometry, grand scale, high-tech motion, sleek product orbits.

#### A. Cyberpunk Megacity Exploration (SF 도시 탐구)
* **Tag**: `drone push in`, `infinite zoom`
* **English AI Prompt**:
  `Flying between towering holographic skyscrapers in a futuristic mega-city at dusk. drone push in. Movement: swoop forward along the aerial traffic lane of flying vehicles. Speed: smooth aerodynamic glide. Framing: deep perspective grid, glowing neon advertisements passing overhead. End: arrive at the entrance of a massive central megastructure.`

#### B. Sleek Commercial Product / Tech Orbit (광고/제품 하이라이트)
* **Tag**: `clockwise orbit`, `slider right`
* **English AI Prompt**:
  `A luxurious futuristic smartwatch floating over a dark liquid surface with rim light reflections. clockwise orbit. Movement: circle 360 degrees around the device at eye level. Speed: sleek, high-precision product commercial sweep. Framing: macro close-up highlighting metallic bevels and glowing interface. End: complete seamless rotation.`

---

## Part 2: Complete Camera Movement Reference Library (46 Moves Across 7 Categories)

### Category 1: Pan / Tilt (Fixed Pivot Rotations)
1. **Static Shot** (`locked-off static shot`): Hold one fixed position for the full clip.
2. **Pan Right** (`pan right`): Rotate horizontally from left to right.
3. **Pan Left** (`pan left`): Rotate horizontally from right to left.
4. **Whip Pan Right** (`whip pan right`): Rapid snap rotation to right with motion blur.
5. **Whip Pan Left** (`whip pan left`): Rapid snap rotation to left with motion blur.
6. **Tilt Up** (`tilt up`): Rotate vertically upward from fixed pivot.
7. **Tilt Down** (`tilt down`): Rotate vertically downward from fixed pivot.

### Category 2: Zoom / Lens (Focal Length Adjustments)
8. **Slow Zoom In** (`slow zoom in`): Gradually increase focal length toward target.
9. **Slow Zoom Out** (`slow zoom out`): Gradually decrease focal length toward wider frame.
10. **Fast Zoom In** (`fast zoom in`): Quick decisive zoom inward.
11. **Fast Zoom Out** (`fast zoom out`): Quick decisive zoom outward.
12. **Crash Zoom In** (`crash zoom in`): Very fast, punchy snap zoom in.
13. **Crash Zoom Out** (`crash zoom out`): Very fast, punchy snap zoom out.

### Category 3: Dolly / Track (Physical Distance & Path Moves)
14. **Dolly In** (`dolly in`): Move camera physically forward in straight line.
15. **Dolly Out** (`dolly out`): Move camera physically backward in straight line.
16. **Tracking Shot** (`tracking shot`): Move through scene alongside subject.
17. **Follow Shot From Behind** (`follow shot from behind`): Travel behind subject along route.
18. **Reverse Tracking Shot** (`reverse tracking shot`): Travel backward in front of walking subject.
19. **Side Tracking Shot** (`side tracking shot`): Parallel movement beside subject profile.
20. **Low Tracking Shot** (`low tracking shot`): Low-angle ground/waist height tracking.
21. **Vehicle Tracking Shot** (`vehicle tracking shot`): Move with vehicle along route.
22. **Chase Shot** (`chase shot`): Rapid, energetic close-range pursuit.

### Category 4: Physical Moves (Lateral, Vertical & Curving Moves)
23. **Truck Right** (`truck right`): Straight lateral movement to the right.
24. **Truck Left** (`truck left`): Straight lateral movement to the left.
25. **Pedestal Up** (`pedestal up`): Straight vertical lift upward.
26. **Pedestal Down** (`pedestal down`): Straight vertical descent downward.
27. **Slider Right** (`slider right`): Small-scale precise glide to the right.
28. **Slider Left** (`slider left`): Small-scale precise glide to the left.
29. **Push Past** (`push past`): Forward glide passing through a foreground opening/edge.
30. **Arc Right** (`arc right`): Curved motion around subject toward the right.
31. **Arc Left** (`arc left`): Curved motion around subject toward the left.
32. **Clockwise Orbit** (`clockwise orbit`): Full 360-degree rotation clockwise around subject.
33. **Counterclockwise Orbit** (`counterclockwise orbit`): Full 360-degree rotation counterclockwise around subject.

### Category 5: Human Camera (Operator-Centric Moves)
34. **Handheld Shot** (`handheld shot`): Organic human operator swaying and posture adjustments.
35. **Body-Mounted Camera / Snorricam** (`body-mounted Snorricam`): Lock camera frame to torso while world moves.

### Category 6: Drone / Crane (Aerial & Elevation Glides)
36. **Crane Up** (`crane up`): Smooth upward vertical rise through open air.
37. **Crane Down** (`crane down`): Smooth downward vertical descent through open air.
38. **Drone Push In** (`drone push in`): Forward aerial flight toward target.
39. **Drone Pull Back** (`drone pull back`): Backward aerial flight away from target.
40. **Helicopter Shot** (`helicopter-style aerial shot`): High-altitude expansive landscape flight.

### Category 7: Specials (Stylized & VFX Camera Effects)
41. **First-Person View** (`first-person view`): 1st person perspective with visible arms/body.
42. **Tilt-Shift Miniature View** (`tilt-shift miniature view`): High-angle narrow depth of field toy effect.
43. **Infinite Zoom** (`infinite zoom`): Continuous accelerating zoom into center target.
44. **Earth Zoom Out** (`earth zoom out`): Rapid expansion from street scale to planet Earth.
45. **Locked-Camera Time-Lapse** (`locked-camera time-lapse`): Fixed framing while time accelerates.
46. **Pass-Through Movement** (`pass-through movement`): Seamless glide through solid surfaces or walls.

---

## Part 3: Best Practices & Guidance for AI Video Prompt Engineering

1. **Keep Subject Description Separate from Camera Specs**: Always place the scene subject first, followed by clear movement tags and structural parameters.
2. **Specify Speed and End State**: AI video generators produce far better stability when given explicit speed (e.g., `slow, reverent glide`) and end states (e.g., `settle on close-up`).
3. **Genre Alignment**: Align camera speed and movement type with genre intent—educational videos require steady, distraction-free glides, while action videos benefit from rapid tracking and whip pans.
