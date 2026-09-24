#!/usr/bin/env python3
"""สร้างคู่มือปฏิบัติการ LabStock (HTML -> PDF) จากซอร์สโค้ดจริงในโฟลเดอร์ lib/"""
import base64
import html
import subprocess
from datetime import date
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import BashLexer, DartLexer, YamlLexer

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SHOTS = DOCS / "shots"
OUT_HTML = DOCS / "LabStock-คู่มือปฏิบัติการ.html"
OUT_PDF_RAW = DOCS / "_raw.pdf"
OUT_PDF = DOCS / "LabStock-คู่มือปฏิบัติการ.pdf"

FMT = HtmlFormatter(style="friendly", nowrap=True)
THAI_MONTHS = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
               "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
today = date.today()
TODAY_TH = f"{today.day} {THAI_MONTHS[today.month - 1]} {today.year + 543}"


# ---------------------------------------------------------------- helpers
def src(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def code(text: str, lang: str = "dart", path: str | None = None) -> str:
    lexer = {"dart": DartLexer, "bash": BashLexer, "yaml": YamlLexer}[lang]()
    body = highlight(text.rstrip("\n"), lexer, FMT)
    n = text.rstrip("\n").count("\n") + 1
    cap = f'<div class="codecap"><span class="path">{html.escape(path)}</span><span class="lines">{n} บรรทัด</span></div>' if path else ""
    return f'<div class="codeblock">{cap}<pre class="hl">{body}</pre></div>'


def file_block(rel: str) -> str:
    return code(src(rel), "dart", rel)


def img(name: str, caption: str, w: int = 52) -> str:
    from io import BytesIO
    from PIL import Image
    im = Image.open(SHOTS / name).convert("RGB")
    im.thumbnail((640, 1400))
    buf = BytesIO()
    im.save(buf, "JPEG", quality=82)
    data = base64.b64encode(buf.getvalue()).decode()
    return (f'<figure class="shot" style="width:{w}mm">'
            f'<img src="data:image/jpeg;base64,{data}" alt="{html.escape(caption)}">'
            f'<figcaption>{caption}</figcaption></figure>')


def figrow(*figs: str) -> str:
    return '<div class="figrow">' + "".join(figs) + "</div>"


def box(kind: str, title: str, body: str) -> str:
    return f'<div class="box {kind}"><div class="boxtitle">{title}</div>{body}</div>'


def ul(*items: str) -> str:
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(*items: str) -> str:
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def p(t: str) -> str:
    return f"<p>{t}</p>"


def c(t: str) -> str:  # inline code
    return f"<code>{html.escape(t)}</code>"


STEPS: list[dict] = []


def step(no: int, title: str, minutes: int, goal: str, body: str) -> None:
    STEPS.append(dict(no=no, title=title, minutes=minutes, goal=goal, body=body))


# ================================================================ STEP 0
step(0, "เตรียมเครื่องมือและสร้างโปรเจกต์", 30,
     "ติดตั้งและตรวจสอบ Flutter SDK, สร้างโปรเจกต์ labstock และรันแอปเริ่มต้นได้",
     p("ก่อนเริ่มเขียนโค้ด ให้นักศึกษาทุกคนตรวจสอบสภาพแวดล้อมให้พร้อม เพื่อไม่ให้ต้องเสียเวลาแก้ปัญหาการติดตั้งระหว่างคาบเรียน")
     + "<h3>1) ตรวจสอบ Flutter</h3>"
     + code("flutter --version\nflutter doctor", "bash")
     + p("ควรเห็น Flutter เวอร์ชัน 3.x และ Dart 3.x ถ้า " + c("flutter doctor") + " มีเครื่องหมาย [!] ในส่วน Android toolchain หรือ Xcode ให้แก้ตามคำแนะนำที่แสดง")
     + "<h3>2) สร้างโปรเจกต์</h3>"
     + code("flutter create --project-name labstock --org th.ac.pbru.ice labstock\ncd labstock\nflutter run", "bash")
     + p("ตัวเลือก " + c("--org") + " กำหนด bundle id เป็น th.ac.pbru.ice.labstock ซึ่งต้องไม่ซ้ำกับแอปอื่นในเครื่อง")
     + "<h3>3) ทำความรู้จักโครงสร้างโปรเจกต์</h3>"
     + ul("<b>lib/main.dart</b> จุดเริ่มต้นของแอป (ฟังก์ชัน main และ runApp)",
          "<b>pubspec.yaml</b> รายการ package ที่ใช้ และ asset ต่าง ๆ",
          "<b>android/</b>, <b>ios/</b> โค้ดเฉพาะแพลตฟอร์ม (ปกติแทบไม่ต้องแตะ)",
          "<b>test/</b> ไฟล์ทดสอบอัตโนมัติ")
     + box("check", "Checkpoint",
           ul("แอป Counter เริ่มต้นเปิดขึ้นบน Emulator/Simulator หรือ Chrome ได้",
              "กดปุ่ม + แล้วตัวเลขเพิ่ม",
              "ลองแก้ข้อความใน main.dart แล้วกด r ในเทอร์มินัล (Hot reload) เห็นผลทันที"))
     + box("teacher", "สำหรับผู้สอน",
           ul("ให้นักศึกษาสร้างโฟลเดอร์ย่อยไว้ล่วงหน้า: " + c("lib/models lib/data lib/utils lib/widgets lib/screens") + " จะช่วยลดความสับสนเรื่อง path ในขั้นถัดไป",
              "แนะนำให้ติดตั้ง VS Code extension: Flutter และ Dart",
              "ถ้าเครื่องช้า ให้รันบน Chrome ด้วย " + c("flutter run -d chrome") + " ก่อน แล้วค่อยย้ายไป Emulator ทีหลัง")))

# ================================================================ STEP 1
MAIN_TEMP = '''import 'package:flutter/material.dart';

import 'theme.dart';

void main() {
  runApp(const LabStockApp());
}

class LabStockApp extends StatelessWidget {
  const LabStockApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LabStock',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      // ชั่วคราว: จะเปลี่ยนเป็น LoginScreen ใน Step 3
      home: Scaffold(
        appBar: AppBar(title: const Text('LabStock')),
        body: const Center(child: Text('เริ่มต้น LabStock')),
      ),
    );
  }
}
'''
step(1, "ธีมสีและจุดเริ่มต้นของแอป", 40,
     "กำหนดธีม Indigo / Sky / Amber ไว้ที่เดียว และเข้าใจโครง MaterialApp → Scaffold",
     p("แอปที่ดีควรกำหนดสี ฟอนต์ และรูปทรงปุ่มไว้ที่เดียวใน " + c("ThemeData") + " แล้วให้ทุกหน้าสืบทอดไปใช้ นักศึกษาจะได้ไม่ต้องใส่สีซ้ำ ๆ ในทุก widget")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("ThemeData") + " และ " + c("ColorScheme.fromSeed") + " สร้างชุดสีทั้งระบบจากสีตั้งต้น",
              c("AppBarTheme") + ", " + c("ElevatedButtonThemeData") + ", " + c("InputDecorationTheme") + " กำหนดหน้าตาเริ่มต้นของ widget แต่ละชนิด",
              "การแยกไฟล์และ " + c("import") + " ไฟล์ในโปรเจกต์เดียวกันด้วย relative path"))
     + "<h3>1) สร้างไฟล์ lib/theme.dart</h3>" + file_block("lib/theme.dart")
     + "<h3>2) แก้ไฟล์ lib/main.dart (แทนที่ทั้งไฟล์)</h3>" + code(MAIN_TEMP, "dart", "lib/main.dart (ชั่วคราว)")
     + box("check", "Checkpoint",
           ul("AppBar เป็นสีน้ำเงินเข้ม (Indigo) ตัวอักษรขาว",
              "พื้นหลังหน้าจอเป็นสีเทาอ่อน ไม่ใช่ขาวล้วน",
              "ไม่มีป้าย DEBUG ที่มุมขวาบน"))
     + box("challenge", "ท้าทาย", ul("ลองเปลี่ยน " + c("AppColors.indigo") + " เป็นสีอื่นแล้ว Hot reload ดูว่าส่วนไหนเปลี่ยนตามบ้าง แล้วเปลี่ยนกลับ")))

