<?php
// POST login.php  {username, password}  →  ข้อมูลผู้ใช้ (ไม่มีรหัสผ่าน)
require_once __DIR__ . '/db.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') json_error('ต้องใช้ POST', 405);

$in       = input();
$username = trim(need($in, 'username'));
$password = need($in, 'password');

$stmt = $pdo->prepare('SELECT * FROM users WHERE username = ?');
$stmt->execute([$username]);
$user = $stmt->fetch();

// password_verify เทียบรหัสผ่านกับ hash ที่เก็บไว้ (ไม่เก็บรหัสผ่านจริงในฐานข้อมูล)
if (!$user || !password_verify($password, $user['password_hash'])) {
    json_error('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 401);
}

json_ok(user_public($user));
