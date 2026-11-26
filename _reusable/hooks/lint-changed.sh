#!/usr/bin/env bash
# lint-changed.sh — lint เฉพาะไฟล์ที่เพิ่งถูกแก้ (generic, ไม่ hardcode folder)
#
# Claude Code เรียก hook นี้ตอน PostToolUse (Edit|Write) และส่ง JSON เข้าทาง stdin
# ตัวอย่าง stdin: {"tool_input":{"file_path":"/abs/path/to/file.tsx"}, ...}
#
# หลักการ: อ่าน file_path -> ดูนามสกุล -> เลือก linter -> lint ไฟล์เดียว
# ถ้าไม่รู้จักนามสกุล หรือ linter ไม่มีในเครื่อง -> เงียบ ๆ ผ่านไป (exit 0) ไม่รบกวน flow
#
# exit code: 0 = ผ่าน/ข้าม, 2 = ให้ Claude Code มองว่า "มี error ต้องแก้" (block)
# ที่นี่เลือกคืน 0 เสมอเพื่อ "เตือนแต่ไม่ block"; อยาก block เปลี่ยน EXIT_ON_ERROR=2

set -euo pipefail
EXIT_ON_ERROR=0   # ตั้ง 2 ถ้าอยากให้ lint error block การทำงาน

# --- 1) อ่าน file_path จาก stdin (JSON) ---
input="$(cat || true)"
file_path=""
if command -v jq >/dev/null 2>&1; then
  file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null || true)"
else
  # fallback ไม่มี jq: ดึงด้วย grep/sed แบบหยาบ ๆ
  file_path="$(printf '%s' "$input" | grep -oE '"file_path"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed -E 's/.*:"([^"]+)"/\1/' || true)"
fi

[ -z "$file_path" ] && exit 0          # ไม่มี path -> ข้าม
[ ! -f "$file_path" ] && exit 0        # ไฟล์ไม่มีอยู่ (เช่นถูกลบ) -> ข้าม

ext="${file_path##*.}"

# helper: รัน linter เฉพาะเมื่อ command มีในเครื่อง
run_if_exists() {
  command -v "$1" >/dev/null 2>&1 || { echo "ℹ️  ข้าม lint: ไม่พบ '$1' ในเครื่อง"; return 0; }
  echo "🔍 lint ($1): $file_path"
  "$@" || { echo "⚠️  lint พบปัญหาใน $file_path"; return "$EXIT_ON_ERROR"; }
}

# --- 2) เลือก linter ตามนามสกุล ---
case "$ext" in
  ts|tsx|js|jsx|mjs|cjs)
    # ใช้ eslint กับไฟล์เดียว (npx จะหา config ที่ใกล้ไฟล์ให้เอง)
    run_if_exists npx eslint "$file_path"
    ;;
  rs)
    # rustfmt เช็ค format เฉพาะไฟล์ (ไม่แก้, แค่เตือน); clippy ต้องทั้ง crate เลยไม่ใส่ที่นี่
    run_if_exists rustfmt --check --edition 2021 "$file_path"
    ;;
  py)
    run_if_exists ruff check "$file_path"
    ;;
  *)
    exit 0   # นามสกุลอื่น -> ไม่ทำอะไร
    ;;
esac