# ================================================================ STEP 2
step(2, "โมเดลข้อมูลและข้อมูลจำลอง", 50,
     "ออกแบบคลาสข้อมูล 3 ตัว (User, Equipment, Borrow) และเตรียมข้อมูลจำลองสำหรับเฟส UI",
     p("ก่อนวาดหน้าจอ เราต้องตกลงกันก่อนว่า \"ข้อมูล\" ของแอปมีหน้าตาอย่างไร โครงสร้างนี้จะตรงกับตารางใน MySQL ที่จะต่อในคาบถัด ๆ ไป (users, items, borrows)")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("คลาสธรรมดาใน Dart, " + c("const") + " constructor และ named parameters " + c("required"),
              c("enum") + " แบบมีค่าประกอบ (enhanced enum) ใช้เก็บหมวดหมู่พร้อมไอคอน",
              "getter คำนวณค่า เช่น " + c("isOutOfStock") + ", " + c("daysLeft"),
              c("DateTime") + " และการคำนวณจำนวนวัน"))
     + "<h3>1) lib/models/user.dart</h3>" + file_block("lib/models/user.dart")
     + "<h3>2) lib/models/equipment.dart</h3>" + file_block("lib/models/equipment.dart")
     + p("สังเกตว่า " + c("EquipmentCategory") + " เป็น enum ที่มีทั้งข้อความภาษาไทยและไอคอน ทำให้หน้ารายการและฟอร์มใช้ค่าชุดเดียวกันโดยไม่ต้องพิมพ์ซ้ำ")
     + "<h3>3) lib/models/borrow.dart</h3>" + file_block("lib/models/borrow.dart")
     + "<h3>4) lib/utils/thai_date.dart</h3>" + file_block("lib/utils/thai_date.dart")
     + "<h3>5) lib/data/mock_data.dart</h3>" + file_block("lib/data/mock_data.dart")
     + p("ข้อมูลจำลองตั้งวันที่สัมพัทธ์กับวันนี้ (" + c("d(-5)") + " = 5 วันก่อน) เพื่อให้ป้าย \"ใกล้ครบกำหนด\" แสดงถูกต้องไม่ว่าจะเปิดแอปวันไหน")
     + box("check", "Checkpoint",
           ul("รัน " + c("flutter analyze") + " แล้วได้ No issues found!",
              "แอปยังหน้าตาเหมือน Step 1 (ขั้นนี้ยังไม่มีการเปลี่ยน UI)"))
     + box("challenge", "ท้าทาย", ul("เพิ่มอุปกรณ์จำลองอีก 2 ชิ้นในหมวด \"เครื่องมือ\"", "เพิ่มหมวดหมู่ใหม่ใน enum เช่น \"จอแสดงผล\" พร้อมไอคอน " + c("Icons.monitor"))))

