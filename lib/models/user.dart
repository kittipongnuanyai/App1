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
}
