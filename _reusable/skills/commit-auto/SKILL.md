---
name: commit-auto
description: ดู staged changes (git diff --cached) ร่าง commit message ภาษาอังกฤษแบบกระชับ (ไม่ต้องอธิบายรายละเอียด) แล้ว git commit ให้เลย ใช้เมื่อผู้ใช้ขอให้ commit staged changes ให้อัตโนมัติ
---

# commit-auto

ดู staged changes ร่าง commit message ภาษาอังกฤษ แล้ว **commit ให้เลย** โดยไม่ต้องอธิบายรายละเอียดการเปลี่ยนแปลง

## ขอบเขต

- ดูเฉพาะไฟล์ที่ **staged ไว้แล้ว** (`git diff --cached`) เท่านั้น — ไฟล์ที่ยังไม่ stage ไม่ต้องสนใจ และ**ห้าม `git add` เพิ่มเอง**
- ถ้าทำงานกับ repo บนเครื่องผู้ใช้ผ่าน connected folder ให้ใช้ `device_bash` และ `cd` เข้า repo ก่อนทุกครั้ง

## ขั้นตอน

1. **เช็กว่ามีอะไร staged ไว้**
   ```
   git diff --cached --stat
   ```
   ถ้าว่างเปล่า → บอกผู้ใช้ว่ายังไม่มีไฟล์ staged แล้วหยุด **อย่า commit empty**

2. **อ่าน diff เพื่อเข้าใจพอร่าง message**
   ```
   git diff --cached
   ```
   ดูพอให้สรุป type/scope/summary ได้ ไม่ต้องอธิบายให้ผู้ใช้ฟัง

3. **ร่าง commit message ภาษาอังกฤษ** แบบกระชับ ตาม Conventional Commits:
   - `type(scope): summary` ขึ้นต้น imperative ≤ ~72 ตัวอักษร
   - type: feat / fix / docs / style / refactor / perf / test / build / ci / chore
   - ถ้าเปลี่ยนหลายส่วนจริง ๆ ใส่ body bullet สั้น ๆ ได้ แต่โดยรวมเน้นกระชับ
   - ให้เข้ากับสไตล์เดิมจาก `git log --oneline -10`

4. **commit ให้เลย**
   ```
   git commit -m "type(scope): summary"
   ```
   (หลายบรรทัดใช้ `-m` ซ้ำสำหรับ body)

5. **ยืนยันผล** — รายงานสั้น ๆ ว่า commit แล้ว พร้อม hash:
   ```
   git log --oneline -1
   ```

## สำคัญ

- commit **เฉพาะสิ่งที่ staged อยู่** ไม่ `git add -A` / `git add .` เพิ่ม
- ไม่ push ให้ เว้นแต่ผู้ใช้สั่ง
- commit message เป็นภาษาอังกฤษ
- ถ้า commit ล้มเหลว (เช่น pre-commit hook ไม่ผ่าน) ให้รายงาน error ตามจริง อย่าพยายาม bypass hook