# ================================================================ STEP 3
STUBS = '''// ---------- lib/screens/login_screen.dart ----------
import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('Login (TODO)')));
}

// ---------- lib/screens/register_screen.dart ----------
import 'package:flutter/material.dart';

class RegisterScreen extends StatelessWidget {
  const RegisterScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('Register (TODO)')));
}

// ---------- lib/screens/home_shell.dart ----------
import 'package:flutter/material.dart';

class HomeShell extends StatelessWidget {
  final int initialIndex;
  const HomeShell({super.key, this.initialIndex = 0});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('Home (TODO)')));
}

// ---------- lib/screens/equipment_list_screen.dart ----------
import 'package:flutter/material.dart';

class EquipmentListScreen extends StatelessWidget {
  const EquipmentListScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('List (TODO)')));
}

// ---------- lib/screens/equipment_detail_screen.dart ----------
import 'package:flutter/material.dart';

class EquipmentDetailScreen extends StatelessWidget {
  final String equipmentId;
  const EquipmentDetailScreen({super.key, required this.equipmentId});
  @override
  Widget build(BuildContext context) =>
      Scaffold(body: Center(child: Text('Detail $equipmentId (TODO)')));
}

// ---------- lib/screens/equipment_form_screen.dart ----------
import 'package:flutter/material.dart';
import '../models/equipment.dart';

class EquipmentFormScreen extends StatelessWidget {
  final Equipment? existing;
  const EquipmentFormScreen({super.key, this.existing});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('Form (TODO)')));
}

// ---------- lib/screens/my_borrows_screen.dart ----------
import 'package:flutter/material.dart';

class MyBorrowsScreen extends StatelessWidget {
  const MyBorrowsScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('My Borrows (TODO)')));
}

// ---------- lib/screens/profile_screen.dart ----------
import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});
  @override
  Widget build(BuildContext context) =>
      const Scaffold(body: Center(child: Text('Profile (TODO)')));
}
'''
step(3, "สถานะของแอป (AppState) และโครงหน้าเปล่าทุกหน้า", 50,
     "สร้างชั้นข้อมูลกลางที่ทุกหน้าใช้ร่วมกัน และสร้างไฟล์หน้าจอทั้ง 8 ไฟล์เป็นโครงเปล่า เพื่อให้ import ระหว่างหน้าไม่พัง",
     p("แอปของเรามีหลายหน้าที่ต้องเห็นข้อมูลชุดเดียวกัน (เช่น ยืมที่หน้ารายละเอียด แล้วต้องไปโผล่ที่หน้าการยืมของฉัน) จึงต้องมี \"ที่เก็บสถานะกลาง\" หนึ่งจุด ในเฟสนี้ใช้ " + c("ChangeNotifier") + " แบบ singleton ซึ่งเป็นวิธีที่ง่ายที่สุดใน Flutter โดยไม่ต้องใช้ package เพิ่ม")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("ChangeNotifier") + " + " + c("notifyListeners()") + " แจ้งให้หน้าจอที่ฟังอยู่วาดใหม่",
              "Singleton pattern: " + c("AppState.instance"),
              c("List.unmodifiable") + " ป้องกันหน้าจอแก้ list โดยตรง",
              "เทคนิค \"สร้างโครงเปล่าก่อน แล้วค่อยเติมทีละหน้า\" (stub) เพื่อให้โปรเจกต์คอมไพล์ผ่านตลอดเวลา"))
     + "<h3>1) lib/data/app_state.dart</h3>" + file_block("lib/data/app_state.dart")
     + "<h3>2) lib/widgets/equipment_image.dart</h3>" + file_block("lib/widgets/equipment_image.dart")
     + p("widget เล็ก ๆ นี้ใช้ซ้ำใน 3 หน้า (รายการ, รายละเอียด, ฟอร์ม) ถ้ายังไม่มีรูปจะแสดงไอคอนตามหมวดแทน")
     + "<h3>3) สร้างไฟล์หน้าจอทั้ง 8 ไฟล์เป็นโครงเปล่า</h3>"
     + p("สร้างไฟล์ต่อไปนี้ใน " + c("lib/screens/") + " <b>ทีละไฟล์</b> ตามชื่อในบรรทัดคอมเมนต์ (แต่ละบล็อกคือ 1 ไฟล์) ไฟล์เหล่านี้จะถูกแทนที่ด้วยโค้ดจริงใน Step 4–10")
     + code(STUBS, "dart", "lib/screens/*.dart (โครงเปล่า 8 ไฟล์)")
     + "<h3>4) เปลี่ยน main.dart ให้เปิดหน้า Login</h3>" + file_block("lib/main.dart")
     + box("check", "Checkpoint",
           ul(c("flutter analyze") + " ไม่มี error",
              "รันแอปแล้วเห็นข้อความ \"Login (TODO)\" กลางจอ"))
     + box("teacher", "สำหรับผู้สอน",
           ul("อธิบายให้เห็นภาพว่า AppState คือ \"ฐานข้อมูลชั่วคราวในหน่วยความจำ\" เมื่อต่อ MySQL จะเปลี่ยนแค่ข้างในเมธอด login / borrow / returnItem ให้ไปเรียก API แทน หน้าจอไม่ต้องแก้",
              "constructor ของ stub ต้องมีพารามิเตอร์ตรงกับของจริง (" + c("equipmentId") + ", " + c("existing") + ", " + c("initialIndex") + ") ไม่เช่นนั้นหน้าที่เขียนก่อนจะ error เมื่อเรียกใช้")))

# ================================================================ STEP 4
step(4, "หน้าเข้าสู่ระบบและสมัครสมาชิก", 60,
     "สร้างฟอร์ม Login ที่รับข้อความ ซ่อน/แสดงรหัสผ่าน และนำทางไปหน้าหลักเมื่อสำเร็จ",
     p("นี่คือหน้าแรกที่ผู้ใช้เห็น จุดสำคัญคือการรับค่าจาก " + c("TextField") + " ด้วย " + c("TextEditingController") + " และการเปลี่ยนหน้าแบบ \"แทนที่\" (" + c("pushReplacement") + ") เพื่อไม่ให้กด back กลับมาหน้า Login ได้อีก")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("StatefulWidget") + " และ " + c("setState") + " สำหรับสลับไอคอนตา (ซ่อน/แสดงรหัสผ่าน)",
              c("TextEditingController") + " และการ " + c("dispose()"),
              c("Navigator.push") + " กับ " + c("Navigator.pushReplacement") + " ต่างกันอย่างไร",
              c("Form") + " + " + c("TextFormField") + " + " + c("validator") + " สำหรับตรวจสอบข้อมูลในหน้าสมัคร",
              c("SnackBar") + " แจ้งผลสั้น ๆ",
              c("ConstrainedBox(maxWidth: 420)") + " ทำให้ฟอร์มไม่กว้างเกินไปบนแท็บเล็ต/เว็บ"))
     + "<h3>1) lib/screens/login_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/login_screen.dart")
     + "<h3>2) lib/screens/register_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/register_screen.dart")
     + box("check", "Checkpoint",
           ul("หน้า Login มีโลโก้ ชื่อแอป ช่องกรอก 2 ช่อง ปุ่ม และลิงก์สมัครสมาชิก ตามภาพ",
              "กดไอคอนตาแล้วรหัสผ่านแสดง/ซ่อนสลับกัน",
              "กดเข้าสู่ระบบโดยไม่กรอกอะไร ต้องมี SnackBar เตือน",
              "กรอกอะไรก็ได้แล้วกดเข้าสู่ระบบ ต้องไปหน้า \"Home (TODO)\"",
              "หน้าสมัครสมาชิก: กดสมัครโดยไม่กรอก ต้องเห็นข้อความแดงใต้ช่อง"))
     + figrow(img("01_login.png", "หน้า 1 เข้าสู่ระบบ"), img("02_register.png", "หน้าสมัครสมาชิก"))
     + box("challenge", "ท้าทาย", ul("เพิ่ม validator ให้ช่องอีเมลในหน้า Login ต้องมี @",
                                    "ใส่ " + c("Image.asset") + " โลโก้จริงของสาขาแทนไอคอน (ต้องประกาศ asset ใน pubspec.yaml)")))

# ================================================================ STEP 5
step(5, "โครงหน้าหลักและแถบเมนูด้านล่าง", 40,
     "สร้าง HomeShell ที่มี BottomNavigationBar สลับ 3 หน้า โดยแต่ละหน้ายังคงสถานะไว้",
     p("แถบล่างเป็นรูปแบบการนำทางหลักของแอปมือถือ เราจะสร้าง \"เปลือก\" หนึ่งอันที่ถือ 3 หน้าไว้ และใช้ " + c("IndexedStack") + " เพื่อให้เมื่อสลับแท็บไปมา ข้อความที่พิมพ์ค้นหาหรือตำแหน่งที่เลื่อนไว้ไม่หาย")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("BottomNavigationBar") + " กับ " + c("currentIndex") + " / " + c("onTap"),
              c("IndexedStack") + " แสดงลูกทีละตัวแต่สร้างไว้ทั้งหมด",
              "ทำไมหน้า Login และหน้าฟอร์มไม่มีแถบล่าง (เพราะไม่ได้อยู่ใน HomeShell แต่ถูก push ทับ)"))
     + "<h3>1) lib/screens/home_shell.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/home_shell.dart")
     + box("check", "Checkpoint",
           ul("หลัง Login เห็นแถบล่าง 3 เมนู",
              "กดแต่ละเมนูแล้วข้อความกลางจอเปลี่ยนเป็น List / My Borrows / Profile (TODO)",
              "ไอคอนเมนูที่เลือกอยู่เป็นสี Indigo"))
     + box("teacher", "สำหรับผู้สอน",
           ul("ให้นักศึกษาลองเปลี่ยน " + c("IndexedStack") + " เป็น " + c("_pages[_index]") + " แล้วสังเกตความต่างหลังจาก Step 6 (ข้อความค้นหาจะหายเมื่อสลับแท็บ)")))

