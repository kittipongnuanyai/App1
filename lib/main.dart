import 'package:flutter/material.dart';

import 'screens/login_screen.dart';
import 'theme.dart';

void main() {
  runApp(const LabStockApp());
}

/// LabStock — คลังอุปกรณ์แล็บ ICE
/// แอปอ้างอิงวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่
class LabStockApp extends StatelessWidget {
  const LabStockApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LabStock',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const LoginScreen(),
    );
  }
}
