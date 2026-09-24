import 'package:flutter/material.dart';

import '../data/app_state.dart';
import '../models/equipment.dart';
import '../theme.dart';
import '../widgets/equipment_image.dart';
import 'equipment_detail_screen.dart';
import 'equipment_form_screen.dart';

/// หน้า 2 — รายการอุปกรณ์ (หน้าหลัก)
class EquipmentListScreen extends StatefulWidget {
  const EquipmentListScreen({super.key});

  @override
  State<EquipmentListScreen> createState() => _EquipmentListScreenState();
}

class _EquipmentListScreenState extends State<EquipmentListScreen> {
  String _query = '';
  EquipmentCategory? _category; // null = ทั้งหมด

  List<Equipment> _filtered(List<Equipment> all) {
    final q = _query.trim().toLowerCase();
    return all.where((e) {
      final matchCat = _category == null || e.category == _category;
      final matchQ = q.isEmpty || e.name.toLowerCase().contains(q);
      return matchCat && matchQ;
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    final state = AppState.instance;
    return ListenableBuilder(
      listenable: state,
      builder: (context, _) {
        final items = _filtered(state.equipment);
        return Scaffold(
          appBar: AppBar(
            title: const Text('LabStock'),
            actions: [
              IconButton(
                icon: const Icon(Icons.notifications_outlined),
                tooltip: 'แจ้งเตือน',
                onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('ยังไม่มีการแจ้งเตือนใหม่')),
                ),
              ),
            ],
          ),
          body: Column(
            children: [
              // ---------- ส่วนบน: ค้นหา ----------
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: TextField(
                  onChanged: (v) => setState(() => _query = v),
                  decoration: InputDecoration(
                    hintText: 'ค้นหาอุปกรณ์...',
                    prefixIcon: const Icon(Icons.search),
                    isDense: true,
                    contentPadding: const EdgeInsets.symmetric(vertical: 12),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(30),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
              // ---------- ชิปกรองหมวด ----------
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Row(
                  children: [
                    _chip('ทั้งหมด', null),
                    for (final c in EquipmentCategory.values) _chip(c.label, c),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              // ---------- ส่วนกลาง: รายการ ----------
              Expanded(
                child: items.isEmpty
                    ? const Center(child: Text('ไม่พบอุปกรณ์ที่ค้นหา'))
                    : GridView.builder(
                        padding: const EdgeInsets.fromLTRB(16, 4, 16, 88),
                        gridDelegate:
                            const SliverGridDelegateWithMaxCrossAxisExtent(
                          maxCrossAxisExtent: 220,
                          mainAxisSpacing: 12,
                          crossAxisSpacing: 12,
                          childAspectRatio: 0.82,
                        ),
                        itemCount: items.length,
                        itemBuilder: (_, i) => _EquipmentCard(item: items[i]),
                      ),
              ),
            ],
          ),
          // ---------- ปุ่มลอย เฉพาะแอดมิน ----------
          floatingActionButton: state.isAdmin
              ? FloatingActionButton(
                  tooltip: 'เพิ่มอุปกรณ์',
                  onPressed: () => Navigator.of(context).push(
                    MaterialPageRoute(
                        builder: (_) => const EquipmentFormScreen()),
                  ),
                  child: const Icon(Icons.add),
                )
              : null,
        );
      },
    );
  }

  Widget _chip(String label, EquipmentCategory? cat) {
    final selected = _category == cat;
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ChoiceChip(
        label: Text(label),
        selected: selected,
        onSelected: (_) => setState(() => _category = cat),
      ),
    );
  }
}

class _EquipmentCard extends StatelessWidget {
  final Equipment item;
  const _EquipmentCard({required this.item});

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: () => Navigator.of(context).push(
          MaterialPageRoute(
              builder: (_) => EquipmentDetailScreen(equipmentId: item.id)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(child: EquipmentImage(item: item)),
            Padding(
              padding: const EdgeInsets.fromLTRB(12, 10, 12, 12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(item.name,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: text.titleMedium),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      Expanded(
                        child: Text('เหลือ ${item.available}',
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: text.bodyMedium?.copyWith(
                                color: item.isOutOfStock
                                    ? AppColors.danger
                                    : Colors.grey[700])),
                      ),
                      if (item.isOutOfStock)
                        Container(
                          padding: const EdgeInsets.symmetric(
                              horizontal: 8, vertical: 2),
                          decoration: BoxDecoration(
                            color: AppColors.danger,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: const Text('ยืมไม่ได้',
                              style: TextStyle(
                                  color: Colors.white, fontSize: 11)),
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
