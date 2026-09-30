<?php
// หน้าแรกของ API — เปิดในเบราว์เซอร์เพื่อเช็กว่าเซิร์ฟเวอร์และฐานข้อมูลพร้อม
require_once __DIR__ . '/db.php';

$counts = [];
foreach (['users', 'items', 'borrows'] as $t) {
    $counts[$t] = (int) $pdo->query("SELECT COUNT(*) FROM $t")->fetchColumn();
}

json_ok([
    'app'       => 'LabStock API',
    'version'   => '1.0',
    'php'       => PHP_VERSION,
    'database'  => DB_NAME,
    'rows'      => $counts,
    'endpoints' => [
        'POST login.php'            => '{username, password}',
        'POST register.php'         => '{username, password, name, student_id}',
        'GET  items.php'            => 'รายการอุปกรณ์ทั้งหมด (หรือ ?id=)',
        'POST items.php'            => 'เพิ่มอุปกรณ์ {name, category, total, description}',
        'PUT  items.php'            => 'แก้ไขอุปกรณ์ {id, name, category, total, description}',
        'GET  borrows.php?user_id=' => 'รายการยืมของผู้ใช้',
        'POST borrows.php'          => 'ยืม {user_id, item_id, quantity, due_date}',
        'PUT  borrows.php'          => 'คืน {id}',
    ],
]);
