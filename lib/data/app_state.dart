import 'package:flutter/foundation.dart';

import '../models/borrow.dart';
import '../models/equipment.dart';
import '../models/user.dart';
import 'mock_data.dart';

/// สถานะรวมของแอป (เก็บในหน่วยความจำ) — ในคาบถัดไปจะเปลี่ยนไปเรียก API/MySQL แทน
class AppState extends ChangeNotifier {
  AppState._();
  static final AppState instance = AppState._();

  AppUser? _currentUser;
  final List<Equipment> _equipment = MockData.equipment();
  final List<Borrow> _borrows = MockData.borrows();

  AppUser? get currentUser => _currentUser;
  bool get isAdmin => _currentUser?.isAdmin ?? false;
  List<Equipment> get equipment => List.unmodifiable(_equipment);
  List<Borrow> get borrows => List.unmodifiable(_borrows);

  List<Borrow> get activeBorrows =>
      _borrows.where((b) => !b.isReturned).toList()
        ..sort((a, b) => a.dueDate.compareTo(b.dueDate));

  List<Borrow> get borrowHistory =>
      _borrows.where((b) => b.isReturned).toList()
        ..sort((a, b) => b.returnDate!.compareTo(a.returnDate!));

  // ---------- Auth ----------
  /// จำลองการเข้าสู่ระบบ: ถ้าชื่อผู้ใช้ขึ้นต้นด้วย "admin" จะได้บทบาทแอดมิน
  bool login(String username, String password) {
    if (username.trim().isEmpty || password.isEmpty) return false;
    _currentUser =
        username.trim().toLowerCase().startsWith('admin')
            ? MockData.admin
            : MockData.student;
    notifyListeners();
    return true;
  }

  void logout() {
    _currentUser = null;
    notifyListeners();
  }

  // ---------- Equipment ----------
  Equipment? findEquipment(String id) {
    for (final e in _equipment) {
      if (e.id == id) return e;
    }
    return null;
  }

  void addEquipment(Equipment item) {
    _equipment.add(item);
    notifyListeners();
  }

  void updateEquipment(Equipment item) {
    final i = _equipment.indexWhere((e) => e.id == item.id);
    if (i != -1) _equipment[i] = item;
    notifyListeners();
  }

  // ---------- Borrow / Return ----------
  bool borrow(Equipment item, int quantity, DateTime dueDate) {
    if (quantity <= 0 || quantity > item.available) return false;
    item.available -= quantity;
    _borrows.add(
      Borrow(
        id: 'b${DateTime.now().millisecondsSinceEpoch}',
        equipmentId: item.id,
        equipmentName: item.name,
        quantity: quantity,
        borrowDate: DateTime.now(),
        dueDate: dueDate,
      ),
    );
    notifyListeners();
    return true;
  }

  void returnItem(Borrow b) {
    if (b.isReturned) return;
    b.returnDate = DateTime.now();
    final item = findEquipment(b.equipmentId);
    if (item != null) {
      item.available = (item.available + b.quantity).clamp(0, item.total);
    }
    notifyListeners();
  }
}
