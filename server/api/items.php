<?php
// items.php — อุปกรณ์
//   GET  items.php          → รายการทั้งหมด
//   GET  items.php?id=3     → ชิ้นเดียว
//   POST items.php          → เพิ่ม   {name, category, total, description}
//   PUT  items.php          → แก้ไข  {id, name, category, total, description}
require_once __DIR__ . '/db.php';

$method = $_SERVER['REQUEST_METHOD'];
$categories = ['board', 'sensor', 'cable', 'module', 'tool'];

// ---------- GET ----------
if ($method === 'GET') {
    if (isset($_GET['id'])) {
        $stmt = $pdo->prepare('SELECT * FROM items WHERE id = ?');
        $stmt->execute([(int) $_GET['id']]);
        $row = $stmt->fetch();
        if (!$row) json_error('ไม่พบอุปกรณ์', 404);
        json_ok(item_row($row));
    }
    $rows = $pdo->query('SELECT * FROM items ORDER BY name')->fetchAll();
    json_ok(array_map('item_row', $rows));
}

// ---------- POST / PUT ใช้ข้อมูลชุดเดียวกัน ----------
$in          = input();
$name        = trim(need($in, 'name'));
$category    = need($in, 'category');
$total       = (int) need($in, 'total');
$description = trim($in['description'] ?? '');
$image_url   = $in['image_url'] ?? null;

if (!in_array($category, $categories, true)) json_error('หมวดหมู่ไม่ถูกต้อง');
if ($total <= 0) json_error('จำนวนต้องมากกว่า 0');

if ($method === 'POST') {
    $stmt = $pdo->prepare(
        'INSERT INTO items (name, category, total, available, description, image_url)
         VALUES (?, ?, ?, ?, ?, ?)'
    );
    $stmt->execute([$name, $category, $total, $total, $description, $image_url]);
    $id = (int) $pdo->lastInsertId();
    json_ok(item_row($pdo->query("SELECT * FROM items WHERE id = $id")->fetch()));
}

if ($method === 'PUT') {
    $id = (int) need($in, 'id');
    $stmt = $pdo->prepare('SELECT * FROM items WHERE id = ?');
    $stmt->execute([$id]);
    $old = $stmt->fetch();
    if (!$old) json_error('ไม่พบอุปกรณ์', 404);

    // จำนวนใหม่ต้องไม่น้อยกว่าที่ถูกยืมอยู่ แล้วคำนวณ available ใหม่
    $borrowed = (int) $old['total'] - (int) $old['available'];
    if ($total < $borrowed) json_error("จำนวนต้องไม่น้อยกว่าที่ถูกยืมอยู่ ($borrowed)");
    $available = $total - $borrowed;

    $stmt = $pdo->prepare(
        'UPDATE items SET name = ?, category = ?, total = ?, available = ?, description = ?, image_url = ?
         WHERE id = ?'
    );
    $stmt->execute([$name, $category, $total, $available, $description, $image_url, $id]);
    json_ok(item_row($pdo->query("SELECT * FROM items WHERE id = $id")->fetch()));
}

json_error('method ไม่รองรับ', 405);
