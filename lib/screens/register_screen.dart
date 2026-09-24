import 'package:flutter/material.dart';

/// หน้าสมัครสมาชิก (ฟอร์มคล้ายหน้า Login)
class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _obscure = true;

  void _submit() {
    if (!_formKey.currentState!.validate()) return;
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('สมัครสมาชิกสำเร็จ (จำลอง) — กรุณาเข้าสู่ระบบ')),
    );
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('สมัครสมาชิก  ')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                decoration: const InputDecoration(
                  labelText: 'ชื่อ-นามสกุล',
                  prefixIcon: Icon(Icons.badge_outlined),
                ),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'กรุณากรอกชื่อ' : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'รหัสนักศึกษา',
                  prefixIcon: Icon(Icons.numbers),
                ),
                validator: (v) => (v == null || v.trim().length < 9)
                    ? 'รหัสนักศึกษาต้องมีอย่างน้อย 9 หลัก'
                    : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                keyboardType: TextInputType.emailAddress,
                decoration: const InputDecoration(
                  labelText: 'อีเมล',
                  prefixIcon: Icon(Icons.email_outlined),
                ),
                validator: (v) => (v == null || !v.contains('@'))
                    ? 'รูปแบบอีเมลไม่ถูกต้อง'
                    : null,
              ),
              const SizedBox(height: 14),
              TextFormField(
                obscureText: _obscure,
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
                validator: (v) => (v == null || v.length < 6)
                    ? 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'
                    : null,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submit,
                child: const Text('สมัครสมาชิก'),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('มีบัญชีแล้ว? เข้าสู่ระบบ'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