# ================================================================ STEP 6
step(6, "หน้ารายการอุปกรณ์", 70,
     "แสดงอุปกรณ์เป็นกริดการ์ด ค้นหา กรองตามหมวด และแสดงปุ่ม + เฉพาะแอดมิน",
     p("หน้านี้เป็นหัวใจของแอป มีทั้งการแสดงรายการแบบกริด การกรองข้อมูลตามข้อความและหมวด และการแสดง widget ตามเงื่อนไข (role)")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("GridView.builder") + " + " + c("SliverGridDelegateWithMaxCrossAxisExtent") + " ปรับจำนวนคอลัมน์ตามความกว้างจอโดยอัตโนมัติ",
              c("ChoiceChip") + " ในแถวเลื่อนแนวนอน",
              c("ListenableBuilder") + " ฟัง AppState แล้ววาดใหม่เมื่อข้อมูลเปลี่ยน",
              c("Card") + " + " + c("InkWell") + " ทำการ์ดกดได้พร้อมเอฟเฟกต์",
              "การกรอง list ด้วย " + c("where") + " และ " + c("toLowerCase()"),
              "แสดง FAB ตามเงื่อนไข: " + c("state.isAdmin ? FloatingActionButton(...) : null"),
              c("Expanded") + " ในแถวเพื่อป้องกันข้อความล้น (overflow)"))
     + "<h3>1) lib/screens/equipment_list_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/equipment_list_screen.dart")
     + box("check", "Checkpoint",
           ul("เห็นการ์ดอุปกรณ์ 8 ใบ เป็นกริด 2 คอลัมน์บนมือถือ",
              "DHT22 มีข้อความ \"เหลือ 0\" สีแดง และป้ายแดง \"ยืมไม่ได้\"",
              "พิมพ์ \"ard\" ในช่องค้นหา เหลือแค่ Arduino",
              "กดชิป \"สาย\" เหลือเฉพาะสาย USB และสาย Jumper",
              "Login ด้วยชื่อ admin จึงเห็นปุ่ม + สีอำพัน · ชื่ออื่นไม่เห็น",
              "แตะการ์ดแล้วไปหน้า \"Detail e1 (TODO)\""))
     + figrow(img("03_list_admin.png", "หน้า 2 รายการอุปกรณ์ (มุมมองแอดมิน)"))
     + box("challenge", "ท้าทาย", ul("เพิ่มตัวเลือกเรียงลำดับ (ชื่อ / จำนวนคงเหลือ) ด้วย " + c("PopupMenuButton") + " ใน AppBar",
                                    "ทำให้การ์ดที่เหลือ 0 มีสีจางลง (" + c("Opacity"), ")")))

# ================================================================ STEP 7
step(7, "หน้ารายละเอียดอุปกรณ์และ Dialog ยืม", 70,
     "รับ id จากหน้ารายการ แสดงข้อมูลชิ้นเดียว เปิด Dialog เลือกจำนวน/วันคืน แล้วบันทึกการยืมลง AppState",
     p("หน้านี้สอนการ \"ส่งข้อมูลระหว่างหน้า\" (ส่ง equipmentId ผ่าน constructor) และการ \"รับค่ากลับจาก Dialog\" ด้วย " + c("await showDialog") + " ซึ่งเป็นแพตเทิร์นที่ใช้บ่อยมาก")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("ส่งพารามิเตอร์ให้หน้าใหม่ผ่าน constructor แล้วค้นข้อมูลจาก AppState ด้วย id (ไม่ส่ง object ทั้งก้อน เพื่อให้ข้อมูลสดเสมอ)",
              c("showDialog<T>") + " คืนค่าเป็น Future และ " + c("Navigator.pop(context, value)") + " ส่งค่ากลับ",
              c("showDatePicker") + " เลือกวันที่",
              c("context.mounted") + " ตรวจสอบก่อนใช้ context หลัง await",
              "ปุ่มที่ " + c("onPressed: null") + " จะถูกปิดอัตโนมัติ (กรณีของหมด)",
              "แสดงไอคอนแก้ไขใน AppBar เฉพาะแอดมิน"))
     + "<h3>1) lib/screens/equipment_detail_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/equipment_detail_screen.dart")
     + box("check", "Checkpoint",
           ul("แตะ Arduino จากหน้ารายการ เห็นรูปใหญ่ ชื่อ หมวด คงเหลือ 5 / 10 และรายละเอียด",
              "แตะ DHT22 ปุ่มยืมเป็นสีเทา กดไม่ได้",
              "กดยืมอุปกรณ์ เห็น Dialog กด + ได้ไม่เกินจำนวนที่เหลือ",
              "กดยืนยันยืม แล้วกลับหน้ารายการ การ์ด Arduino เปลี่ยนเป็น \"เหลือ 4\" ทันที (เพราะ ListenableBuilder)",
              "Login เป็น admin เห็นไอคอนดินสอใน AppBar กดแล้วไป \"Form (TODO)\""))
     + figrow(img("04_detail.png", "หน้า 3 รายละเอียดอุปกรณ์"), img("05_borrow_dialog.png", "Dialog เลือกจำนวนและวันคืน"))
     + box("challenge", "ท้าทาย", ul("เพิ่มช่อง \"เหตุผลที่ยืม\" ใน Dialog แล้วเก็บลง Borrow",
                                    "จำกัดวันคืนสูงสุดไม่เกิน 14 วัน")))

