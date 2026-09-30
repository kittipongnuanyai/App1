import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../models/equipment.dart';
import '../theme.dart';

/// รูปอุปกรณ์:
///  - imagePath ขึ้นต้นด้วย http  → รูปจากเซิร์ฟเวอร์ (Image.network)
///  - imagePath เป็นไฟล์ในเครื่องที่มีอยู่จริง → Image.file (จาก image_picker)
///  - อื่น ๆ → ไอคอนตามหมวด
class EquipmentImage extends StatelessWidget {
  final Equipment item;
  final double iconSize;

  const EquipmentImage({super.key, required this.item, this.iconSize = 48});

  @override
  Widget build(BuildContext context) {
    final path = item.imagePath;
    final placeholder = Container(
      color: AppColors.sky.withValues(alpha: 0.12),
      alignment: Alignment.center,
      child: Icon(item.category.icon, size: iconSize, color: AppColors.indigo),
    );

    if (path == null || path.isEmpty) return placeholder;
    if (path.startsWith('http')) {
      return Image.network(path,
          fit: BoxFit.cover, errorBuilder: (_, __, ___) => placeholder);
    }
    if (!kIsWeb && File(path).existsSync()) {
      return Image.file(File(path), fit: BoxFit.cover);
    }
    return placeholder;
  }
}
