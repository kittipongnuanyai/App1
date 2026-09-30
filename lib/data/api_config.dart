import 'package:flutter/foundation.dart';

/// ============================================================
///  ที่อยู่ของ API — แก้ค่านี้ค่าเดียว
/// ============================================================
///
///  XAMPP ในเครื่องตัวเอง (โฟลเดอร์ htdocs/labstock/api):
///     'http://localhost/labstock/api'
///
///  มือถือจริงต่อ Wi-Fi วงเดียวกับคอม (ดู IP จาก ipconfig / ifconfig):
///     'http://192.168.1.23/labstock/api'
///
///  โฮสต์จริง (เช่น AlwaysData):
///     'https://ชื่อบัญชี.alwaysdata.net/api'
///
const String kApiBase = 'http://localhost/labstock/api';

/// Android Emulator มองเครื่องคอมของเราเป็น 10.0.2.2 ไม่ใช่ localhost
/// ฟังก์ชันนี้แปลงให้อัตโนมัติ ส่วนแพลตฟอร์มอื่นใช้ค่าตรง ๆ
String get apiBase {
  if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
    return kApiBase.replaceFirst('localhost', '10.0.2.2');
  }
  return kApiBase;
}