# ================================================================ STEP 8
step(8, "หน้าการยืมของฉัน", 50,
     "แสดงรายการยืมแยกแท็บ กำลังยืม / ประวัติ พร้อมป้ายเตือนใกล้ครบกำหนด และปุ่มคืนของ",
     p("หน้านี้แสดงข้อมูลชุดเดียวกันใน 2 มุมมองด้วย " + c("TabBar") + " และมีตรรกะแสดงป้ายเตือนตามจำนวนวันที่เหลือ ซึ่งคำนวณไว้แล้วในโมเดล Borrow")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("DefaultTabController") + " + " + c("TabBar") + " (ใน AppBar.bottom) + " + c("TabBarView"),
              c("ListView.builder") + " สำหรับรายการแนวตั้ง",
              "การแยก widget ย่อย (" + c("_BorrowList") + ", " + c("_BorrowCard") + ", " + c("_Badge") + ") เพื่อให้โค้ดอ่านง่ายและใช้ซ้ำ",
              "Dialog ยืนยันก่อนทำรายการสำคัญ",
              "Empty state: แสดงไอคอนและข้อความเมื่อไม่มีข้อมูล"))
     + "<h3>1) lib/screens/my_borrows_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/my_borrows_screen.dart")
     + box("check", "Checkpoint",
           ul("แท็บกำลังยืม มี Arduino x1 (ป้ายส้ม อีก 2 วันครบกำหนด) และ Servo x2",
              "แท็บประวัติ มี 2 รายการที่คืนแล้ว มีเครื่องหมายถูกสีเขียว",
              "กดคืนของ → ยืนยัน → รายการย้ายไปแท็บประวัติ และหน้ารายการอุปกรณ์ได้จำนวนคืน",
              "ยืมจากหน้ารายละเอียดแล้วกลับมาแท็บนี้ ต้องเห็นรายการใหม่"))
     + figrow(img("07_borrows.png", "หน้า 5 การยืมของฉัน"))
     + box("challenge", "ท้าทาย", ul("แก้ข้อมูลจำลองให้มีรายการที่เลยกำหนดแล้ว (" + c("dueDate: d(-1)") + ") แล้วดูป้ายแดง",
                                    "เพิ่ม Badge ตัวเลขบนไอคอนแท็บ \"การยืมของฉัน\" แสดงจำนวนที่กำลังยืม")))

# ================================================================ STEP 9
step(9, "หน้าโปรไฟล์และออกจากระบบ", 30,
     "แสดงข้อมูลผู้ใช้ปัจจุบัน เมนูรายการ และเคลียร์ session กลับหน้า Login",
     p("หน้าที่ง่ายที่สุดแต่มีจุดสำคัญคือการออกจากระบบต้อง \"ล้าง stack ของหน้าทั้งหมด\" ด้วย " + c("pushAndRemoveUntil") + " เพื่อไม่ให้กด back กลับเข้าแอปได้")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("CircleAvatar"), c("ListTile") + " + " + c("Divider") + " สร้างเมนูแบบรายการ",
              c("Navigator.pushAndRemoveUntil"), c("showAboutDialog") + " ของ Flutter",
              c("Spacer") + " ดันปุ่มลงล่างสุด"))
     + "<h3>1) lib/screens/profile_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/profile_screen.dart")
     + box("check", "Checkpoint",
           ul("เห็นชื่อ บทบาท และรหัสของผู้ใช้ที่ login (admin เห็นชื่ออาจารย์ · อื่น ๆ เห็นสมชาย ใจดี)",
              "กดเกี่ยวกับแอป เห็น Dialog ข้อมูลแอป",
              "กดออกจากระบบ กลับหน้า Login และกดปุ่ม back ของระบบแล้วไม่กลับเข้าแอป"))
     + figrow(img("08_profile.png", "หน้า 6 โปรไฟล์"))
     + box("challenge", "ท้าทาย", ul("ทำเมนู \"ประวัติการยืมทั้งหมด\" ให้เปิด HomeShell แท็บที่ 2 (ใช้ " + c("initialIndex: 1") + ")")))

# ================================================================ STEP 10
step(10, "ฟอร์มเพิ่ม/แก้ไขอุปกรณ์ และการเลือกรูปภาพ", 70,
     "สร้างฟอร์มที่ใช้ได้ทั้งโหมดเพิ่มและแก้ไข ตรวจสอบข้อมูล และเลือกรูปจากกล้อง/คลังภาพด้วย image_picker",
     p("ขั้นนี้เป็นครั้งแรกที่เราใช้ package ภายนอก และเข้าถึงความสามารถของเครื่อง (กล้อง) จึงต้องตั้งค่า permission ของ iOS เพิ่ม")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul("เพิ่ม dependency ด้วย " + c("flutter pub add"),
              "widget เดียวรองรับ 2 โหมดด้วยพารามิเตอร์ " + c("Equipment? existing"),
              c("DropdownButtonFormField") + " ผูกกับ enum",
              c("inputFormatters") + " จำกัดให้พิมพ์ได้เฉพาะตัวเลข",
              c("showModalBottomSheet") + " ให้ผู้ใช้เลือกกล้อง/คลังภาพ",
              "async/await กับ " + c("ImagePicker().pickImage"),
              "การคำนวณจำนวนคงเหลือใหม่เมื่อแก้จำนวนทั้งหมด (ต้องไม่น้อยกว่าที่ถูกยืมอยู่)"))
     + "<h3>1) ติดตั้ง package</h3>" + code("flutter pub add image_picker", "bash")
     + "<h3>2) ตั้งค่า permission ของ iOS</h3>"
     + p("เปิดไฟล์ " + c("ios/Runner/Info.plist") + " แล้วเพิ่ม 2 คีย์นี้ก่อน " + c("</dict>") + " บรรทัดสุดท้าย (Android ไม่ต้องตั้งค่าเพิ่ม)")
     + code('<key>NSCameraUsageDescription</key>\n<string>ใช้กล้องเพื่อถ่ายรูปอุปกรณ์</string>\n<key>NSPhotoLibraryUsageDescription</key>\n<string>ใช้คลังภาพเพื่อเลือกรูปอุปกรณ์</string>', "yaml", "ios/Runner/Info.plist (ส่วนที่เพิ่ม)")
     + "<h3>3) lib/screens/equipment_form_screen.dart (แทนที่โครงเปล่า)</h3>" + file_block("lib/screens/equipment_form_screen.dart")
     + box("check", "Checkpoint",
           ul("Login เป็น admin กด + เห็นฟอร์มว่าง หัวข้อ \"เพิ่มอุปกรณ์\"",
              "กดบันทึกโดยไม่กรอก เห็นข้อความเตือนใต้ช่องชื่อและจำนวน",
              "กรอกครบแล้วบันทึก กลับหน้ารายการและเห็นการ์ดใหม่ต่อท้าย",
              "จากหน้ารายละเอียด กดดินสอ ฟอร์มมีข้อมูลเดิมกรอกไว้ หัวข้อ \"แก้ไขอุปกรณ์\"",
              "กดถ่าย/เลือกรูป เห็น bottom sheet 2 ตัวเลือก (บน Simulator ใช้ \"เลือกจากคลังภาพ\")"))
     + figrow(img("09_form_add.png", "หน้า 4 เพิ่มอุปกรณ์"), img("06_form_edit.png", "หน้า 4 โหมดแก้ไข (ข้อมูลเดิมถูกกรอกไว้)"))
     + box("teacher", "สำหรับผู้สอน",
           ul("iOS Simulator ไม่มีกล้อง ตัวเลือก \"ถ่ายรูป\" จะ error ซึ่งโค้ดดักไว้ด้วย try/catch แล้ว ให้ใช้เป็นตัวอย่างสอนการจัดการข้อผิดพลาด",
              "บน Flutter web " + c("Image.file") + " ใช้ไม่ได้ โค้ดจึงตรวจ " + c("kIsWeb") + " ก่อน"))
     + box("challenge", "ท้าทาย", ul("เพิ่มปุ่ม \"ลบอุปกรณ์\" ในโหมดแก้ไข พร้อม Dialog ยืนยัน และเมธอด " + c("removeEquipment") + " ใน AppState")))

