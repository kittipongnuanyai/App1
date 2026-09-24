import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:labstock/main.dart';

void main() {
  testWidgets('login as student then navigate tabs', (tester) async {
    await tester.pumpWidget(const LabStockApp());
    expect(find.text('LabStock'), findsOneWidget);
    expect(find.text('คลังอุปกรณ์แล็บ ICE'), findsOneWidget);

    await tester.enterText(find.byType(TextField).first, 'somchai');
    await tester.enterText(find.byType(TextField).last, '123456');
    await tester.tap(find.widgetWithText(ElevatedButton, 'เข้าสู่ระบบ'));
    await tester.pumpAndSettle();

    // หน้ารายการ: นักศึกษาไม่เห็นปุ่ม +
    expect(find.text('Arduino UNO R3'), findsOneWidget);
    expect(find.byType(FloatingActionButton), findsNothing);
    expect(find.text('ยืมไม่ได้'), findsOneWidget); // DHT22 เหลือ 0

    // ไปแท็บการยืม
    await tester.tap(find.text('การยืมของฉัน'));
    await tester.pumpAndSettle();
    expect(find.text('กำลังยืม'), findsOneWidget);
    expect(find.textContaining('อีก 2 วันครบกำหนด'), findsOneWidget);

    // ไปโปรไฟล์ แล้วออกจากระบบ
    await tester.tap(find.text('โปรไฟล์'));
    await tester.pumpAndSettle();
    expect(find.text('สมชาย ใจดี'), findsOneWidget);
    await tester.tap(find.text('ออกจากระบบ'));
    await tester.pumpAndSettle();
    expect(find.text('เข้าสู่ระบบ'), findsOneWidget);
  });

  testWidgets('admin sees add button', (tester) async {
    await tester.pumpWidget(const LabStockApp());
    await tester.enterText(find.byType(TextField).first, 'admin');
    await tester.enterText(find.byType(TextField).last, 'x');
    await tester.tap(find.widgetWithText(ElevatedButton, 'เข้าสู่ระบบ'));
    await tester.pumpAndSettle();
    expect(find.byType(FloatingActionButton), findsOneWidget);
  });
}
