---
name: commit-explain
description: ดู staged changes (git diff --cached) อธิบายเป็นภาษาไทยว่าแต่ละส่วนเพิ่ม/ลด/แก้อะไรและเพราะอะไร แล้วร่าง commit message ภาษาอังกฤษให้ โดยยังไม่ commit ให้ ใช้เมื่อผู้ใช้ขอให้ช่วยอธิบายและร่าง commit message
---

# commit-explain

อธิบาย staged changes เป็นภาษาไทย แล้วร่าง commit message ภาษาอังกฤษ **โดยไม่ commit ให้** ผู้ใช้จะรีวิวและ commit เอง

## ขอบเขต

- ดูเฉพาะไฟล์ที่ **staged ไว้แล้ว** (`git diff --cached`) เท่านั้น — ไฟล์ที่ยังไม่ stage ไม่ต้องสนใจ
- ถ้าทำงานกับ repo บนเครื่องผู้ใช้ผ่าน connected folder ให้ใช้ `device_bash` และ `cd` เข้า repo ก่อนทุกครั้ง

## ขั้นตอน

1. **เช็กว่ามีอะไร staged ไว้**
   ```
   git diff --cached --stat
   ```
   ถ้าว่างเปล่า → บอกผู้ใช้ว่ายังไม่มีไฟล์ staged (ยังไม่ `git add`) แล้วหยุด อย่าเดา

2. **อ่าน diff เต็ม**
   ```
   git diff --cached
   ```
   ถ้า diff ยาวมาก อ่านทีละไฟล์: `git diff --cached -- <path>`

3. **อธิบายเป็นภาษาไทย** ทีละไฟล์ (หรือจัดกลุ่มตามหัวข้อการเปลี่ยนแปลง) ว่า:
   - **เพิ่มอะไร** — โค้ด/ฟังก์ชัน/ไฟล์ใหม่
   - **ลบอะไร** — อะไรที่เอาออก
   - **แก้อะไร** — บรรทัดที่เปลี่ยนจากอะไรเป็นอะไร
   - **เพราะอะไร** — เหตุผล/ผลลัพธ์ของการเปลี่ยน อ้างจากสิ่งที่เห็นใน diff อย่าแต่งเหตุผลที่ไม่มีหลักฐาน ถ้าไม่แน่ใจเจตนาให้บอกตามตรง

4. **ร่าง commit message ภาษาอังกฤษ** ตาม Conventional Commits:
   - subject line: `type(scope): summary` (เช่น `fix(portal): ...`, `feat(auth): ...`) สั้น ≤ ~72 ตัวอักษร ขึ้นต้น imperative
   - type ที่ใช้: feat / fix / docs / style / refactor / perf / test / build / ci / chore
   - ถ้ามีหลายส่วน เพิ่ม body เป็น bullet อธิบายแต่ละการเปลี่ยน (ภาษาอังกฤษ)
   - อ้างอิง convention ที่ repo ใช้อยู่จาก `git log --oneline -10` ให้ message เข้ากับสไตล์เดิม

5. **ส่ง commit message ให้ในรูปแบบ code block** พร้อมคำสั่งที่ผู้ใช้ copy ไปรันเองได้ เช่น:
   ```
   git commit -m "..."
   ```

## สำคัญ

- **ห้าม commit ให้เด็ดขาด** — งานของ skill นี้จบที่การส่ง message ให้ผู้ใช้ตัดสินใจเอง
- อย่าแก้ไขไฟล์หรือ stage เพิ่ม
- commit message เป็นภาษาอังกฤษ, คำอธิบายเป็นภาษาไทย
