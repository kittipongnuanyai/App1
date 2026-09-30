<?php
// borrows.php — การยืม/คืน
//   GET  borrows.php?user_id=2   → รายการยืมของผู้ใช้ (ทั้งกำลังยืมและคืนแล้ว)
//   POST borrows.php             → ยืม {user_id, item_id, quantity, due_date: 'YYYY-MM-DD'}
//   PUT  borrows.php             → คืน {id}
require_once __DIR__ . '/db.php';

$method = $_SERVER['REQUEST_METHOD'];

// ---------- GET ----------
if ($method === 'GET') {
    $user_id = (int) ($_GET['user_id'] ?? 0);
    if ($user_id <= 0) json_error("ต้องส่ง ?user_id=");
    $stmt = $pdo->prepare(
        'SELECT b.*, i.name AS item_name
         FROM borrows b JOIN items i ON i.id = b.item_id
         WHERE b.user_id = ?
         ORDER BY b.return_date IS NOT NULL, b.due_date'
    );
    $stmt->execute([$user_id]);
    json_ok(array_map('borrow_row', $stmt->fetchAll()));
}

$in = input();

// ---------- POST: ยืม ----------
if ($method === 'POST') {
    $user_id  = (int) need($in, 'user_id');
    $item_id  = (int) need($in, 'item_id');
    $quantity = (int) need($in, 'quantity');
    $due_date = need($in, 'due_date');
    if ($quantity <= 0) json_error('จำนวนต้องมากกว่า 0');

    // Transaction: ตัดสต็อกและบันทึกการยืมต้องสำเร็จพร้อมกัน ไม่งั้นยกเลิกทั้งคู่
    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('SELECT available FROM items WHERE id = ? FOR UPDATE');
        $stmt->execute([$item_id]);
        $item = $stmt->fetch();
        if (!$item) throw new RuntimeException('ไม่พบอุปกรณ์');
        if ((int) $item['available'] < $quantity) throw new RuntimeException('จำนวนคงเหลือไม่พอ');

        $pdo->prepare('UPDATE items SET available = available - ? WHERE id = ?')
            ->execute([$quantity, $item_id]);
        $pdo->prepare(
            'INSERT INTO borrows (user_id, item_id, quantity, borrow_date, due_date)
             VALUES (?, ?, ?, CURDATE(), ?)'
        )->execute([$user_id, $item_id, $quantity, $due_date]);
        $id = (int) $pdo->lastInsertId();
        $pdo->commit();
    } catch (Exception $e) {
        $pdo->rollBack();
        json_error($e->getMessage());
    }
    $row = $pdo->query(
        "SELECT b.*, i.name AS item_name FROM borrows b JOIN items i ON i.id = b.item_id WHERE b.id = $id"
    )->fetch();
    json_ok(borrow_row($row));
}

// ---------- PUT: คืน ----------
if ($method === 'PUT') {
    $id = (int) need($in, 'id');

    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare('SELECT * FROM borrows WHERE id = ? FOR UPDATE');
        $stmt->execute([$id]);
        $b = $stmt->fetch();
        if (!$b) throw new RuntimeException('ไม่พบรายการยืม');
        if ($b['return_date'] !== null) throw new RuntimeException('รายการนี้คืนแล้ว');

        $pdo->prepare('UPDATE borrows SET return_date = CURDATE() WHERE id = ?')->execute([$id]);
        $pdo->prepare('UPDATE items SET available = LEAST(total, available + ?) WHERE id = ?')
            ->execute([(int) $b['quantity'], (int) $b['item_id']]);
        $pdo->commit();
    } catch (Exception $e) {
        $pdo->rollBack();
        json_error($e->getMessage());
    }
    $row = $pdo->query(
        "SELECT b.*, i.name AS item_name FROM borrows b JOIN items i ON i.id = b.item_id WHERE b.id = $id"
    )->fetch();
    json_ok(borrow_row($row));
}

json_error('method ไม่รองรับ', 405);
