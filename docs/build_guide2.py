#!/usr/bin/env python3
"""สร้างคู่มือเฟส 2 (ต่อ MySQL ผ่าน REST API) เป็น HTML -> PDF จากซอร์สโค้ดจริงและ git diff"""
import base64
import html
import subprocess
import sys
from datetime import date
from io import BytesIO
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import (BashLexer, DartLexer, DiffLexer, JsonLexer,
                             MySqlLexer, PhpLexer, XmlLexer)

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
# python3 build_guide2.py            → ฉบับผู้สอน (มีแผนการสอนและกล่อง "สำหรับผู้สอน")
# python3 build_guide2.py student    → ฉบับนักศึกษา (ตัดส่วนผู้สอนออก เพิ่ม "ก่อนเริ่ม" และ "สิ่งที่ต้องส่ง")
EDITION = sys.argv[1] if len(sys.argv) > 1 else "teacher"
STUDENT = EDITION == "student"
SUFFIX = "-ฉบับนักศึกษา" if STUDENT else ""
OUT_HTML = DOCS / f"LabStock-คู่มือเฟส2-MySQL{SUFFIX}.html"
OUT_PDF_RAW = DOCS / f"_raw2{EDITION}.pdf"
OUT_PDF = DOCS / f"LabStock-คู่มือเฟส2-MySQL{SUFFIX}.pdf"
REPO = "https://github.com/kittipongnuanyai/App1"
BASE_TAG = "phase1-ui"

FMT = HtmlFormatter(style="friendly", nowrap=True)
THAI_MONTHS = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
               "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
today = date.today()
TODAY_TH = f"{today.day} {THAI_MONTHS[today.month - 1]} {today.year + 543}"

LEXERS = {"dart": DartLexer, "bash": BashLexer, "php": PhpLexer, "sql": MySqlLexer,
          "json": JsonLexer, "xml": XmlLexer, "diff": DiffLexer}


