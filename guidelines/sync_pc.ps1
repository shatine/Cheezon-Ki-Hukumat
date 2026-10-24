# Cheezon PC 동기화: 깃(main)을 기준으로 PC 스킬·지침을 맞춘다. 이전 판은 지운다.
# 사용: PowerShell에서
#   powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1"          (미리보기, 아무것도 안 바꿈)
#   powershell -ExecutionPolicy Bypass -File "D:\youtube\Cheezon-Ki-Hukumat\guidelines\sync_pc.ps1" -Apply   (실제 실행)
param([switch]$Apply)
$ErrorActionPreference = "Stop"
$Repo    = "D:\youtube\Cheezon-Ki-Hukumat"
$Channel = "D:\youtube\7. Cheezon Ki Hukumat"
$Skills  = Join-Path $Channel ".claude\skills"
$Old = @(
  "$Channel\폐버스가집이 될수없는 이유\skills_copy",
  "$Channel\폐버스가집이 될수없는 이유\제작_인계가이드\스킬_원문",
  "$Channel\episodes\05_morbi_dam_bridge_CODEX\outputs\channel_benchmark_20261015\skill_upgrade",
  "C:\Users\developer1\.codex\skills\cheezon-video",
  "C:\Users\developer1\.codex\skills\cheezon-script",
  "C:\Users\developer1\.codex\skills\cheezon-claude-review"
)
function Say($m){ Write-Host $m -ForegroundColor Cyan }

Say "1) 깃 최신으로 받기: $Repo"
$dirty = git -C $Repo status --porcelain
if ($dirty) {
  Write-Host "   커밋 안 된 변경을 그대로 커밋·푸시합니다(지우지 않음):" -ForegroundColor Yellow
  $dirty | ForEach-Object { "     $_" }
  if ($Apply) { git -C $Repo add -A; git -C $Repo commit -m "WIP: auto-commit before PC sync"; git -C $Repo pull --no-rebase origin main; git -C $Repo push origin main }
}
if ($Apply) { git -C $Repo pull --ff-only origin main }

Say "2) 스킬 폴더를 깃과 똑같이 맞추기 (깃에 없는 이전 스킬은 삭제): $Skills"
Get-ChildItem $Skills -Directory -ErrorAction SilentlyContinue | ForEach-Object {
  $keep = Test-Path (Join-Path "$Repo\skills" $_.Name)
  "   {0}  {1}" -f ($(if($keep){"유지"}else{"삭제"})), $_.Name }
if ($Apply) {
  New-Item -ItemType Directory -Force $Skills | Out-Null
  robocopy "$Repo\skills" $Skills /MIR /NFL /NDL /NJH /NJS /NP | Out-Null
}

Say "3) 지침 파일 교체: CLAUDE.md, CHANNEL.md"
if ($Apply) {
  Copy-Item -Force "$Repo\guidelines\CLAUDE.md"  "$Channel\CLAUDE.md"
  Copy-Item -Force "$Repo\guidelines\CHANNEL.md" "$Channel\CHANNEL.md"
}

Say "4) 이전 스킬 사본·교훈 폴더 삭제"
foreach ($p in $Old) { "   {0}  {1}" -f ($(if(Test-Path $p){"삭제"}else{"없음"})), $p
  if ($Apply -and (Test-Path $p)) { Remove-Item -Recurse -Force $p } }

Say "5) 확인"
Get-ChildItem $Skills -Directory | Select-Object Name
$tools = "$Skills\cheezon-production\tools"
foreach ($f in "tts_vs.py","junk_check.py") { "   {0}  {1}" -f ($(if(Test-Path "$tools\$f"){"있음"}else{"없음 ← TTS에 필요"})), $f }
Get-ChildItem $Channel -Filter AGENTS.md -Recurse -Depth 2 -ErrorAction SilentlyContinue | ForEach-Object { "   AGENTS.md 확인 필요: " + $_.FullName }
if (-not $Apply) { Write-Host "`n미리보기였습니다. 실제로 바꾸려면 -Apply 를 붙여 다시 실행하세요." -ForegroundColor Yellow }