# ================================================================ STEP 11
step(11, "ทดสอบอัตโนมัติ สรุป และก้าวต่อไป", 40,
     "เขียน widget test ตรวจ flow หลัก และทบทวนสิ่งที่เรียนรู้ทั้งหมด",
     p("การทดสอบอัตโนมัติช่วยยืนยันว่าเมื่อแก้โค้ดในอนาคต (เช่น ตอนต่อ MySQL) flow เดิมยังทำงาน Flutter มี " + c("flutter_test") + " มาให้แล้วโดยไม่ต้องติดตั้งเพิ่ม")
     + box("learn", "ความรู้ใหม่ในขั้นนี้",
           ul(c("testWidgets") + ", " + c("WidgetTester") + " (" + c("pumpWidget") + ", " + c("enterText") + ", " + c("tap") + ", " + c("pumpAndSettle") + ")",
              c("find.text") + ", " + c("find.byType") + ", " + c("find.widgetWithText"),
              c("expect") + " กับ " + c("findsOneWidget") + " / " + c("findsNothing")))
     + "<h3>1) test/widget_test.dart (แทนที่ทั้งไฟล์)</h3>" + file_block("test/widget_test.dart")
     + "<h3>2) รันทดสอบ</h3>" + code("flutter analyze\nflutter test", "bash")
     + box("check", "Checkpoint", ul("ผลลัพธ์ All tests passed!", c("flutter analyze") + " No issues found!"))
     + "<h3>3) สรุปสิ่งที่ได้เรียนรู้</h3>"
     + '<table class="tbl"><tr><th>หมวด</th><th>สิ่งที่ใช้ในแอปนี้</th></tr>'
       '<tr><td>โครงสร้าง</td><td>MaterialApp, Scaffold, AppBar, BottomNavigationBar, IndexedStack, TabBar</td></tr>'
       '<tr><td>แสดงผล</td><td>GridView, ListView, Card, ListTile, CircleAvatar, Chip, Container/BoxDecoration</td></tr>'
       '<tr><td>รับข้อมูล</td><td>TextField, TextFormField, Form/validator, DropdownButtonFormField, showDatePicker, image_picker</td></tr>'
       '<tr><td>นำทาง</td><td>Navigator.push / pushReplacement / pushAndRemoveUntil, ส่งพารามิเตอร์ผ่าน constructor, รับค่ากลับจาก Dialog</td></tr>'
       '<tr><td>สถานะ</td><td>StatefulWidget/setState, ChangeNotifier + ListenableBuilder, singleton</td></tr>'
       '<tr><td>ภาษา Dart</td><td>class, enhanced enum, getter, named parameters, async/await, where/map, cascade (..)</td></tr>'
       '<tr><td>คุณภาพ</td><td>flutter analyze, widget test, แยก widget ย่อย, ธีมกลาง</td></tr></table>'
     + "<h3>4) ก้าวต่อไป: ต่อฐานข้อมูล MySQL</h3>"
     + p("เพราะทุกหน้าคุยกับ " + c("AppState") + " เท่านั้น การต่อฐานข้อมูลจึงทำได้โดยไม่แก้หน้าจอ แนวทางที่แนะนำ:")
     + ol("สร้าง REST API (PHP หรือ Node.js) ครอบตาราง users / items / borrows",
          "เพิ่ม package " + c("http") + " และสร้าง " + c("lib/data/api_service.dart"),
          "เปลี่ยนเมธอดใน AppState ให้เป็น " + c("Future") + " เรียก API แล้ว " + c("notifyListeners()") + " เมื่อได้ผล",
          "เพิ่ม loading state (" + c("CircularProgressIndicator") + ") และการจัดการ error",
          "เก็บ session ด้วย " + c("shared_preferences") + " เพื่อไม่ต้อง login ทุกครั้ง")
     + box("challenge", "โปรเจกต์ท้ายบท (เลือก 1 ข้อ)",
           ol("ระบบแจ้งเตือน: ไอคอนกระดิ่งแสดงจำนวนรายการที่จะครบกำหนดใน 3 วัน และกดแล้วเห็นรายการ",
              "หน้าแอดมิน: ดูรายการยืมของทุกคน และกดอนุมัติ/ปฏิเสธ",
              "โหมดมืด: เพิ่ม " + c("darkTheme") + " ใน MaterialApp และสวิตช์ในหน้าตั้งค่า",
              "ค้นหาขั้นสูง: กรองหลายหมวดพร้อมกันด้วย " + c("FilterChip") + " และแสดงจำนวนผลลัพธ์")))

# ================================================================ HTML
FILE_TREE = """lib/
├─ main.dart                       จุดเริ่มต้น MaterialApp + ธีม
├─ theme.dart                      สีหลัก Indigo · รอง Sky · เน้น Amber
├─ models/
│  ├─ user.dart                    ผู้ใช้ + บทบาท (student / admin)
│  ├─ equipment.dart               อุปกรณ์ + หมวดหมู่ (enum)
│  └─ borrow.dart                  รายการยืม + คำนวณวันครบกำหนด
├─ data/
│  ├─ mock_data.dart               ข้อมูลจำลอง
│  └─ app_state.dart               สถานะรวมในหน่วยความจำ (ChangeNotifier)
├─ utils/thai_date.dart            แปลงวันที่เป็นข้อความไทย
├─ widgets/equipment_image.dart    รูปอุปกรณ์ / ไอคอนตามหมวด
└─ screens/
   ├─ login_screen.dart            หน้า 1 เข้าสู่ระบบ
   ├─ register_screen.dart         หน้าสมัครสมาชิก
   ├─ home_shell.dart              โครง BottomNavigationBar 3 เมนู
   ├─ equipment_list_screen.dart   หน้า 2 รายการอุปกรณ์
   ├─ equipment_detail_screen.dart หน้า 3 รายละเอียด + Dialog ยืม
   ├─ equipment_form_screen.dart   หน้า 4 เพิ่ม/แก้ไข (แอดมิน)
   ├─ my_borrows_screen.dart       หน้า 5 การยืมของฉัน (TabBar)
   └─ profile_screen.dart          หน้า 6 โปรไฟล์ + ออกจากระบบ
test/widget_test.dart              ทดสอบอัตโนมัติ"""

