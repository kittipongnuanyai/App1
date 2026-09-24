import 'package:flutter/material.dart';

import '../data/app_state.dart';
import '../theme.dart';
import 'login_screen.dart';

/// หน้า 6 — โปรไฟล์
class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  void _logout(BuildContext context) {
    AppState.instance.logout();
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
      (route) => false,
    );
  }

  void _todo(BuildContext context, String name) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('หน้า "$name" จะเพิ่มในคาบถัดไป')),
    );
  }

  @override
  Widget build(BuildContext context) {
    final state = AppState.instance;
    final text = Theme.of(context).textTheme;
    return ListenableBuilder(
      listenable: state,
      builder: (context, _) {
        final user = state.currentUser;
        return Scaffold(
          appBar: AppBar(title: const Text('โปรไฟล์')),
          body: Column(
            children: [
              // ---------- ส่วนบน ----------
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 28),
                color: AppColors.indigo,
                child: Column(
                  children: [
                    const CircleAvatar(
                      radius: 44,
                      backgroundColor: Colors.white,
                      child: Icon(Icons.person, size: 52, color: AppColors.indigo),
                    ),
                    const SizedBox(height: 12),
                    Text(user?.name ?? '-',
                        style: text.titleLarge?.copyWith(color: Colors.white)),
                    const SizedBox(height: 4),
                    Text('${user?.roleLabel ?? '-'} · ${user?.studentId ?? '-'}',
                        style: text.bodyMedium?.copyWith(color: Colors.white70)),
                  ],
                ),
              ),
              // ---------- ส่วนกลาง: เมนู ----------
              ListTile(
                leading: const Icon(Icons.history, color: AppColors.indigo),
                title: const Text('ประวัติการยืมทั้งหมด'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _todo(context, 'ประวัติการยืมทั้งหมด'),
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.settings_outlined, color: AppColors.indigo),
                title: const Text('ตั้งค่า'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _todo(context, 'ตั้งค่า'),
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.info_outline, color: AppColors.indigo),
                title: const Text('เกี่ยวกับแอป'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => showAboutDialog(
                  context: context,
                  applicationName: 'LabStock',
                  applicationVersion: '1.0.0 (UI phase)',
                  applicationIcon: const Icon(Icons.inventory_2_outlined,
                      size: 40, color: AppColors.indigo),
                  children: const [
                    Text('แอปอ้างอิงวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่'),
                    Text('คลังอุปกรณ์แล็บ ICE'),
                  ],
                ),
              ),
              const Divider(height: 1),
              const Spacer(),
              // ---------- ส่วนล่าง ----------
              Padding(
                padding: const EdgeInsets.all(20),
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(backgroundColor: AppColors.danger),
                  onPressed: () => _logout(context),
                  icon: const Icon(Icons.logout),
                  label: const Text('ออกจากระบบ'),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
