"""9편 아탈 터널: 실측 내레이션으로만 만드는 30fps 컷 계획.

실행: python plan/plan_v1.py --clip-seconds 10
--clip-seconds는 확인할 제작 요구 사양이다. 기본값으로 10초를 가정하지 않는다.
현재 Muse 설정 확인 및 생성 후 실측 usable range/파일 검사는 별도 필수 단계다.
이 스크립트의 초기 통과는 미생성 asset의 등록과 컷 계획 논리에 한정된다.
확정 한국어/힌디어를 편집하지 않으며 문장 길이로 초를 추정하지 않는다.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

EP = Path(__file__).resolve().parent.parent
FPS, TAIL, IMG_MAX = 30, 1.0, 4.5
OPENING_FRAMES = 30 * FPS
SOURCE_MARGIN = 0.05
MIN_VIDEO_FRAMES = 30
PREFERRED_VIDEO_MIN = 3 * FPS
MOVES = ["in_c", "out_l", "in_r", "out_c", "in_l", "out_r"]
PRINCIPLE_SENT = {
    "S05a", "S05b", "S05c", "S06b", "S06c", "S06d", "S07b", "S07c", "S07d", "S08b", "S08c",
    "S09a", "S09b", "S09c", "S09d", "S10a", "S10b", "S10c", "S10d", "S11b", "S11c",
    "S12a", "S12b", "S12c", "S12d", "S13c", "S13d", "S14b", "S14c", "S15a", "S15b", "S15c",
    "S16a", "S16b", "S16c", "S17a", "S17b", "S17c", "S17d", "S18a", "S18b", "S18c",
    "S19b", "S19c", "S21a", "S21c", "S23a", "S23b", "S23c",
}

# 화면 의미만 설계한다. 실제 장면의 초는 아래 표에 없으며 narr_timing.json에서만 읽는다.
# tuple = (기준 그림 그룹, 화면에 보여 줄 상태, 영상일 때의 구체적인 변화).
SCENE = {
    "S01a": ("R_GROUND_REAL", "산속 굴착면에서 물이 유입되는 모습과 그 앞에서 확보한 작업 공간을 함께 보여 준다.", "굴착면 틈에서 물이 흘러나오고 작업 공간은 유지된다."),
    "S01b": ("R_GROUND_REAL", "시공 당시를 재구성한 굴착면에서 물이 쏟아져 바닥의 배수 방향으로 흐른다. 수치 표시는 편집에서 한다.", "지속적인 물 유입과 바닥의 배수 흐름. 사람은 먼 옆모습만 보인다."),
    "S01c": ("R_GROUND_REAL", "물만 보이는 좁은 구도를 벗어나 물과 토사가 함께 있는 굴착면을 드러낸다.", "카메라는 고정하고 물에 섞여 내려오는 토사가 보인다."),
    "S01d": ("R_GROUND_REAL", "굴착면 아래로 젖은 흙과 작은 부서진 돌이 물에 섞여 내려온다.", "작은 토사와 파편이 물과 함께 흘러 작업 공간 앞에 쌓인다. 대규모 폭발이나 인명 사고는 만들지 않는다."),
    "S02a": ("R_SOUTH", "확인한 남측 실제 포털 형상을 유지하며 작은 차량이 터널에 진입한다.", "작은 승용차가 일정한 정상 속도로 입구를 통과한다."),
    "S02b": ("R_SOUTH", "히말라야 산악 지형 속의 남측 터널 포털을 넓게 보여 준다. 길이 9.02킬로미터와 고도는 편집 오버레이로만 표시한다.", "카메라는 고정하고 남측 포털을 통과하는 작은 차량이 산악 규모를 드러낸다."),
    "S02c": ("R_SOUTH", "완성된 남측 입구와 산악 배경을 별도 넓은 구도로 보여 주며, 600미터 미만의 어려운 구간과 약 4년 공사 기간은 편집 오버레이로 대비한다.", "작은 차량이 완성된 입구를 통과한다. 카메라는 고정이며 포털 형상은 바뀌지 않는다."),
    "S03a": ("R_TERRAIN", "높은 산 능선 앞에서 갈 곳이 막힌 구불구불한 고갯길을 넓게 보여 준다.", "산악 지형을 가로로 천천히 살피는 한 방향 무빙."),
    "S03b": ("R_TERRAIN", "로탕 고개를 넘는 굽이진 기존 산길을 위에서 본다. 지리 경로는 확인 자료를 바탕으로 후속 검수한다.", "산길의 굽이를 따라 멀리 있는 작은 차량이 이동한다."),
    "S03c": ("R_TERRAIN_SNOW", "폭설로 통행이 막힌 산길을 전경에, 눈에 덮인 산악 마을을 먼 배경에 둔 하나의 넓은 설경.", "눈이 쌓인 길은 막혀 있으며 인물의 과장된 사고 행동은 없다."),
    "S03d": ("R_TERRAIN", "산 위의 긴 고갯길과 산 아래로 지나가는 터널을 같은 지형의 설명용 투시도에서 대비한다.", "산은 고정하고 지상 길과 지하 길을 순서대로 구별한다."),
    "S04a": ("R_TERRAIN", "산 위로 여러 번 돌아가는 길과 아래의 짧은 터널 경로를 나란히 보여 준다.", "작은 차량이 지상 산길을 따라 움직인다."),
    "S04b": ("R_TERRAIN", "기존 길과 새 길을 비교하는 간결한 지형 화면. 46킬로미터와 약 4~5시간은 정확한 편집 글자로만 넣는다.", "비교 경로 위의 작은 차량이 각각 정상 속도로 이동한다."),
    "S04c": ("R_GROUND", "부서진 지반과 작은 작업 공간이 드러난 산속 굴착면의 한 장면. 지도에 선을 긋는 것과 실제 지반 굴착의 차이를 읽게 한다.", "굴착면의 느슨한 지반과 작은 작업 공간을 유지하며 마법 같은 천공이나 지도에서 현장으로의 모핑은 만들지 않는다."),
    "S05a": ("R_GROUND", "한 덩어리의 바위와 달리 틈과 입자가 많은 산속 지반의 절개 모형을 보여 준다.", "작은 틈 속 물이 이동하고 느슨한 입자가 조금씩 흘러내린다."),
    "S05b": ("R_GROUND", "회갈색 진흙과 잘게 부서진 암석, 파란 설명용 지하수를 분리해 읽을 수 있는 파쇄대 단면.", "물은 입자 사이로 흐르고 느슨한 입자는 중력 방향으로 이동한다."),
    "S05c": ("R_GROUND", "미보강 굴착면에서 물과 느슨한 재료가 빈 공간 쪽으로 밀려드는 단면.", "파란 물과 회갈색 토사가 굴착면에서 터널 내부 방향으로 함께 흐른다."),
    "S06a": ("R_PUMP", "유입수 옆의 펌프와 느슨한 천장 지반을 한 화면에 놓는다.", "펌프 배출관으로 물이 흘러도 천장 입자는 계속 느슨한 상태다."),
    "S06b": ("R_PUMP", "펌프로 바닥 물은 빠져나가지만 갈라진 천장과 벽은 여전히 약한 비교 모형.", "수위만 낮아지고 약한 천장 입자는 계속 움직여 물 제거와 지반 보강의 차이가 보인다."),
    "S06c": ("R_GROUND", "장비가 들어가야 할 굴착 공간 앞에 흙과 작은 돌이 쌓이는 모형.", "토사가 장비 작업 공간 쪽으로 밀려와 빈 공간을 줄인다."),
    "S06d": ("R_SUPPORT", "배수되는 물과 천장·벽을 받치는 지보를 같은 절개 모형에 보여 준다.", "배수 흐름과 지보 설치가 함께 진행되어 작업 공간을 지킨다."),
    "S07a": ("R_PIPE", "아직 파지 않은 앞쪽 지반과 이미 확보한 뒤쪽 작업 공간을 구분한다.", "굴착면 위쪽에서 선행 보강할 위치를 보여 주고 다음 단계 강관이 앞으로 들어간다."),
    "S07b": ("R_PIPE", "곧은 긴 강관들이 진행 방향으로 앞쪽 지반에 들어가는 종단 절개 모형.", "각 강관은 굽지 않은 직선 상태로 굴착 진행 방향을 따라 전진한다."),
    "S07c": ("R_PIPE", "전방을 향한 곧은 강관의 입구들이 터널 천장 둘레에서 아치 배열을 이루는 횡단면.", "고정 카메라에서 강관 입구가 둘레 순서로 드러난다. 강관 자체를 휘어진 아치로 바꾸지 않는다."),
    "S07d": ("R_PIPE", "미굴착 지반 안에 미리 들어간 강관 지붕과 바로 아래 다음 굴착 구간을 함께 보여 준다.", "강관은 제자리를 유지하고 아래쪽 굴착만 짧게 진행된다."),
    "S08a": ("R_PIPE", "파이프 루프의 종단 길이와 천장 둘레 배열을 읽을 수 있는 동일 모형.", "카메라는 고정하고 선행 강관 아래의 안전한 굴착 순서를 보여 준다."),
    "S08b": ("R_PIPE_DOUBLE", "확인한 현장 사진에 맞춰 천장 둘레에 강관 입구 두 줄이 놓인 설명용 모형.", "두 번째 줄의 강관이 앞쪽 지반으로 차례로 들어간다. 새로 휘어진 부재는 생기지 않는다."),
    "S08c": ("R_PIPE_DOUBLE", "전방 지반을 지지하는 이중 강관과 그 아래 짧은 굴착 공간.", "강관은 고정된 채 아래의 짧은 흙 구간이 제거되고 뒤에서 지보가 이어진다."),
    "S09a": ("R_EXCAVATION", "강관 아래 열린 구간을 짧게 제한하는 상부 굴착 모형.", "짧은 한 구간만 제거되고 앞의 긴 미굴착 지반은 남아 있다."),
    "S09b": ("R_EXCAVATION", "상부를 짧게 판 직후 새 면을 바로 받치는 두 단계.", "상부 소량 굴착 뒤 곧바로 지보와 숏크리트가 이어진다."),
    "S09c": ("R_EXCAVATION", "한 번의 짧은 굴착 전진을 측면에서 읽을 수 있는 모형. 약 1미터는 편집 표기로만 넣는다.", "짧은 전진 한 번만 진행하고 작업 공간을 넓게 한꺼번에 열지 않는다."),
    "S09d": ("R_EXCAVATION", "이미 받친 구간 옆의 다음 짧은 구간을 같은 좌표계에서 보여 준다.", "새 짧은 구간의 굴착과 지보 설치가 앞 구간에 이어 진행된다. 이전 동작의 영상 루프는 쓰지 않는다."),
    "S10a": ("R_SUPPORT", "새로 드러난 거친 지반 표면에 숏크리트 층을 형성하는 단면.", "분사 노즐에서 콘크리트가 나와 노출 지반을 얇은 연속층으로 덮는다."),
    "S10b": ("R_SUPPORT", "필요 위치에 철망과 횡방향 강철 지보가 놓이는 상부 단면.", "철망과 강철 지보가 지반 면을 따라 설치된다. 종방향 강관과 부재 방향을 구별한다."),
    "S10c": ("R_SUPPORT", "갈라진 암반 안으로 들어가는 긴 록볼트의 측면 절개.", "볼트가 균열을 가로질러 암반 내부로 들어가 여러 조각을 묶는다."),
    "S10d": ("R_SUPPORT", "지반 상태가 다른 인접 구간의 콘크리트 층과 받침 조합을 나누어 보여 준다.", "각 지반에 필요한 지보 조합이 순차적으로 설치된다. 실제 미확인 두께 수치는 쓰지 않는다."),
    "S11a": ("R_FOOTING", "천장 지보의 양발이 닿는 바닥 부분을 포함한 단면.", "카메라는 고정하고 주목할 변화는 약한 받침 발 아래에서만 일어난다."),
    "S11b": ("R_FOOTING", "약한 바닥에 선 받침과 안정된 받침을 대비하는 일반 원리 모형.", "약한 바닥 쪽 받침이 조금 내려앉으며 단면이 변형된다. 아탈 현장 바닥 융기 실측 재현으로 표기하지 않는다."),
    "S11c": ("R_FOOTING", "지보가 힘을 전달할 바닥 받침 자리까지 확보한 모형.", "양쪽 지보 발 아래가 보강되어 하중을 받을 자리가 형성된다."),
    "S12a": ("R_INVERT_TEMP", "상부 굴착 상태에서 양쪽 지보 발을 잇는 임시 인버트. 미굴착 하부는 그대로 남겨 둔다.", "상부 양측 받침 사이 임시 바닥 연결이 닫힌다. 이 장면에 깊은 최종 인버트를 동시에 시공하지 않는다."),
    "S12b": ("R_INVERT_FINAL", "시간이 지난 후 하부를 추가 굴착하고 깊은 최종 인버트를 만드는 별도 공정 모형.", "남은 하부를 제거한 뒤 깊은 곡선 바닥 구조가 양측 벽과 이어진다."),
    "S12c": ("R_INVERT_FINAL", "천장·벽·깊은 바닥이 연결된 난구간 최종 단면.", "부재는 유지되고 설명용 힘의 전달이 연결된 구조 둘레를 따라 순서대로 표현된다. 물길과 혼동하지 않는다."),
    "S12d": ("R_INVERT_FINAL", "깊은 최종 인버트 안쪽 위에 평평한 차도가 놓이는 단면.", "최종 곡선 바닥 위의 내부 공간에 평평한 도로 구조가 완성된다."),
    "S13a": ("R_GROUND_REAL", "처음과 다른 구도로 물이 나오는 굴착면과 확보된 공간을 다시 본다.", "유입수는 계속 흐르고 재현 인물의 얼굴은 작게 유지한다."),
    "S13b": ("R_GROUND_REAL", "물이 쏟아지는 굴착면 앞의 지보와 배수 공간을 함께 보여 주어 질문을 회수한다.", "카메라는 고정하고 물과 작은 토사만 이동한다. 도입 영상의 재사용은 하지 않는다."),
    "S13c": ("R_RECAP_SUPPORT", "선행 강관·짧은 굴착·즉시 지보·바닥 연결을 같은 모형에서 순서대로 정리한다.", "서로 다른 공정을 시간 순서대로 보여 주며 임시 바닥과 최종 인버트를 동시에 만들지 않는다."),
    "S13d": ("R_DRAIN", "지보로 형태를 지킨 터널 바깥 틈에는 여전히 물이 남아 있는 단면.", "지보는 고정되고 바깥 지하수 흐름이 계속되어 다음 배수 문제로 연결한다."),
    "S14a": ("R_DRAIN", "터널 뒤편에서 들어오는 물과 비어 있는 배수 경로를 함께 보여 준다.", "물은 낮은 배수 방향으로 흐르고 도로 또는 하부 대피 통로로 들어가지 않는다."),
    "S14b": ("R_GROUT_DRAIN", "작은 틈의 주입 보강과 별도 관의 배수를 분리한 두 구역 절개 모형.", "작은 틈은 주입재로 메워 유입이 줄고, 별도의 주요 물길은 배수관으로 계속 빠져나간다."),
    "S14c": ("R_GROUT_DRAIN", "틈 유입과 큰 물길을 같은 방법으로 막지 않는 비교 모형.", "작은 틈의 차수와 큰 물길의 배수가 각기 다른 경로로 작동한다."),
    "S15a": ("R_PRESSURE", "큰 물길을 막은 벽 뒤에 물이 고이는 일반 원리 모형.", "막힌 뒤편에 물이 차오르기 시작하고 배출되지 않는다."),
    "S15b": ("R_PRESSURE", "막힌 뒤쪽 수위가 높아지며 구조를 누르는 부담이 커지는 모형.", "수위가 올라가고 설명용 압력 표현이 점차 강해진다. 폭발과 댐 붕괴를 추가하지 않는다."),
    "S15c": ("R_PRESSURE", "물이 가득 찬 뒤편과 이를 받는 터널 외측 구조를 함께 보여 준다.", "물이 구조를 누르는 방향이 보이고 과도한 붕괴는 일으키지 않는다."),
    "S15d": ("R_DOCUMENT", "실존 기술책자 내용 확인을 나타내는 무문자 책자와 손, 옆의 방수·배수 모형. 실제 문서처럼 가짜 글자를 만들지 않는다.", "인도 성인의 작은 손이 무문자 자료 한 장을 넘긴다."),
    "S16a": ("R_DRAIN", "주요 유입수를 모으는 배수관과 배수구의 연속된 경로.", "파란 설명용 물이 집수 위치에서 관과 배수구를 따라 낮은 쪽으로 흐른다."),
    "S16b": ("R_MEMBRANE", "해당 구간의 방수막 뒤 배수 공간·관·마른 차도를 구별한 단면.", "막 뒤 물이 배수 통로로 빠져나가며 차도와 하부 대피 통로는 마르게 유지된다."),
    "S16c": ("R_MEMBRANE", "차수 부분과 배수 부분이 함께 작동하는 같은 단면.", "차도로 향하는 누수는 줄고 뒤편 물은 따로 빠져나간다. 전 구간이 같은 시공 단면이라고 일반화하지 않는다."),
    "S17a": ("R_MONITOR", "지보를 설치한 뒤에도 조금씩 변형되는 약한 지반 모형.", "지반은 미세하게 계속 움직이고 지보는 고정된 위치에서 하중을 받는다."),
    "S17b": ("R_MONITOR", "천장·벽의 계측점을 따라 변화량을 확인하는 설명용 단면.", "계측점 사이 간격이 미세하게 바뀌고 측정 표식이 그 변화를 따라간다. 임의 수치는 쓰지 않는다."),
    "S17c": ("R_MONITOR", "변형이 커진 구간에서 보강 조합을 다시 검토하는 비교 모형.", "관측된 변형 뒤에 추가 받침과 더 짧은 굴착 단계가 적용된다."),
    "S17d": ("R_MONITOR", "서로 다른 지반 두 구간에 서로 다른 보강을 적용한 연속 단면.", "각 구간의 관측과 지보 조정이 개별적으로 진행된다."),
    "S18a": ("R_GROUND_RECON", "세리 날라에서 추가 붕괴·큰 변형이 발생했다는 기록을 설명하는 단순화 재구성 단면.", "기존 보강 주변의 토사가 추가로 흘러들고 지보가 변형된다. 실제 사고 영상이나 실측 재현으로 소개하지 않는다."),
    "S18b": ("R_REINFORCE", "배수관·주입 보강·추가 강관을 순서대로 적용하는 모형.", "관으로 물을 빼고 틈 주입과 선행 강관 추가가 이어진 뒤 짧게 전진한다."),
    "S18c": ("R_REINFORCE", "새로 드러난 지반을 보고 필요한 보강을 바꾸는 전후 상태.", "확인한 지반 부분에 맞춰 추가 지보가 설치된다. 모든 구간에 같은 조합을 복제하지 않는다."),
    "S19a": ("R_HISTORY", "한 구간 공사가 길어진 이유를 상부 굴착·배수·보강으로 나눈 무문자 공정 요약. 약 4년은 편집에서만 쓴다.", "서로 다른 공정 상태가 시간 순서대로 전환된다."),
    "S19b": ("R_REINFORCE", "물 처리·붕괴부 안정·지보 보강을 함께 진행하는 모형.", "배수 흐름, 토사 안정화, 추가 받침이 같은 작업 공간에서 순서대로 진행된다."),
    "S19c": ("R_INVERT_FINAL", "상부 관통 이후 남은 하부 굴착과 깊은 최종 인버트의 후속 시공.", "상부 지보를 유지하며 하부를 추가 굴착하고 최종 바닥 구조를 닫는다."),
    "S20a": ("R_BREAKTHROUGH", "2017년 양쪽 굴착이 만나는 순간을 실사풍으로 재구성한다. 실제 인물과 행사는 재현하지 않는다.", "얇게 남은 굴착면이 제거되며 반대편 작업등이 드러난다. 인도 성인은 멀리서 안전하게 서 있다."),
    "S20b": ("R_SOUTH", "완공 후 남측 포털과 입구 안쪽이 함께 읽히는 하나의 넓은 구도. 개통 날짜는 편집에서만 표시한다.", "작은 차가 정상 속도로 터널에 진입하고 실내 조명은 일정하다."),
    "S21a": ("R_MEMBRANE", "차량이 달리는 마른 차도 바깥에는 지하수와 배수 시설이 남아 있는 절개 단면.", "작은 차량은 위 차도로 지나가고 물은 도로 바깥 별도 배수 경로로 흐른다."),
    "S21b": ("R_MAINTENANCE", "2024년 후속 기록의 누수 관리 어려움을 설명하는 과거 재구성. 기술자가 벽면 누수와 배수구를 확인한다.", "인도 성인 기술자의 먼 뒷모습이 손전등으로 벽면의 작은 누수와 배수구를 점검한다. 현재 2026년 실황으로 표시하지 않는다."),
    "S21c": ("R_DRAIN", "차도는 운영하면서 뒤편 물길과 구조를 관리하는 분리된 경로.", "배수관의 물 흐름과 구조 계측을 계속 유지한다. 대피 통로를 배수관처럼 쓰지 않는다."),
    "S22a": ("R_NORTH", "도입과 다른 북측 포털 형상을 유지한 넓은 화면에서 처음 질문을 회수한다.", "작은 차량은 통과하고 카메라는 정면 고정이다."),
    "S22b": ("R_GROUND_REAL", "밝고 읽기 쉬운 굴착면 물길과 그 앞의 확보된 공간을 다시 보여 준다. 이전 소스 재사용은 하지 않는다.", "카메라는 고정하고 물만 연속해서 흐른다."),
    "S23a": ("R_RECAP_SUPPORT", "물길 확인→선행 보강→짧은 굴착→즉시 지보를 같은 좌표계에서 요약한다.", "물길 탐색 후 강관, 짧은 굴착, 지보가 시간 순서대로 이어진다."),
    "S23b": ("R_RECAP_DRAIN", "바닥까지 닫힌 구조와 별도로 물을 빼는 경로를 동시에 읽게 한다.", "구조는 연결된 채 유지되고 물은 따로 마련한 관으로 흘러나간다."),
    "S23c": ("R_FINISHED_CUTAWAY", "작은 차량이 달리는 차도와 이를 둘러싼 지반·지보·바닥·배수의 전체 단면.", "차량이 정상 속도로 통과하고 구조는 공간을 유지하며 뒤편 물은 별도 경로로 흐른다."),
    "S24a": ("R_NORTH", "북측 포털과 넓은 산악 배경으로 마무리한다. 구독·하이프 문구는 정확한 편집 글자로만 넣는다.", "아주 느린 드론 풀백 한 번 뒤 산과 포털이 함께 보이는 정지 구도로 끝난다."),
}

# 원리 구간은 질문/명명 문장도 동일한 3D 공정 안에 넣는다.
# Q = 앞 질문 회수, R = 실사·장소, P = 고정카메라 3D 원리.
BEATS = [
    ("S01a", "S02c", "R"), ("S03a", "S03d", "R"), ("S04a", "S04c", "R"),
    ("S05a", "S05c", "P"), ("S06a", "S06d", "P"), ("S07a", "S07d", "P"),
    ("S08a", "S08c", "P"), ("S09a", "S09d", "P"), ("S10a", "S10d", "P"),
    ("S11a", "S11c", "P"), ("S12a", "S12a", "P"), ("S12b", "S12d", "P"),
    ("S13a", "S13b", "R"), ("S13c", "S13d", "P"), ("S14a", "S14c", "P"),
    ("S15a", "S15c", "P"), ("S15d", "S15d", "R"), ("S16a", "S16c", "P"),
    ("S17a", "S17d", "P"), ("S18a", "S18c", "P"), ("S19a", "S19a", "R"),
    ("S19b", "S19b", "P"), ("S19c", "S19c", "P"), ("S20a", "S20b", "R"),
    ("S21a", "S21a", "P"), ("S21b", "S21b", "R"), ("S21c", "S21c", "P"),
    ("S22a", "S22b", "R"), ("S23a", "S23a", "P"), ("S23b", "S23c", "P"), ("S24a", "S24a", "R"),
]

REFERENCE_GROUPS = {
    "R_SOUTH": "남측 실제 포털 master: 노랑·주황 세로 외장/갈색 사선 차양/어두운 사각 차량 개구부/숲 계곡. 접근 장식문과 합치지 않음.",
    "R_NORTH": "북측 실제 포털 master: 진녹색 큰 박공/적갈색 작은 전면 박공/황색 패널/사진 오른쪽 차량 개구부/회색 옹벽/벌거벗은 산악 사면.",
    "R_TERRAIN": "확인 지형을 바탕으로 만들 산악 경로 master. 생성된 지형의 정확성은 후속 별도 검수. 경로·수치는 편집에서 표시.",
    "R_TERRAIN_SNOW": "같은 산악 지역의 설경 master. 실제 과거 폭설 순간 영상으로 주장하지 않음.",
    "R_GROUND": "공통 공학 좌표계: 진행 방향 +X, 종방향 곧은 강관/횡방향 지보 구별. 파란 설명용 지하수/회갈색 토사. 원리 설명용 단순화.",
    "R_GROUND_REAL": "시공 당시 물과 토사 유입의 실사풍 재구성. 실제 기록 영상/정확한 사고 순간 재현으로 주장하지 않음.",
    "R_HISTORY": "공정·거리·기간 비교용 무문자 설명 화면. 4년은 상부 굴착 통과 기간이며 최종 인버트 완료 기간과 구분.",
    "R_PIPE": "공통 지반 master에서 진행 방향으로 뻗는 곧은 강관, 횡단면에서 천장 둘레 아치 배열. 횡지보와 다름.",
    "R_PIPE_DOUBLE": "R_PIPE와 같은 좌표계. Bernard Fig.7에서 확인한 강관 입구 이중 배열을 반영.",
    "R_PUMP": "공통 지반 master에 펌프·배수관. 물 제거와 지반 지지의 구별이 명확함.",
    "R_SUPPORT": "공통 지반 master의 숏크리트/철망/횡방향 지보/록볼트. 확인되지 않은 두께·치수는 지정하지 않음.",
    "R_EXCAVATION": "R_PIPE와 R_SUPPORT를 유지한 짧은 상부 굴착→즉시 지보의 순차 모형. 한 번에 길게 개방하지 않음.",
    "R_FOOTING": "약한 기초와 지보 안정의 일반 원리 모형. 아탈 터널의 실제 바닥 융기를 단정하지 않음.",
    "R_INVERT_TEMP": "상부 굴착 당시 임시 바닥 폐합. 하부 미굴착 상태이며 깊은 최종 인버트는 이 단계에 없음.",
    "R_INVERT_FINAL": "후속 하부 굴착과 세리 날라의 깊은 최종 인버트. 일반 본선 Fig.2 단면을 전 구간 동일한 최종 단면으로 쓰지 않음.",
    "R_RECAP_SUPPORT": "공통 공학 master. 임시 인버트와 후속 최종 인버트의 시간 순서 유지.",
    "R_DRAIN": "차도/배수/차도 아래 중앙 대피 통로를 분리. 대피 통로는 마르게 유지. 별도 지하수 배수는 확인된 해당 구간만 설명.",
    "R_GROUT_DRAIN": "작은 틈 주입 보강과 주요 유입수 배수의 다른 경로. 임의로 전수 차수하지 않음.",
    "R_PRESSURE": "큰 유입수를 막을 때 뒤편 수위와 압력이 높아지는 일반 원리. 과장된 폭발·확인되지 않은 현장 붕괴 없음.",
    "R_DOCUMENT": "무문자 재구성 자료/손. 가짜 기술책자 글자나 로고를 만들지 않음. 출처 명시는 정확한 후속 편집 글자.",
    "R_MEMBRANE": "해당 구간의 방수막과 뒤편 배수 공간. 일반 구간 전체 동일 시공으로 확대하지 않음. 대피 통로와 배수 분리.",
    "R_MONITOR": "공통 단면과 천장·벽 계측점. 실제 관측 숫자를 새로 만들지 않음.",
    "R_GROUND_RECON": "세리 날라 추가 붕괴/변형 기록을 설명하는 단순화 재구성. 실측 사고 형상 재현 아님.",
    "R_REINFORCE": "주입·배수·추가 강관·지보를 지반에 따라 바꾸는 공통 공정 master.",
    "R_BREAKTHROUGH": "2017년 관통의 실사풍 재구성. 실존 인물과 구체적 행사 재현 없음.",
    "R_MAINTENANCE": "2024년 후속 기록을 설명하는 누수 점검의 과거 재구성. 현재 상태나 누수량을 주장하지 않음.",
    "R_RECAP_DRAIN": "R_INVERT_FINAL과 R_DRAIN의 구조/물길 분리 관계를 유지한 정리용 모형.",
    "R_FINISHED_CUTAWAY": "최종 차도·구조·주변 지반·배수 관계를 보여 주는 단순화 투시. 양방향 차도 한 개 본선 튜브, 대피 통로와 배수 분리.",
}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def partition(total, capacity, minimum, prefer_long=False):
    """정수 프레임을 잃지 않고 분할한다. 초 추정/속도 변경을 하지 않는다."""
    if total <= 0:
        return []
    n = math.ceil(total / capacity)
    if total < minimum * n:
        raise ValueError(f"{total}프레임을 최대 {capacity}, 최소 {minimum}프레임 컷으로 분할할 수 없음")
    if prefer_long:
        out = [capacity] * (n - 1) + [total - capacity * (n - 1)]
        preferred = min(PREFERRED_VIDEO_MIN, total // n)
        if n > 1 and out[-1] < preferred:
            borrow = preferred - out[-1]
            out[-2] -= borrow
            out[-1] += borrow
        return out
    q, r = divmod(total, n)
    return [q + (i < r) for i in range(n)]


def opening_parts(capacity, measured_boundaries, mandatory_boundaries):
    """30초 3~5개 긴 영상. 공사 내부→완공 포털은 실제 문장 시작에서 분리한다."""
    hard = sorted({0, OPENING_FRAMES} | {x for x in mandatory_boundaries if 0 < x < OPENING_FRAMES})
    possibilities = []
    for a, b in zip(hard, hard[1:]):
        possibilities.append([n for n in range(1, 6) if n * 5 * FPS <= b - a <= n * capacity])
    feasible = [ns for ns in itertools.product(*possibilities) if 3 <= sum(ns) <= 5]
    if not feasible:
        raise ValueError("이 제작 길이/실측 장소 전환 경계로 도입 30초를 5초 이상 영상 3~5개로 구성할 수 없음")
    counts = min(feasible, key=lambda ns: (abs(sum(ns) - 4), sum(ns), ns))
    bounds = [0]
    for section, n in enumerate(counts):
        a, b = hard[section], hard[section + 1]
        previous = a
        for i in range(1, n):
            remaining = n - i
            lo = max(previous + 5 * FPS, b - remaining * capacity)
            hi = min(previous + capacity, b - remaining * 5 * FPS)
            target = a + round(i * (b - a) / n)
            candidates = [x for x in measured_boundaries if lo <= x <= hi]
            selected = min(candidates, key=lambda x: abs(x - target)) if candidates else min(hi, max(lo, target))
            bounds.append(selected)
            previous = selected
        bounds.append(b)
    return bounds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clip-seconds", type=float, default=os.environ.get("CHEEZON_CLIP_SECONDS"),
                        help="확인할 제작 요구 사양의 영상 길이(필수). 현재 설정/생성 후 실측을 대신하지 않음")
    parser.add_argument("--timing", type=Path, default=EP / "review_edit/narr_timing.json")
    args = parser.parse_args()
    if args.clip_seconds is None:
        parser.error("--clip-seconds 또는 CHEEZON_CLIP_SECONDS에 확인할 제작 길이를 명시해야 합니다")
    if not math.isfinite(args.clip_seconds) or args.clip_seconds <= SOURCE_MARGIN:
        parser.error("클립 길이는 유한 양수이고 소스 끝 여유보다 길어야 합니다")
    if not args.timing.is_file():
        parser.error(f"실측 시간표가 없습니다. 완료 전 추정 계획을 만들지 않습니다: {args.timing}")
    timing = read_json(args.timing)
    source = read_json(EP / "script/source_ko_sentences.json")
    source_ids = [x["id"] for x in source]
    if len(timing) != 78 or [x["id"] for x in timing] != source_ids:
        parser.error("실측 시간표의 78개 문장 ID/순서가 확정 원문과 다릅니다")
    if set(source_ids) != set(SCENE):
        parser.error("문장 의미 카탈로그의 ID가 확정 원문과 다릅니다")
    if not PRINCIPLE_SENT <= set(source_ids):
        parser.error("원리 문장 ID가 원문에 없습니다")
    last_end = 0.0
    for row in timing:
        a, b = row.get("start"), row.get("end")
        if not isinstance(a, (float, int)) or not isinstance(b, (float, int)) or not (math.isfinite(a) and math.isfinite(b)):
            parser.error(f"실측값이 유효하지 않습니다: {row['id']}")
        if a < last_end - 0.001 or b <= a:
            parser.error(f"실측 순서/길이 오류: {row['id']}")
        last_end = b
    if timing[0]["start"] != 0:
        parser.error("첫 내레이션 문장이 0초에서 시작하지 않습니다")
    # 원문 자체를 바꾸지 않았음을 plan에도 확인 가능한 값으로 남긴다.
    locked = read_json(EP / "script/script_lock.json")
    ko = (EP / "script/script_ko_final.md").read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    body = ko.split("## 대본\n", 1)[1].split("## 근거표\n", 1)[0]
    actual_ko_sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if actual_ko_sha != "b6f91f4fcf8a86d100157ee3e1bdb51f4c392780625716b845d7075333eb34c6":
        parser.error("승인된 한국어 내레이션 본문 해시가 다릅니다")
    if locked.get("body_sha256") != actual_ko_sha or locked.get("sentence_count") != 78:
        parser.error("승인 잠금 기록이 원문/문장 수와 다릅니다")
    # TTS가 합격한 실제 시간표만 계획 입력으로 사용한다.
    checks_path = args.timing.parent / "narr_check.json"
    if not checks_path.is_file():
        parser.error(f"문장별 실제 음성 검사 결과가 없습니다: {checks_path}")
    checks = read_json(checks_path)
    # ep09 runner는 ID별 dict로 보존한다. 리스트도 명시적 ID로만 대응한다.
    checks_by_id = checks if isinstance(checks, dict) else {x["id"]: x for x in checks}
    for sid in source_ids:
        rec = checks_by_id.get(sid, {})
        sentences = rec.get("sentences", [])
        if not sentences or not all(x.get("pass") is True and x.get("check", {}).get("pass") is True for x in sentences):
            parser.error(f"엄격 음성 검사에 통과하지 않은 문장이 있습니다: {sid}")
        if rec.get("hi") != next(x["hi"] for x in timing if x["id"] == sid):
            parser.error(f"시간표와 실제 음성 검사의 힌디어가 다릅니다: {sid}")

    capacity = math.floor((args.clip_seconds - SOURCE_MARGIN) * FPS + 1e-6)
    narration_end = float(timing[-1]["end"])
    vend_f = round((narration_end + TAIL) * FPS)
    if vend_f <= OPENING_FRAMES:
        parser.error("내레이션 전체가 도입 30초보다 짧습니다")
    index = {x["id"]: i for i, x in enumerate(timing)}
    by_id = {x["id"]: x for x in timing}
    source_by_id = {x["id"]: x["ko_source"] for x in source}
    start_f = {x["id"]: round(x["start"] * FPS) for x in timing}
    end_f = {x["id"]: round(x["end"] * FPS) for x in timing}
    sentence_slot_end = {x["id"]: (round(timing[i + 1]["start"] * FPS) if i + 1 < len(timing) else vend_f)
                         for i, x in enumerate(timing)}
    beat_ranges, seen = [], []
    for first, last, mode in BEATS:
        a, b = index[first], index[last]
        if a > b:
            parser.error(f"의미 블록의 ID 순서 오류: {first}~{last}")
        ids = source_ids[a:b + 1]
        seen.extend(ids)
        st, en = max(OPENING_FRAMES, start_f[first]), sentence_slot_end[last]
        if en > st:
            beat_ranges.append(dict(f0=st, f1=en, mode=mode, ids=ids))
    if seen != source_ids:
        parser.error("의미 블록에서 문장 누락/중복/순서 변경이 있습니다")

    # 원리 외 총시간은 도입 뒤 P가 아닌 구간. 실사 동작은 의미가 맞는 두 구간에서만 사용한다.
    rest_f = sum(b["f1"] - b["f0"] for b in beat_ranges if b["mode"] != "P")
    target_action_f = round(rest_f * 0.15)
    candidate_intervals = [
        ("S20a", start_f["S20a"], sentence_slot_end["S20a"]),
        ("S21b", start_f["S21b"], sentence_slot_end["S21b"]),
    ]
    action_intervals, remaining = [], target_action_f
    for sid, a, b in candidate_intervals:
        if remaining <= 0:
            break
        total = b - a
        length = min(remaining, total)
        # 남은 이미지/영상이 1초 미만의 파편이 되지 않게 만든다.
        if 0 < total - length < 2 * FPS:
            if length + (total - length) <= math.floor(rest_f * 0.20) - sum(y - x for x, y in action_intervals):
                length = total
            else:
                length = max(0, total - 2 * FPS)
        if length >= MIN_VIDEO_FRAMES:
            action_intervals.append((a, a + length))
            remaining -= length

    cuts, catalog, VID, IMG, SEG = [], [], {}, {}, []
    serial = {"o": 0, "p": 0, "a": 0, "i": 0}
    variants = {}

    def overlapping_ids(a, b):
        # 30fps 경계 반올림의 수 ms만 걸치는 이웃 문장을 다른 장소/공정으로 오인하지 않는다.
        # 발화와 0.05초 이상 겹칠 때 의미 카탈로그에 넣고, 쉼 전용 컷은 직전 문장을 유지한다.
        ids = [x["id"] for x in timing if min(b, x["end"] * FPS) - max(a, x["start"] * FPS) > 0.05 * FPS]
        if not ids:
            ids = [next((x["id"] for x in reversed(timing) if x["start"] * FPS <= a), source_ids[0])]
        return ids

    def append_cut(a, b, kind, role, prefix):
        serial[prefix] += 1
        sid = f"{prefix}{serial[prefix]:03d}"
        d = b - a
        ids = overlapping_ids(a, b)
        relevant = sorted(ids, key=lambda s: max(0, min(by_id[s]["end"] * FPS, b) - max(by_id[s]["start"] * FPS, a)), reverse=True)
        dominant = relevant[0]
        variants[(kind, dominant)] = variants.get((kind, dominant), 0) + 1
        is_principle = role == "원리"
        # 정지 이미지와 실사 장면은 한 master의 단일 상태를 고른다. 발화 대응 ID 전체는 따로 남긴다.
        # 원리 영상은 같은 공학 좌표계에서 실제 포함된 공정들을 시간 순서대로 보여 준다.
        visual_ids = ids if is_principle else [dominant]
        refs = list(dict.fromkeys(SCENE[s][0] for s in visual_ids))
        descriptions = [SCENE[s][1] for s in visual_ids]
        actions = [SCENE[s][2] for s in visual_ids]
        if kind == "v":
            file = f"clips_v1/{sid}.mp4"
            VID[sid] = (file, [(0, args.clip_seconds - SOURCE_MARGIN)], role)
            camera = "locked-off static shot; no zoom, no pan"
            framing = "설명 대상과 모든 작동 경로가 보이는 고정 절개 구도"
            if role == "도입":
                # 장소 전환은 S02a의 실제 문장 경계로 나누어 다른 master를 한 소스에 합치지 않는다.
                framing = ("얼굴이 커지지 않는 넓은 고정 구도; 물·토사와 작업 공간의 관계가 한눈에 읽힘"
                           if a < start_f["S02a"] else "남측 포털 형상과 주변 산악 규모가 함께 읽히는 넓은 고정 구도")
            cut = dict(start=round(a / FPS, 6), end=round(b / FPS, 6), out_f0=a, out_f1=b,
                       dur=round(d / FPS, 6), src=sid, kind=kind, opt="", src_start=0.0,
                       src_end=round(d / FPS, 6), file=file, role=role)
        else:
            file = f"img/v1_{sid}_1.png"
            IMG[sid] = f"v1_{sid}_1"
            effect = MOVES[(serial["i"] - 1) % len(MOVES)]
            camera, framing = "still image + 6% edit zoom/pan", [
                "대상과 주변 상황이 함께 읽히는 넓은 구도",
                "핵심 대상의 옆면·부분 구조를 보여 주는 구도; 인물 얼굴 근접 금지",
                "앞선 컷과 다른 높이·거리에서 원인과 결과를 한 화면에 보여 주는 구도",
            ][(serial["i"] - 1) % 3]
            cut = dict(start=round(a / FPS, 6), end=round(b / FPS, 6), out_f0=a, out_f1=b,
                       dur=round(d / FPS, 6), src=sid, kind=kind, opt="", file=file,
                       role="고정+효과", effect=effect)
        cuts.append(cut)
        SEG.append((a / FPS, sid, kind, 0.0, ""))
        catalog.append(dict(
            source_id=sid, file=file, kind=kind, role=role, sentence_ids=ids,
            visual_sentence_ids=visual_ids,
            visual_selection_basis="all principle sentences in one engineering master" if is_principle else "one dominant sentence state; no place morphing",
            variant_index=variants[(kind, dominant)],
            master_id_override=("AT_C" if a < start_f["S02a"] else "AT_S") if role == "도입" else None,
            sentence_ko=[source_by_id[s] for s in ids], dominant_sentence_id=dominant,
            plan_start_frame=a, plan_end_frame=b, required_use_sec=round(d / FPS, 6),
            screen_ko=" ".join(descriptions), framing_ko=framing,
            style="bright 3D educational diorama" if is_principle else (
                "photorealistic Indian reconstruction / place" if not all(r in {"R_TERRAIN", "R_HISTORY"} for r in refs)
                else "geographical / historical explanatory visual"),
            principle=is_principle, reference_groups=refs, required_master_reference=True,
            camera=camera,
            movement_ko=" ".join(actions) if kind == "v" else "생성 그림은 정지. 편집에서만 약 6% 줌·좌중우 이동을 적용한다.",
            end_ko="같은 형상과 밝기를 유지한 구도로 끝난다. 감속·정지 프레임 연장·반복·역재생 금지.",
            generation_status="not_generated", actual_file_existence_checked=False,
            visual_review_status="not_performed", usable_range_status="production_requirement_only" if kind == "v" else "not_applicable",
            restrictions=["생성 글자·로고·번호판·치수선 없음", "인도 성인만, 얼굴 작게, 실존 인물 재현 없음",
                          "기준 그림 형상·색·좌표계를 유지", "실제 도면/기록 영상과 구별되는 설명용 재구성"],
        ))

    boundaries = sorted({start_f[s] for s in source_ids} | {end_f[s] for s in source_ids})
    op = opening_parts(capacity, boundaries, [start_f["S02a"]])
    for a, b in zip(op, op[1:]):
        append_cut(a, b, "v", "도입", "o")
    for beat in beat_ranges:
        a, b = beat["f0"], beat["f1"]
        if beat["mode"] == "P":
            lengths = partition(b - a, capacity, MIN_VIDEO_FRAMES, prefer_long=True)
            for length in lengths:
                append_cut(a, a + length, "v", "원리", "p")
                a += length
            continue
        # 동작 후보의 실측 발화 구간을 제외한 나머지는 이미지로 2~4초 분할.
        edges = sorted({a, b} | {max(a, x) for x, y in action_intervals if x < b and y > a}
                       | {min(b, y) for x, y in action_intervals if x < b and y > a})
        for st, en in zip(edges, edges[1:]):
            active = any(x <= st and en <= y for x, y in action_intervals)
            lengths = partition(en - st, capacity if active else 4 * FPS,
                                MIN_VIDEO_FRAMES if active else 2 * FPS, prefer_long=active)
            for length in lengths:
                append_cut(st, st + length, "v" if active else "i", "동작" if active else "고정+효과", "a" if active else "i")
                st += length

    errors, warnings, used = [], [], {}
    if not cuts or cuts[0]["out_f0"] != 0 or cuts[-1]["out_f1"] != vend_f:
        errors.append("시작/총 길이 프레임 불일치")
    for i, c in enumerate(cuts):
        d = c["out_f1"] - c["out_f0"]
        if d <= 0:
            errors.append(f"{c['src']}: 길이 0 이하")
        if d < MIN_VIDEO_FRAMES:
            errors.append(f"{c['src']}: 1초 미만 컷")
        if i and cuts[i - 1]["out_f1"] != c["out_f0"]:
            errors.append(f"{c['src']}: 타임라인 틈/겹침")
        if c["kind"] == "v":
            if c["src"] not in VID:
                errors.append(f"{c['src']}: 미등록 영상")
            if not any(a - 1e-6 <= c["src_start"] and c["src_end"] <= b + 1e-6 for a, b in VID[c["src"]][1]):
                errors.append(f"{c['src']}: 제작 요구 쓸 구간 밖")
            for a, b in used.get(c["src"], []):
                if c["src_start"] < b - 1e-6 and c["src_end"] > a + 1e-6:
                    errors.append(f"{c['src']}: 소스 재생 구간 겹침")
            used.setdefault(c["src"], []).append((c["src_start"], c["src_end"]))
        else:
            if c["src"] not in IMG:
                errors.append(f"{c['src']}: 미등록 이미지")
            if c["src"] in used:
                errors.append(f"{c['src']}: 이미지 재사용")
            if d > round(IMG_MAX * FPS):
                errors.append(f"{c['src']}: 이미지 4.5초 초과")
            if not 2 * FPS <= d <= 4 * FPS:
                errors.append(f"{c['src']}: 이미지 2~4초 범위 밖")
            used[c["src"]] = [(0, d / FPS)]
    unused = sorted((set(VID) | set(IMG)) - set(used))
    if unused:
        errors.append(f"미사용 등록 소스: {unused}")
    missing_sentences = [s for s in source_ids if not any(c["start"] < by_id[s]["end"] and c["end"] > by_id[s]["start"] for c in cuts)]
    if missing_sentences:
        errors.append(f"화면 누락 문장: {missing_sentences}")
    principle_coverage = []
    for sid in sorted(PRINCIPLE_SENT, key=index.get):
        row = by_id[sid]
        dur = row["end"] - row["start"]
        covered = sum(max(0, min(row["end"], c["end"]) - max(row["start"], c["start"])) for c in cuts if c["kind"] == "v" and c["role"] == "원리")
        proportion = min(1.0, covered / dur)
        principle_coverage.append(dict(id=sid, narration_sec=round(dur, 6), principle_video_sec=round(covered, 6), ratio=round(proportion, 6)))
        # 반올림 전 발화 경계와 30fps 경계의 차이만 1프레임 이내 허용한다.
        if covered + 1 / FPS + 1e-6 < dur:
            errors.append(f"{sid}: 원리 영상 100% 미달({covered:.3f}/{dur:.3f}초)")
    opening = [c for c in cuts if c["out_f0"] < OPENING_FRAMES]
    if not (3 <= len(opening) <= 5 and all(c["kind"] == "v" and c["dur"] >= 5 for c in opening)):
        errors.append("도입 30초 영상 3~5개/각 5초 이상 조건 불충족")
    if 0 < start_f["S02a"] < OPENING_FRAMES and not any(c["out_f0"] == start_f["S02a"] for c in opening):
        errors.append("도입의 공사 내부/완공 포털 장소 전환 경계 누락")
    rest = [c for c in cuts if c["out_f0"] >= OPENING_FRAMES and c["role"] != "원리"]
    nonprinciple_total_f = sum(c["out_f1"] - c["out_f0"] for c in rest)
    nonprinciple_video_f = sum(c["out_f1"] - c["out_f0"] for c in rest if c["kind"] == "v")
    share = nonprinciple_video_f / nonprinciple_total_f if nonprinciple_total_f else 0
    if not 0.10 <= share <= 0.20:
        errors.append(f"원리 외 영상 {share * 100:.2f}%: 10~20% 범위 밖")
    img_cuts = [c for c in cuts if c["kind"] == "i"]
    for a, b in zip(img_cuts, img_cuts[1:]):
        if a["effect"].split("_")[0] == b["effect"].split("_")[0] or a["effect"][-1] == b["effect"][-1]:
            errors.append(f"이미지 효과 방향 반복: {a['src']} / {b['src']}")
    if abs(vend_f / FPS - (narration_end + TAIL)) > 1 / FPS / 2 + 1e-6:
        errors.append("내레이션 끝+1초와 총길이 불일치")
    paths = [c["file"].casefold() for c in cuts]
    if len(paths) != len(set(paths)):
        errors.append("Windows 대소문자 비구분 파일명 충돌 또는 재사용")
    warnings.extend([
        "미디어 미생성: 실제 파일 존재·길이·밝기·형상·동작·글자·워터마크 검수는 수행하지 않음.",
        f"클립 {args.clip_seconds:g}초는 명시한 제작 요구 사양. 현재 Muse 설정 직접 확인과 생성 후 USE 실측 갱신이 필요함.",
        "계획상 영상은 정상 1.0배속의 새 소스. 감속·정지·반복·역재생은 허용하지 않음.",
        "생성 뒤 탈락/사용 가능 구간 변경이 생기면 이 계획을 재배정하고 자동 점검을 다시 통과해야 함.",
    ])
    out = EP / "plan"
    out.mkdir(parents=True, exist_ok=True)
    report = dict(status="pass" if not errors else "fail", scope="registered_assets_and_plan_logic_only",
                  actual_media_generated=False, actual_file_existence_checked=False, actual_visual_review_performed=False,
                  fps=FPS, narration_sec=narration_end, tail_sec=TAIL, output_frames=vend_f, video_sec=vend_f / FPS,
                  input_timing="review_edit/narr_timing.json",
                  input_timing_sha256=hashlib.sha256(args.timing.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode("utf-8")).hexdigest(),
                  input_timing_hash_canonicalization="UTF-8 without BOM; LF line endings",
                  approved_ko_body_sha256=actual_ko_sha,
                  clip_requirement_seconds=args.clip_seconds, source_requirement_usable_end=args.clip_seconds - SOURCE_MARGIN,
                  source_requirement_usable_frames=capacity, clip_setting_confirmed_in_current_muse_ui=False,
                  total_cuts=len(cuts), video_sources=len(VID), image_sources=len(IMG),
                  opening_video_count=len(opening), nonprinciple_video_ratio=share,
                  nonprinciple_video_frames=nonprinciple_video_f, nonprinciple_frames=nonprinciple_total_f,
                  principle_sentences=len(PRINCIPLE_SENT), principle_coverage=principle_coverage,
                  errors=errors, warnings=warnings)
    write_json(out / "shot_list_v1.json", dict(fps=FPS, narration_sec=narration_end, video_sec=vend_f / FPS,
                                               media_status="not_generated", validation_scope=report["scope"],
                                               cuts=cuts))
    write_json(out / "plan_validation_v1.json", report)
    write_json(out / "scene_catalog_v1.json", dict(status="semantic_design_only_not_generated",
                                                  reference_brief="images/reference_brief.md", reference_groups=REFERENCE_GROUPS,
                                                  video_requirement_seconds=args.clip_seconds, assets=catalog))
    write_json(out / "source_registry_v1.json", dict(media_status="not_generated", VID=VID, IMG=IMG, SEG=SEG,
                                                    USE_basis="production_requirement_only; replace with measured reviewed usable ranges"))
    lines = ["# 9편 아탈 터널 컷 표 v1", "", "자동 생성: `plan/plan_v1.py`. 시각 의미는 확정 78문장, 시간은 완료된 실제 TTS 시간표에서 읽었다.", "",
             f"- 내레이션 {narration_end:.3f}초 / 꼬리 {TAIL:.1f}초 / 영상 {vend_f / FPS:.3f}초({vend_f}프레임, {FPS}fps).",
             f"- 컷 {len(cuts)}개: 영상 {len(VID)}개, 이미지 {len(IMG)}개. 모든 소스는 한 번만 사용한다.",
             f"- 도입 0~30초: {len(opening)}개의 5초 이상 영상. 원리 문장 {len(PRINCIPLE_SENT)}개는 전 구간 원리 영상(발화 경계 반올림 차이 1프레임 이내).",
             f"- 도입 이후 원리 외 영상: {share * 100:.2f}% ({nonprinciple_video_f / FPS:.3f}/{nonprinciple_total_f / FPS:.3f}초).",
             f"- 영상 제작 요구 사양: {args.clip_seconds:g}초, 끝 {SOURCE_MARGIN:.2f}초를 비우고 최대 {capacity / FPS:.3f}초 사용. 현재 Muse 설정 확인·생성 후 실측 검수는 남아 있다.",
             f"- **계획 논리 점검: {'통과' if not errors else '실패 ' + str(len(errors)) + '건'}.** 등록 asset·프레임·재사용·원리·도입·비율 검사에 한정한다.",
             "- **미디어 미생성.** 실제 파일 존재/길이와 시각 검수를 통과했다는 뜻이 아니다.", ""]
    lines.extend(f"- 오류: {e}" for e in errors)
    lines += ["", "| 출력 시간 | 프레임 | 초 | 문장 | 소스 | 종류 | 소스 구간 / 효과 |", "|---|---:|---:|---|---|---|---|"]
    cat_by_id = {x["source_id"]: x for x in catalog}
    for c in cuts:
        src = f"{c['src_start']:.3f}–{c['src_end']:.3f} / {c['role']}" if c["kind"] == "v" else c["effect"]
        lines.append(f"| {c['start']:.3f}–{c['end']:.3f} | {c['out_f0']}–{c['out_f1']} | {c['dur']:.3f} | {' '.join(cat_by_id[c['src']]['sentence_ids'])} | {c['src']} | {'영상' if c['kind']=='v' else '이미지'} | {src} |")
    (out / "shot_table_v1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    scene_lines = ["# 9편 의미별 장면 카탈로그 v1", "", "실제 미디어는 아직 생성하지 않았다. 컷 시간은 TTS 실측, 형상·색·공정은 `images/reference_brief.md`와 기준 그림 그룹에 맞춰 후속 프롬프트로 구체화한다.", "",
                   "공통: 밝고 선명한 화면, 글자·로고·번호판 없음. 인도 성인만, 얼굴 작게. 실제 포털은 남·북 master를 분리하고, 원리 장면은 고정 카메라에서 상태만 움직인다.", "",
                   "| 소스 | 문장 | 표현 / 기준 그룹 | 한국어 화면 의미 | 영상 동작 / 카메라 |", "|---|---|---|---|---|"]
    for item in catalog:
        scene_lines.append(f"| {item['source_id']} | {' '.join(item['sentence_ids'])} | {'원리 3D' if item['principle'] else item['role']} / {', '.join(item['reference_groups'])} | {item['screen_ko']} {item['framing_ko']} | {item['movement_ko']} / {item['camera']} |")
    (out / "scene_catalog_v1.md").write_text("\n".join(scene_lines) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("status", "scope", "narration_sec", "video_sec", "total_cuts", "video_sources", "image_sources", "opening_video_count", "nonprinciple_video_ratio", "errors")}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
