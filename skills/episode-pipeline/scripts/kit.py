"""공통 설정 읽기. 에피소드 폴더(이 스크립트들을 복사해 둔 곳)에서 쓴다.
- channel.json : 채널 설정(한 번 정하면 편마다 복사). templates/channel.example.json 참고
- scenes.json  : 이번 편 장면 목록. templates/scenes.example.json 참고
- scene_lines.json : 장면별 나레이션 문장 배열 {"H1": ["문장1", "문장2"], ...}"""
import json, subprocess
from pathlib import Path

HERE = Path.cwd()
LEAD, GAP, TAIL = 0.35, 0.3, 0.6  # 장면 길이 = LEAD + 문장 합 + 문장 사이 GAP + TAIL
NO_TEXT = "no dialogue, no voice, no narration, no speech, no text, no letters, no numbers, no logos, no watermark"


def load(name, default=None):
    p = HERE / name
    if not p.exists():
        if default is not None:
            return default
        raise SystemExit(f"{name} 가 없습니다 (templates/ 예시를 복사해 채우세요)")
    return json.loads(p.read_text(encoding="utf-8"))


def save(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")


CH = load("channel.json")
NAME = f"{CH['slug']}_{HERE.name}"  # 결과 파일·캡컷 드래프트 이름: <채널>_<에피소드 폴더>


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
