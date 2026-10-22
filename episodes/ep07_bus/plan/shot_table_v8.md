# 7편 문장별 컷 표 v8 (자동 생성: plan/plan_v8.py)

- **나레이션 실측:** 403.5초 (narr_timing.json). 영상은 끝에 1초 여유를 더해 404.5초.
- **컷:** 158개, 길이 2.00~3.03초, 모두 1.0배속.
- **클립:** 79개 사용, 그중 신규·재생성 36개.
- **점검:** 통과 (컷 2~3초, 같은 클립 연속 금지, 클립당 3컷 이하, 쓸 구간 안, 구간 겹침 없음, 문장 누락 없음).
- **가정:** 신규 클립은 10초 전체를 쓸 수 있다고 가정했다. 생성 후 실제 쓸 구간을 USE에 넣고 다시 실행해야 확정된다.


**만들었지만 이 계획에서 안 쓰는 신규 클립(도입 컷 길이 결정에 따라 사용):** m4, m5

## 문장별

| 문장 | 시작~끝 | 초 | 한국어 | 컷: 클립[소스 초] | 기준 그림 | 화면 변화 |
|---|---|---|---|---|---|---|
| S01a | 0.0–2.3 | 2.3 | 버스 안에서 살 수 있나? | h1[0.0–2.3] | - | (v5 도입 클립, 프롬프트 기록 없음) |
| S02a | 2.3–8.3 | 6.0 | 낡은 버스 하나를 집으로 만들어 그 안에서 살려고 갔던 몇몇 사람들이, 한 달 만에 포기했다. | h1[0.0–2.3]<br>h2[0.0–3.0]<br>m1[0.0–3.0] | -<br>-<br>- | (v5 도입 클립, 프롬프트 기록 없음)<br>(v5 도입 클립, 프롬프트 기록 없음)<br>(v5 도입 클립, 프롬프트 기록 없음) |
| S02b | 8.3–10.5 | 2.2 | 도대체 문제가 뭐였나? | m1[0.0–3.0]<br>**m3s**[0.0–2.2] | -<br>PB | (v5 도입 클립, 프롬프트 기록 없음)<br>The man carrying the two buckets walks slowly away from the bus, turni |
| S03a | 10.5–13.5 | 3.0 | 이것은 운행이 끝난 버스 한 대다. | **m3s**[0.0–2.2]<br>PB[0.0–2.5]<br>s03[0.0–2.5] | PB<br>-<br>PB | The man carrying the two buckets walks slowly away from the bus, turni<br>The retired red-maroon KSRTC bus stands still in the sunny scrapyard; <br>Retired KSRTC buses stand in a row; inspectors in the distance walk sl |
| S03b | 13.5–19.6 | 6.1 | 케랄라의 KSRTC는, 15년을 달린 버스들을 노선에서 빼서 경매로 팔아 버린다. | s03[0.0–2.5]<br>**s03b**[0.0–2.5]<br>s03[2.5–5.0] | PB<br>PB<br>PB | Retired KSRTC buses stand in a row; inspectors in the distance walk sl<br>The buyer hands the bundle of notes to the official, who takes it and <br>Retired KSRTC buses stand in a row; inspectors in the distance walk sl |
| S03c | 19.6–23.0 | 3.4 | 싸게는 이것들이 2라크 루피에도 팔린다. | s03[2.5–5.0]<br>**s03b**[2.5–5.0] | PB<br>PB | Retired KSRTC buses stand in a row; inspectors in the distance walk sl<br>The buyer hands the bundle of notes to the official, who takes it and  |
| S04a | 23.0–26.4 | 3.4 | 길이 11미터, 폭 2.5미터. | **s03b**[2.5–5.0]<br>s04a[0.0–2.3]<br>M3[0.0–2.3] | PB<br>M3<br>- | The buyer hands the bundle of notes to the official, who takes it and <br>The yellow outline lines around the bus floor glow softly and pulse on<br>The cut-away bus home stays still; soft light shifts slightly across t |
| S04b | 26.4–30.0 | 3.6 | 밖에서 재면 약 296스퀘어피트. | M3[0.0–2.3]<br>s04a[2.3–4.7]<br>s01[0.0–2.9] | -<br>M3<br>PB | The cut-away bus home stays still; soft light shifts slightly across t<br>The yellow outline lines around the bus floor glow softly and pulse on<br>Clothes on the line beside the bus flutter in a light breeze; palm lea |
| S04c | 30.0–32.2 | 2.2 | 지붕도 있고, 벽도, 창문도 있다. | s01[0.0–2.9] | PB | Clothes on the line beside the bus flutter in a light breeze; palm lea |
| S04d | 32.2–35.7 | 3.5 | 좌석만 빼면, 침대 하나가 넉넉히 들어온다. | s01[0.0–2.9]<br>s04b[0.0–2.9] | PB<br>PB | Clothes on the line beside the bus flutter in a light breeze; palm lea<br>Empty bus interior with seats removed; sunlight patches lie still on t |
| S04e | 35.7–40.4 | 4.6 | 매달 월세를 내는 것보다, 이 버스 한 대면 충분하지 않나? | s04b[0.0–2.9]<br>s04c[0.0–2.3]<br>s01[2.9–5.2] | PB<br>-<br>PB | Empty bus interior with seats removed; sunlight patches lie still on t<br>On the crowded rental balcony the landlord and tenant talk with small <br>Clothes on the line beside the bus flutter in a light breeze; palm lea |
| S05a | 40.4–44.9 | 4.5 | 그러면, 한 달 만에 포기한 사람들의 문제는 도대체 뭐였나? | s01[2.9–5.2]<br>**m2**[0.0–2.3]<br>s02[0.0–2.2]<br>s06b[0.0–3.0] | PB<br>PB<br>PB<br>M3 | Clothes on the line beside the bus flutter in a light breeze; palm lea<br>The sweating man fans himself faster and wipes his forehead; the table<br>The adult man sitting beside his bags slowly lowers his head and sighs<br>Orange heat glow flows from the sun into the roof and walls of the bus |
| S06a | 44.9–47.5 | 2.6 | 첫 번째 문제는, 더위다. | s06b[0.0–3.0] | M3 | Orange heat glow flows from the sun into the roof and walls of the bus |
| S06b | 47.5–50.9 | 3.4 | 버스의 바깥 판과 뼈대는, 둘 다 금속으로 되어 있다. | s06b[0.0–3.0]<br>**s09b**[0.0–3.0] | M3<br>PB | Orange heat glow flows from the sun into the roof and walls of the bus<br>Sunlight from the windows slides very slightly across the bare steel r |
| S06c | 50.9–55.2 | 4.3 | 햇볕에 서 있는 차의 손잡이를 잡자마자, 깜짝 놀라 손을 뗀 적 있나? | **s09b**[0.0–3.0]<br>s06a[0.0–2.2]<br>**s06d**[0.0–2.2] | PB<br>-<br>PB | Sunlight from the windows slides very slightly across the bare steel r<br>The hand touches the hot car door handle and snaps back quickly; heat <br>The hand grabs the hot metal handrail and snaps back quickly; heat shi |
| S06d | 55.2–58.8 | 3.6 | 바로 그 열이 지붕과 벽을 거쳐 곧장 안으로 들어온다. | **s06d**[0.0–2.2]<br>s06b[3.0–5.6]<br>**s06c**[0.0–2.6] | PB<br>M3<br>PB | The hand grabs the hot metal handrail and snaps back quickly; heat shi<br>Orange heat glow flows from the sun into the roof and walls of the bus<br>Sunbeams through the windows stay bright on the bed and floor; dust dr |
| S06e | 58.8–63.1 | 4.2 | 그리고 옆면을 채운 창문들로 햇빛까지 안으로 쏟아진다. | **s06c**[0.0–2.6]<br>s06b[5.6–8.3] | PB<br>M3 | Sunbeams through the windows stay bright on the bed and floor; dust dr<br>Orange heat glow flows from the sun into the roof and walls of the bus |
| S07a | 63.1–67.4 | 4.3 | 델리의 5월 한낮, 이 안에서 자야 하고, 밥을 해야 한다면? | s06b[5.6–8.3]<br>s07a[0.0–2.1]<br>**s06c**[2.6–4.8]<br>s07b[0.0–2.9] | M3<br>PB<br>PB<br>M3 | Orange heat glow flows from the sun into the roof and walls of the bus<br>The man lying in the hot bus fans himself slowly and wipes sweat; a sm<br>Sunbeams through the windows stay bright on the bed and floor; dust dr<br>The outdoor AC unit fan spins and a yellow glow pulses along the power |
| S07b | 67.4–68.4 | 1.1 | 에어컨을 달면 된다. | s07b[0.0–2.9] | M3 | The outdoor AC unit fan spins and a yellow glow pulses along the power |
| S07c | 68.4–76.0 | 7.6 | 하지만 열이 쉬지 않고 들어오는 방을 시원하게 두려면, 전기도 쉬지 않고 써야 한다. | s07b[0.0–2.9]<br>s07a[2.1–5.0]<br>s07b[2.9–5.8] | M3<br>PB<br>M3 | The outdoor AC unit fan spins and a yellow glow pulses along the power<br>The man lying in the hot bus fans himself slowly and wipes sweat; a sm<br>The outdoor AC unit fan spins and a yellow glow pulses along the power |
| S08a | 76.0–77.9 | 1.9 | 그러면 벽에 단열재를 채우면? | s07b[2.9–5.8]<br>**s08b**[0.0–2.9] | M3<br>PB | The outdoor AC unit fan spins and a yellow glow pulses along the power<br>The worker presses one insulation panel into the gap between two steel |
| S08b | 77.9–78.9 | 1.0 | 채울 수 있다. | **s08b**[0.0–2.9] | PB | The worker presses one insulation panel into the gap between two steel |
| S08c | 78.9–87.1 | 8.2 | 하지만 벽, 지붕, 바닥에 겹을 올릴수록, 그 296스퀘어피트는 안에서부터 그만큼 작아진다. | **s08b**[0.0–2.9]<br>s08[0.0–2.9]<br>**s08b**[2.9–5.8]<br>s08[2.9–5.9] | PB<br>M3<br>PB<br>M3 | The worker presses one insulation panel into the gap between two steel<br>The thick insulation layers in walls, ceiling and floor glow softly; t<br>The worker presses one insulation panel into the gap between two steel<br>The thick insulation layers in walls, ceiling and floor glow softly; t |
| S08d | 87.1–90.7 | 3.6 | 그리고 머리 위 높이도 낮아진다. | s08[2.9–5.9]<br>**s08c**[0.0–3.0] | M3<br>PB | The thick insulation layers in walls, ceiling and floor glow softly; t<br>The man straightens up slowly and his head nearly touches the low ceil |
| S09a | 90.7–92.9 | 2.1 | 그리고 진짜 문제는 그다음이다. | **s08c**[0.0–3.0]<br>**s09b**[3.0–5.7] | PB<br>PB | The man straightens up slowly and his head nearly touches the low ceil<br>Sunlight from the windows slides very slightly across the bare steel r |
| S09b | 92.9–98.7 | 5.9 | 단열재로 벽을 꽉 채워도, 열이 안으로 들어오는 길 하나가 남아 있다. | **s09b**[3.0–5.7]<br>s09[0.0–2.7]<br>**s09b**[5.7–8.3]<br>**s09z**[0.0–3.0] | PB<br>-<br>PB<br>s09 | Sunlight from the windows slides very slightly across the bare steel r<br>Orange heat travels from the hot outer sheet along the steel beam thro<br>Sunlight from the windows slides very slightly across the bare steel r<br>The red heat glow enters the steel rib from the outer sheet and travel |
| S09c | 98.7–100.6 | 1.8 | 그것은, 금속 뼈대다. | **s09z**[0.0–3.0] | s09 | The red heat glow enters the steel rib from the outer sheet and travel |
| S09d | 100.6–108.3 | 7.7 | 바깥과 안쪽이 금속으로 이어져 있으면, 바깥의 열은 단열재를 피해, 그 금속을 타고 안으로 들어온다. | **s09z**[0.0–3.0]<br>s09[2.7–5.6]<br>**s09z**[3.0–5.9]<br>s09[5.6–8.5] | s09<br>-<br>s09<br>- | The red heat glow enters the steel rib from the outer sheet and travel<br>Orange heat travels from the hot outer sheet along the steel beam thro<br>The red heat glow enters the steel rib from the outer sheet and travel<br>Orange heat travels from the hot outer sheet along the steel beam thro |
| S09e | 108.3–110.5 | 2.3 | 이것을 열교라고 부른다. | s09[5.6–8.5]<br>**s09z**[5.9–8.5] | -<br>s09 | Orange heat travels from the hot outer sheet along the steel beam thro<br>The red heat glow enters the steel rib from the outer sheet and travel |
| S10a | 110.5–113.1 | 2.5 | 이 길로는 열만 들어오는 게 아니다. | **s09z**[5.9–8.5]<br>**s10b**[0.0–2.1] | s09<br>- | The red heat glow enters the steel rib from the outer sheet and travel<br>The hand lifts the cold bottle out of the fridge; a thin cold mist dri |
| S10b | 113.1–116.4 | 3.3 | 냉장고에서 꺼낸 병에 물방울이 맺히지 않나? | **s10b**[0.0–2.1]<br>s10[0.0–2.1] | -<br>- | The hand lifts the cold bottle out of the fridge; a thin cold mist dri<br>Water droplets slowly form and grow on the cold metal bottle; a few sl |
| S10c | 116.4–121.4 | 5.0 | 병이 새는 게 아니라, 공기 속 수증기가 차가운 표면에서 물이 된 것이다. | s10[0.0–2.1]<br>**s10b**[2.1–4.2]<br>s10[2.1–4.2]<br>**s11c**[0.0–2.3] | -<br>-<br>-<br>PB | Water droplets slowly form and grow on the cold metal bottle; a few sl<br>The hand lifts the cold bottle out of the fridge; a thin cold mist dri<br>Water droplets slowly form and grow on the cold metal bottle; a few sl<br>The fingertips slide on the wet steel rib; water droplets gather and a |
| S11a | 121.4–123.7 | 2.3 | 버스 안에서도 똑같은 일이 일어난다. | **s11c**[0.0–2.3] | PB | The fingertips slide on the wet steel rib; water droplets gather and a |
| S11b | 123.7–129.2 | 5.5 | 추운 밤에는 바깥의 냉기가 같은 금속 길로 들어와서, 뼈대를 차갑게 만든다. | **s11c**[0.0–2.3]<br>s11a[0.0–2.9]<br>**s11c**[2.3–5.2] | PB<br>s09<br>PB | The fingertips slide on the wet steel rib; water droplets gather and a<br>Cold blue spreads along the steel beam; water droplets form on it, gro<br>The fingertips slide on the wet steel rib; water droplets gather and a |
| S11c | 129.2–135.2 | 6.0 | 그 차가운 뼈대에, 숨 쉬고, 밥 하고, 씻으면서 생긴 따뜻하고 습한 공기가 부딪힌다. | **s11c**[2.3–5.2]<br>s11a[2.9–5.7]<br>**s11c**[5.2–8.0] | PB<br>s09<br>PB | The fingertips slide on the wet steel rib; water droplets gather and a<br>Cold blue spreads along the steel beam; water droplets form on it, gro<br>The fingertips slide on the wet steel rib; water droplets gather and a |
| S11d | 135.2–140.7 | 5.5 | 벽 안에 물방울이 맺히고, 마르지 않으면, 곰팡이가 자라난다. | **s11c**[5.2–8.0]<br>s11b[0.0–2.8]<br>s11a[5.7–8.5]<br>**s12b**[0.0–2.4] | PB<br>PB<br>s09<br>PB | The fingertips slide on the wet steel rib; water droplets gather and a<br>Mould on the damp bus wall stays still; a drip of water slowly runs do<br>Cold blue spreads along the steel beam; water droplets form on it, gro<br>The spray foam slowly covers the steel rib and the metal skin beside i |
| S12a | 140.7–148.0 | 7.2 | 그래서 뼈대까지 덮는 단열, 틈새 막기, 그리고 공기가 드나들게 하기를, 전부 함께 해야 한다. | **s12b**[0.0–2.4]<br>s12[0.0–2.4]<br>**s12c**[0.0–2.4]<br>s11b[2.8–5.3] | PB<br>s09<br>PB<br>PB | The spray foam slowly covers the steel rib and the metal skin beside i<br>The green seals glow softly around the covered beam and fresh air flow<br>The sealant bead runs along the window gap; the roof vent fan spins st<br>Mould on the damp bus wall stays still; a drip of water slowly runs do |
| S12b | 148.0–153.0 | 5.0 | 단열재를 붙이고 예쁜 합판으로 덮는다고 일이 끝나지 않는다. | s11b[2.8–5.3]<br>s12[2.4–4.9] | PB<br>s09 | Mould on the damp bus wall stays still; a drip of water slowly runs do<br>The green seals glow softly around the covered beam and fresh air flow |
| S12c | 153.0–158.1 | 5.2 | 그래도, 여기까지의 문제들은 돈과 시간을 들이면 고칠 수 있다. | s12[2.4–4.9]<br>**s12b**[2.4–5.0]<br>**s12c**[2.4–5.0]<br>s13[0.0–3.0] | s09<br>PB<br>PB<br>PB | The green seals glow softly around the covered beam and fresh air flow<br>The spray foam slowly covers the steel rib and the metal skin beside i<br>The sealant bead runs along the window gap; the roof vent fan spins st<br>In the finished bright bus room a curtain moves softly in the breeze;  |
| S13a | 158.1–161.0 | 2.8 | 좋다. 다 고쳤다고 치자. | s13[0.0–3.0] | PB | In the finished bright bus room a curtain moves softly in the breeze;  |
| S13b | 161.0–163.7 | 2.8 | 시원하고, 비도 새지 않고, 곰팡이도 없다. | s13[0.0–3.0]<br>**s13b**[0.0–3.0] | PB<br>PB | In the finished bright bus room a curtain moves softly in the breeze; <br>The man sits up in bed, stretches his arms and turns toward the toilet |
| S13c | 163.7–170.1 | 6.4 | 하지만 아침에 일어나서 화장실에 한 번 가는 순간, 두 번째 문제가 앞에 나타난다. | **s13b**[0.0–3.0]<br>s13[3.0–6.0]<br>**s13b**[3.0–6.0]<br>**s14c**[0.0–2.1] | PB<br>PB<br>PB<br>PB | The man sits up in bed, stretches his arms and turns toward the toilet<br>In the finished bright bus room a curtain moves softly in the breeze; <br>The man sits up in bed, stretches his arms and turns toward the toilet<br>The woman rinses the steel plate under the thin trickle of water and p |
| S14a | 170.1–173.8 | 3.7 | 물은 어디서 오고, 쓴 물은 어디로 가나? | **s14c**[0.0–2.1]<br>M3[2.3–4.4] | PB<br>- | The woman rinses the steel plate under the thin trickle of water and p<br>The cut-away bus home stays still; soft light shifts slightly across t |
| S14b | 173.8–176.5 | 2.7 | 물탱크와 오수탱크를 달면 된다. | M3[2.3–4.4]<br>s14a[3.0–5.1]<br>s14b[3.0–5.3] | -<br>M3<br>s14a | The cut-away bus home stays still; soft light shifts slightly across t<br>Blue water level in the fresh tank slowly drops while the brown level <br>The empty blue tank stays empty and the brimming brown tank bubbles sl |
| S14c | 176.5–183.5 | 6.9 | 하지만 물탱크는 쓰는 만큼 비고, 오수탱크는 그만큼 찬다. | s14b[3.0–5.3]<br>s14a[5.1–7.4]<br>s14b[5.3–7.6]<br>**s14c**[2.1–4.7] | s14a<br>M3<br>s14a<br>PB | The empty blue tank stays empty and the brimming brown tank bubbles sl<br>Blue water level in the fresh tank slowly drops while the brown level <br>The empty blue tank stays empty and the brimming brown tank bubbles sl<br>The woman rinses the steel plate under the thin trickle of water and p |
| S14d | 183.5–188.6 | 5.1 | 왜냐하면 씻고, 설거지하고, 화장실 가는, 이 생활은 매일 계속되니까. | **s14c**[2.1–4.7]<br>M3[4.4–7.0]<br>**s15c**[0.0–2.2] | PB<br>-<br>s24 | The woman rinses the steel plate under the thin trickle of water and p<br>The cut-away bus home stays still; soft light shifts slightly across t<br>The hands push the water hose onto the pedestal and plug in the power  |
| S15a | 188.6–195.2 | 6.6 | 결국, 물을 채워 주고 오수를 받아 주는 곳에, 매일 또는 며칠에 한 번은 연결해야만 한다. | **s15c**[0.0–2.2]<br>s15a[5.0–7.2]<br>**s15c**[2.2–4.4] | s24<br>M3<br>s24 | The hands push the water hose onto the pedestal and plug in the power <br>Blue water flows in, brown waste flows out and a yellow glow travels a<br>The hands push the water hose onto the pedestal and plug in the power  |
| S15b | 195.2–196.8 | 1.7 | 전기도 마찬가지다. | **s15c**[2.2–4.4]<br>s15b[0.0–2.6] | s24<br>M3 | The hands push the water hose onto the pedestal and plug in the power <br>Sun rays hit the roof solar panels and a thin yellow glow runs to the  |
| S15c | 196.8–205.7 | 8.9 | 지붕에 태양광을 달아도, 델리의 한낮에 에어컨을 돌릴 만큼 전기가 모자라면, 바깥 전기 플러그를 꽂아야 한다. | s15b[0.0–2.6]<br>s07b[5.8–8.4]<br>s15b[2.6–5.3]<br>**s15c**[4.4–7.0] | M3<br>M3<br>M3<br>s24 | Sun rays hit the roof solar panels and a thin yellow glow runs to the <br>The outdoor AC unit fan spins and a yellow glow pulses along the power<br>Sun rays hit the roof solar panels and a thin yellow glow runs to the <br>The hands push the water hose onto the pedestal and plug in the power  |
| S16a | 205.7–207.4 | 1.7 | 그리고, 세 번째 문제는 이것이다. | **s15c**[4.4–7.0]<br>s15a[7.2–9.9] | s24<br>M3 | The hands push the water hose onto the pedestal and plug in the power <br>Blue water flows in, brown waste flows out and a yellow glow travels a |
| S16b | 207.4–211.2 | 3.8 | 그 호스와 전선의 반대쪽 끝에는 무엇이 있어야 하나? | s15a[7.2–9.9]<br>s16a[0.0–2.7]<br>**s16c**[0.0–2.3] | M3<br>s15a<br>- | Blue water flows in, brown waste flows out and a yellow glow travels a<br>Blue, brown and yellow lines under the ground glow and flow between th<br>Grass at the edge of the plot moves in the wind; the tap stand, manhol |
| S16c | 211.2–215.7 | 4.5 | 물, 하수, 전기 선이 들어온 땅, 버스를 세울 수 있는 곳. | **s16c**[0.0–2.3]<br>s16a[2.7–5.0]<br>**s16d**[0.0–2.3] | -<br>s15a<br>- | Grass at the edge of the plot moves in the wind; the tap stand, manhol<br>Blue, brown and yellow lines under the ground glow and flow between th<br>The man runs his pen down the bill, stops, and rubs his forehead. |
| S16d | 215.7–222.5 | 6.8 | 버스는 2라크에 샀지만, 그 버스를 세워 놓고 살 땅은, 계산에 아예 없었다. | **s16d**[0.0–2.3]<br>s16b[0.0–2.3]<br>**s16d**[2.3–4.6]<br>s16b[2.3–4.3] | -<br>PB<br>-<br>PB | The man runs his pen down the bill, stops, and rubs his forehead.<br>Traffic passes in the background; a scooter rides by slowly behind the<br>The man runs his pen down the bill, stops, and rubs his forehead.<br>Traffic passes in the background; a scooter rides by slowly behind the |
| S17a | 222.5–224.8 | 2.3 | 그럼 길가에 세워 놓고 살면? | s16b[2.3–4.3]<br>s17a[0.0–2.1] | PB<br>PB | Traffic passes in the background; a scooter rides by slowly behind the<br>The traffic police officer walks toward the bus; clothes on the bus si |
| S17b | 224.8–226.7 | 1.8 | 여기서 법이 길을 막는다. | s17a[0.0–2.1] | PB | The traffic police officer walks toward the bus; clothes on the bus si |
| S17c | 226.7–237.9 | 11.2 | 2019년 인도 대법원은 판결했다, 어떤 차량도 이렇게 개조될 수 없다고, 만든 회사의 원래 사양이 바뀌도록. | s17a[0.0–2.1]<br>s17b[0.0–2.8]<br>**s18b**[0.0–2.8]<br>s17b[2.8–5.6]<br>**s18b**[2.8–5.6]<br>s17a[2.1–4.4] | PB<br>-<br>-<br>-<br>-<br>PB | The traffic police officer walks toward the bus; clothes on the bus si<br>The fountain plays, small figures walk on the paths, flags move gently<br>The hand presses the rubber stamp onto the file and lifts it; the ceil<br>The fountain plays, small figures walk on the paths, flags move gently<br>The hand presses the rubber stamp onto the file and lifts it; the ceil<br>The traffic police officer walks toward the bus; clothes on the bus si |
| S17d | 237.9–244.8 | 6.9 | 그리고 차가 등록되었다고 해서, 아무 땅에서나 그것을 집으로 삼아 살 권리가 생기지는 않는다. | s17a[2.1–4.4]<br>s16b[4.3–6.7]<br>s17a[4.4–6.7]<br>**s16c**[2.3–4.3] | PB<br>PB<br>PB<br>- | The traffic police officer walks toward the bus; clothes on the bus si<br>Traffic passes in the background; a scooter rides by slowly behind the<br>The traffic police officer walks toward the bus; clothes on the bus si<br>Grass at the edge of the plot moves in the wind; the tap stand, manhol |
| S18a | 244.8–250.9 | 6.1 | 버스를 살 만하게 고치면, 그것을 세울 땅이 필요하고, 허가가 필요하다. | **s16c**[2.3–4.3]<br>s18[0.0–2.1]<br>**s18b**[5.6–7.6]<br>s05[0.0–2.6] | -<br>s16a<br>-<br>PB | Grass at the edge of the plot moves in the wind; the tap stand, manhol<br>The floating document with red stamp sways slightly and the padlock on<br>The hand presses the rubber stamp onto the file and lifts it; the ceil<br>The man in front of the bus home scratches his head and looks around;  |
| S18b | 250.9–253.5 | 2.6 | 그러면 버스에서 사는 것은 불가능한가? | s05[0.0–2.6]<br>s19[0.0–2.1] | PB<br>- | The man in front of the bus home scratches his head and looks around; <br>The couple set up folding chairs beside the white camper van; trees mo |
| S19a | 253.5–259.9 | 6.4 | 그럼 인도에서 정말로 차를 집 삼아 사는 사람들은, 이 문제들을 어떻게 풀었나? | s19[0.0–2.1]<br>**s19b**[0.0–2.1]<br>s19[2.1–4.2]<br>s20[0.0–3.0] | -<br>-<br>-<br>s19 | The couple set up folding chairs beside the white camper van; trees mo<br>The man stirs the pot on the small stove; steam rises; dhaba lights gl<br>The couple set up folding chairs beside the white camper van; trees mo<br>Inside the camper the woman cooks at the small sink and the man sorts  |
| S20a | 259.9–265.8 | 5.9 | 데라둔의 판데이 부부는 2021년에, 포스 트래블러 승합차를 캠핑카로 만들었다. | s20[0.0–3.0]<br>**s20b**[0.0–3.0]<br>s20[3.0–5.9] | s19<br>s19<br>s19 | Inside the camper the woman cooks at the small sink and the man sorts <br>The two mechanics lift the AC unit into place inside the van and fix i<br>Inside the camper the woman cooks at the small sink and the man sorts  |
| S20b | 265.8–270.4 | 4.6 | 개조에만 12라크가 들었고, 차를 합치면 약 18라크. | s20[3.0–5.9]<br>**s20b**[3.0–5.9] | s19<br>s19 | Inside the camper the woman cooks at the small sink and the man sorts <br>The two mechanics lift the AC unit into place inside the van and fix i |
| S20c | 270.4–274.6 | 4.2 | 에어컨 하나에만 2라크 넘게 썼다. | **s20b**[3.0–5.9]<br>s20[5.9–8.8] | s19<br>s19 | The two mechanics lift the AC unit into place inside the van and fix i<br>Inside the camper the woman cooks at the small sink and the man sorts  |
| S21a | 274.6–280.1 | 5.4 | 150리터 물탱크는, 아끼고 아껴도 4~5일이면 빈다. | s20[5.9–8.8]<br>s21a[0.0–2.7]<br>**s21c**[0.0–2.7]<br>s21b[0.0–2.3] | s19<br>s19<br>s20<br>s19 | Inside the camper the woman cooks at the small sink and the man sorts <br>The man pumps the hand pump and water pours into the plastic can.<br>The hand turns the tap; a few last drops fall and then nothing; the ha<br>The white camper van rolls slowly into the hotel parking while the gua |
| S21b | 280.1–283.7 | 3.6 | 그리고 매일 저녁, 차를 세울 자리를 찾아야 한다. | s21b[0.0–2.3]<br>**s26b**[0.0–2.3] | s19<br>s19 | The white camper van rolls slowly into the hotel parking while the gua<br>Car headlights pass behind the parked camper van; the curtains on its  |
| S21c | 283.7–289.2 | 5.5 | 도시에서는 24시간 주차장이나 호텔 주차장을 쓴다. | **s26b**[0.0–2.3]<br>s21b[2.3–4.5]<br>**s26b**[2.3–4.6] | s19<br>s19<br>s19 | Car headlights pass behind the parked camper van; the curtains on its <br>The white camper van rolls slowly into the hotel parking while the gua<br>Car headlights pass behind the parked camper van; the curtains on its  |
| S22a | 289.2–291.3 | 2.1 | 허가는 더 어려웠다. | **s26b**[2.3–4.6]<br>s22[0.0–2.5] | s19<br>- | Car headlights pass behind the parked camper van; the curtains on its <br>The clerk shakes his head and pushes the file back; the queue shuffles |
| S22b | 291.3–299.0 | 7.8 | 큰 차를 개인 차로 등록하려고, 4개월 동안 전국의 RTO를 돌았다. | s22[0.0–2.5]<br>**s22b**[0.0–2.5]<br>s22[2.5–4.9]<br>**s22b**[2.5–4.9]<br>s22[4.9–7.8] | -<br>s19<br>-<br>s19<br>- | The clerk shakes his head and pushes the file back; the queue shuffles<br>The white camper van drives through the frame from left to right past <br>The clerk shakes his head and pushes the file back; the queue shuffles<br>The white camper van drives through the frame from left to right past <br>The clerk shakes his head and pushes the file back; the queue shuffles |
| S22c | 299.0–304.7 | 5.7 | 우타라칸드에서는 거절당했고, 결국 아마다바드에 가서야 등록됐다. | s22[4.9–7.8]<br>**s22c**[0.0–2.8]<br>**s23b**[0.0–2.1] | -<br>s22<br>s23 | The clerk shakes his head and pushes the file back; the queue shuffles<br>The clerk slides the file back with a nod and the man takes it with bo<br>The ring light glows and the tripod stays still; leaves move behind th |
| S23a | 304.7–308.9 | 4.1 | 허가 없이 개조했다가, 크게 걸려든 사람들도 있다. | **s23b**[0.0–2.1]<br>s23[0.0–2.1] | s23<br>- | The ring light glows and the tripod stays still; leaves move behind th<br>Police officers stand around the painted van; one walks around it writ |
| S23b | 308.9–319.8 | 10.9 | 2021년 8월, 구독자 170만 명이 넘는 케랄라 유튜버 형제, E Bull Jet의 캠핑카 나폴레옹이, 불법 개조로 압수됐다. | s23[0.0–2.1]<br>**s23b**[2.1–4.8]<br>s23[2.1–4.8]<br>**s23e**[0.0–2.7]<br>s23[4.8–7.5]<br>**s23c**[0.0–2.0] | -<br>s23<br>-<br>s23<br>-<br>s23 | Police officers stand around the painted van; one walks around it writ<br>The ring light glows and the tripod stays still; leaves move behind th<br>Police officers stand around the painted van; one walks around it writ<br>The tow truck winch slowly pulls the painted van up onto the flatbed; <br>Police officers stand around the painted van; one walks around it writ<br>The crowd at the gate pushes and shifts; the police officers hold thei |
| S23c | 319.8–323.8 | 4.0 | RTO 사무실에서 소동을 벌여 두 형제는 체포됐다. | **s23c**[0.0–2.0]<br>**s23d**[0.0–2.0]<br>s18[2.1–4.9] | s23<br>s23<br>s16a | The crowd at the gate pushes and shifts; the police officers hold thei<br>The padlocked gate stays shut; a police officer walks past slowly in t<br>The floating document with red stamp sways slightly and the padlock on |
| S23d | 323.8–332.4 | 8.6 | 그리고 4만 2천4백 루피의 벌금을 내지 않자, 차량 등록이 6개월 동안 취소됐다. | s18[2.1–4.9]<br>**s23d**[2.0–4.9]<br>**s23e**[2.7–5.6]<br>s24[0.0–2.6] | s16a<br>s23<br>s23<br>- | The floating document with red stamp sways slightly and the padlock on<br>The padlocked gate stays shut; a police officer walks past slowly in t<br>The tow truck winch slowly pulls the painted van up onto the flatbed; <br>Caravans parked on pads with hoses connected; a person walks to the to |
| S24a | 332.4–336.2 | 3.8 | 인도에서 캠핑카에 머무는 방식도 같은 답을 준다. | s24[0.0–2.6]<br>**s24b**[0.0–2.6] | -<br>s24 | Caravans parked on pads with hoses connected; a person walks to the to<br>The white caravan drives slowly through the gate; the guard raises the |
| S24b | 336.2–340.1 | 3.9 | 케랄라는 2021년에 카라반 관광 정책을 내놓았다. | **s24b**[0.0–2.6]<br>s24[2.6–5.2]<br>**s24c**[0.0–3.0] | s24<br>-<br>s24 | The white caravan drives slowly through the gate; the guard raises the<br>Caravans parked on pads with hoses connected; a person walks to the to<br>Water drips once from the hose connector; the cables stay still; grass |
| S24c | 340.1–352.0 | 11.9 | 카라반이 머무는 카라반 파크에는 전기, 물, 오수 연결, 쓰레기 분리 처리, 화장실, 담장과 경비를 반드시 갖추도록 했다. | **s24c**[0.0–3.0]<br>**s24b**[2.6–5.5]<br>**s24d**[0.0–3.0]<br>**s24c**[3.0–6.0] | s24<br>s24<br>s24<br>s24 | Water drips once from the hose connector; the cables stay still; grass<br>The white caravan drives slowly through the gate; the guard raises the<br>An adult walks along the path past the three bins toward the toilet bl<br>Water drips once from the hose connector; the cables stay still; grass |
| S24d | 352.0–355.9 | 3.9 | 그리고 카라반은 그 연결에 맞게 만들어져야 한다. | **s24c**[3.0–6.0]<br>s24[5.2–8.1]<br>**s24c**[6.0–9.0] | s24<br>-<br>s24 | Water drips once from the hose connector; the cables stay still; grass<br>Caravans parked on pads with hoses connected; a person walks to the to<br>Water drips once from the hose connector; the cables stay still; grass |
| S24e | 355.9–360.9 | 5.0 | 바퀴 달린 방은 차가 주고, 그 방에서 살게 해 주는 것은, 땅이다. | **s24c**[6.0–9.0]<br>s16a[5.0–7.9]<br>s25[0.0–2.0] | s24<br>s15a<br>- | Water drips once from the hose connector; the cables stay still; grass<br>Blue, brown and yellow lines under the ground glow and flow between th<br>The man stands looking at the bus, then tilts his head thinking; palm  |
| S25a | 360.9–362.8 | 1.9 | 그럼 첫 질문으로 돌아갈까? | s25[0.0–2.0] | - | The man stands looking at the bus, then tilts his head thinking; palm  |
| S25b | 362.8–364.9 | 2.1 | 버스에서 살 수 있나? | s25[0.0–2.0]<br>h1[7.0–9.0] | -<br>- | The man stands looking at the bus, then tilts his head thinking; palm <br>(v5 도입 클립, 프롬프트 기록 없음) |
| S26a | 364.9–367.4 | 2.4 | 차를 집으로 삼아 사는 사람들은 있다. | h1[7.0–9.0]<br>s19[4.2–6.7] | -<br>- | (v5 도입 클립, 프롬프트 기록 없음)<br>The couple set up folding chairs beside the white camper van; trees mo |
| S26b | 367.4–375.0 | 7.7 | 하지만 그들도 차 값의 두 배를 들여 안을 고쳤고, 매일 세울 자리를 찾아야 했다. | s19[4.2–6.7]<br>**s26c**[0.0–2.5]<br>**s20b**[5.9–8.5]<br>**s26b**[4.6–7.1] | -<br>-<br>s19<br>s19 | The couple set up folding chairs beside the white camper van; trees mo<br>The couple count the notes and put them down on the bill; one rubs the<br>The two mechanics lift the AC unit into place inside the van and fix i<br>Car headlights pass behind the parked camper van; the curtains on its  |
| S26c | 375.0–378.2 | 3.2 | 한 달 만에 포기하게 만드는 것은 침대가 아니다. | **s26b**[4.6–7.1]<br>s04b[2.9–5.3]<br>**s26d**[0.0–2.4] | s19<br>PB<br>PB | Car headlights pass behind the parked camper van; the curtains on its <br>Empty bus interior with seats removed; sunlight patches lie still on t<br>Droplets slide down the fogged windows of the bus; the hoses outside s |
| S26d | 378.2–382.2 | 4.0 | 살려면 버스 안에서는 열과 물방울을 막아야 한다. | **s26d**[0.0–2.4]<br>s12[4.9–7.3]<br>s26[0.0–2.9] | PB<br>s09<br>M3 | Droplets slide down the fogged windows of the bus; the hoses outside s<br>The green seals glow softly around the covered beam and fresh air flow<br>Blue water, brown waste and yellow power flow along the lines between  |
| S26e | 382.2–390.7 | 8.5 | 그리고 버스 밖에서는 물을 채우고, 오수를 비우고, 전기를 대고, 버스를 세울 땅과 허가를 구해야 한다. | s26[0.0–2.9]<br>**s26d**[2.4–5.2]<br>s26[2.9–5.7] | M3<br>PB<br>M3 | Blue water, brown waste and yellow power flow along the lines between <br>Droplets slide down the fogged windows of the bus; the hoses outside s<br>Blue water, brown waste and yellow power flow along the lines between  |
| S27a | 390.7–394.5 | 3.7 | 2라크 루피로 산 것은, 집이 아니라 침실 하나였다. | s26[2.9–5.7]<br>s04b[5.3–8.0]<br>**s27b**[0.0–2.7] | M3<br>PB<br>PB | Blue water, brown waste and yellow power flow along the lines between <br>Empty bus interior with seats removed; sunlight patches lie still on t<br>Seen from high above, trees sway gently and a few leaves move; the bus |
| S27b | 394.5–398.9 | 4.5 | 집은 버스만이 아니었다, 집은 버스가 서 있는 그 자리까지였다. | **s27b**[0.0–2.7]<br>s27[0.0–2.7]<br>s28[4.0–6.8] | PB<br>PB<br>- | Seen from high above, trees sway gently and a few leaves move; the bus<br>The family sitting outside the bus home talk and laugh; clothes on the<br>The family outside the bus home wave up; clothes flutter, palms sway. |
| S28a | 398.9–404.5 | 5.6 | 이런 이야기를 더 받으려면, 구독과 하이프를 세게 누르세요! | s28[4.0–6.8]<br>**s28b**[0.0–2.8] | -<br>PB | The family outside the bus home wave up; clothes flutter, palms sway.<br>The window lights glow steadily; the clothesline moves gently in the e |

