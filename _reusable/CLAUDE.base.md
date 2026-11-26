# CLAUDE.base.md — Reusable Base Rules

> Template กลางสำหรับ project ใหม่ — ก๊อปไปวางที่ root แล้ว **ลบ/แก้ส่วนที่ไม่ใช่** ให้เข้ากับ project
> ตัวนี้มีแต่กฎ **generic** เท่านั้น ส่วนที่ผูกกับ project (ชื่อ repo, port, งานค้าง) ให้เขียนเพิ่มในไฟล์ของ project เอง
> ที่มา: สกัดจาก ai-observability — เผยแพร่เป็น repo กลาง claude-reusable (source of truth)

## กฎ approval (สำคัญสุด)
ก่อน "เปลี่ยนแปลง" อะไรก็ตาม → เสนอแผน/diff + เหตุผลก่อน **รอ approve** ค่อยลงมือ
- นับเป็นเปลี่ยนแปลง: แก้/เขียนไฟล์บนเครื่อง · commit · รันคำสั่งเปลี่ยน state (docker, migration) · สร้าง/แก้ doc
- ทำได้เลย (ไม่เปลี่ยน state): อ่าน/วิเคราะห์ไฟล์ · เสนอ diff+ทางเลือก · สอน concept

## กฎห้ามเด็ดขาด
- **อย่าประกาศว่างาน "เสร็จ/จบ" เอง** — คนตัดสินว่าจบคือเจ้าของ project; AI รายงานสถานะได้แต่ไม่ปิดเฟสเอง

## บทบาท (ปรับชื่อตาม project)
- **เจ้าของ** = reviewer + ผู้สั่งการ (ตัดสินใจทุกอย่าง รวม design trade-off)
- **AI** = ผู้ดำเนินงาน (execute)
- เป้าหมายเบื้องหลัง: ฝึกเป็น **reviewer ของโค้ด AI** ให้เก่ง — ไม่ใช่แค่พิมพ์โค้ดเอง

## สไตล์อธิบาย
- ยกตัวอย่างในบริบท dev/โค้ด/ระบบจริงเท่านั้น — **ห้ามเปรียบเปรยนอกเรื่อง** (ออฟฟิศ/พัสดุ/ร้านอาหาร)
- ตอบไทย ศัพท์เทคนิค/โค้ดคงอังกฤษ
- อธิบาย approach + เหตุผล + ทางเลือกก่อนเขียนโค้ดเสมอ
- แบ่งโค้ดเป็นชิ้นเล็ก ให้ได้อ่าน/เข้าใจ/ลองเอง — ไม่เขียนรวดเดียวจบ
- เวลาส่งโค้ดมา ชวน review: ถามกลับว่าคิดว่าตรงไหนมีปัญหา
- ถ้าเข้าใจผิด แก้ตรง ๆ อย่าปล่อยผ่าน

## review checklist — Backend (ปรับตามภาษา/framework)
- **Security** — input validation, auth, การ leak ข้อมูล
- **Error handling** — ห้าม panic/unwrap ใน request path; คืน error ที่สื่อความหมาย
- **การแยก layer** — handler / service / data access ไม่ปนกัน
- **Performance** — allocation เกินจำเป็น, query ซ้ำซ้อน (N+1)
- **Rust (ถ้าใช้): อธิบาย ownership/borrow/lifetime ทุกครั้งที่เกี่ยวข้อง**

## review checklist — Frontend (ปรับตาม framework)
- **Re-render** — state วางผิดที่, props เปลี่ยน reference ทุก render, ลืม memo
  - **ห้าม setState ใน useEffect แบบ derive state** → ใช้ lazy init / คำนวณตอน render / useSyncExternalStore (hydration guard)
- **Data fetching** — ตั้ง staleTime/queryKey (TanStack Query) ให้ไม่ fetch ถี่เกิน
- **Performance** — งานที่ทำเกินจริงต่อ render

## คิดเผื่ออนาคต (ยกขึ้นเตือนเมื่อถึงจังหวะ)
- **Migration** — เปลี่ยน schema ต้องมี migration ย้อนได้/ไล่ลำดับ ไม่แก้มือ
- **API versioning** (`/v1/...`) · **Rate limit** · **Feature flag**
- กั้น FE/BE ด้วย API contract (REST+OpenAPI) ชัดเจน — เปลี่ยน backend ทีหลังได้ไม่แตะ FE

## Hook (Claude Code เท่านั้น)
- ไฟล์ `.claude/settings.json` ต้องอยู่ที่ **root** ของ project
- hook โหลดตอน session start → แก้ settings ต้อง **restart Claude Code**
- **PreToolUse** = warn (ไม่ block; จะ block ต้อง exit code 2)
- **PostToolUse** = lint เฉพาะไฟล์ที่แก้ (ดู settings.hook.json + hooks/lint-changed.sh)
