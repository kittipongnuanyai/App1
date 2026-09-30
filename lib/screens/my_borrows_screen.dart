import 'package:flutter/material.dart';

import '../data/api_service.dart';
import '../data/app_state.dart';
import '../models/borrow.dart';
import '../theme.dart';
import '../utils/thai_date.dart';

/// หน้า 5 — การยืมของฉัน
class MyBorrowsScreen extends StatelessWidget {
  const MyBorrowsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = AppState.instance;
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('การยืมของฉัน'),
          bottom: const TabBar(
            indicatorColor: AppColors.amber,
            labelColor: Colors.white,
            unselectedLabelColor: Colors.white70,
            tabs: [Tab(text: 'กำลังยืม'), Tab(text: 'ประวัติ')],
          ),
        ),
        body: ListenableBuilder(
          listenable: state,
          builder: (context, _) => TabBarView(
            children: [
              _BorrowList(
                borrows: state.activeBorrows,
                emptyText: 'ยังไม่มีรายการที่กำลังยืม',
              ),
              _BorrowList(
                borrows: state.borrowHistory,
                emptyText: 'ยังไม่มีประวัติการยืม',
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _BorrowList extends StatelessWidget {
  final List<Borrow> borrows;
  final String emptyText;
  const _BorrowList({required this.borrows, required this.emptyText});

  @override
  Widget build(BuildContext context) {
    if (borrows.isEmpty) {
      return Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.inbox_outlined, size: 56, color: Colors.grey[400]),
            const SizedBox(height: 8),
            Text(emptyText, style: TextStyle(color: Colors.grey[600])),
          ],
        ),
      );
    }
    return RefreshIndicator(
      onRefresh: AppState.instance.refresh,
      child: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: borrows.length,
        itemBuilder: (_, i) => _BorrowCard(borrow: borrows[i]),
      ),
    );
  }
}

class _BorrowCard extends StatelessWidget {
  final Borrow borrow;
  const _BorrowCard({required this.borrow});

  Future<void> _confirmReturn(BuildContext context) async {
    final ok = await showDialog<bool>(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('คืนอุปกรณ์'),
        content: Text('ยืนยันคืน ${borrow.equipmentName} x${borrow.quantity} ?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('ยกเลิก'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('คืนของ'),
          ),
        ],
      ),
    );
    if (ok != true || !context.mounted) return;
    try {
      await AppState.instance.returnItem(borrow);
    } on ApiException catch (e) {
      if (!context.mounted) return;
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text(e.message)));
      return;
    }
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('คืน ${borrow.equipmentName} สำเร็จ')),
    );
  }

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final b = borrow;

    Widget? badge;
    if (b.isOverdue) {
      badge = _Badge(
        color: AppColors.danger,
        icon: Icons.error_outline,
        label: 'เลยกำหนด ${-b.daysLeft} วัน',
      );
    } else if (b.isDueSoon) {
      badge = _Badge(
        color: Colors.orange.shade700,
        icon: Icons.warning_amber_rounded,
        label: b.daysLeft == 0 ? 'ครบกำหนดวันนี้' : 'อีก ${b.daysLeft} วันครบกำหนด',
      );
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text('${b.equipmentName}  x${b.quantity}',
                      style: text.titleMedium),
                ),
                if (b.isReturned)
                  const Icon(Icons.check_circle, color: Colors.green, size: 22),
              ],
            ),
            const SizedBox(height: 6),
            Text(
              b.isReturned
                  ? 'ยืม ${thaiShortDate(b.borrowDate)} · คืนแล้ว ${thaiShortDate(b.returnDate!)}'
                  : 'ยืม ${thaiShortDate(b.borrowDate)} · คืน ${thaiShortDate(b.dueDate)}',
              style: text.bodyMedium?.copyWith(color: Colors.grey[700]),
            ),
            if (badge != null) ...[const SizedBox(height: 10), badge],
            if (!b.isReturned) ...[
              const SizedBox(height: 12),
              Align(
                alignment: Alignment.centerRight,
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    minimumSize: const Size(0, 40),
                    backgroundColor: AppColors.sky,
                  ),
                  onPressed: () => _confirmReturn(context),
                  icon: const Icon(Icons.assignment_return_outlined, size: 18),
                  label: const Text('คืนของ'),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _Badge extends StatelessWidget {
  final Color color;
  final IconData icon;
  final String label;
  const _Badge({required this.color, required this.icon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withValues(alpha: 0.5)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: 6),
          Text(label,
              style: TextStyle(
                  color: color, fontSize: 13, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