## 클립별 사용

| 클립 | 컷 수 | 소스 구간 |
|---|---|---|
| M3 | 3 | 0.0–2.3, 2.3–4.4, 4.4–7.0 |
| PB | 1 | 0.0–2.5 |
| h1 | 2 | 0.0–2.3, 7.0–9.0 |
| h2 | 1 | 0.0–3.0 |
| m1 | 1 | 0.0–3.0 |
| **m2** | 1 | 0.0–2.3 |
| **m3s** | 1 | 0.0–2.2 |
| s01 | 2 | 0.0–2.9, 2.9–5.2 |
| s02 | 1 | 0.0–2.2 |
| s03 | 2 | 0.0–2.5, 2.5–5.0 |
| **s03b** | 2 | 0.0–2.5, 2.5–5.0 |
| s04a | 2 | 0.0–2.3, 2.3–4.7 |
| s04b | 3 | 0.0–2.9, 2.9–5.3, 5.3–8.0 |
| s04c | 1 | 0.0–2.3 |
| s05 | 1 | 0.0–2.6 |
| s06a | 1 | 0.0–2.2 |
| s06b | 3 | 0.0–3.0, 3.0–5.6, 5.6–8.3 |
| **s06c** | 2 | 0.0–2.6, 2.6–4.8 |
| **s06d** | 1 | 0.0–2.2 |
| s07a | 2 | 0.0–2.1, 2.1–5.0 |
| s07b | 3 | 0.0–2.9, 2.9–5.8, 5.8–8.4 |
| s08 | 2 | 0.0–2.9, 2.9–5.9 |
| **s08b** | 2 | 0.0–2.9, 2.9–5.8 |
| **s08c** | 1 | 0.0–3.0 |
| s09 | 3 | 0.0–2.7, 2.7–5.6, 5.6–8.5 |
| **s09b** | 3 | 0.0–3.0, 3.0–5.7, 5.7–8.3 |
| **s09z** | 3 | 0.0–3.0, 3.0–5.9, 5.9–8.5 |
| s10 | 2 | 0.0–2.1, 2.1–4.2 |
| **s10b** | 2 | 0.0–2.1, 2.1–4.2 |
| s11a | 3 | 0.0–2.9, 2.9–5.7, 5.7–8.5 |
| s11b | 2 | 0.0–2.8, 2.8–5.3 |
| **s11c** | 3 | 0.0–2.3, 2.3–5.2, 5.2–8.0 |
| s12 | 3 | 0.0–2.4, 2.4–4.9, 4.9–7.3 |
| **s12b** | 2 | 0.0–2.4, 2.4–5.0 |
| **s12c** | 2 | 0.0–2.4, 2.4–5.0 |
| s13 | 2 | 0.0–3.0, 3.0–6.0 |
| **s13b** | 2 | 0.0–3.0, 3.0–6.0 |
| s14a | 2 | 3.0–5.1, 5.1–7.4 |
| s14b | 2 | 3.0–5.3, 5.3–7.6 |
| **s14c** | 2 | 0.0–2.1, 2.1–4.7 |
| s15a | 2 | 5.0–7.2, 7.2–9.9 |
| s15b | 2 | 0.0–2.6, 2.6–5.3 |
| **s15c** | 3 | 0.0–2.2, 2.2–4.4, 4.4–7.0 |
| s16a | 3 | 0.0–2.7, 2.7–5.0, 5.0–7.9 |
| s16b | 3 | 0.0–2.3, 2.3–4.3, 4.3–6.7 |
| **s16c** | 2 | 0.0–2.3, 2.3–4.3 |
| **s16d** | 2 | 0.0–2.3, 2.3–4.6 |
| s17a | 3 | 0.0–2.1, 2.1–4.4, 4.4–6.7 |
| s17b | 2 | 0.0–2.8, 2.8–5.6 |
| s18 | 2 | 0.0–2.1, 2.1–4.9 |
| **s18b** | 3 | 0.0–2.8, 2.8–5.6, 5.6–7.6 |
| s19 | 3 | 0.0–2.1, 2.1–4.2, 4.2–6.7 |
| **s19b** | 1 | 0.0–2.1 |
| s20 | 3 | 0.0–3.0, 3.0–5.9, 5.9–8.8 |
| **s20b** | 3 | 0.0–3.0, 3.0–5.9, 5.9–8.5 |
| s21a | 1 | 0.0–2.7 |
| s21b | 2 | 0.0–2.3, 2.3–4.5 |
| **s21c** | 1 | 0.0–2.7 |
| s22 | 3 | 0.0–2.5, 2.5–4.9, 4.9–7.8 |
| **s22b** | 2 | 0.0–2.5, 2.5–4.9 |
| **s22c** | 1 | 0.0–2.8 |
| s23 | 3 | 0.0–2.1, 2.1–4.8, 4.8–7.5 |
| **s23b** | 2 | 0.0–2.1, 2.1–4.8 |
| **s23c** | 1 | 0.0–2.0 |
| **s23d** | 2 | 0.0–2.0, 2.0–4.9 |
| **s23e** | 2 | 0.0–2.7, 2.7–5.6 |
| s24 | 3 | 0.0–2.6, 2.6–5.2, 5.2–8.1 |
| **s24b** | 2 | 0.0–2.6, 2.6–5.5 |
| **s24c** | 3 | 0.0–3.0, 3.0–6.0, 6.0–9.0 |
| **s24d** | 1 | 0.0–3.0 |
| s25 | 1 | 0.0–2.0 |
| s26 | 2 | 0.0–2.9, 2.9–5.7 |
| **s26b** | 3 | 0.0–2.3, 2.3–4.6, 4.6–7.1 |
| **s26c** | 1 | 0.0–2.5 |
| **s26d** | 2 | 0.0–2.4, 2.4–5.2 |
| s27 | 1 | 0.0–2.7 |
| **s27b** | 1 | 0.0–2.7 |
| s28 | 1 | 4.0–6.8 |
| **s28b** | 1 | 0.0–2.8 |
