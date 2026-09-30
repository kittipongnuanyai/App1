enum UserRole { student, admin }

class AppUser {
  final String id;
  final String name;
  final String studentId; // รหัสนักศึกษา หรือรหัสพนักงาน
  final UserRole role;

  const AppUser({
    required this.id,
    required this.name,
    required this.studentId,
    required this.role,
  });

  bool get isAdmin => role == UserRole.admin;
  String get roleLabel => isAdmin ? 'แอดมิน' : 'นักศึกษา';

  /// แปลงจาก JSON ที่ API ส่งมา (ตาราง users)
  factory AppUser.fromJson(Map<String, dynamic> json) => AppUser(
        id: '${json['id']}',
        name: json['name'] as String,
        studentId: json['student_id'] as String,
        role: json['role'] == 'admin' ? UserRole.admin : UserRole.student,
      );
}