# ---------------------------------------------------------------- helpers
def src(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def code(text: str, lang: str = "dart", path: str | None = None, note: str | None = None) -> str:
    lexer = LEXERS[lang]()
    if lang == "php":
        lexer = PhpLexer(startinline=False)
    body = highlight(text.rstrip("\n"), lexer, FMT)
    n = text.rstrip("\n").count("\n") + 1
    right = note if note else f"{n} บรรทัด"
    cap = f'<div class="codecap"><span class="path">{html.escape(path)}</span><span class="lines">{right}</span></div>' if path else ""
    return f'<div class="codeblock">{cap}<pre class="hl">{body}</pre></div>'


def file_block(rel: str, lang: str = "dart") -> str:
    return code(src(rel), lang, rel, note="ไฟล์ใหม่ · คัดลอกทั้งไฟล์")


def diff_block(rel: str) -> str:
    out = subprocess.run(["git", "diff", "-U2", "--no-color", BASE_TAG, "--", rel],
                         cwd=ROOT, capture_output=True, text=True).stdout
    # ตัด header ที่ไม่จำเป็นออก เหลือแค่ hunk
    lines = out.splitlines()
    body = "\n".join(l for l in lines if not (l.startswith("diff --git") or l.startswith("index ")
                                              or l.startswith("--- ") or l.startswith("+++ ")))
    added = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
    return code(body, "diff", rel, note=f"ไฟล์เดิม · แก้ +{added} / −{removed} บรรทัด")


def box(kind: str, title: str, body: str) -> str:
    if STUDENT and kind == "teacher":
        return ""
    return f'<div class="box {kind}"><div class="boxtitle">{title}</div>{body}</div>'


def ul(*items: str) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(*items: str) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def p(t: str) -> str:
    return f"<p>{t}</p>"


def c(t: str) -> str:
    return f"<code>{html.escape(t)}</code>"


def table(headers: list[str], rows: list[list[str]]) -> str:
    h = "".join(f"<th>{x}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in r) + "</tr>" for r in rows)
    return f'<table class="tbl"><tr>{h}</tr>{b}</table>'


STEPS: list[dict] = []


def step(no: int, title: str, minutes: int, goal: str, body: str) -> None:
    STEPS.append(dict(no=no, title=title, minutes=minutes, goal=goal, body=body))


# ================================================================ STEP 12
step(12, "ตั้งต้นที่จุดเดียวกัน: ดึงโค้ดเฟส 1 จาก GitHub", 20,
     "ทุกคนมีโค้ดเฟส 1 ที่รันได้เหมือนกัน และเปิด XAMPP (Apache + MySQL) ได้",
     p("คนที่ทำเฟส 1 ไม่ทัน หรือโค้ดมีปัญหา ให้ใช้โค้ดจาก GitHub แทนของตัวเองได้เลย รีโปมี <b>tag</b> ชื่อ "
       + c("phase1-ui") + " คือจุดจบของเฟส 1 พอดี")
     + "<h3>วิธีที่ 1: ดาวน์โหลด ZIP (ไม่ต้องใช้ git)</h3>"
     + ol(f"ดาวน์โหลด <b>{REPO}/archive/refs/tags/phase1-ui.zip</b>",
          "แตกไฟล์ จะได้โฟลเดอร์ App1-phase1-ui ให้เปลี่ยนชื่อเป็น " + c("labstock"),
          "เปิดโฟลเดอร์ใน VS Code แล้วรัน " + c("flutter pub get") + " และ " + c("flutter run"))
     + "<h3>วิธีที่ 2: ใช้ git (แนะนำ จะได้ดึงโค้ดขั้นถัดไปได้ง่าย)</h3>"
     + code(f"git clone {REPO}.git labstock\ncd labstock\ngit checkout phase1-ui      # ไปยังจุดจบเฟส 1\nflutter pub get\nflutter run", "bash")
     + p("ระหว่างทำเฟส 2 ถ้าอยากดูโค้ดของขั้นไหน ให้เปิดหน้า <b>compare</b> บน GitHub จะเห็นว่าแต่ละไฟล์ต้องแก้บรรทัดไหน (สีเขียว = เพิ่ม, สีแดง = ลบ):")
     + code(f"{REPO}/compare/phase1-ui...phase2-mysql", "bash")
     + box("warn", "ถ้า pub get ขึ้นว่า requires SDK version ^3.9.2",
           p("แปลว่า Flutter ในเครื่องเก่ากว่าที่โปรเจกต์ใช้ ให้รัน " + c("flutter upgrade") + " (ใช้เน็ต 5–10 นาที) แล้วตรวจด้วย " + c("flutter --version") + " ต้องได้ 3.35 ขึ้นไป ถ้ายังเก่าอยู่ให้ " + c("flutter channel stable && flutter upgrade") + " อย่าแก้เลขเวอร์ชันใน pubspec.yaml เพราะโค้ดจะไปพังที่อื่นแทน"))
     + "<h3>เปิด XAMPP</h3>"
     + ol("เปิด XAMPP Control Panel → Start <b>Apache</b> และ <b>MySQL</b> (ทั้งสองต้องเป็นสีเขียว)",
          "เปิดเบราว์เซอร์ไปที่ " + c("http://localhost/phpmyadmin") + " ต้องเห็นหน้า phpMyAdmin",
          "โฟลเดอร์เว็บของ XAMPP คือ " + c("C:\\xampp\\htdocs") + " (Windows) หรือ " + c("/Applications/XAMPP/htdocs") + " (Mac)")
     + box("check", "Checkpoint",
           ul("แอปเฟส 1 รันได้ login ด้วยชื่ออะไรก็ได้ เห็นการ์ดอุปกรณ์ 8 ใบ",
              "phpMyAdmin เปิดได้",
              "รู้ว่าโฟลเดอร์ htdocs อยู่ที่ไหน"))
     + box("teacher", "สำหรับผู้สอน",
           ul("MySQL ใน XAMPP สตาร์ตไม่ขึ้น มักเพราะพอร์ต 3306 ถูกใช้โดย MySQL ตัวอื่นที่ติดตั้งไว้ตอนเรียนวิชาฐานข้อมูล ให้ปิด service นั้นก่อน หรือเปลี่ยนพอร์ตใน my.ini แล้วแก้ " + c("DB_PORT") + " ใน config.php ตาม",
              "Apache ไม่ขึ้นเพราะพอร์ต 80 ชนกับ Skype/IIS ให้เปลี่ยนเป็น 8080 แล้วแก้ URL ในแอปเป็น " + c("http://localhost:8080/labstock/api"),
              "ให้นักศึกษาที่ทำเฟส 1 เองสำเร็จ ยังคงใช้โค้ดตัวเองได้ แต่ถ้าติดตอน Step 16 ให้สลับมาใช้โค้ดจาก GitHub ทันที อย่าเสียเวลาดีบักของเก่า")))

# ================================================================ STEP 13
step(13, "สร้างฐานข้อมูล MySQL", 40,
     "มีฐานข้อมูล labstock 3 ตาราง (users, items, borrows) พร้อมข้อมูลเริ่มต้น และอธิบายความสัมพันธ์ได้",
     p("โมเดล 3 ตัวที่เขียนใน Dart ตอนเฟส 1 (AppUser, Equipment, Borrow) ตอนนี้จะกลายเป็นตาราง 3 ตาราง คอลัมน์ตั้งชื่อแบบ snake_case ตามธรรมเนียม SQL (" + c("student_id") + ") ส่วน Dart ใช้ camelCase (" + c("studentId") + ") ตอนแปลง JSON จะต้องจับคู่กัน")
     + box("learn", "ความรู้ที่ทบทวนจากวิชาฐานข้อมูล",
           ul("PRIMARY KEY + AUTO_INCREMENT", "FOREIGN KEY (borrows → users, items)",
              "ENUM สำหรับค่าที่มีตัวเลือกจำกัด (role, category)",
              "utf8mb4 เพื่อเก็บภาษาไทยและอีโมจิ",
              "ไม่เก็บรหัสผ่านจริง เก็บ " + c("password_hash") + " ที่ PHP สร้างด้วย bcrypt",
              "DATE_ADD(CURDATE(), ...) สร้างข้อมูลทดสอบที่สัมพันธ์กับวันนี้"))
     + "<h3>1) นำเข้าไฟล์ SQL</h3>"
     + ol("ดาวน์โหลด " + c("server/labstock.sql") + " จาก GitHub",
          "phpMyAdmin → แท็บ <b>Import</b> → เลือกไฟล์ → กด Go (ไฟล์มีคำสั่ง CREATE DATABASE ให้แล้ว)",
          "ดูซ้ายมือ ต้องมีฐานข้อมูล <b>labstock</b> และตาราง users / items / borrows")
     + "<h3>2) โครงสร้างและข้อมูลเริ่มต้น</h3>"
     + file_block("server/labstock.sql", "sql")
     + "<h3>3) ความสัมพันธ์</h3>"
     + code("""users (1) ──< borrows (n) >── (1) items
  id                user_id      id
  username          item_id      name
  password_hash     quantity     category
  name              borrow_date  total
  student_id        due_date     available   ← ลดเมื่อยืม เพิ่มเมื่อคืน
  role              return_date  description (NULL = ยังไม่คืน)""", "bash", "ER แบบย่อ")
     + box("check", "Checkpoint",
           ul("phpMyAdmin → labstock → users มี 3 แถว (admin, somchai, somsri)",
              "items มี 8 แถว · borrows มี 4 แถว",
              "ลองรัน SQL: " + c("SELECT b.*, i.name FROM borrows b JOIN items i ON i.id=b.item_id WHERE return_date IS NULL") + " ต้องได้ 2 แถว",
              "ตอบได้: ทำไม available ต้องเป็นคอลัมน์แยกจาก total"))
     + box("challenge", "ท้าทาย", ul("เพิ่มนักศึกษาอีก 1 คนด้วย INSERT (ใช้ password_hash ตัวเดียวกับ somchai ก็ได้ = รหัส 1234)",
                                    "เขียน SQL หาว่าอุปกรณ์ชิ้นไหนถูกยืมมากที่สุด")))

# ================================================================ STEP 14
step(14, "สร้าง REST API ด้วย PHP", 70,
     "วาง PHP 7 ไฟล์ใน htdocs แล้วเรียกผ่านเบราว์เซอร์/curl ได้ JSON ครบทุก endpoint",
     p("แอปมือถือไม่ควรต่อ MySQL ตรง ๆ (เปิดพอร์ตฐานข้อมูลสู่อินเทอร์เน็ตอันตราย และโฮสต์ส่วนใหญ่ไม่อนุญาต) จึงต้องมี <b>ตัวกลาง</b> คือ PHP ที่รับคำขอ HTTP → คุยกับ MySQL → ตอบกลับเป็น JSON แอปเรียก PHP ผ่าน URL เหมือนเปิดเว็บ")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("REST: ใช้ HTTP method บอกความหมาย GET = อ่าน · POST = สร้าง · PUT = แก้ไข",
              "รูปแบบคำตอบเดียวกันทุก endpoint: " + c('{"ok":true,"data":...}') + " หรือ " + c('{"ok":false,"error":"..."}'),
              "PDO + prepared statement (เครื่องหมาย ?) ป้องกัน SQL injection",
              c("password_hash") + " / " + c("password_verify"),
              "Transaction (beginTransaction / commit / rollBack) สำหรับการยืมที่ต้องแก้ 2 ตารางพร้อมกัน",
              "header CORS และ Content-Type: application/json"))
     + "<h3>1) วางไฟล์</h3>"
     + p("สร้างโฟลเดอร์ " + c("htdocs/labstock/api") + " แล้วคัดลอก 7 ไฟล์จาก " + c("server/api/") + " บน GitHub ไปไว้ทั้งหมด จากนั้นเปิด "
         + c("http://localhost/labstock/api/index.php") + " ต้องเห็น JSON ที่นับจำนวนแถวได้")
     + code("htdocs/\n└─ labstock/\n   └─ api/\n      ├─ config.php     ← ค่าเชื่อมต่อ (แก้ไฟล์นี้ไฟล์เดียวเมื่อย้ายโฮสต์)\n      ├─ db.php         ← เชื่อม PDO + ฟังก์ชัน json_ok / json_error / input\n      ├─ index.php      ← หน้าเช็กสถานะ\n      ├─ login.php      ← POST\n      ├─ register.php   ← POST\n      ├─ items.php      ← GET / POST / PUT\n      └─ borrows.php    ← GET / POST / PUT", "bash", "โครงสร้างบนเซิร์ฟเวอร์")
     + "<h3>2) config.php และ db.php (โครงพื้นฐาน)</h3>"
     + file_block("server/api/config.php", "php")
     + file_block("server/api/db.php", "php")
     + p("สังเกต: ทุก endpoint จะเริ่มด้วย " + c("require_once __DIR__ . '/db.php';") + " แล้วได้ตัวแปร " + c("$pdo") + " กับฟังก์ชันช่วยมาใช้ทันที")
     + "<h3>3) index.php</h3>" + file_block("server/api/index.php", "php")
     + "<h3>4) login.php และ register.php</h3>"
     + file_block("server/api/login.php", "php")
     + file_block("server/api/register.php", "php")
     + "<h3>5) items.php</h3>" + file_block("server/api/items.php", "php")
     + "<h3>6) borrows.php (มี Transaction)</h3>" + file_block("server/api/borrows.php", "php")
     + "<h3>7) ทดสอบ</h3>"
     + p("GET ทดสอบในเบราว์เซอร์ได้เลย ส่วน POST/PUT ใช้ curl (มีใน Windows 10+ และ Mac) หรือ extension Thunder Client ใน VS Code")
     + code("""# เปิดในเบราว์เซอร์
http://localhost/labstock/api/index.php
http://localhost/labstock/api/items.php
http://localhost/labstock/api/borrows.php?user_id=2

# curl (Windows: ใช้ PowerShell หรือ cmd)
curl -X POST http://localhost/labstock/api/login.php -H "Content-Type: application/json" -d "{\\"username\\":\\"somchai\\",\\"password\\":\\"1234\\"}"

curl -X POST http://localhost/labstock/api/borrows.php -H "Content-Type: application/json" -d "{\\"user_id\\":2,\\"item_id\\":1,\\"quantity\\":1,\\"due_date\\":\\"2026-10-15\\"}"

curl -X PUT http://localhost/labstock/api/borrows.php -H "Content-Type: application/json" -d "{\\"id\\":5}\"""", "bash", "ทดสอบ API")
     + code('''{"ok":true,"data":{"id":2,"username":"somchai","name":"สมชาย ใจดี","student_id":"674659001","role":"student"}}

{"ok":false,"error":"ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"}        ← HTTP 401

{"ok":false,"error":"จำนวนคงเหลือไม่พอ"}                       ← HTTP 400''', "json", "ตัวอย่างคำตอบ")
     + box("check", "Checkpoint",
           ul("index.php แสดง rows: users 3, items 8, borrows 4",
              "items.php ได้ JSON 8 ชิ้น ภาษาไทยอ่านได้ (ไม่เป็น ???)",
              "login ด้วย somchai/1234 ได้ ok:true · รหัสผิดได้ ok:false",
              "ยืม Arduino 1 ชิ้นแล้วเปิด items.php?id=1 เห็น available ลดลง 1 · คืนแล้วกลับมาเท่าเดิม",
              "ยืม DHT22 (available 0) ต้องได้ error \"จำนวนคงเหลือไม่พอ\""))
     + box("teacher", "สำหรับผู้สอน",
           ul("ให้ดูใน phpMyAdmin คู่กันทุกครั้งที่ curl เพื่อเชื่อม \"คำขอ HTTP\" กับ \"แถวในตาราง\"",
              "ถ้าเห็น HTML แทน JSON แปลว่า PHP error ให้เปิด URL นั้นในเบราว์เซอร์จะเห็นข้อความ error ชัดกว่า",
              "ถามชวนคิด: ถ้าไม่มี transaction แล้วไฟดับหลัง UPDATE items แต่ก่อน INSERT borrows จะเกิดอะไร",
              "ข้อจำกัดที่ต้องบอกตรง ๆ: API นี้ยังไม่มี token ใครก็ส่ง user_id ของคนอื่นได้ เป็นเรื่องของเฟส 3")))

# ================================================================ STEP 15
step(15, "ฝั่ง Flutter: ApiService และการแปลง JSON", 60,
     "แอปมีชั้น ApiService ที่เรียก API ได้ทุก endpoint และโมเดลแปลง JSON ↔ object ได้",
     p("ตอนนี้เราจะเพิ่ม \"ชั้นเครือข่าย\" เข้าไปโดย<b>ยังไม่แตะหน้าจอ</b> ไฟล์ใหม่ 2 ไฟล์ + แก้โมเดล 3 ไฟล์เล็กน้อย + ตั้งค่าสิทธิ์อินเทอร์เน็ต")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("package " + c("http") + ": " + c("http.get / post / put") + " คืน " + c("Future<Response>"),
              c("jsonEncode / jsonDecode") + " และ " + c("utf8.decode(res.bodyBytes)") + " (สำคัญกับภาษาไทย)",
              "factory constructor " + c("fromJson") + " และเมธอด " + c("toJson"),
              "Exception ที่กำหนดเอง (" + c("ApiException") + ") เพื่อส่งข้อความผิดพลาดจากเซิร์ฟเวอร์ถึงหน้าจอ",
              c("timeout") + " และการดัก " + c("ClientException"),
              "Android Emulator ใช้ 10.0.2.2 แทน localhost · Android 9+ และ iOS บล็อก http ธรรมดา ต้องเปิดใน manifest/plist"))
     + "<h3>1) ติดตั้ง package</h3>" + code("flutter pub add http", "bash")
     + "<h3>2) lib/data/api_config.dart (ไฟล์ใหม่)</h3>" + file_block("lib/data/api_config.dart")
     + "<h3>3) lib/data/api_service.dart (ไฟล์ใหม่)</h3>" + file_block("lib/data/api_service.dart")
     + p("ทุกเมธอดเรียก " + c("_send") + " ตัวเดียว ซึ่งจัดการ URL, header, timeout, แปลง JSON และเช็ก " + c("ok") + " ให้ หน้าจอจึงไม่ต้องรู้เรื่อง HTTP เลย")
     + "<h3>4) แก้โมเดล 3 ไฟล์ — เพิ่ม fromJson / toJson</h3>"
     + diff_block("lib/models/user.dart")
     + diff_block("lib/models/equipment.dart")
     + diff_block("lib/models/borrow.dart")
     + p("ข้อสังเกต: id จากเซิร์ฟเวอร์เป็นตัวเลข แต่โมเดลของเราใช้ String จึงแปลงด้วย " + c("'${json['id']}'") + " เพื่อไม่ต้องแก้ทั้งแอป")
     + "<h3>5) อนุญาตให้แอปใช้อินเทอร์เน็ตแบบ http</h3>"
     + diff_block("android/app/src/main/AndroidManifest.xml")
     + diff_block("ios/Runner/Info.plist")
     + box("check", "Checkpoint",
           ul(c("flutter analyze") + " → No issues found! (แอปยังทำงานเหมือนเดิม เพราะยังไม่ได้ใช้ ApiService)",
              "อธิบายได้ว่า " + c("apiBase") + " จะเป็นค่าอะไรบน Android Emulator, iOS Simulator และมือถือจริง",
              "อธิบายได้ว่าทำไมต้องใช้ " + c("utf8.decode(res.bodyBytes)") + " แทน " + c("res.body")))
     + box("teacher", "สำหรับผู้สอน",
           ul("ให้เปิด items.php ในเบราว์เซอร์ค้างไว้ข้าง ๆ โค้ด fromJson แล้วชี้ทีละ key ว่าไปลง field ไหน",
              "ย้ำเรื่อง URL 3 แบบ (localhost / 10.0.2.2 / IP วง LAN) เป็นจุดที่นักศึกษาติดมากที่สุดในคาบนี้")))

