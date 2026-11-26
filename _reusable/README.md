# _reusable — คลังกลางของกฎ/hook ที่ reuse ได้

ชุด template กลางที่สกัดจาก project นี้ (ai-observability) เอาไปเริ่ม project ใหม่ได้เลย
**source of truth = โฟลเดอร์นี้บน GitHub** — แก้ที่นี่ที่เดียว project อื่นดึงไปใช้

```
_reusable/
├── CLAUDE.base.md         # กฎ generic (approval, review FE+BE, สไตล์) → ก๊อปไป root
├── settings.hook.json     # hook generic → ก๊อปเนื้อ hooks ไป .claude/settings.json
├── hooks/lint-changed.sh  # script: lint เฉพาะไฟล์ที่แก้ ตามนามสกุล → ก๊อปไป .claude/hooks/
├── skills/<name>/SKILL.md # คลัง skill (slash command) → ก๊อปไป .claude/skills/
├── INBOX.md               # ที่พักความรู้ใหม่รอกลั่น
└── README.md              # ไฟล์นี้
```

---

## เอาไปใช้กับ project ใหม่

### วิธี A — clone ทั้ง repo แล้วก๊อปเฉพาะโฟลเดอร์ (ง่ายสุด)
```bash
cd /tmp                       # ออกไปยืนที่ปลอดภัยก่อน (กัน rm ลบ dir ที่ตัวเองอยู่)
rm -rf /tmp/hub               # ลบของค้างรอบก่อนเสมอ — ไม่งั้น clone ลง dir ไม่ว่างไม่ได้ แล้วเผลอใช้ของเก่า
git clone https://github.com/patcharanut-bit/claude-reusable.git /tmp/hub
cp -r /tmp/hub/_reusable/CLAUDE.base.md   ./CLAUDE.md
mkdir -p .claude/hooks
cp -r /tmp/hub/_reusable/hooks/lint-changed.sh ./.claude/hooks/
# skills: ก๊อปทั้งโฟลเดอร์ (แต่ละ skill = <name>/SKILL.md)
mkdir -p .claude/skills && cp -r /tmp/hub/_reusable/skills/* ./.claude/skills/
# แล้วเปิด settings.hook.json ก๊อปเฉพาะ key "hooks" ไปใส่ .claude/settings.json (ลบ _comment)
rm -rf /tmp/hub
```

### วิธี B — ดึงเฉพาะโฟลเดอร์ _reusable (git sparse-checkout, ไม่โหลดทั้ง repo)
```bash
cd /tmp                       # ออกไปยืนที่ปลอดภัยก่อน (กัน rm ลบ dir ที่ตัวเองอยู่)
rm -rf /tmp/hub               # ลบของค้างรอบก่อนเสมอ — ไม่งั้น clone ไม่ลง แล้วเผลอ cd เข้าของเก่า นึกว่าดึงมาแล้ว
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/patcharanut-bit/claude-reusable.git /tmp/hub
git -C /tmp/hub sparse-checkout set _reusable   # ใช้ -C แทน cd เข้าไป จะได้ไม่ค้างอยู่ใน /tmp/hub หลังเสร็จ
# ได้เฉพาะ _reusable/ ที่ /tmp/hub/_reusable — ก๊อปไปใช้ตามวิธี A
```

---

## skills/ — คลัง slash command ที่ reuse ได้

แต่ละ skill = โฟลเดอร์ `<name>/SKILL.md` (มี YAML frontmatter: `name`, `description`)
`description` คือสิ่งที่ Claude ใช้ตัดสินว่าจะ trigger skill ไหน → เขียนให้ชัดว่า "ใช้เมื่อไร"

ตอนนี้มี:
- `commit-auto` — ดู staged changes → ร่าง commit message EN กระชับ → commit ให้เลย
- `commit-explain` — ดู staged changes → อธิบายเป็นไทยว่าเพิ่ม/ลด/แก้อะไร → ร่าง message EN **ไม่ commit** (ให้รีวิวเอง)
- `ui-parity-port` — port UI screen จาก reference เข้า Next.js + Tailwind frontend พร้อม verify computed styles ใน browser

> **source of truth = `_reusable/skills/` บน GitHub** — แก้ที่นี่ที่เดียว
> `.claude/skills/` บนเครื่อง = สำเนา local (อยู่ใต้ `.claude/` ที่ gitignore ไว้ → ไม่ขึ้น git)
> อยากให้ Claude app (claude.ai) เห็นด้วย ต้อง upload/sync เป็น custom skill ของบัญชีแยกต่างหาก

---

## checklist หลังก๊อปไป project ใหม่ (ต้องปรับให้เข้ากับ project)
- [ ] `CLAUDE.md` — เพิ่มส่วน project-specific: ชื่อ repo, port, วิธีรัน, งานค้าง
- [ ] `CLAUDE.md` — แก้ "บทบาท" ใส่ชื่อเจ้าของจริง
- [ ] ลบ review checklist ของภาษาที่ project นี้ไม่ใช้ (เช่นไม่มี Rust ก็ลบส่วน Rust)
- [ ] `.claude/skills/` — ก๊อป skill ที่ต้องใช้มาแล้ว (master อยู่ `_reusable/skills/`)
- [ ] `.claude/settings.json` — ตรวจว่า path hook ถูก, ลบ `_comment`
- [ ] `.gitignore` — เพิ่ม `.claude/` ถ้าไม่อยากให้ hook settings ขึ้น git
- [ ] restart Claude Code เพื่อโหลด hook

---

## เอาความรู้ใหม่กลับเข้าคลังกลาง (contribute back)

**ปัญหา:** ก๊อปไปแล้วแก้ที่ปลายทาง → git history ไม่เชื่อมกัน → ย้อนกลับด้วย merge ไม่ได้
**ทางแก้:** เอากลับด้วยการ copy เนื้อหา ไม่ใช่ git merge

flow ที่ใช้:
1. เจอของดี/ที่ต้องกังวลใน project อื่น → **จดลง `INBOX.md`** (บรรทัดเดียวก็พอ จากเครื่องไหนก็ได้ที่เปิด repo นี้)
2. พอว่าง → เปิดแชท project นี้ บอกว่า **"เคลียร์ INBOX"**
3. AI ช่วยกลั่นว่าของนั้น generic พอจะเข้า `CLAUDE.base.md` ไหม → เสนอ diff → approve → commit
4. ย้ายรายการที่กลั่นเสร็จไปท่อน log ล่างของ INBOX (เก็บที่มาไว้)

> ทำไมผ่าน INBOX ไม่แก้ base.md ตรง ๆ: INBOX = ของรอ review, base.md = ของผ่าน review แล้ว
> กันของ project-specific หลุดเข้าคลังกลาง และฝึกนิสัย reviewer
