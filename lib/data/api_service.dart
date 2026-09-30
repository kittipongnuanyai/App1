import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/borrow.dart';
import '../models/equipment.dart';
import '../models/user.dart';
import 'api_config.dart';

/// ข้อผิดพลาดจาก API — ข้อความพร้อมแสดงให้ผู้ใช้เห็นได้เลย
class ApiException implements Exception {
  final String message;
  final int status;
  ApiException(this.message, [this.status = 0]);

  @override
  String toString() => message;
}

/// ชั้นเดียวที่คุยกับเซิร์ฟเวอร์ — หน้าจอไม่เรียกไฟล์นี้โดยตรง แต่เรียกผ่าน AppState
class ApiService {
  final http.Client _client;
  ApiService([http.Client? client]) : _client = client ?? http.Client();

  // ---------- Auth ----------
  Future<AppUser> login(String username, String password) async {
    final data = await _send('POST', 'login.php',
        body: {'username': username, 'password': password});
    return AppUser.fromJson(data);
  }

  Future<AppUser> register({
    required String username,
    required String password,
    required String name,
    required String studentId,
  }) async {
    final data = await _send('POST', 'register.php', body: {
      'username': username,
      'password': password,
      'name': name,
      'student_id': studentId,
    });
    return AppUser.fromJson(data);
  }

  // ---------- Items ----------
  Future<List<Equipment>> getItems() async {
    final data = await _send('GET', 'items.php') as List;
    return data.map((e) => Equipment.fromJson(e)).toList();
  }

  Future<Equipment> createItem(Equipment item) async {
    final data = await _send('POST', 'items.php', body: item.toJson());
    return Equipment.fromJson(data);
  }

  Future<Equipment> updateItem(Equipment item) async {
    final data = await _send('PUT', 'items.php', body: item.toJson());
    return Equipment.fromJson(data);
  }

  // ---------- Borrows ----------
  Future<List<Borrow>> getBorrows(String userId) async {
    final data =
        await _send('GET', 'borrows.php', query: {'user_id': userId}) as List;
    return data.map((e) => Borrow.fromJson(e)).toList();
  }

  Future<Borrow> borrow({
    required String userId,
    required String itemId,
    required int quantity,
    required DateTime dueDate,
  }) async {
    final data = await _send('POST', 'borrows.php', body: {
      'user_id': userId,
      'item_id': itemId,
      'quantity': quantity,
      'due_date': dueDate.toIso8601String().substring(0, 10), // YYYY-MM-DD
    });
    return Borrow.fromJson(data);
  }

  Future<Borrow> returnItem(String borrowId) async {
    final data = await _send('PUT', 'borrows.php', body: {'id': borrowId});
    return Borrow.fromJson(data);
  }

  // ---------- ตัวส่งคำขอกลาง ----------
  /// ส่งคำขอ อ่าน JSON {"ok":..,"data":..,"error":..} แล้วคืน data
  /// ถ้า ok=false หรือเชื่อมต่อไม่ได้ → โยน ApiException
  Future<dynamic> _send(
    String method,
    String path, {
    Map<String, String>? query,
    Object? body,
  }) async {
    final uri = Uri.parse('$apiBase/$path').replace(queryParameters: query);
    final headers = {'Content-Type': 'application/json'};
    final encoded = body == null ? null : jsonEncode(body);

    http.Response res;
    try {
      final future = switch (method) {
        'GET' => _client.get(uri, headers: headers),
        'POST' => _client.post(uri, headers: headers, body: encoded),
        'PUT' => _client.put(uri, headers: headers, body: encoded),
        _ => throw ArgumentError('method $method'),
      };
      res = await future.timeout(const Duration(seconds: 10));
    } on TimeoutException {
      throw ApiException('เซิร์ฟเวอร์ไม่ตอบสนอง (timeout)\n$uri');
    } on http.ClientException catch (e) {
      throw ApiException('เชื่อมต่อเซิร์ฟเวอร์ไม่ได้: ${e.message}\n$uri');
    }

    Map<String, dynamic> json;
    try {
      json = jsonDecode(utf8.decode(res.bodyBytes)) as Map<String, dynamic>;
    } catch (_) {
      // เซิร์ฟเวอร์ตอบเป็น HTML (เช่น PHP error หรือหน้าตรวจเบราว์เซอร์ของโฮสต์ฟรี)
      throw ApiException(
          'เซิร์ฟเวอร์ตอบไม่ใช่ JSON (HTTP ${res.statusCode})\n$uri');
    }

    if (json['ok'] != true) {
      throw ApiException(
          json['error']?.toString() ?? 'เกิดข้อผิดพลาด', res.statusCode);
    }
    return json['data'];
  }
}