# ================================================================ STEP 16
step(16, "เปลี่ยน AppState ไปใช้ API และปรับหน้าจอ", 80,
     "แอปทำงานกับข้อมูลจริงใน MySQL ครบทุก flow: login, รายการ, ยืม, คืน, เพิ่ม/แก้ไข, สมัครสมาชิก",
     p("นี่คือขั้นที่เห็นผล เปลี่ยน " + c("AppState") + " จาก \"เก็บ list ในหน่วยความจำ\" เป็น \"เรียก ApiService แล้วเก็บผลลัพธ์\" เมธอดชื่อเดิมทั้งหมดแต่กลายเป็น " + c("Future") + " หน้าจอจึงต้องเติม " + c("await") + " และดัก " + c("ApiException"))
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("async/await ในเมธอดของ StatefulWidget และการเช็ก " + c("mounted") + " หลัง await",
              "แพตเทิร์น loading: " + c("setState(() => _busy = true)") + " → try/await → finally reset",
              "แสดง 3 สถานะ: กำลังโหลด / ผิดพลาด+ลองใหม่ / ข้อมูล",
              c("RefreshIndicator") + " ดึงลงเพื่อโหลดใหม่",
              "หลังเขียนข้อมูลให้ " + c("refresh()") + " ดึงจากเซิร์ฟเวอร์ใหม่ทั้งหมด = เซิร์ฟเวอร์เป็น single source of truth",
              "ทดสอบโดยไม่ต้องมีเซิร์ฟเวอร์ด้วยการ inject " + c("FakeApiService")))
     + "<h3>1) lib/data/app_state.dart (แทนที่ทั้งไฟล์)</h3>" + file_block("lib/data/app_state.dart")
     + p("เทียบกับเฟส 1: " + c("login") + " ไม่ได้เช็กชื่อขึ้นต้นด้วย admin แล้ว แต่ให้เซิร์ฟเวอร์ตัดสิน · ทุกเมธอดที่เขียนข้อมูลจบด้วย " + c("await refresh()"))
     + "<h3>2) แก้หน้าจอ — ดู diff แล้วแก้ตามเฉพาะบรรทัดสีเขียว/แดง</h3>"
     + p("<b>login_screen.dart</b> — เพิ่ม _busy, เปลี่ยน _login เป็น async, ปุ่มแสดงวงกลมหมุนตอนรอ")
     + diff_block("lib/screens/login_screen.dart")
     + p("<b>equipment_list_screen.dart</b> — เพิ่มปุ่มโหลดใหม่, RefreshIndicator และ _buildGrid ที่แสดงสถานะโหลด/ผิดพลาด")
     + diff_block("lib/screens/equipment_list_screen.dart")
     + p("<b>equipment_detail_screen.dart</b> — await borrow และดัก ApiException")
     + diff_block("lib/screens/equipment_detail_screen.dart")
     + p("<b>my_borrows_screen.dart</b> — RefreshIndicator และ await returnItem")
     + diff_block("lib/screens/my_borrows_screen.dart")
     + p("<b>equipment_form_screen.dart</b> — _saving และ await add/update (id ให้เซิร์ฟเวอร์กำหนด)")
     + diff_block("lib/screens/equipment_form_screen.dart")
     + p("<b>register_screen.dart</b> — เฟส 1 ยังไม่มี controller เลย จึงแทนที่ทั้งไฟล์ง่ายกว่า")
     + file_block("lib/screens/register_screen.dart")
     + p("<b>widgets/equipment_image.dart</b> — รองรับ URL รูปจากเซิร์ฟเวอร์ และไม่พังถ้า path ในเครื่องไม่มีจริง")
     + diff_block("lib/widgets/equipment_image.dart")
     + "<h3>3) ทดสอบอัตโนมัติด้วย API ปลอม</h3>"
     + file_block("test/widget_test.dart")
     + code("flutter analyze\nflutter test\nflutter run", "bash")
     + box("check", "Checkpoint (ต้องเปิด XAMPP ก่อน)",
           ul("login somchai/1234 ได้ · รหัสผิดเห็นข้อความจากเซิร์ฟเวอร์ \"ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง\"",
              "หน้ารายการโหลดจาก MySQL (ลองแก้ชื่ออุปกรณ์ใน phpMyAdmin แล้วดึงลงรีเฟรช ต้องเปลี่ยนตาม)",
              "ยืม Arduino → phpMyAdmin ตาราง borrows มีแถวใหม่ และ items.available ลด",
              "คืนของ → return_date มีค่า และ available กลับมา",
              "login admin/1234 → เพิ่มอุปกรณ์ → เห็นในตาราง items",
              "สมัครสมาชิกใหม่ → login ด้วยบัญชีนั้นได้",
              "ปิด MySQL แล้วเปิดแอป → เห็นหน้า \"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้\" พร้อมปุ่มลองใหม่ ไม่ crash",
              c("flutter test") + " → All tests passed! (ผ่านแม้ไม่เปิดเซิร์ฟเวอร์ เพราะใช้ FakeApiService)"))
     + box("teacher", "สำหรับผู้สอน",
           ul("แบ่งเป็น 2 รอบ: รอบแรก app_state + login + list (เห็นข้อมูลจริงขึ้นจอ = กำลังใจ) รอบสองที่เหลือ",
              "ให้จับคู่: คนหนึ่งเปิด phpMyAdmin คนหนึ่งกดแอป แล้วเล่าให้กันฟังว่าตารางเปลี่ยนอย่างไร",
              "error ที่พบบ่อยสุด: (1) ลืม await เลยไม่เห็น error (2) ใช้ context หลัง await โดยไม่เช็ก mounted (3) URL ผิดแพลตฟอร์ม")))

