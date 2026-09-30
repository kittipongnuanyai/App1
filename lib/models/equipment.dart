import 'package:flutter/material.dart';

/// หมวดหมู่อุปกรณ์ — ชื่อ (board, sensor, ...) ตรงกับคอลัมน์ category ในฐานข้อมูล
enum EquipmentCategory {
  board('บอร์ด', Icons.developer_board),
  sensor('เซนเซอร์', Icons.sensors),
  cable('สาย', Icons.cable),
  module('โมดูล', Icons.memory),
  tool('เครื่องมือ', Icons.build);

  const EquipmentCategory(this.label, this.icon);
  final String label;
  final IconData icon;
}

class Equipment {
  final String id;
  String name;
  EquipmentCategory category;
  int total;
  int available;
  String description;
  String? imagePath; // path รูปจาก image_picker (ถ้ามี)

  Equipment({
    required this.id,
    required this.name,
    required this.category,
    required this.total,
    required this.available,
    required this.description,
    this.imagePath,
  });

  bool get isOutOfStock => available <= 0;

  /// แปลงจาก JSON ที่ API ส่งมา (ตาราง items)
  factory Equipment.fromJson(Map<String, dynamic> json) => Equipment(
        id: '${json['id']}',
        name: json['name'] as String,
        category: EquipmentCategory.values.byName(json['category'] as String),
        total: json['total'] as int,
        available: json['available'] as int,
        description: (json['description'] ?? '') as String,
        imagePath: json['image_url'] as String?,
      );

  /// แปลงเป็น JSON เพื่อส่งไปเพิ่ม/แก้ไข (available ให้เซิร์ฟเวอร์คำนวณเอง)
  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'category': category.name,
        'total': total,
        'description': description,
        'image_url': imagePath,
      };
}
