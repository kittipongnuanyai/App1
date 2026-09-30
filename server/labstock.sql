-- ============================================================
--  LabStock — โครงสร้างฐานข้อมูล + ข้อมูลเริ่มต้น
--  วิธีใช้: phpMyAdmin → เลือกฐานข้อมูล labstock → Import ไฟล์นี้
--  (บนโฮสต์ฟรี ให้สร้างฐานข้อมูลจากแผงควบคุมก่อน แล้ว Import โดยไม่ต้อง CREATE DATABASE)
-- ============================================================

CREATE DATABASE IF NOT EXISTS labstock CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE labstock;

-- ---------- ผู้ใช้ ----------
DROP TABLE IF EXISTS borrows;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id            INT AUTO_INCREMENT PRIMARY KEY,
  username      VARCHAR(50)  NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,          -- เก็บ hash ไม่เก็บรหัสผ่านจริง
  name          VARCHAR(100) NOT NULL,
  student_id    VARCHAR(20)  NOT NULL,
  role          ENUM('student','admin') NOT NULL DEFAULT 'student',
  created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- อุปกรณ์ ----------
CREATE TABLE items (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  category    ENUM('board','sensor','cable','module','tool') NOT NULL,   -- ตรงกับ enum ในแอป
  total       INT NOT NULL DEFAULT 0,
  available   INT NOT NULL DEFAULT 0,           -- คงเหลือ (ลดเมื่อยืม เพิ่มเมื่อคืน)
  description TEXT,
  image_url   VARCHAR(255) DEFAULT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ---------- การยืม ----------
CREATE TABLE borrows (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  user_id     INT  NOT NULL,
  item_id     INT  NOT NULL,
  quantity    INT  NOT NULL DEFAULT 1,
  borrow_date DATE NOT NULL,
  due_date    DATE NOT NULL,
  return_date DATE DEFAULT NULL,                -- NULL = ยังไม่คืน
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (item_id) REFERENCES items(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
--  ข้อมูลเริ่มต้น (รหัสผ่านของทุกคนคือ 1234)
-- ============================================================
INSERT INTO users (username, password_hash, name, student_id, role) VALUES
('admin',   '$2y$10$lhGUPqOkvHtXKdBIx37ln.UP8f1/on70F6GtNp4iugqrclaFpcKJq', 'อ.สมหญิง แล็บดี', 'ICE-ADMIN', 'admin'),
('somchai', '$2y$10$lhGUPqOkvHtXKdBIx37ln.UP8f1/on70F6GtNp4iugqrclaFpcKJq', 'สมชาย ใจดี',      '674659001', 'student'),
('somsri',  '$2y$10$lhGUPqOkvHtXKdBIx37ln.UP8f1/on70F6GtNp4iugqrclaFpcKJq', 'สมศรี มีสุข',     '674659002', 'student');

INSERT INTO items (name, category, total, available, description) VALUES
('Arduino UNO R3',          'board',  10,  5, 'บอร์ดไมโครคอนโทรลเลอร์ ATmega328P ใช้สำหรับเรียนพื้นฐาน Embedded และ IoT รองรับการเขียนโปรแกรมผ่าน Arduino IDE'),
('DHT22',                   'sensor',  6,  0, 'เซนเซอร์วัดอุณหภูมิและความชื้นแบบดิจิทัล ความแม่นยำสูงกว่า DHT11'),
('สาย USB Type-B',          'cable',  15, 12, 'สาย USB A-to-B ยาว 1 เมตร สำหรับต่อบอร์ด Arduino UNO'),
('Servo SG90',              'module',  8,  3, 'เซอร์โวมอเตอร์ขนาดเล็ก หมุนได้ 0–180 องศา แรงบิด 1.8 kg·cm'),
('ESP32 DevKit',            'board',  12,  7, 'บอร์ดไมโครคอนโทรลเลอร์ที่มี Wi-Fi และ Bluetooth ในตัว เหมาะกับงาน IoT'),
('Ultrasonic HC-SR04',      'sensor', 10,  9, 'เซนเซอร์วัดระยะทางด้วยคลื่นอัลตราโซนิก ระยะ 2–400 ซม.'),
('สาย Jumper (ชุด 40 เส้น)', 'cable',  20, 14, 'สายจั๊มเปอร์ ผู้-ผู้ ยาว 20 ซม. ชุดละ 40 เส้น'),
('มัลติมิเตอร์ดิจิทัล',      'tool',    5,  2, 'เครื่องวัดแรงดัน กระแส และความต้านทาน แบบดิจิทัล');

-- การยืมของ somchai (id=2): ใช้วันที่สัมพัทธ์กับวันนี้ เพื่อให้ป้าย "ใกล้ครบกำหนด" แสดงถูกต้อง
INSERT INTO borrows (user_id, item_id, quantity, borrow_date, due_date, return_date) VALUES
(2, 1, 1, DATE_SUB(CURDATE(), INTERVAL 5 DAY),  DATE_ADD(CURDATE(), INTERVAL 2 DAY),  NULL),
(2, 4, 2, DATE_SUB(CURDATE(), INTERVAL 2 DAY),  DATE_ADD(CURDATE(), INTERVAL 5 DAY),  NULL),
(2, 3, 1, DATE_SUB(CURDATE(), INTERVAL 20 DAY), DATE_SUB(CURDATE(), INTERVAL 13 DAY), DATE_SUB(CURDATE(), INTERVAL 14 DAY)),
(2, 6, 1, DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(CURDATE(), INTERVAL 23 DAY), DATE_SUB(CURDATE(), INTERVAL 23 DAY));
