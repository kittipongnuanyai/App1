import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../data/app_state.dart';
import '../models/equipment.dart';
import '../theme.dart';

/// หน้า 4 — เพิ่ม/แก้ไขอุปกรณ์ (เฉพาะแอดมิน)
/// ถ้า [existing] เป็น null = โหมดเพิ่ม, ไม่ null = โหมดแก้ไข
class EquipmentFormScreen extends StatefulWidget {
  final Equipment? existing;
  const EquipmentFormScreen({super.key, this.existing});

  @override
  State<EquipmentFormScreen> createState() => _EquipmentFormScreenState();
}

class _EquipmentFormScreenState extends State<EquipmentFormScreen> {
  final _formKey = GlobalKey<FormState>();
  late final _nameCtrl = TextEditingController(text: widget.existing?.name);
  late final _totalCtrl =
      TextEditingController(text: widget.existing?.total.toString());
  late final _descCtrl =
      TextEditingController(text: widget.existing?.description);
  late EquipmentCategory _category =
      widget.existing?.category ?? EquipmentCategory.board;
  late String? _imagePath = widget.existing?.imagePath;

  bool get _isEdit => widget.existing != null;

  @override
  void dispose() {
    _nameCtrl.dispose();
    _totalCtrl.dispose();
    _descCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickImage() async {
    final source = await showModalBottomSheet<ImageSource>(
      context: context,
      builder: (_) => SafeArea(
        child: Wrap(
          children: [
            ListTile(
              leading: const Icon(Icons.photo_camera_outlined),
              title: const Text('ถ่ายรูป'),
              onTap: () => Navigator.pop(context, ImageSource.camera),
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_outlined),
              title: const Text('เลือกจากคลังภาพ'),
              onTap: () => Navigator.pop(context, ImageSource.gallery),
            ),
          ],
        ),
      ),
    );
    if (source == null) return;
    try {
      final file = await ImagePicker().pickImage(source: source, maxWidth: 1200);
      if (file != null) setState(() => _imagePath = file.path);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('เลือกรูปไม่สำเร็จ: $e')),
      );
    }
  }

  void _save() {
    if (!_formKey.currentState!.validate()) return;
    final state = AppState.instance;
    final total = int.parse(_totalCtrl.text.trim());

    if (_isEdit) {
      final item = widget.existing!;
      final borrowed = item.total - item.available;
      item
        ..name = _nameCtrl.text.trim()
        ..category = _category
        ..total = total
        ..available = (total - borrowed).clamp(0, total)
        ..description = _descCtrl.text.trim()
        ..imagePath = _imagePath;
      state.updateEquipment(item);
    } else {
      state.addEquipment(Equipment(
        id: 'e${DateTime.now().millisecondsSinceEpoch}',
        name: _nameCtrl.text.trim(),
        category: _category,
        total: total,
        available: total,
        description: _descCtrl.text.trim(),
        imagePath: _imagePath,
      ));
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(_isEdit ? 'บันทึกการแก้ไขแล้ว' : 'เพิ่มอุปกรณ์แล้ว')),
    );
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(_isEdit ? 'แก้ไขอุปกรณ์' : 'เพิ่มอุปกรณ์')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // ---------- ส่วนบน: รูป ----------
              Row(
                children: [
                  GestureDetector(
                    onTap: _pickImage,
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(14),
                      child: SizedBox(
                        width: 110,
                        height: 110,
                        child: _imagePath != null && !kIsWeb
                            ? Image.file(File(_imagePath!), fit: BoxFit.cover)
                            : Container(
                                color: AppColors.sky.withValues(alpha: 0.15),
                                child: Icon(_category.icon,
                                    size: 48, color: AppColors.indigo),
                              ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: _pickImage,
                      icon: const Icon(Icons.photo_camera_outlined),
                      label: const Text('ถ่าย/เลือกรูป'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),
              // ---------- ส่วนกลาง: ฟอร์ม ----------
              TextFormField(
                controller: _nameCtrl,
                decoration: const InputDecoration(labelText: 'ชื่ออุปกรณ์'),
                validator: (v) =>
                    (v == null || v.trim().isEmpty) ? 'กรุณากรอกชื่ออุปกรณ์' : null,
              ),
              const SizedBox(height: 14),
              DropdownButtonFormField<EquipmentCategory>(
                initialValue: _category,
                decoration: const InputDecoration(labelText: 'หมวดหมู่'),
                items: [
                  for (final c in EquipmentCategory.values)
                    DropdownMenuItem(
                      value: c,
                      child: Row(
                        children: [
                          Icon(c.icon, size: 18),
                          const SizedBox(width: 8),
                          Text(c.label),
                        ],
                      ),
                    ),
                ],
                onChanged: (v) => setState(() => _category = v!),
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _totalCtrl,
                keyboardType: TextInputType.number,
                inputFormatters: [FilteringTextInputFormatter.digitsOnly],
                decoration: const InputDecoration(labelText: 'จำนวนทั้งหมด'),
                validator: (v) {
                  final n = int.tryParse(v ?? '');
                  if (n == null || n <= 0) return 'กรุณากรอกจำนวนเป็นตัวเลขมากกว่า 0';
                  if (_isEdit) {
                    final borrowed =
                        widget.existing!.total - widget.existing!.available;
                    if (n < borrowed) return 'จำนวนต้องไม่น้อยกว่าที่ถูกยืมอยู่ ($borrowed)';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 14),
              TextFormField(
                controller: _descCtrl,
                maxLines: 4,
                decoration: const InputDecoration(
                  labelText: 'รายละเอียด',
                  alignLabelWithHint: true,
                ),
              ),
              const SizedBox(height: 28),
              // ---------- ส่วนล่าง: บันทึก ----------
              ElevatedButton.icon(
                onPressed: _save,
                icon: const Icon(Icons.save_outlined),
                label: const Text('บันทึก'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
