---
name: figma-port
description: ใช้เมื่อพอร์ตหน้า/คอมโพเนนต์จาก Figma เข้า React Native (Expo) โดยต้องได้ค่า padding / spacing / สี / font ที่ designer ตั้งไว้จริง — ดึงผ่าน Figma REST API ไม่ใช่เดาจาก screenshot. (สำหรับ web Next.js+Tailwind ใช้ ui-parity-port แทน)
---

# figma-port — พอร์ต Figma → React Native ด้วยค่าจริง

เป้าหมาย: หน้าที่ build ออกมา spacing/สี/font **ตรงกับ Figma เป๊ะ** ไม่ใช่วัดเอาจากรูป
(screenshot ให้ได้แค่ "หน้าตา" — ค่า padding/gap จริงอยู่ใน node data ของ Figma)

## 1. แกะ file key + node id จาก URL ที่ผู้ใช้ส่ง

```
https://www.figma.com/design/<FILE_KEY>/<name>?node-id=<A>-<B>
```
- `FILE_KEY` = ส่วนหลัง `/design/`
- node id = `<A>-<B>` ใน query → ใช้กับ API เป็น `<A>:<B>` (ขีดกลาง → โคลอน)

## 2. ขอ Figma personal access token

บอกผู้ใช้สร้าง: figma.com → Settings → **Personal access tokens** → Generate
scope ที่พอ: **File content → Read-only**

- token เป็น **ความลับ** → ยิงแค่ `api.figma.com` เท่านั้น ห้ามส่งที่อื่น/ห้าม log/ห้าม commit
- เสร็จแล้วผู้ใช้ revoke ได้

## 3. ดึง node JSON (ค่า layout จริง)

```bash
curl -s -H "X-Figma-Token: $TOKEN" \
  "https://api.figma.com/v1/files/$FILE_KEY/nodes?ids=$NODE" -o node.json
```
field ที่สนใจ: `layoutMode` (auto-layout), `paddingTop/Right/Bottom/Left`, `itemSpacing` (gap),
`absoluteBoundingBox` (กล่อง layout), `absoluteRenderBounds` (กล่องที่วาดจริง — ต่างกัน = overflow),
`cornerRadius`, `fills[].color`, `strokes`, `style.fontSize/fontWeight/lineHeightPx`, `characters`

## 4. รัน parse script → ได้ตาราง spec

```bash
python3 -I parse_figma.py node.json
```
(`parse_figma.py` อยู่ข้างไฟล์นี้ — เดินทั้ง tree พิมพ์ type/ขนาด/auto-layout/padding/gap/สี/font/text)

## 5. ดึงภาพ render ยืนยัน

```bash
curl -s -H "X-Figma-Token: $TOKEN" \
  "https://api.figma.com/v1/images/$FILE_KEY?ids=$NODE&format=png&scale=3"
# → { "images": { "<NODE>": "<s3 url>" } } → curl url -o render.png → เปิดดู
```
export asset (โลโก้/ไอคอน vector): เรียก images endpoint ที่ node นั้นได้ PNG พื้นโปร่ง

## 6. map Figma → RN

- **หน่วย:** เฟรมมือถือ (กว้าง ~375–414) = points 1:1 กับ RN → ใช้เลขตรง ๆ
- **auto-layout** → `flex` + `gap` (RN รองรับ `gap`); `paddingX/Y` → padding; align → justify/align
- **overflow:** ถ้า `absoluteRenderBounds` ใหญ่กว่า `absoluteBoundingBox` (เช่นโลโก้ล้นกรอบ) → ทำ slot เท่า **bbox** (เพื่อให้ gap ถูก) แล้วให้รูป/เนื้อหาล้นออก (RN `overflow: visible` เป็น default)
- **สี** → เก็บเป็น semantic token (CSS var + tailwind) ไม่ฮาร์ดโค้ด hex — เผื่อ dark/light
- **font weight** → RN ไม่ synth bold จากฟอนต์ custom: แต่ละน้ำหนัก = คนละ family/ไฟล์
  - `@expo-google-fonts/*`: **import ttf จาก subpath** (`.../400Regular/Xxx_400Regular.ttf`) ไม่ใช่จาก package root — import จาก root ดึง ttf ทุกน้ำหนักเข้า bundle (บวมเป็น MB)

## 7. ข้อควรระวัง (review checklist)

- **ไม่วาดเอง:** status bar (เวลา/แบต/wifi) + home indicator = OS วาด → ใช้ `SafeAreaView` + `expo-status-bar`
- **ค่าตัวอย่างใน mockup** (เช่นอีเมล/จุดรหัสผ่านที่เห็น) = sample ไม่ใช่ UI ว่าง → ทำเป็น placeholder/`secureTextEntry` จริง
- **touch target ≥44pt** — ลิงก์/ปุ่มเล็กใช้ `hitSlop` ขยายพื้นที่แตะโดยไม่ขยับ layout
- ทำทีละชิ้น (token → i18n → ฟอนต์/asset → screen → route) เสนอ diff รอ approve ตาม working agreement
