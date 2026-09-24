import '../models/borrow.dart';
import '../models/equipment.dart';
import '../models/user.dart';

/// ข้อมูลจำลองสำหรับเฟส UI (ยังไม่ต่อฐานข้อมูล)
class MockData {
  static const student = AppUser(
    id: 'u1',
    name: 'สมชาย ใจดี',
    studentId: '674659001',
    role: UserRole.student,
  );

  static const admin = AppUser(
    id: 'u0',
    name: 'อ.สมหญิง แล็บดี',
    studentId: 'ICE-ADMIN',
    role: UserRole.admin,
  );

  static List<Equipment> equipment() => [
        Equipment(
          id: 'e1',
          name: 'Arduino UNO R3',
          category: EquipmentCategory.board,
          total: 10,
          available: 5,
          description:
              'บอร์ดไมโครคอนโทรลเลอร์ ATmega328P ใช้สำหรับเรียนพื้นฐาน Embedded และ IoT รองรับการเขียนโปรแกรมผ่าน Arduino IDE',
        ),
        Equipment(
          id: 'e2',
          name: 'DHT22',
          category: EquipmentCategory.sensor,
          total: 6,
          available: 0,
          description:
              'เซนเซอร์วัดอุณหภูมิและความชื้นแบบดิจิทัล ความแม่นยำสูงกว่า DHT11',
        ),
        Equipment(
          id: 'e3',
          name: 'สาย USB Type-B',
          category: EquipmentCategory.cable,
          total: 15,
          available: 12,
          description: 'สาย USB A-to-B ยาว 1 เมตร สำหรับต่อบอร์ด Arduino UNO',
        ),
        Equipment(
          id: 'e4',
          name: 'Servo SG90',
          category: EquipmentCategory.module,
          total: 8,
          available: 3,
          description: 'เซอร์โวมอเตอร์ขนาดเล็ก หมุนได้ 0–180 องศา แรงบิด 1.8 kg·cm',
        ),
        Equipment(
          id: 'e5',
          name: 'ESP32 DevKit',
          category: EquipmentCategory.board,
          total: 12,
          available: 7,
          description:
              'บอร์ดไมโครคอนโทรลเลอร์ที่มี Wi-Fi และ Bluetooth ในตัว เหมาะกับงาน IoT',
        ),
        Equipment(
          id: 'e6',
          name: 'Ultrasonic HC-SR04',
          category: EquipmentCategory.sensor,
          total: 10,
          available: 9,
          description: 'เซนเซอร์วัดระยะทางด้วยคลื่นอัลตราโซนิก ระยะ 2–400 ซม.',
        ),
        Equipment(
          id: 'e7',
          name: 'สาย Jumper (ชุด 40 เส้น)',
          category: EquipmentCategory.cable,
          total: 20,
          available: 14,
          description: 'สายจั๊มเปอร์ ผู้-ผู้ ยาว 20 ซม. ชุดละ 40 เส้น',
        ),
        Equipment(
          id: 'e8',
          name: 'มัลติมิเตอร์ดิจิทัล',
          category: EquipmentCategory.tool,
          total: 5,
          available: 2,
          description: 'เครื่องวัดแรงดัน กระแส และความต้านทาน แบบดิจิทัล',
        ),
      ];

  static List<Borrow> borrows() {
    final now = DateTime.now();
    DateTime d(int offset) => DateTime(now.year, now.month, now.day + offset);
    return [
      Borrow(
        id: 'b1',
        equipmentId: 'e1',
        equipmentName: 'Arduino UNO R3',
        quantity: 1,
        borrowDate: d(-5),
        dueDate: d(2),
      ),
      Borrow(
        id: 'b2',
        equipmentId: 'e4',
        equipmentName: 'Servo SG90',
        quantity: 2,
        borrowDate: d(-2),
        dueDate: d(5),
      ),
      Borrow(
        id: 'b3',
        equipmentId: 'e3',
        equipmentName: 'สาย USB Type-B',
        quantity: 1,
        borrowDate: d(-20),
        dueDate: d(-13),
        returnDate: d(-14),
      ),
      Borrow(
        id: 'b4',
        equipmentId: 'e6',
        equipmentName: 'Ultrasonic HC-SR04',
        quantity: 1,
        borrowDate: d(-30),
        dueDate: d(-23),
        returnDate: d(-23),
      ),
    ];
  }
}
