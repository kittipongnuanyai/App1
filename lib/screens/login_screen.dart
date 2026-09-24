import 'package:flutter/material.dart';

import '../data/app_state.dart';
import '../theme.dart';
import 'home_shell.dart';
import 'register_screen.dart';

/// หน้า 1 — เข้าสู่ระบบ
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _userCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  bool _obscure = true;

  @override
  void dispose() {
    _userCtrl.dispose();
    _passCtrl.dispose();
    super.dispose();
  }

  void _login() {
    final ok = AppState.instance.login(_userCtrl.text, _passCtrl.text);
    if (!ok) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('กรุณากรอกอีเมล/ชื่อผู้ใช้ และรหัสผ่าน')),
      );
      return;
    }
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const HomeShell()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 24),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 420),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // ---------- ส่วนบน: โลโก้ + ชื่อแอป ----------
                  Center(
                    child: Container(
                      width: 96,
                      height: 96,
                      alignment: Alignment.center,
                      decoration: BoxDecoration(
                        color: AppColors.indigo,
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: const Icon(Icons.inventory_2_outlined,
                          size: 52, color: Colors.white),
                    ),
                  ),
                  Text('LabStock',
                      textAlign: TextAlign.center,
                      style: text.headlineSmall?.copyWith(
                          fontSize: 32, color: AppColors.indigo)),
                  Text('คลังอุปกรณ์แล็บ ICE',
                      textAlign: TextAlign.center,
                      style: text.bodyLarge?.copyWith(color: Colors.grey[600])),
                  const SizedBox(height: 32),

                  // ---------- ส่วนกลาง: ฟอร์ม ----------
                  TextField(
                    controller: _userCtrl,
                    keyboardType: TextInputType.emailAddress,
                    textInputAction: TextInputAction.next,
                    decoration: const InputDecoration(
                      labelText: 'อีเมล/ชื่อผู้ใช้',
                      prefixIcon: Icon(Icons.person_outline),
                    ),
                  ),
                  const SizedBox(height: 14),
                  TextField(
                    controller: _passCtrl,
                    obscureText: _obscure,
                    textInputAction: TextInputAction.done,
                    onSubmitted: (_) => _login(),
                    decoration: InputDecoration(
                      labelText: 'รหัสผ่าน',
                      prefixIcon: const Icon(Icons.lock_outline),
                      suffixIcon: IconButton(
                        icon: Icon(_obscure
                            ? Icons.visibility_outlined
                            : Icons.visibility_off_outlined),
                        onPressed: () => setState(() => _obscure = !_obscure),
                      ),
                    ),
                  ),
                  const SizedBox(height: 22),
                  ElevatedButton(
                    onPressed: _login,
                    child: const Text('เข้าสู่ระบบ'),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'ทดลอง: ชื่อผู้ใช้ขึ้นต้นด้วย "admin" = แอดมิน · อื่น ๆ = นักศึกษา',
                    textAlign: TextAlign.center,
                    style: text.bodySmall?.copyWith(color: Colors.grey),
                  ),
                  const SizedBox(height: 24),

                  // ---------- ส่วนล่าง: ลิงก์สมัคร ----------
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text('ยังไม่มีบัญชี?'),
                      TextButton(
                        onPressed: () => Navigator.of(context).push(
                          MaterialPageRoute(
                              builder: (_) => const RegisterScreen()),
                        ),
                        child: const Text('สมัครสมาชิก'),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
