<?php
// ============================================================
//  LabStock API — เชื่อมต่อฐานข้อมูล + ฟังก์ชันช่วยตอบ JSON
//  ทุก endpoint จะ require_once ไฟล์นี้เป็นบรรทัดแรก
// ============================================================
require_once __DIR__ . '/config.php';

// ---------- ส่วนหัวของทุกคำตอบ ----------
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');                       // ให้ Flutter web / เครื่องอื่นเรียกได้
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

// ---------- เชื่อมต่อด้วย PDO ----------
try {
    $pdo = new PDO(
        'mysql:host=' . DB_HOST . ';port=' . DB_PORT . ';dbname=' . DB_NAME . ';charset=utf8mb4',
        DB_USER,
        DB_PASS,
        [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION, // ผิดพลาด → โยน exception
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,       // ได้ array แบบ key = ชื่อคอลัมน์
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]
    );
} catch (PDOException $e) {
    json_error('เชื่อมต่อฐานข้อมูลไม่ได้: ' . $e->getMessage(), 500);
}

// ---------- ฟังก์ชันช่วย ----------

/** ตอบสำเร็จ: {"ok":true,"data":...} */
function json_ok($data = null): void {
    echo json_encode(['ok' => true, 'data' => $data], JSON_UNESCAPED_UNICODE);
    exit;
}

/** ตอบผิดพลาด: {"ok":false,"error":"..."} พร้อม HTTP status */
function json_error(string $message, int $status = 400): void {
    http_response_code($status);
    echo json_encode(['ok' => false, 'error' => $message], JSON_UNESCAPED_UNICODE);
    exit;
}

/** อ่านข้อมูลที่ส่งมา รองรับทั้ง JSON body และ form-data */
function input(): array {
    $raw = file_get_contents('php://input');
    $json = json_decode($raw, true);
    if (is_array($json)) return $json;
    return $_POST ?: [];
}

/** ดึงค่าจาก input โดยบังคับว่าต้องมี ไม่มี → ตอบ 400 */
function need(array $in, string $key) {
    if (!isset($in[$key]) || $in[$key] === '') json_error("ต้องส่งค่า '$key'");
    return $in[$key];
}

/** แปลงแถว users ให้ไม่ส่ง password_hash ออกไป */
function user_public(array $row): array {
    unset($row['password_hash']);
    $row['id'] = (int) $row['id'];
    return $row;
}

/** แปลงชนิดตัวเลขของแถว items ให้เป็น int (JSON จะได้ไม่เป็น string) */
function item_row(array $row): array {
    $row['id']        = (int) $row['id'];
    $row['total']     = (int) $row['total'];
    $row['available'] = (int) $row['available'];
    return $row;
}

function borrow_row(array $row): array {
    foreach (['id', 'user_id', 'item_id', 'quantity'] as $k) $row[$k] = (int) $row[$k];
    return $row;
}