# ================================================================ STEP 17
step(17, "นำขึ้นโฮสต์จริง และก้าวต่อไป", 40,
     "เข้าใจข้อจำกัดของโฮสต์ฟรี นำ API ขึ้นโฮสต์ที่รองรับแอปมือถือได้ และเห็นภาพเฟส 3",
     box("warn", "คำเตือนสำคัญเรื่อง InfinityFree",
         p("InfinityFree (และโฮสต์ฟรีในเครือ iFastNet เช่น Byet, ProFreeHost) มี <b>ระบบตรวจสอบเบราว์เซอร์</b> ที่ต้องรัน JavaScript (aes.js) และเก็บคุกกี้ก่อนจึงจะเข้าถึงไฟล์ PHP ได้ "
           "แอป Flutter ไม่ใช่เบราว์เซอร์ จึงได้รับหน้า HTML แทน JSON ทุกครั้ง เอกสารของ InfinityFree ระบุตรง ๆ ว่า "
           "<i>\"Android or iOS mobile apps cannot connect to your website\"</i> และ <i>\"REST APIs ... are blocked\"</i> "
           "ต้องซื้อ premium (iFastNet) จึงจะปลดล็อก จึง<b>ไม่แนะนำ</b>ให้ใช้กับวิชานี้ ในแอปของเรา error จะขึ้นว่า \"เซิร์ฟเวอร์ตอบไม่ใช่ JSON\"")
         + p("ทางเลือกที่ทดสอบแนวคิดแล้วว่าเข้ากับแอปมือถือ: <b>XAMPP ในเครื่อง</b> (เหมาะกับในห้องเรียน ไม่พึ่งอินเทอร์เน็ต) และโฮสต์ฟรี <b>AlwaysData</b> (PHP + MySQL + HTTPS ไม่มีระบบตรวจเบราว์เซอร์) สำหรับส่งงานหรือลองใช้จากมือถือจริงนอกวง LAN"))
     + "<h3>1) ใช้จากมือถือจริงในห้อง (วง Wi-Fi เดียวกับคอม)</h3>"
     + ol("หา IP ของคอม: Windows " + c("ipconfig") + " (IPv4 Address) · Mac " + c("ifconfig en0"),
          "Windows: อนุญาต Apache ผ่าน Firewall (ครั้งแรกจะมี popup ตอนสตาร์ต Apache ให้กด Allow)",
          "ทดสอบจากเบราว์เซอร์มือถือ: " + c("http://192.168.x.x/labstock/api/index.php"),
          "แก้ " + c("kApiBase") + " ใน api_config.dart เป็น IP นั้น แล้วรันแอปบนมือถือ")
     + "<h3>2) นำขึ้น AlwaysData (ฟรี)</h3>"
     + ol("สมัครที่ alwaysdata.com เลือกแผนฟรี ตั้งชื่อบัญชี เช่น " + c("labstock-somchai") + " จะได้เว็บ " + c("https://labstock-somchai.alwaysdata.net"),
          "แผงควบคุม → Databases → MySQL → สร้างฐานข้อมูล (ชื่อจะขึ้นต้นด้วยชื่อบัญชี_) และผู้ใช้ฐานข้อมูล",
          "เปิด phpMyAdmin ของ AlwaysData → Import " + c("labstock.sql") + " <b>โดยลบ 2 บรรทัดแรก (CREATE DATABASE / USE) ออกก่อน</b> เพราะชื่อฐานข้อมูลไม่ใช่ labstock",
          "อัปโหลดโฟลเดอร์ api ไปที่ " + c("www/api") + " ผ่าน FTP (FileZilla) หรือ File manager",
          "แก้ config.php: DB_HOST = " + c("mysql-ชื่อบัญชี.alwaysdata.net") + " DB_NAME / DB_USER / DB_PASS ตามที่สร้าง",
          "เปิด " + c("https://ชื่อบัญชี.alwaysdata.net/api/index.php") + " ต้องได้ JSON",
          "แก้ " + c("kApiBase") + " ในแอปเป็น URL นั้น (https ไม่ต้องตั้งค่า cleartext ใด ๆ)")
     + "<h3>3) สรุปสถาปัตยกรรมที่ได้</h3>"
     + code("""Flutter (หน้าจอ) ──> AppState ──> ApiService ──HTTP/JSON──> PHP (api/*.php) ──PDO──> MySQL
                                              ▲                                    ▲
                                   เปลี่ยนแค่ kApiBase                   เปลี่ยนแค่ config.php
                                   เมื่อย้ายเซิร์ฟเวอร์                  เมื่อย้ายฐานข้อมูล""", "bash", "ภาพรวม")
     + "<h3>4) เฟส 3 (ท้าทาย / โปรเจกต์)</h3>"
     + ol("<b>Token</b>: login แล้วเซิร์ฟเวอร์ออก token สุ่ม เก็บในตาราง users ทุกคำขอต้องส่ง header Authorization และเซิร์ฟเวอร์ตรวจว่า user_id ตรงกับ token",
          "<b>จำการเข้าสู่ระบบ</b>: เก็บ user ด้วย " + c("shared_preferences") + " เปิดแอปครั้งถัดไปข้ามหน้า Login",
          "<b>อัปโหลดรูป</b>: เพิ่ม upload.php รับไฟล์ (multipart) บันทึกใน htdocs/labstock/uploads แล้วคืน URL → image_url",
          "<b>หน้าแอดมิน</b>: GET borrows.php ทั้งหมด (ไม่ระบุ user_id) พร้อมชื่อผู้ยืม แสดงเป็นตารางให้แอดมิน",
          "<b>แจ้งเตือน</b>: endpoint นับรายการที่จะครบกำหนดใน 3 วัน แสดงตัวเลขบนกระดิ่ง"))

