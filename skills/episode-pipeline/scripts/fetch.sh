#!/bin/bash
# Veo 타임아웃 뒤 버킷의 장면별 폴더에서 영상 받기 -> clips/<id>.mp4 (이미 있으면 건너뜀)
# 사용: BUCKET=gs://<버킷>/<slug>_<에피소드>/clips bash fetch.sh H1 H2 ...
B=${BUCKET:?BUCKET 환경변수에 gs://.../clips 경로를 넣으세요}
mkdir -p clips
for id in "$@"; do
  [ -f clips/$id.mp4 ] && { echo "$id have"; continue; }
  f=$(gcloud storage ls -r "$B/$id/" 2>/dev/null | grep mp4 | head -1)
  if [ -n "$f" ]; then gcloud storage cp "$f" clips/$id.mp4 >/dev/null 2>&1 && echo "$id got"; else echo "$id NONE"; fi
done
