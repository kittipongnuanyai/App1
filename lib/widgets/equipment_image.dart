import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../models/equipment.dart';
import '../theme.dart';

/// รูปอุปกรณ์: ถ้ามีรูปที่เลือกจาก image_picker ให้แสดง ถ้าไม่มีแสดงไอคอนตามหมวด
class EquipmentImage extends StatelessWidget {
  final Equipment item;
  final double iconSize;

  const EquipmentImage({super.key, required this.item, this.iconSize = 48});

  @override
  Widget build(BuildContext context) {
    final path = item.imagePath;
    if (path != null && !kIsWeb) {
      return Image.file(File(path), fit: BoxFit.cover);
    }
    return Container(
      color: AppColors.sky.withValues(alpha: 0.12),
      alignment: Alignment.center,
      child: Icon(item.category.icon, size: iconSize, color: AppColors.indigo),
    );
  }
}
