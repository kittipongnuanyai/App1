<?php
// POST register.php  {username, password, name, student_id}  →  ผู้ใช้ใหม่ (บทบาท student)
require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_error('ต้องใช้ POST', 405);

$in         = input();
$username   = trim(need($in, 'username'));
$password   = need($in, 'password');
$name       = trim(need($in, 'name'));
$student_id = trim(need($in, 'student_id'));

if (strlen($password) < 6) json_error('รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร');

// ตรวจชื่อซ้ำ
$stmt = $pdo->prepare('SELECT id FROM users WHERE username = ?');
$stmt->execute([$username]);
if ($stmt->fetch()) json_error('ชื่อผู้ใช้นี้ถูกใช้แล้ว', 409);

$stmt = $pdo->prepare(
    'INSERT INTO users (username, password_hash, name, student_id, role) VALUES (?, ?, ?, ?, ?)'
);
$stmt->execute([$username, password_hash($password, PASSWORD_DEFAULT), $name, $student_id, 'student']);

$id   = (int) $pdo->lastInsertId();
$user = $pdo->query("SELECT * FROM users WHERE id = $id")->fetch();
json_ok(user_public($user));
