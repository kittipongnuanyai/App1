# LabStock — คลังอุปกรณ์แล็บ ICE

แอปอ้างอิงวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่ (เฟส UI ยังไม่ต่อฐานข้อมูล)

## รันแอป

```bash
flutter pub get
flutter run
```

ทดลองเข้าสู่ระบบ: ชื่อผู้ใช้ขึ้นต้นด้วย `admin` = บทบาทแอดมิน (เห็นปุ่ม + และปุ่มแก้ไข) · ชื่ออื่น = นักศึกษา

## โครงสร้างไฟล์

```
lib/
├─ main.dart                  จุดเริ่มต้น MaterialApp + ธีม
├─ theme.dart                 สีหลัก Indigo · รอง Sky · เน้น Amber
├─ models/
│  ├─ user.dart               ผู้ใช้ + บทบาท (student/admin)
│  ├─ equipment.dart          อุปกรณ์ + หมวดหมู่ (enum)
│  └─ borrow.dart             รายการยืม + คำนวณวันครบกำหนด
├─ data/
│  ├─ mock_data.dart          ข้อมูลจำลอง
│  └─ app_state.dart          สถานะรวมในหน่วยความจำ (ChangeNotifier)
├─ utils/thai_date.dart       แปลงวันที่เป็นข้อความไทย
├─ widgets/equipment_image.dart  รูปอุปกรณ์ / ไอคอนตามหมวด
└─ screens/
   ├─ login_screen.dart            หน้า 1 เข้าสู่ระบบ
   ├─ register_screen.dart         หน้าสมัครสมาชิก
   ├─ home_shell.dart              โครง BottomNavigationBar 3 เมนู
   ├─ equipment_list_screen.dart   หน้า 2 รายการอุปกรณ์
   ├─ equipment_detail_screen.dart หน้า 3 รายละเอียด + Dialog ยืม
   ├─ equipment_form_screen.dart   หน้า 4 เพิ่ม/แก้ไข (แอดมิน, image_picker)
   ├─ my_borrows_screen.dart       หน้า 5 การยืมของฉัน (TabBar)
   └─ profile_screen.dart          หน้า 6 โปรไฟล์ + ออกจากระบบ
```

## Navigation Map

```
Login ──(เข้าสำเร็จ)──> HomeShell (รายการ · การยืมของฉัน · โปรไฟล์)
รายการ ──(แตะการ์ด)──> รายละเอียด ──(ปุ่มยืม)──> Dialog ──> บันทึก borrow ──> กลับ
รายการ ──(ปุ่ม + แอดมิน)──> เพิ่มอุปกรณ์     รายละเอียด ──(ดินสอ แอดมิน)──> แก้ไข
การยืมของฉัน ──(คืนของ)──> อัปเดต return_date + คืนจำนวน
โปรไฟล์ ──(ออกจากระบบ)──> Login
```

## ขั้นถัดไป (คาบต่อ ๆ ไป)

แทนที่ `AppState` ด้วยการเรียก REST API ที่ต่อ MySQL — หน้าจอทั้งหมดอ่านข้อมูลผ่าน `AppState.instance` อยู่แล้ว จึงเปลี่ยนแค่ชั้นข้อมูล
