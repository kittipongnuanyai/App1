import 'package:flutter/material.dart';

import '../data/app_state.dart';
import '../models/equipment.dart';
import '../theme.dart';
import '../utils/thai_date.dart';
import '../widgets/equipment_image.dart';
import 'equipment_form_screen.dart';

/// หน้า 3 — รายละเอียดอุปกรณ์
class EquipmentDetailScreen extends StatelessWidget {
  final String equipmentId;
  const EquipmentDetailScreen({super.key, required this.equipmentId});

  @override
  Widget build(BuildContext context) {
    final state = AppState.instance;
    return ListenableBuilder(
      listenable: state,
      builder: (context, _) {
        final item = state.findEquipment(equipmentId);
        if (item == null) {
          return Scaffold(
            appBar: AppBar(title: const Text('รายละเอียดอุปกรณ์')),
            body: const Center(child: Text('ไม่พบอุปกรณ์')),
          );
        }
        final text = Theme.of(context).textTheme;
        return Scaffold(
          appBar: AppBar(
            title: const Text('รายละเอียดอุปกรณ์'),
            actions: [
              if (state.isAdmin)
                IconButton(
                  icon: const Icon(Icons.edit_outlined),
                  tooltip: 'แก้ไข',
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(
                        builder: (_) => EquipmentFormScreen(existing: item)),
                  ),
                ),
            ],
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ---------- ส่วนบน: รูปใหญ่ ----------
                ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: AspectRatio(
                    aspectRatio: 16 / 10,
                    child: EquipmentImage(item: item, iconSize: 96),
                  ),
                ),
                const SizedBox(height: 20),
                // ---------- ส่วนกลาง: ข้อมูล ----------
                Text(item.name, style: text.headlineSmall),
                const SizedBox(height: 8),
                _InfoRow(
                  icon: item.category.icon,
                  label: 'หมวด',
                  value: item.category.label,
                ),
                _InfoRow(
                  icon: Icons.inventory_outlined,
                  label: 'คงเหลือ',
                  value: '${item.available} / ${item.total} ชิ้น',
                  valueColor: item.isOutOfStock ? AppColors.danger : null,
                ),
                const SizedBox(height: 16),
                Text('รายละเอียด:', style: text.titleMedium),
                const SizedBox(height: 6),
                Text(item.description, style: text.bodyLarge),
                const SizedBox(height: 32),
                // ---------- ส่วนล่าง: ปุ่มยืม ----------
                ElevatedButton.icon(
                  icon: const Icon(Icons.shopping_bag_outlined),
                  label: Text(item.isOutOfStock ? 'ยืมไม่ได้ (หมด)' : 'ยืมอุปกรณ์'),
                  onPressed:
                      item.isOutOfStock ? null : () => _showBorrowDialog(context, item),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _showBorrowDialog(BuildContext context, Equipment item) async {
    final result = await showDialog<_BorrowRequest>(
      context: context,
      builder: (_) => _BorrowDialog(item: item),
    );
    if (result == null || !context.mounted) return;

    final ok = AppState.instance.borrow(item, result.quantity, result.dueDate);
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(ok
            ? 'ยืม ${item.name} x${result.quantity} สำเร็จ · คืน ${thaiShortDate(result.dueDate)}'
            : 'ยืมไม่สำเร็จ'),
      ),
    );
    if (ok) Navigator.of(context).pop(); // กลับหน้ารายการ
  }
}

class _InfoRow extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;
  final Color? valueColor;
  const _InfoRow({
    required this.icon,
    required this.label,
    required this.value,
    this.valueColor,
  });

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(icon, size: 20, color: AppColors.indigo),
          const SizedBox(width: 8),
          Text('$label: ', style: text.bodyLarge?.copyWith(color: Colors.grey[700])),
          Text(value,
              style: text.bodyLarge?.copyWith(
                  fontWeight: FontWeight.w600, color: valueColor)),
        ],
      ),
    );
  }
}

class _BorrowRequest {
  final int quantity;
  final DateTime dueDate;
  const _BorrowRequest(this.quantity, this.dueDate);
}

/// Dialog ยืม: เลือกจำนวน + วันคืน
class _BorrowDialog extends StatefulWidget {
  final Equipment item;
  const _BorrowDialog({required this.item});

  @override
  State<_BorrowDialog> createState() => _BorrowDialogState();
}

class _BorrowDialogState extends State<_BorrowDialog> {
  int _qty = 1;
  late DateTime _due = DateTime.now().add(const Duration(days: 7));

  Future<void> _pickDate() async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: _due,
      firstDate: now,
      lastDate: now.add(const Duration(days: 60)),
    );
    if (picked != null) setState(() => _due = picked);
  }

  @override
  Widget build(BuildContext context) {
    final max = widget.item.available;
    return AlertDialog(
      title: Text('ยืม ${widget.item.name}'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              const Expanded(child: Text('จำนวน')),
              IconButton(
                onPressed: _qty > 1 ? () => setState(() => _qty--) : null,
                icon: const Icon(Icons.remove_circle_outline),
              ),
              Text('$_qty', style: const TextStyle(fontSize: 18)),
              IconButton(
                onPressed: _qty < max ? () => setState(() => _qty++) : null,
                icon: const Icon(Icons.add_circle_outline),
              ),
            ],
          ),
          Text('คงเหลือ $max ชิ้น',
              style: TextStyle(color: Colors.grey[600], fontSize: 12)),
          const SizedBox(height: 12),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.event),
            title: const Text('วันคืน'),
            subtitle: Text(thaiFullDate(_due)),
            trailing: const Icon(Icons.chevron_right),
            onTap: _pickDate,
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('ยกเลิก'),
        ),
        FilledButton(
          onPressed: () => Navigator.pop(context, _BorrowRequest(_qty, _due)),
          child: const Text('ยืนยันยืม'),
        ),
      ],
    );
  }
}
