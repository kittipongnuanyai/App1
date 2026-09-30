import 'package:flutter/foundation.dart';

import '../models/borrow.dart';
import '../models/equipment.dart';
import '../models/user.dart';
import 'api_service.dart';

/// สถานะรวมของแอป — เฟส 2: ข้อมูลทุกอย่างมาจาก API/MySQL ผ่าน [ApiService]
/// หน้าจอยังเรียกเมธอดชื่อเดิม แต่ตอนนี้เป็น Future (ต้อง await)
class AppState extends ChangeNotifier {
  AppState._();
  static final AppState instance = AppState._();

  /// ตัวคุยกับเซิร์ฟเวอร์ — เปลี่ยนเป็นตัวปลอมได้ตอนทดสอบ
  ApiService api = ApiService();

  AppUser? _currentUser;
  List<Equipment> _equipment = [];
  List<Borrow> _borrows = [];

  bool isLoading = false;
  String? error;

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
  /// เข้าสู่ระบบผ่าน API แล้วโหลดข้อมูลทั้งหมด (โยน ApiException ถ้าไม่สำเร็จ)
  Future<void> login(String username, String password) async {
    _currentUser = await api.login(username.trim(), password);
    notifyListeners();
    await refresh();
  }

  Future<void> register({
    required String username,
    required String password,
    required String name,
    required String studentId,
  }) async {
    await api.register(
      username: username.trim(),
      password: password,
      name: name.trim(),
      studentId: studentId.trim(),
    );
  }

  void logout() {
    _currentUser = null;
    _equipment = [];
    _borrows = [];
    notifyListeners();
  }

  // ---------- โหลดข้อมูลจากเซิร์ฟเวอร์ ----------
  /// ดึงอุปกรณ์ + รายการยืมของผู้ใช้ปัจจุบันใหม่ทั้งหมด (ใช้หลังทุกการเปลี่ยนแปลง)
  Future<void> refresh() async {
    isLoading = true;
    error = null;
    notifyListeners();
    try {
      _equipment = await api.getItems();
      final user = _currentUser;
      _borrows = user == null ? [] : await api.getBorrows(user.id);
    } on ApiException catch (e) {
      error = e.message;
    } finally {
      isLoading = false;
      notifyListeners();
    }
  }

  // ---------- Equipment ----------
  Equipment? findEquipment(String id) {
    for (final e in _equipment) {
      if (e.id == id) return e;
    }
    return null;
  }

  Future<void> addEquipment(Equipment item) async {
    await api.createItem(item);
    await refresh();
  }

  Future<void> updateEquipment(Equipment item) async {
    await api.updateItem(item);
    await refresh();
  }

  // ---------- Borrow / Return ----------
  Future<void> borrow(Equipment item, int quantity, DateTime dueDate) async {
    final user = _currentUser;
    if (user == null) throw ApiException('กรุณาเข้าสู่ระบบก่อน');
    await api.borrow(
      userId: user.id,
      itemId: item.id,
      quantity: quantity,
      dueDate: dueDate,
    );
    await refresh();
  }

  Future<void> returnItem(Borrow b) async {
    await api.returnItem(b.id);
    await refresh();
  }
}