# ================================================================ HTML
CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'TH Sarabun New', 'TH SarabunPSK', 'Sarabun', sans-serif; font-size: 16pt; line-height: 1.35; color: #1a1a1a; margin: 0; }
h1, h2, h3 { color: #283593; margin: 0.6em 0 0.3em; line-height: 1.2; }
h1 { font-size: 30pt; } h2 { font-size: 24pt; border-bottom: 2px solid #283593; padding-bottom: 4px; margin-top: 1em; } h3 { font-size: 19pt; color: #1f2a80; }
p { margin: 0.35em 0 0.6em; } ul, ol { margin: 0.2em 0 0.7em; padding-left: 1.5em; } li { margin: 0.12em 0; }
code { font-family: Menlo, 'SF Mono', Consolas, monospace; font-size: 10.5pt; background: #eef0f7; padding: 1px 5px; border-radius: 4px; }
.codeblock { margin: 0.5em 0 0.9em; border: 1px solid #d5d8e5; border-radius: 6px; overflow: hidden; }
.codecap { display: flex; justify-content: space-between; background: #283593; color: #fff; font-family: Menlo, monospace; font-size: 10pt; padding: 4px 10px; }
.codecap .lines { opacity: 0.85; }
pre.hl { margin: 0; padding: 8px 10px; font-family: Menlo, 'SF Mono', Consolas, monospace; font-size: 9.6pt; line-height: 1.32; white-space: pre-wrap; word-break: break-all; background: #f7f8fc; }
pre.hl .gi { background: #dcf5dc; color: #0b5a0b; display: inline-block; width: 100%; } pre.hl .gd { background: #fde0e0; color: #8a0000; display: inline-block; width: 100%; }
pre.hl .gu { color: #6a1b9a; font-weight: bold; }
.box { border-left: 6px solid; border-radius: 6px; padding: 8px 14px 6px; margin: 0.8em 0; page-break-inside: avoid; }
.box .boxtitle { font-weight: bold; font-size: 17pt; margin-bottom: 2px; } .box ul, .box ol { margin-bottom: 0.3em; }
.box.learn { border-color: #03a9f4; background: #e8f6fd; } .box.learn .boxtitle { color: #01579b; }
.box.check { border-color: #2e7d32; background: #eaf5ea; } .box.check .boxtitle { color: #1b5e20; } .box.check .boxtitle::before { content: '✔ '; }
.box.teacher { border-color: #6a1b9a; background: #f3e9f8; } .box.teacher .boxtitle { color: #4a148c; }
.box.challenge { border-color: #ffb300; background: #fff7e0; } .box.challenge .boxtitle { color: #8d5a00; }
.box.warn { border-color: #d32f2f; background: #fdecea; } .box.warn .boxtitle { color: #b71c1c; }
.step { page-break-before: always; }
.stephead { background: #283593; color: #fff; padding: 12px 18px; border-radius: 8px; margin-bottom: 10px; }
.stephead .no { font-size: 13pt; letter-spacing: 1px; opacity: 0.85; } .stephead h1 { color: #fff; margin: 0; font-size: 26pt; } .stephead .meta { font-size: 14pt; opacity: 0.9; margin-top: 4px; }
.goal { border: 1px dashed #283593; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; } .goal b { color: #283593; }
table.tbl { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; font-size: 15pt; }
table.tbl th, table.tbl td { border: 1px solid #c9ccd9; padding: 4px 8px; vertical-align: top; } table.tbl th { background: #e8eaf6; color: #283593; text-align: left; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .band { background: #283593; color: #fff; padding: 30px 36px; border-radius: 14px; }
.cover .band .sup { font-size: 16pt; opacity: 0.85; } .cover .band h1 { color: #fff; font-size: 40pt; margin: 4px 0; } .cover .band .sub { font-size: 22pt; }
.cover .info { margin-top: 26px; font-size: 17pt; line-height: 1.6; } .cover .accent { height: 8px; background: linear-gradient(90deg, #ffb300, #03a9f4); border-radius: 4px; margin-top: 18px; }
.small { font-size: 13pt; color: #555; }
"""

H: list[str] = []
H.append("<!DOCTYPE html><html lang='th'><head><meta charset='utf-8'><title>LabStock คู่มือเฟส 2</title>")
H.append("<style>" + CSS + FMT.get_style_defs(".hl") + "</style></head><body>")

H.append(f"""
<div class="cover">
  <div class="band">
    <div class="sup">คู่มือปฏิบัติการ · รายวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่</div>
    <h1>LabStock เฟส 2</h1>
    <div class="sub">เชื่อมต่อฐานข้อมูล MySQL ผ่าน REST API (PHP)</div>
  </div>
  <div class="accent"></div>
  <div class="info">
    <b>{"ฉบับนักศึกษา · " if STUDENT else ""}ต่อจากเฟส 1 (Step 0–11)</b> · Step 12–17 · ประมาณ 5 คาบ<br>
    เปลี่ยนข้อมูลจำลองในหน่วยความจำให้เป็นฐานข้อมูลจริง โดยหน้าจอแทบไม่ต้องแก้<br>
    <span class="small">Flutter 3.35 · PHP 8 · MySQL/MariaDB (XAMPP) · โค้ดทั้งหมดที่ {REPO} · ปรับปรุง {TODAY_TH}</span>
  </div>
</div>
""")

TROUBLE = table(["อาการ", "สาเหตุ", "แก้"], [
    ["แอปขึ้น \"เชื่อมต่อเซิร์ฟเวอร์ไม่ได้\" บน Android Emulator", "ใช้ localhost ซึ่งหมายถึงตัว emulator เอง", "ใช้ 10.0.2.2 (api_config.dart ทำให้อัตโนมัติ ตรวจว่า kApiBase ยังเป็น localhost)"],
    ["มือถือจริงต่อไม่ได้ แต่ emulator ได้", "Firewall ของ Windows บล็อก Apache หรือมือถือคนละ Wi-Fi", "อนุญาต Apache ใน Firewall · เช็ก IP ด้วยเบราว์เซอร์มือถือก่อน"],
    ["Android ขึ้น CLEARTEXT communication not permitted", "Android 9+ ห้าม http", "เพิ่ม usesCleartextTraffic=\"true\" ใน AndroidManifest (Step 15)"],
    ["iOS ขึ้น App Transport Security", "iOS ห้าม http", "เพิ่ม NSAllowsArbitraryLoads ใน Info.plist (Step 15)"],
    ["\"เซิร์ฟเวอร์ตอบไม่ใช่ JSON\"", "PHP error (HTML) · path ผิด (404) · หรือโฮสต์ฟรีมีระบบตรวจเบราว์เซอร์", "เปิด URL เดียวกันในเบราว์เซอร์ดูข้อความจริง"],
    ["ภาษาไทยใน JSON เป็น ??? หรือ à¸", "ฐานข้อมูลไม่ใช่ utf8mb4 หรืออ่าน res.body", "import ด้วยไฟล์ที่ให้ (utf8mb4) · ใช้ utf8.decode(res.bodyBytes)"],
    ["MySQL ใน XAMPP สตาร์ตไม่ขึ้น", "พอร์ต 3306 ถูกใช้แล้ว", "ปิด MySQL service ตัวอื่น หรือเปลี่ยนพอร์ตและแก้ DB_PORT"],
    ["login ได้แต่รายการว่าง", "items.php error หรือ category ในตารางไม่ตรง enum", "เปิด items.php ในเบราว์เซอร์ · category ต้องเป็น board/sensor/cable/module/tool"],
    ["ยืมแล้วจำนวนไม่ลด", "ลืม await refresh() หรือ PUT/POST ไปไม่ถึง", "ดู log Apache หรือ print ใน _send"],
])

# ---- intro section (ต่างกันตามฉบับ)
if STUDENT:
    H.append('<div class="step"><h2>ก่อนเริ่ม: อ่านหน้านี้ก่อน</h2>')
    H.append(p("ในเฟส 1 แอป LabStock ใช้ข้อมูลจำลองที่อยู่ในหน่วยความจำ ปิดแอปแล้วหาย คนอื่นก็ไม่เห็น ในเฟส 2 เราจะย้ายข้อมูลไปไว้ใน <b>MySQL</b> จริง โดยให้ <b>PHP</b> เป็นตัวกลางรับคำขอจากแอป (REST API) แอปจึงใช้ได้หลายเครื่องพร้อมกันเหมือนแอปจริง"))
    H.append("<h3>สิ่งที่ต้องมีในเครื่อง</h3>")
    H.append(ul("Flutter <b>3.35 ขึ้นไป</b> (ตรวจด้วย " + c("flutter --version") + " ถ้าเก่ากว่าให้ " + c("flutter upgrade") + ")",
                "XAMPP (Apache + MySQL + phpMyAdmin) ตัวเดียวกับที่ใช้ตอนเรียนวิชาฐานข้อมูล",
                "VS Code หรือ Android Studio และ Git",
                "Emulator/Simulator หรือมือถือจริงที่ต่อ Wi-Fi วงเดียวกับคอม"))
    H.append("<h3>เอาโค้ดมาจากไหน</h3>")
    H.append(table(["ต้องการ", "ลิงก์ / คำสั่ง"], [
        ["โค้ดจุดเริ่มต้น (จบเฟส 1) แบบ ZIP", f"{REPO}/archive/refs/tags/phase1-ui.zip"],
        ["clone ด้วย git หรือ Android Studio (Get from VCS)", c(f"{REPO}.git") + " แล้ว " + c("git checkout phase1-ui")],
        ["ดูว่าแต่ละไฟล์ต้องแก้บรรทัดไหน", f"{REPO}/compare/phase1-ui...phase2-mysql"],
        ["ไฟล์ SQL และ PHP", f"{REPO}/tree/phase2-mysql/server"],
        ["โค้ดจบเฟส 2 (ใช้เทียบเมื่อติด)", f"{REPO}/archive/refs/tags/phase2-mysql.zip"],
    ]))
    H.append("<h3>วิธีอ่านคู่มือนี้</h3>")
    H.append(ul("แต่ละ Step มี <b>เป้าหมาย</b> → กล่องฟ้า <b>ความรู้ใหม่</b> (อ่านให้เข้าใจก่อนลงมือ) → <b>โค้ด</b> → กล่องเขียว <b>Checkpoint</b> (ต้องผ่านทุกข้อก่อนไป Step ถัดไป) → กล่องเหลือง <b>ท้าทาย</b> (ทำเมื่อเสร็จก่อนเพื่อน)",
                "กล่องโค้ดที่หัวเขียนว่า <b>ไฟล์ใหม่ · คัดลอกทั้งไฟล์</b>: สร้างไฟล์ตาม path ที่หัวกล่อง แล้วคัดลอกจาก GitHub (เปิดไฟล์ → ปุ่ม Raw → เลือกทั้งหมด) ไม่ต้องพิมพ์เอง",
                "กล่องโค้ดที่หัวเขียนว่า <b>ไฟล์เดิม · แก้ +N / −M บรรทัด</b>: เปิดไฟล์เดิมของตัวเอง แล้วแก้เฉพาะบรรทัด <span style='background:#dcf5dc'>สีเขียว (+) คือเพิ่ม</span> และ <span style='background:#fde0e0'>สีแดง (−) คือลบ</span> บรรทัดสีขาวคือบริบทให้หาตำแหน่ง",
                "ทำไม่ทันหรือพังจนแก้ไม่ไหว: ดาวน์โหลดโค้ดจบเฟส 2 มาแทน แล้วแก้แค่ " + c("kApiBase") + " ใน api_config.dart กับ " + c("config.php") + " จากนั้นค่อยย้อนกลับมาอ่านว่าแต่ละ Step ทำอะไร"))
    H.append("<h3>ลำดับที่จะทำ</h3>")
    H.append(table(["Step", "หัวข้อ", "ทำเสร็จแล้วจะได้อะไร", "นาที"],
                   [[str(s_["no"]), f"<b>{s_['title']}</b>", s_["goal"], str(s_["minutes"])] for s_ in STEPS]))
    H.append(box("challenge", "สิ่งที่ต้องส่งเมื่อจบเฟส 2",
                 ol("ภาพหน้าจอแอปหลัง login ด้วยบัญชีที่<b>สมัครเอง</b>ผ่านหน้าสมัครสมาชิก และหน้ารายการที่มีอุปกรณ์ที่ตัวเองเพิ่ม (login เป็น admin เพิ่ม)",
                    "ภาพ phpMyAdmin ตาราง borrows ที่มีแถวการยืมของบัญชีตัวเอง และหลังกดคืน return_date มีค่า",
                    "ภาพผล " + c("flutter test") + " ที่ขึ้น All tests passed!",
                    "ลิงก์รีโป GitHub ของตัวเอง หรือไฟล์ ZIP โค้ด (ไม่ต้องส่งโฟลเดอร์ build)")))
    H.append("</div>")
else:
  H.append('<div class="step"><h2>สำหรับผู้สอน: เตรียมอะไร และสอนอย่างไร</h2>')
  H.append("<h3>สิ่งที่ต้องเตรียมก่อนคาบแรกของเฟส 2</h3>")
  H.append(ol(
      f"push โค้ดขึ้น GitHub พร้อม tag <b>phase1-ui</b> และ <b>phase2-mysql</b> แล้วทดสอบเปิด {REPO}/compare/phase1-ui...phase2-mysql ว่าเห็น diff",
      "ทุกเครื่องในห้องมี XAMPP และสตาร์ต Apache + MySQL ได้ (ทดสอบก่อนคาบ 1 วัน เพราะปัญหาพอร์ตชนแก้นาน)",
      "เครื่องผู้สอน: import labstock.sql และวาง api ไว้แล้ว เปิด index.php ได้ทันทีตอนสาธิต",
      "เตรียม IP ของเครื่องผู้สอนไว้ ให้นักศึกษาที่ XAMPP มีปัญหาชี้แอปมาที่เซิร์ฟเวอร์ของผู้สอนชั่วคราว (ทุกคนอยู่วง Wi-Fi เดียวกัน) จะได้ไม่หยุดเรียน",
      "ติดตั้ง Thunder Client (VS Code) หรือใช้ curl เพื่อสาธิต POST/PUT",
      "แจ้งล่วงหน้าว่า<b>ไม่ใช้ InfinityFree</b> (ดูเหตุผลใน Step 17) ถ้าจะให้ส่งงานบนโฮสต์ ให้สมัคร AlwaysData ไว้ก่อน",
  ))
  H.append("<h3>แผนการสอน</h3>")
  H.append(table(["Step", "หัวข้อ", "เป้าหมาย", "นาที"],
                 [[str(s["no"]), f"<b>{s['title']}</b>", s["goal"], str(s["minutes"])] for s in STEPS]
                 + [["", "<b>รวม</b>", "", f"<b>{sum(s['minutes'] for s in STEPS)}</b>"]]))
  H.append("<h3>ลำดับการสอนที่แนะนำในแต่ละ Step</h3>")
  H.append(ol("<b>เห็นก่อน (5 นาที)</b> ผู้สอนสาธิตผลลัพธ์ปลายทางของ Step นั้น เช่น curl แล้วเห็นแถวเพิ่มใน phpMyAdmin",
              "<b>เข้าใจ (10–15 นาที)</b> อธิบายกล่อง \"ความรู้ใหม่\" ด้วยโค้ดจริงบนจอ ไม่ต้องอธิบายทุกบรรทัด เน้นบรรทัดที่เป็นแนวคิด",
              "<b>ทำเอง (ส่วนใหญ่ของเวลา)</b> นักศึกษาคัดลอกไฟล์ใหม่จาก GitHub และแก้ไฟล์เดิมตาม diff — ห้ามพิมพ์ตามทั้งไฟล์ เสียเวลาและผิดง่าย",
              "<b>Checkpoint (5 นาที)</b> เดินดูทีละโต๊ะตามรายการในกล่องเขียว ใครผ่านให้ทำท้าทาย ใครไม่ผ่านให้จับคู่กับคนที่ผ่าน",
              "<b>จุดที่ต้องรอทั้งห้อง</b>: จบ Step 14 (API ต้องได้ทุกคน) และจบ Step 16 รอบแรก (login + list) ก่อนไปต่อ"))
  H.append("<h3>วิธีให้นักศึกษา \"โหลดโค้ดเป็นส่วน ๆ\"</h3>")
  H.append(p("โค้ดใน GitHub แยก commit ตาม Step (Step 13, 14, 15, 16) นักศึกษาเลือกได้ 3 ระดับตามความพร้อม:"))
  H.append(table(["ระดับ", "วิธี", "เหมาะกับ"], [
      ["A ทำเอง", "อ่าน diff ในคู่มือ แล้วแก้โค้ดตัวเองทีละบรรทัด", "คนที่เฟส 1 ทำเองสำเร็จ"],
      ["B คัดลอกทีละไฟล์", f"เปิดไฟล์บน GitHub → ปุ่ม Raw → คัดลอกทั้งไฟล์ทับของเดิม (เฉพาะไฟล์ที่ Step นั้นบอก)", "คนที่ตามทันแต่พิมพ์ช้า"],
      ["C ข้ามไปจุดจบของ Step", c("git checkout <commit ของ Step>") + " หรือดาวน์โหลด ZIP ของ tag phase2-mysql แล้วแก้ค่า kApiBase / config.php อย่างเดียว", "คนที่ตามไม่ทัน ให้ไปต่อพร้อมเพื่อนก่อน แล้วค่อยย้อนอ่าน"],
  ]))
  H.append("<h3>ปัญหาที่พบบ่อยและวิธีแก้</h3>")
  H.append(TROUBLE)
  H.append("</div>")

for s in STEPS:
    H.append(f"""<div class="step">
<div class="stephead"><div class="no">STEP {s['no']}</div><h1>{s['title']}</h1>
<div class="meta">เวลาโดยประมาณ {s['minutes']} นาที</div></div>
<div class="goal"><b>เป้าหมาย:</b> {s['goal']}</div>
{s['body']}
</div>""")

if STUDENT:
    H.append('<div class="step"><h2>ภาคผนวก: แก้ปัญหาด้วยตัวเอง</h2>')
    H.append(p("ก่อนยกมือถาม ลองไล่ตามตารางนี้ก่อน ส่วนใหญ่แก้ได้ใน 2 นาที"))
    H.append(TROUBLE)
    H.append("</div>")
H.append("</body></html>")
OUT_HTML.write_text("".join(H), encoding="utf-8")
print("HTML:", OUT_HTML)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT_PDF_RAW}", OUT_HTML.as_uri()], check=True, capture_output=True)

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont("Sarabun", str(Path.home() / "Library/Fonts/THSarabunNew.ttf")))
reader = PdfReader(str(OUT_PDF_RAW))
writer = PdfWriter()
total = len(reader.pages)
for i, page in enumerate(reader.pages):
    if i > 0:
        buf = BytesIO()
        cv = canvas.Canvas(buf, pagesize=A4)
        cv.setFont("Sarabun", 12)
        cv.setFillColorRGB(0.35, 0.35, 0.35)
        cv.drawString(16 * 72 / 25.4, 9 * 72 / 25.4, "LabStock เฟส 2 · คู่มือปฏิบัติการ 5534408")
        cv.drawRightString(A4[0] - 16 * 72 / 25.4, 9 * 72 / 25.4, f"หน้า {i + 1} / {total}")
        cv.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
    writer.add_page(page)
writer.add_metadata({"/Title": "LabStock เฟส 2 — เชื่อมต่อ MySQL ผ่าน REST API", "/Author": "รายวิชา 5534408"})
with open(OUT_PDF, "wb") as f:
    writer.write(f)
OUT_PDF_RAW.unlink()
print(f"PDF: {OUT_PDF} ({total} pages)")
