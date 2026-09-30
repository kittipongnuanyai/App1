# LabStock — คลังอุปกรณ์แล็บ ICE

แอปอ้างอิงวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่

| เฟส | เนื้อหา | จุดในรีโป | คู่มือ |
|---|---|---|---|
| 1 | UI 6 หน้า + การนำทาง (ข้อมูลจำลอง) | tag `phase1-ui` | `docs/LabStock-คู่มือปฏิบัติการ.pdf` (Step 0–11) |
| 2 | ต่อ MySQL ผ่าน REST API (PHP) | tag `phase2-mysql` | `docs/LabStock-คู่มือเฟส2-MySQL.pdf` (Step 12–17) |

ดูความต่างระหว่างสองเฟส: https://github.com/kittipongnuanyai/App1/compare/phase1-ui...phase2-mysql

## สำหรับนักศึกษา: เริ่มจากจุดเดียวกัน

```bash
git clone https://github.com/kittipongnuanyai/App1.git labstock
cd labstock
git checkout phase1-ui     # โค้ดจบเฟส 1 (หรือ phase2-mysql = จบเฟส 2)
flutter pub get
flutter run
```

ไม่ใช้ git ก็ได้: หน้า GitHub → Code → Download ZIP (หรือเลือก tag ก่อนดาวน์โหลด)

## รันเฟส 2 (ต้องมี XAMPP)

1. Start Apache + MySQL ใน XAMPP
2. phpMyAdmin → Import `server/labstock.sql`
3. คัดลอก `server/api/` ไปไว้ที่ `htdocs/labstock/api/` แล้วเปิด http://localhost/labstock/api/index.php ต้องได้ JSON
4. ตั้ง URL ใน `lib/data/api_config.dart` (`kApiBase`) ให้ตรงกับเครื่อง/อุปกรณ์ที่ใช้ แล้ว `flutter run`

บัญชีทดสอบ: `admin` / `1234` (แอดมิน) · `somchai` / `1234` (นักศึกษา)

> โฮสต์ฟรี InfinityFree ใช้กับแอปมือถือไม่ได้ (มีระบบตรวจเบราว์เซอร์บล็อกคำขอจากแอป) ดูทางเลือกใน Step 17 ของคู่มือเฟส 2

## โครงสร้างไฟล์

```
lib/
├─ main.dart                  จุดเริ่มต้น MaterialApp + ธีม
├─ theme.dart                 สีหลัก Indigo · รอง Sky · เน้น Amber
├─ models/                    AppUser · Equipment · Borrow (+ fromJson/toJson)
├─ data/
│  ├─ api_config.dart         URL ของ API (แก้ที่เดียว)
│  ├─ api_service.dart        เรียก API ทุก endpoint (http + JSON)
│  ├─ app_state.dart          สถานะรวม (ChangeNotifier) เรียก ApiService
│  └─ mock_data.dart          ข้อมูลจำลอง (ใช้ในเทสต์)
├─ utils/thai_date.dart       แปลงวันที่เป็นข้อความไทย
├─ widgets/equipment_image.dart
└─ screens/                   login · register · home_shell · list · detail · form · my_borrows · profile
server/
├─ labstock.sql               โครงสร้าง 3 ตาราง + ข้อมูลเริ่มต้น
└─ api/                       PHP: config · db · index · login · register · items · borrows
test/widget_test.dart         ทดสอบด้วย FakeApiService (ไม่ต้องมีเซิร์ฟเวอร์)
docs/                         คู่มือ PDF, สไลด์, สคริปต์สร้างเอกสาร
```

## API

| Method | Endpoint | ส่ง | ได้ |
|---|---|---|---|
| POST | `login.php` | `{username, password}` | user |
| POST | `register.php` | `{username, password, name, student_id}` | user |
| GET | `items.php` / `items.php?id=` | – | items / item |
| POST | `items.php` | `{name, category, total, description}` | item |
| PUT | `items.php` | `{id, name, category, total, description}` | item |
| GET | `borrows.php?user_id=` | – | borrows |
| POST | `borrows.php` | `{user_id, item_id, quantity, due_date}` | borrow |
| PUT | `borrows.php` | `{id}` | borrow (คืนแล้ว) |

ทุกคำตอบอยู่ในรูป `{"ok": true, "data": ...}` หรือ `{"ok": false, "error": "..."}`