NAV_MAP = """Login ──(เข้าสำเร็จ)──> รายการอุปกรณ์ (หน้าหลัก)
                          │
      ┌───────────────────┼───────────────────────┐
      │(แตะการ์ด)          │(แถบล่าง)               │(แถบล่าง)
      ▼                   ▼                        ▼
รายละเอียดอุปกรณ์     การยืมของฉัน               โปรไฟล์
      │(ปุ่มยืม)          │(ปุ่มคืน)                │(ออกจากระบบ)
      ▼                   ▼                        ▼
  ยืมสำเร็จ            คืนสำเร็จ                  กลับ Login

รายการอุปกรณ์ ──(ปุ่ม + เฉพาะแอดมิน)──> เพิ่ม/แก้อุปกรณ์"""

CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
html { font-size: 16pt; }
body { font-family: 'TH Sarabun New', 'TH SarabunPSK', 'Sarabun', sans-serif; font-size: 16pt; line-height: 1.35; color: #1a1a1a; margin: 0; }
h1, h2, h3 { font-family: 'TH Sarabun New', 'TH SarabunPSK', sans-serif; color: #283593; margin: 0.6em 0 0.3em; line-height: 1.2; }
h1 { font-size: 30pt; }
h2 { font-size: 24pt; border-bottom: 2px solid #283593; padding-bottom: 4px; margin-top: 1em; }
h3 { font-size: 19pt; color: #1f2a80; }
p { margin: 0.35em 0 0.6em; text-align: left; }
ul, ol { margin: 0.2em 0 0.7em; padding-left: 1.5em; }
li { margin: 0.12em 0; }
code { font-family: Menlo, 'SF Mono', Consolas, monospace; font-size: 10.5pt; background: #eef0f7; padding: 1px 5px; border-radius: 4px; }
.codeblock { margin: 0.5em 0 0.9em; border: 1px solid #d5d8e5; border-radius: 6px; overflow: hidden; }
.codecap { display: flex; justify-content: space-between; background: #283593; color: #fff; font-family: Menlo, monospace; font-size: 10pt; padding: 4px 10px; }
.codecap .lines { opacity: 0.8; }
pre.hl { margin: 0; padding: 8px 10px; font-family: Menlo, 'SF Mono', Consolas, monospace; font-size: 9.6pt; line-height: 1.32; white-space: pre-wrap; word-break: break-all; background: #f7f8fc; }
pre.plain { font-family: Menlo, monospace; font-size: 10pt; line-height: 1.3; background: #f7f8fc; border: 1px solid #d5d8e5; border-radius: 6px; padding: 10px 12px; white-space: pre; overflow: hidden; }
.box { border-left: 6px solid; border-radius: 6px; padding: 8px 14px 6px; margin: 0.8em 0; page-break-inside: avoid; }
.box .boxtitle { font-weight: bold; font-size: 17pt; margin-bottom: 2px; }
.box ul, .box ol { margin-bottom: 0.3em; }
.box.learn { border-color: #03a9f4; background: #e8f6fd; }
.box.learn .boxtitle { color: #01579b; }
.box.check { border-color: #2e7d32; background: #eaf5ea; }
.box.check .boxtitle { color: #1b5e20; }
.box.check .boxtitle::before { content: '✔ '; }
.box.teacher { border-color: #6a1b9a; background: #f3e9f8; }
.box.teacher .boxtitle { color: #4a148c; }
.box.challenge { border-color: #ffb300; background: #fff7e0; }
.box.challenge .boxtitle { color: #8d5a00; }
.step { page-break-before: always; }
.stephead { background: #283593; color: #fff; padding: 12px 18px; border-radius: 8px; margin-bottom: 10px; }
.stephead .no { font-size: 13pt; letter-spacing: 1px; opacity: 0.85; }
.stephead h1 { color: #fff; margin: 0; font-size: 26pt; }
.stephead .meta { font-size: 14pt; opacity: 0.9; margin-top: 4px; }
.goal { background: #fff; border: 1px dashed #283593; padding: 6px 12px; border-radius: 6px; margin-bottom: 8px; }
.goal b { color: #283593; }
.figrow { display: flex; gap: 10mm; justify-content: center; flex-wrap: wrap; margin: 0.6em 0 1em; page-break-inside: avoid; }
figure.shot { margin: 0; text-align: center; }
figure.shot img { width: 100%; border: 1px solid #c9ccd9; border-radius: 10px; }
figure.shot figcaption { font-size: 13pt; color: #555; margin-top: 3px; }
table.tbl { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; font-size: 15pt; }
table.tbl th, table.tbl td { border: 1px solid #c9ccd9; padding: 4px 8px; vertical-align: top; }
table.tbl th { background: #e8eaf6; color: #283593; text-align: left; }
table.tbl td.c, table.tbl th.c { text-align: center; }
/* cover */
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.cover .band { background: #283593; color: #fff; padding: 30px 36px; border-radius: 14px; }
.cover .band .sup { font-size: 16pt; opacity: 0.85; letter-spacing: 1px; }
.cover .band h1 { color: #fff; font-size: 44pt; margin: 4px 0; }
.cover .band .sub { font-size: 22pt; }
.cover .info { margin-top: 26px; font-size: 17pt; line-height: 1.6; }
.cover .accent { height: 8px; background: linear-gradient(90deg, #ffb300, #03a9f4); border-radius: 4px; margin-top: 18px; }
.toc td { padding: 3px 8px; }
.small { font-size: 13pt; color: #555; }
"""

H: list[str] = []
H.append("<!DOCTYPE html><html lang='th'><head><meta charset='utf-8'><title>LabStock คู่มือปฏิบัติการ</title>")
H.append("<style>" + CSS + FMT.get_style_defs(".hl") + "</style></head><body>")

# ---- cover
H.append(f"""
<div class="cover">
  <div class="band">
    <div class="sup">คู่มือปฏิบัติการ · รายวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่</div>
    <h1>LabStock</h1>
    <div class="sub">สร้างแอปคลังอุปกรณ์แล็บ ICE ด้วย Flutter ทีละขั้นตอน</div>
  </div>
  <div class="accent"></div>
  <div class="info">
    <b>เฟส 1: ส่วนติดต่อผู้ใช้ (UI) และการนำทาง</b> · 6 หน้าจอ · 12 ขั้นตอน<br>
    ผู้เรียนจะได้สร้างแอปที่ทำงานได้จริงด้วยข้อมูลจำลอง ก่อนเชื่อมต่อฐานข้อมูล MySQL ในเฟสถัดไป<br>
    <span class="small">Flutter 3.35 · Dart 3.9 · ปรับปรุงล่าสุด {TODAY_TH}</span>
  </div>
</div>
""")

# ---- intro
H.append('<div class="step"><h2>ภาพรวมและวิธีใช้คู่มือ</h2>')
H.append(p("คู่มือนี้พานักศึกษาสร้างแอป <b>LabStock</b> ระบบยืม-คืนอุปกรณ์แล็บ ตั้งแต่โปรเจกต์เปล่าจนได้แอปที่ใช้งานได้ครบ 6 หน้า โดยแบ่งเป็น 12 ขั้นตอน (Step 0–11) แต่ละขั้นตอนใช้เวลาประมาณ 30–70 นาที เหมาะกับการสอน 1–2 ขั้นตอนต่อคาบ"))
H.append("<h3>โครงสร้างของแต่ละขั้นตอน</h3>")
H.append(ul("<b>เป้าหมาย</b> สิ่งที่ต้องทำได้เมื่อจบขั้นตอน",
            "<b>ความรู้ใหม่</b> (กล่องฟ้า) widget และแนวคิดที่จะได้เรียนรู้ ผู้สอนควรอธิบายก่อนลงมือ",
            "<b>ลงมือทำ</b> โค้ดเต็มของไฟล์ที่ต้องสร้างหรือแทนที่ พิมพ์ตามหรือคัดลอกได้",
            "<b>Checkpoint</b> (กล่องเขียว) รายการตรวจสอบว่าทำสำเร็จ พร้อมภาพหน้าจอที่ควรได้",
            "<b>สำหรับผู้สอน</b> (กล่องม่วง) จุดที่ควรเน้นหรือปัญหาที่พบบ่อย",
            "<b>ท้าทาย</b> (กล่องเหลือง) แบบฝึกหัดเพิ่มเติมสำหรับผู้ที่ทำเสร็จก่อน"))
H.append("<h3>แผนการสอน</h3>")
H.append('<table class="tbl toc"><tr><th class="c">Step</th><th>หัวข้อ</th><th>เป้าหมาย</th><th class="c">นาที</th></tr>')
for s in STEPS:
    H.append(f'<tr><td class="c">{s["no"]}</td><td><b>{s["title"]}</b></td><td>{s["goal"]}</td><td class="c">{s["minutes"]}</td></tr>')
H.append(f'<tr><td></td><td colspan="2"><b>รวม</b></td><td class="c"><b>{sum(s["minutes"] for s in STEPS)}</b></td></tr></table>')
H.append("<h3>ข้อกำหนดการออกแบบ (จากสเปก UI)</h3>")
H.append(ul("<b>ธีมสี:</b> หลัก = คราม (Indigo) · รอง = ฟ้า (Sky) · เน้น = ส้มอำพัน (Amber)",
            "<b>ฟอนต์:</b> หัวข้อ ~20–22 · เนื้อหา ~14–16",
            "<b>โครงทุกหน้า:</b> Scaffold → AppBar + body",
            "<b>แถบล่าง 3 เมนู:</b> รายการ · การยืมของฉัน · โปรไฟล์ (หน้า Login และหน้าฟอร์มไม่มีแถบล่าง)",
            "<b>2 บทบาท:</b> นักศึกษา และ แอดมิน (แอดมินเห็นปุ่มเพิ่ม/แก้ไขอุปกรณ์เพิ่มมา)"))
H.append("<h3>แผนผังการเชื่อมหน้า (Navigation Map)</h3>")
H.append(f'<pre class="plain">{html.escape(NAV_MAP)}</pre>')
H.append("<h3>โครงสร้างไฟล์เมื่อทำครบทุกขั้นตอน</h3>")
H.append(f'<pre class="plain">{html.escape(FILE_TREE)}</pre>')
H.append("<h3>หน้าจอทั้ง 6 หน้าที่จะได้</h3>")
H.append(figrow(img("01_login.png", "1 เข้าสู่ระบบ", 42), img("03_list_admin.png", "2 รายการอุปกรณ์", 42),
                img("04_detail.png", "3 รายละเอียด", 42)))
H.append(figrow(img("09_form_add.png", "4 เพิ่ม/แก้ไข (แอดมิน)", 42), img("07_borrows.png", "5 การยืมของฉัน", 42),
                img("08_profile.png", "6 โปรไฟล์", 42)))
H.append("</div>")

# ---- steps
for s in STEPS:
    H.append(f"""<div class="step">
<div class="stephead"><div class="no">STEP {s['no']}</div><h1>{s['title']}</h1>
<div class="meta">เวลาโดยประมาณ {s['minutes']} นาที</div></div>
<div class="goal"><b>เป้าหมาย:</b> {s['goal']}</div>
{s['body']}
</div>""")

H.append("</body></html>")
OUT_HTML.write_text("".join(H), encoding="utf-8")
print("HTML:", OUT_HTML)

# ---------------------------------------------------------------- PDF
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT_PDF_RAW}", OUT_HTML.as_uri()],
               check=True, capture_output=True)
print("raw PDF:", OUT_PDF_RAW)

# ---- page numbers overlay
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FONT = Path.home() / "Library/Fonts/THSarabunNew.ttf"
pdfmetrics.registerFont(TTFont("Sarabun", str(FONT)))

reader = PdfReader(str(OUT_PDF_RAW))
writer = PdfWriter()
total = len(reader.pages)
for i, page in enumerate(reader.pages):
    if i > 0:  # ไม่ใส่เลขหน้าบนหน้าปก
        buf = BytesIO()
        cv = canvas.Canvas(buf, pagesize=A4)
        cv.setFont("Sarabun", 12)
        cv.setFillColorRGB(0.35, 0.35, 0.35)
        cv.drawString(16 * 72 / 25.4, 9 * 72 / 25.4, "LabStock · คู่มือปฏิบัติการ 5534408")
        cv.drawRightString(A4[0] - 16 * 72 / 25.4, 9 * 72 / 25.4, f"หน้า {i + 1} / {total}")
        cv.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
    writer.add_page(page)
writer.add_metadata({"/Title": "LabStock คู่มือปฏิบัติการ", "/Author": "รายวิชา 5534408",
                     "/Subject": "การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่ด้วย Flutter"})
with open(OUT_PDF, "wb") as f:
    writer.write(f)
OUT_PDF_RAW.unlink()
print(f"PDF: {OUT_PDF} ({total} pages)")
