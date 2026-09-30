import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:labstock/data/api_service.dart';
import 'package:labstock/data/app_state.dart';
import 'package:labstock/data/mock_data.dart';
import 'package:labstock/main.dart';
import 'package:labstock/models/borrow.dart';
import 'package:labstock/models/equipment.dart';
import 'package:labstock/models/user.dart';

/// API ปลอมสำหรับทดสอบ — ใช้ข้อมูลจำลองจากเฟส 1 ไม่ต้องมีเซิร์ฟเวอร์จริง
class FakeApiService extends ApiService {
  final List<Equipment> items = MockData.equipment();
  final List<Borrow> borrows = MockData.borrows();

  @override
  Future<AppUser> login(String username, String password) async {
    if (password != '1234') throw ApiException('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 401);
    return username == 'admin' ? MockData.admin : MockData.student;
  }

  @override
  Future<List<Equipment>> getItems() async => items;

  @override
  Future<List<Borrow>> getBorrows(String userId) async => borrows;
}

void main() {
  setUp(() {
    AppState.instance.api = FakeApiService();
    AppState.instance.logout();
  });

  Future<void> login(WidgetTester tester, String user, String pass) async {
    await tester.pumpWidget(const LabStockApp());
    await tester.enterText(find.byType(TextField).first, user);
    await tester.enterText(find.byType(TextField).last, pass);
    await tester.tap(find.widgetWithText(ElevatedButton, 'เข้าสู่ระบบ'));
    await tester.pumpAndSettle();
  }

  testWidgets('login as student then navigate tabs', (tester) async {
    await login(tester, 'somchai', '1234');

    // หน้ารายการ: นักศึกษาไม่เห็นปุ่ม +
    expect(find.text('Arduino UNO R3'), findsOneWidget);
    expect(find.byType(FloatingActionButton), findsNothing);
    expect(find.text('ยืมไม่ได้'), findsOneWidget); // DHT22 เหลือ 0

    await tester.tap(find.text('การยืมของฉัน'));
    await tester.pumpAndSettle();
    expect(find.textContaining('อีก 2 วันครบกำหนด'), findsOneWidget);

    await tester.tap(find.text('โปรไฟล์'));
    await tester.pumpAndSettle();
    expect(find.text('สมชาย ใจดี'), findsOneWidget);
    await tester.tap(find.text('ออกจากระบบ'));
    await tester.pumpAndSettle();
    expect(find.text('เข้าสู่ระบบ'), findsOneWidget);
  });

  testWidgets('admin sees add button', (tester) async {
    await login(tester, 'admin', '1234');
    expect(find.byType(FloatingActionButton), findsOneWidget);
  });

  testWidgets('wrong password shows error from API', (tester) async {
    await login(tester, 'somchai', 'wrong');
    expect(find.text('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'), findsOneWidget);
    expect(find.byType(FloatingActionButton), findsNothing);
  });
}
