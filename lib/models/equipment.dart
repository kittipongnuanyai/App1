import 'package:flutter/material.dart';

/// หมวดหมู่อุปกรณ์
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
}
