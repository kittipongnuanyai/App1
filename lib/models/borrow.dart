class Borrow {
  final String id;
  final String equipmentId;
  final String equipmentName;
  final int quantity;
  final DateTime borrowDate;
  final DateTime dueDate;
  DateTime? returnDate;

  Borrow({
    required this.id,
    required this.equipmentId,
    required this.equipmentName,
    required this.quantity,
    required this.borrowDate,
    required this.dueDate,
    this.returnDate,
  });

  bool get isReturned => returnDate != null;

  /// จำนวนวันที่เหลือก่อนครบกำหนด (ติดลบ = เลยกำหนดแล้ว)
  int get daysLeft {
    final today = DateTime.now();
    final d0 = DateTime(today.year, today.month, today.day);
    final d1 = DateTime(dueDate.year, dueDate.month, dueDate.day);
    return d1.difference(d0).inDays;
  }

  bool get isOverdue => !isReturned && daysLeft < 0;
  bool get isDueSoon => !isReturned && daysLeft >= 0 && daysLeft <= 3;

  /// แปลงจาก JSON ที่ API ส่งมา (ตาราง borrows JOIN items)
  factory Borrow.fromJson(Map<String, dynamic> json) => Borrow(
        id: '${json['id']}',
        equipmentId: '${json['item_id']}',
        equipmentName: json['item_name'] as String,
        quantity: json['quantity'] as int,
        borrowDate: DateTime.parse(json['borrow_date'] as String),
        dueDate: DateTime.parse(json['due_date'] as String),
        returnDate: json['return_date'] == null
            ? null
            : DateTime.parse(json['return_date'] as String),
      );
}
