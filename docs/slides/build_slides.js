// สร้างสไลด์สอน LabStock (Flutter) — 12 Step
const pptxgen = require("pptxgenjs");
const path = require("path");

const SHOTS = path.join(__dirname, "..", "shots");
const OUT = path.join(__dirname, "..", "LabStock-สไลด์สอน.pptx");

const C = {
  indigo: "283593", indigoDark: "1B2470", indigoLight: "E8EAF6",
  sky: "03A9F4", skyLight: "E3F5FD", amber: "FFB300", amberLight: "FFF3D6",
  ink: "1A1A1A", muted: "5F6368", white: "FFFFFF", bg: "FFFFFF",
  code: "1E2235", codeText: "E6E8F0", codeKey: "FFB300", codeStr: "8BE9A0", codeCom: "8A93B0",
  green: "2E7D32", greenLight: "EAF5EA", purple: "6A1B9A", purpleLight: "F3E9F8",
};
const TH = "TH Sarabun New";
const MONO = "Menlo";
const W = 13.33, H = 7.5;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "LabStock — สไลด์สอน Flutter 12 ขั้นตอน";
pres.author = "รายวิชา 5534408";

let slideNo = 0;

// ------------------------------------------------------------ helpers
function runs(text, base = {}) {
  // แปลง `code` ให้เป็น run ฟอนต์ mono
  const parts = text.split("`");
  return parts.map((t, i) =>
    i % 2 === 1
      ? { text: t, options: { ...base, fontFace: MONO, fontSize: (base.fontSize || 20) - 5, color: C.indigo, bold: true } }
      : { text: t, options: { ...base } }
  ).filter(r => r.text !== "");
}

function bullets(slide, items, opt) {
  const { x, y, w, h, size = 20, color = C.ink, gap = 8, bullet = true, lineSpacingMultiple } = opt;
  const arr = [];
  items.forEach((it, i) => {
    const last = i === items.length - 1;
    const rs = runs(it, { fontFace: TH, fontSize: size, color });
    rs[0].options.bullet = bullet ? { indent: 18 } : false;
    rs.forEach(r => { r.options.paraSpaceAfter = gap; });
    if (!last) rs[rs.length - 1].options.breakLine = true;
    arr.push(...rs);
  });
  slide.addText(arr, { x, y, w, h, isTextBox: true, margin: 0, valign: "top", align: "left", lineSpacingMultiple });
}

function tag(slide, text, x, y, w = 1.4, fill = C.amber, color = C.ink) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.42, fill: { color: fill }, line: { color: fill }, rectRadius: 0.21 });
  slide.addText(text, { x, y, w, h: 0.42, isTextBox: true, margin: 0, fontFace: TH, fontSize: 16, bold: true, color, align: "center", valign: "middle" });
}

function footer(slide, dark = false) {
  slideNo += 1;
  slide.addText(`LabStock · 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่`, {
    x: 0.5, y: H - 0.45, w: 8, h: 0.3, isTextBox: true, margin: 0, fontFace: TH, fontSize: 12, color: dark ? "AAB0D6" : C.muted,
  });
  slide.addText(String(slideNo), {
    x: W - 1.3, y: H - 0.45, w: 0.8, h: 0.3, isTextBox: true, margin: 0, fontFace: TH, fontSize: 12, color: dark ? "AAB0D6" : C.muted, align: "right",
  });
}

function content(title, stepNo) {
  const s = pres.addSlide();
  s.background = { color: C.bg };
  s.addText(title, { x: 0.5, y: 0.35, w: 10.4, h: 0.9, isTextBox: true, margin: 0, fontFace: TH, fontSize: 36, bold: true, color: C.indigo, valign: "middle" });
  if (stepNo !== undefined) tag(s, `STEP ${stepNo}`, W - 2.0, 0.55, 1.5);
  footer(s);
  return s;
}

function section(no, title, goal, minutes) {
  const s = pres.addSlide();
  s.background = { color: C.indigo };
  s.addShape(pres.ShapeType.ellipse, { x: 0.9, y: 1.6, w: 2.6, h: 2.6, fill: { color: C.amber }, line: { color: C.amber } });
  s.addText(String(no), { x: 0.9, y: 1.6, w: 2.6, h: 2.6, isTextBox: true, margin: 0, fontFace: TH, fontSize: 96, bold: true, color: C.indigoDark, align: "center", valign: "middle" });
  s.addText("STEP", { x: 0.9, y: 4.35, w: 2.6, h: 0.5, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, color: C.amber, align: "center", bold: true });
  s.addText(title, { x: 4.2, y: 1.5, w: 8.5, h: 1.6, isTextBox: true, margin: 0, fontFace: TH, fontSize: 48, bold: true, color: C.white, valign: "bottom" });
  s.addText([{ text: "เป้าหมาย  ", options: { bold: true, color: C.amber } }, { text: goal, options: { color: C.white } }],
    { x: 4.2, y: 3.3, w: 8.5, h: 1.4, isTextBox: true, margin: 0, fontFace: TH, fontSize: 24, valign: "top" });
  s.addText(`⏱ ประมาณ ${minutes} นาที`, { x: 4.2, y: 4.9, w: 6, h: 0.5, isTextBox: true, margin: 0, fontFace: TH, fontSize: 20, color: "C5CAE9" });
  footer(s, true);
  return s;
}

function codeBox(slide, code, opt) {
  const { x, y, w, h, title } = opt;
  const hasTitle = !!title;
  const nLines = code.replace(/\n$/, "").split("\n").length;
  const avail = h - (hasTitle ? 0.55 : 0.3);
  const maxSize = Math.floor((avail * 72) / (nLines * 1.32) * 2) / 2; // ขั้นละ 0.5pt
  const size = Math.min(opt.size || 13, maxSize);
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: C.code }, line: { color: C.code }, rectRadius: 0.12 });
  if (hasTitle) {
    slide.addText(title, { x: x + 0.2, y: y + 0.08, w: w - 0.4, h: 0.35, isTextBox: true, margin: 0, fontFace: MONO, fontSize: 11, color: C.amber, bold: true });
  }
  // ไฮไลต์อย่างง่าย: คอมเมนต์ (//) เป็นสีจาง, สตริง '...' เป็นเขียว
  const lines = code.replace(/\n$/, "").split("\n");
  const arr = [];
  lines.forEach((ln, i) => {
    const segs = [];
    const cIdx = ln.indexOf("//");
    let main = ln, com = "";
    if (cIdx >= 0 && !ln.slice(0, cIdx).includes("'")) { main = ln.slice(0, cIdx); com = ln.slice(cIdx); }
    // split strings
    const re = /('[^']*')/g;
    let last = 0, m;
    while ((m = re.exec(main)) !== null) {
      if (m.index > last) segs.push({ text: main.slice(last, m.index), options: { color: C.codeText } });
      segs.push({ text: m[1], options: { color: C.codeStr } });
      last = m.index + m[1].length;
    }
    if (last < main.length) segs.push({ text: main.slice(last), options: { color: C.codeText } });
    if (com) segs.push({ text: com, options: { color: C.codeCom, italic: true } });
    if (segs.length === 0) segs.push({ text: " ", options: { color: C.codeText } });
    segs.forEach(sg => { sg.options.fontFace = MONO; sg.options.fontSize = size; });
    if (i < lines.length - 1) segs[segs.length - 1].options.breakLine = true;
    arr.push(...segs);
  });
  slide.addText(arr, { x: x + 0.2, y: y + (hasTitle ? 0.45 : 0.15), w: w - 0.4, h: h - (hasTitle ? 0.55 : 0.3), isTextBox: true, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
}

function shot(slide, file, opt) {
  // ภาพหน้าจอ 1206x2622 → อัตราส่วน 0.46
  const { x, y, h, caption } = opt;
  const w = h * 0.46;
  slide.addShape(pres.ShapeType.roundRect, { x: x - 0.06, y: y - 0.06, w: w + 0.12, h: h + 0.12, fill: { color: C.indigoLight }, line: { color: C.indigoLight }, rectRadius: 0.25 });
  slide.addImage({ path: path.join(SHOTS, file), x, y, w, h });
  if (caption) slide.addText(caption, { x: x - 0.5, y: y + h + 0.1, w: w + 1.0, h: 0.35, isTextBox: true, margin: 0, fontFace: TH, fontSize: 15, color: C.muted, align: "center" });
  return w;
}

function panel(slide, opt) {
  const { x, y, w, h, title, items, kind = "learn", size = 18 } = opt;
  const theme = {
    learn: { fill: C.skyLight, title: "01579B" },
    check: { fill: C.greenLight, title: C.green },
    teacher: { fill: C.purpleLight, title: C.purple },
    challenge: { fill: C.amberLight, title: "8D5A00" },
    plain: { fill: C.indigoLight, title: C.indigo },
  }[kind];
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: theme.fill }, line: { color: theme.fill }, rectRadius: 0.15 });
  slide.addText(title, { x: x + 0.25, y: y + 0.15, w: w - 0.5, h: 0.45, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, bold: true, color: theme.title });
  bullets(slide, items, { x: x + 0.25, y: y + 0.7, w: w - 0.5, h: h - 0.85, size, gap: 5 });
}

function checkSlide(stepNo, title, items, shots, notes) {
  const s = content(title, stepNo);
  const shotH = 5.2;
  const n = shots.length;
  const shotW = shotH * 0.46;
  const totalShotsW = n * shotW + (n - 1) * 0.5;
  const shotsX = W - 0.6 - totalShotsW;
  panel(s, { x: 0.5, y: 1.4, w: shotsX - 0.9, h: 5.4, title: "✔ Checkpoint — ตรวจก่อนไปขั้นถัดไป", items, kind: "check", size: 18 });
  shots.forEach((sh, i) => shot(s, sh.file, { x: shotsX + i * (shotW + 0.5), y: 1.4, h: shotH, caption: sh.caption }));
  if (notes) s.addNotes(notes);
  return s;
}

// ============================================================ 1. ปก
{
  const s = pres.addSlide();
  s.background = { color: C.indigo };
  s.addShape(pres.ShapeType.roundRect, { x: 0.9, y: 1.3, w: 1.6, h: 1.6, fill: { color: C.amber }, line: { color: C.amber }, rectRadius: 0.35 });
  s.addText("LS", { x: 0.9, y: 1.3, w: 1.6, h: 1.6, isTextBox: true, margin: 0, fontFace: "Arial", fontSize: 40, bold: true, color: C.indigoDark, align: "center", valign: "middle" });
  s.addText("รายวิชา 5534408 การพัฒนาแอปพลิเคชันบนอุปกรณ์เคลื่อนที่", { x: 0.9, y: 3.15, w: 11, h: 0.5, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, color: "C5CAE9" });
  s.addText("LabStock", { x: 0.9, y: 3.6, w: 11, h: 1.3, isTextBox: true, margin: 0, fontFace: "Arial", fontSize: 72, bold: true, color: C.white });
  s.addText("สร้างแอปคลังอุปกรณ์แล็บ ICE ด้วย Flutter ทีละขั้นตอน", { x: 0.9, y: 4.9, w: 11, h: 0.7, isTextBox: true, margin: 0, fontFace: TH, fontSize: 32, color: C.white });
  s.addText("เฟส 1 · ส่วนติดต่อผู้ใช้และการนำทาง · 6 หน้าจอ · 12 ขั้นตอน", { x: 0.9, y: 5.65, w: 11, h: 0.5, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, color: C.amber });
  shot(s, "03_list_admin.png", { x: 10.4, y: 0.7, h: 5.9 });
  footer(s, true);
  s.addNotes("สไลด์เปิด: แนะนำว่าตลอดหน่วยนี้จะสร้างแอปจริง 1 ตัวชื่อ LabStock ระบบยืม-คืนอุปกรณ์แล็บ โดยทำทีละขั้นตอน คู่กับคู่มือปฏิบัติการ (PDF) ที่มีโค้ดเต็ม");
}

// ============================================================ 2. แอปที่จะสร้าง
{
  const s = content("แอปที่เราจะสร้างด้วยกัน — 6 หน้าจอ");
  const files = [["01_login.png", "1 เข้าสู่ระบบ"], ["03_list_admin.png", "2 รายการอุปกรณ์"], ["04_detail.png", "3 รายละเอียด"],
                 ["09_form_add.png", "4 เพิ่ม/แก้ไข"], ["07_borrows.png", "5 การยืมของฉัน"], ["08_profile.png", "6 โปรไฟล์"]];
  const h = 4.6, w = h * 0.46, gap = (W - 1.0 - 6 * w) / 5;
  files.forEach(([f, cap], i) => shot(s, f, { x: 0.5 + i * (w + gap), y: 1.45, h, caption: cap }));
  s.addNotes("ให้นักศึกษาเห็นภาพปลายทางก่อน: 6 หน้า มี 2 บทบาท (นักศึกษา/แอดมิน) ชี้ให้เห็นปุ่ม + สีอำพันที่มีเฉพาะแอดมิน และป้ายแดง 'ยืมไม่ได้'");
}

// ============================================================ 3. ทำไมต้องแอปนี้ / ความรู้ที่จะได้
{
  const s = content("ทำแอปเดียว ได้ครบทุกเรื่องพื้นฐานของ Flutter");
  const cards = [
    ["โครงสร้างหน้าจอ", "Scaffold · AppBar · BottomNavigationBar · TabBar · IndexedStack"],
    ["แสดงผลข้อมูล", "GridView · ListView · Card · ListTile · Chip · CircleAvatar"],
    ["รับข้อมูลจากผู้ใช้", "TextField · Form/validator · Dropdown · DatePicker · image_picker"],
    ["การนำทาง", "push · pushReplacement · pushAndRemoveUntil · ส่งค่า/รับค่ากลับจาก Dialog"],
    ["สถานะของแอป", "setState · ChangeNotifier · ListenableBuilder · singleton"],
    ["คุณภาพโค้ด", "ธีมกลาง · แยก widget ย่อย · flutter analyze · widget test"],
  ];
  const cw = 3.95, ch = 2.3, gx = 0.24, gy = 0.3;
  cards.forEach(([t, d], i) => {
    const cx = 0.5 + (i % 3) * (cw + gx), cy = 1.5 + Math.floor(i / 3) * (ch + gy);
    s.addShape(pres.ShapeType.roundRect, { x: cx, y: cy, w: cw, h: ch, fill: { color: i % 2 ? C.skyLight : C.indigoLight }, line: { color: i % 2 ? C.skyLight : C.indigoLight }, rectRadius: 0.15 });
    s.addShape(pres.ShapeType.ellipse, { x: cx + 0.25, y: cy + 0.25, w: 0.55, h: 0.55, fill: { color: C.indigo }, line: { color: C.indigo } });
    s.addText(String(i + 1), { x: cx + 0.25, y: cy + 0.25, w: 0.55, h: 0.55, isTextBox: true, margin: 0, fontFace: "Arial", fontSize: 18, bold: true, color: C.white, align: "center", valign: "middle" });
    s.addText(t, { x: cx + 0.95, y: cy + 0.25, w: cw - 1.2, h: 0.55, isTextBox: true, margin: 0, fontFace: TH, fontSize: 24, bold: true, color: C.indigo, valign: "middle" });
    s.addText(d, { x: cx + 0.25, y: cy + 0.95, w: cw - 0.5, h: ch - 1.1, isTextBox: true, margin: 0, fontFace: TH, fontSize: 18, color: C.ink, valign: "top" });
  });
  s.addNotes("เชื่อมโยงกับผลลัพธ์การเรียนรู้ของรายวิชา: นักศึกษาจะได้แตะทุกหมวดพื้นฐานของ Flutter ผ่านแอปเดียว ไม่ใช่ตัวอย่างแยกชิ้น");
}

// ============================================================ 4. แผนการสอน
{
  const s = content("แผนการสอน 12 ขั้นตอน (ประมาณ 10 คาบ)");
  const steps = [
    [0, "เตรียมเครื่องมือ สร้างโปรเจกต์", 30], [1, "ธีมสีและจุดเริ่มต้นของแอป", 40], [2, "โมเดลข้อมูลและข้อมูลจำลอง", 50],
    [3, "AppState และโครงหน้าเปล่า", 50], [4, "หน้า Login และสมัครสมาชิก", 60], [5, "HomeShell และแถบเมนูล่าง", 40],
    [6, "หน้ารายการอุปกรณ์", 70], [7, "หน้ารายละเอียดและ Dialog ยืม", 70], [8, "หน้าการยืมของฉัน", 50],
    [9, "หน้าโปรไฟล์และออกจากระบบ", 30], [10, "ฟอร์มเพิ่ม/แก้ไข + image_picker", 70], [11, "ทดสอบอัตโนมัติและสรุป", 40],
  ];
  const colW = 6.0, rowH = 0.82;
  steps.forEach(([n, t, m], i) => {
    const col = Math.floor(i / 6), row = i % 6;
    const x = 0.5 + col * (colW + 0.33), y = 1.45 + row * rowH;
    s.addShape(pres.ShapeType.ellipse, { x, y: y + 0.1, w: 0.55, h: 0.55, fill: { color: n <= 3 ? C.sky : n <= 9 ? C.indigo : C.amber }, line: { color: C.white } });
    s.addText(String(n), { x, y: y + 0.1, w: 0.55, h: 0.55, isTextBox: true, margin: 0, fontFace: "Arial", fontSize: 16, bold: true, color: n > 9 ? C.ink : C.white, align: "center", valign: "middle" });
    s.addText(t, { x: x + 0.75, y, w: colW - 1.9, h: 0.75, isTextBox: true, margin: 0, fontFace: TH, fontSize: 21, color: C.ink, valign: "middle" });
    s.addText(`${m} นาที`, { x: x + colW - 1.1, y, w: 1.1, h: 0.75, isTextBox: true, margin: 0, fontFace: TH, fontSize: 17, color: C.muted, valign: "middle", align: "right" });
  });
  s.addText("ฟ้า = วางรากฐาน   ·   คราม = สร้างหน้าจอ   ·   อำพัน = ปรับปรุงและสรุป", { x: 0.5, y: 6.5, w: 12, h: 0.4, isTextBox: true, margin: 0, fontFace: TH, fontSize: 17, color: C.muted });
  s.addNotes("แต่ละ Step ในสไลด์มี 3 ส่วน: ความรู้ใหม่ → โค้ดสำคัญ → Checkpoint โค้ดเต็มอยู่ในคู่มือ PDF ไม่ต้องพิมพ์ตามจากสไลด์");
}

// ============================================================ 5. ข้อกำหนดการออกแบบ
{
  const s = content("ข้อกำหนดการออกแบบ (จากสเปก UI)");
  const sw = [["283593", "Indigo · สีหลัก", C.white], ["03A9F4", "Sky · สีรอง", C.white], ["FFB300", "Amber · สีเน้น", C.ink]];
  sw.forEach(([hex, name, fg], i) => {
    const x = 0.5 + i * 2.55;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.5, w: 2.35, h: 1.6, fill: { color: hex }, line: { color: hex }, rectRadius: 0.15 });
    s.addText(name, { x: x + 0.15, y: 1.6, w: 2.1, h: 0.5, isTextBox: true, margin: 0, fontFace: TH, fontSize: 20, bold: true, color: fg });
    s.addText("#" + hex, { x: x + 0.15, y: 2.55, w: 2.1, h: 0.4, isTextBox: true, margin: 0, fontFace: MONO, fontSize: 13, color: fg });
  });
  bullets(s, [
    "**ฟอนต์** หัวข้อ 20–22 · เนื้อหา 14–16",
    "**โครงทุกหน้า** `Scaffold` → `AppBar` + `body`",
    "**แถบล่าง 3 เมนู** รายการ · การยืมของฉัน · โปรไฟล์ (หน้า Login และฟอร์มไม่มี)",
    "**2 บทบาท** นักศึกษา และ แอดมิน — แอดมินเห็นปุ่มเพิ่ม/แก้ไขเพิ่มมา",
    "**กฎ UI** เหลือ 0 → ป้ายแดง \"ยืมไม่ได้\" · ใกล้ครบกำหนด → ป้ายส้ม",
  ].map(t => t.replace(/\*\*(.+?)\*\*/, "$1")), { x: 0.5, y: 3.5, w: 7.6, h: 3.2, size: 21, gap: 8 });
  shot(s, "04_detail.png", { x: 9.2, y: 1.45, h: 5.4 });
  s.addNotes("ย้ำว่าสเปกกำหนดสีและโครงไว้แล้ว เราจะใส่ไว้ใน ThemeData ที่เดียว (Step 1) ทุกหน้าจึงหน้าตาเหมือนกันอัตโนมัติ");
}

// ============================================================ 6. Navigation map
{
  const s = content("แผนผังการเชื่อมหน้า (Navigation Map)");
  const box = (x, y, w, h, text, fill, fg = C.white, size = 20) => {
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.12 });
    s.addText(text, { x, y, w, h, isTextBox: true, margin: 0.05, fontFace: TH, fontSize: size, bold: true, color: fg, align: "center", valign: "middle" });
  };
  const arrow = (x1, y1, x2, y2, label) => {
    s.addShape(pres.ShapeType.line, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: C.muted, width: 2, endArrowType: "triangle" } });
    if (label) s.addText(label, { x: (x1 + x2) / 2 - 1.0, y: (y1 + y2) / 2 - 0.42, w: 2.0, h: 0.35, isTextBox: true, margin: 0, fontFace: TH, fontSize: 15, color: C.muted, align: "center" });
  };
  box(0.6, 3.2, 2.2, 0.9, "Login", C.indigoDark);
  box(3.9, 3.2, 2.6, 0.9, "รายการอุปกรณ์\n(หน้าหลัก)", C.indigo, C.white, 18);
  arrow(2.8, 3.65, 3.9, 3.65, "เข้าสำเร็จ");
  // bottom nav siblings
  box(3.9, 5.2, 2.6, 0.8, "การยืมของฉัน", C.sky, C.ink, 18);
  box(3.9, 6.25, 2.6, 0.8, "โปรไฟล์", C.sky, C.ink, 18);
  s.addText("แถบล่างสลับ 3 หน้า", { x: 3.9, y: 4.25, w: 2.6, h: 0.3, isTextBox: true, margin: 0, fontFace: TH, fontSize: 14, color: C.muted, align: "center" });
  s.addShape(pres.ShapeType.line, { x: 5.2, y: 4.1, w: 0, h: 1.1, line: { color: C.muted, width: 2, dashType: "dash" } });
  // detail
  box(8.0, 3.2, 2.6, 0.9, "รายละเอียดอุปกรณ์", C.indigo, C.white, 18);
  arrow(6.5, 3.65, 8.0, 3.65, "แตะการ์ด");
  box(11.2, 3.2, 1.7, 0.9, "Dialog ยืม", C.amber, C.ink, 17);
  arrow(10.6, 3.65, 11.2, 3.65);
  // form
  box(8.0, 1.5, 2.6, 0.9, "เพิ่ม/แก้ไขอุปกรณ์", C.purple, C.white, 18);
  arrow(6.5, 3.2, 8.0, 1.95, "ปุ่ม + (แอดมิน)");
  arrow(9.3, 3.2, 9.3, 2.4, "ดินสอ (แอดมิน)");
  // return
  box(8.0, 5.2, 2.6, 0.8, "คืนของ → รีเฟรช", C.skyLight, C.ink, 17);
  arrow(6.5, 5.6, 8.0, 5.6, "ปุ่มคืน");
  box(8.0, 6.25, 2.6, 0.8, "ออกจากระบบ → Login", C.skyLight, C.ink, 17);
  arrow(6.5, 6.65, 8.0, 6.65);
  s.addText("ปุ่ม back ของระบบจะย้อนตามลูกศรได้ ยกเว้น Login → หน้าหลัก (pushReplacement) และออกจากระบบ (pushAndRemoveUntil)", { x: 0.6, y: 1.5, w: 6.8, h: 1.2, isTextBox: true, margin: 0, fontFace: TH, fontSize: 17, color: C.muted, valign: "top" });
  s.addNotes("อธิบายว่ามีหน้าที่ 'อยู่ในแถบล่าง' 3 หน้า กับหน้าที่ 'ถูก push ทับ' (รายละเอียด, ฟอร์ม) ซึ่งไม่มีแถบล่าง เพราะไม่ได้อยู่ใน HomeShell");
}

// ============================================================ 7. สถาปัตยกรรม
{
  const s = content("สถาปัตยกรรม: หน้าจอคุยกับ AppState เท่านั้น");
  const box = (x, y, w, h, text, fill, fg = C.white, size = 20) => {
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.12 });
    s.addText(text, { x, y, w, h, isTextBox: true, margin: 0.05, fontFace: TH, fontSize: size, bold: true, color: fg, align: "center", valign: "middle" });
  };
  ["Login", "รายการ", "รายละเอียด", "ฟอร์ม", "การยืม", "โปรไฟล์"].forEach((t, i) => box(0.6 + i * 1.32, 1.6, 1.2, 0.8, t, C.indigo, C.white, 17));
  s.addText("lib/screens/  (UI เท่านั้น ไม่มีตรรกะข้อมูล)", { x: 0.6, y: 2.45, w: 8, h: 0.35, isTextBox: true, margin: 0, fontFace: TH, fontSize: 15, color: C.muted });
  s.addShape(pres.ShapeType.line, { x: 4.5, y: 2.85, w: 0, h: 0.6, line: { color: C.muted, width: 2.5, endArrowType: "triangle", beginArrowType: "triangle" } });
  box(2.0, 3.5, 5.0, 1.0, "AppState (ChangeNotifier)\nlogin · borrow · returnItem · addEquipment", C.amber, C.ink, 18);
  s.addText("lib/data/app_state.dart · ทุกหน้าฟังผ่าน ListenableBuilder", { x: 2.0, y: 4.55, w: 6, h: 0.35, isTextBox: true, margin: 0, fontFace: TH, fontSize: 15, color: C.muted });
  s.addShape(pres.ShapeType.line, { x: 3.2, y: 4.95, w: 0, h: 0.6, line: { color: C.muted, width: 2.5, endArrowType: "triangle" } });
  box(1.6, 5.6, 3.2, 0.9, "MockData\n(เฟส 1 · ในหน่วยความจำ)", C.sky, C.ink, 17);
  s.addShape(pres.ShapeType.line, { x: 5.8, y: 4.95, w: 0, h: 0.6, line: { color: C.muted, width: 2.5, endArrowType: "triangle", dashType: "dash" } });
  box(4.4, 5.6, 3.2, 0.9, "REST API + MySQL\n(เฟส 2 · คาบถัดไป)", "B0BEC5", C.ink, 17);
  panel(s, { x: 8.6, y: 1.5, w: 4.25, h: 5.1, title: "ทำไมต้องแยกชั้น?", kind: "learn", size: 18, items: [
    "หน้าจอไม่รู้ว่าข้อมูลมาจากไหน รู้แค่ `AppState.instance`",
    "ยืมที่หน้ารายละเอียด → หน้ารายการและหน้าการยืมอัปเดตเอง",
    "ตอนต่อ MySQL แก้แค่ใน AppState ไม่ต้องแตะหน้าจอ",
    "ทดสอบตรรกะได้โดยไม่ต้องเปิดแอป",
  ] });
  s.addNotes("แนวคิดสำคัญที่สุดของหน่วยนี้ ให้เวลาอธิบายภาพนี้ 5 นาที นักศึกษามักเอาตรรกะไปใส่ในหน้าจอ ทำให้ต่อฐานข้อมูลยาก");
}

// ============================================================ STEP 0
section(0, "เตรียมเครื่องมือและสร้างโปรเจกต์", "ทุกคนรัน flutter doctor ผ่าน สร้างโปรเจกต์ labstock และรันแอปเริ่มต้นได้", 30);
{
  const s = content("ตรวจสอบเครื่องมือและสร้างโปรเจกต์", 0);
  codeBox(s, `flutter --version
flutter doctor

flutter create --project-name labstock --org th.ac.pbru.ice labstock
cd labstock
flutter run          # หรือ flutter run -d chrome`, { x: 0.5, y: 1.45, w: 7.4, h: 2.6, title: "Terminal", size: 15 });
  panel(s, { x: 0.5, y: 4.3, w: 7.4, h: 2.5, title: "โครงสร้างโปรเจกต์ที่ควรรู้", kind: "plain", size: 18, items: [
    "`lib/main.dart` จุดเริ่มต้น (main → runApp)",
    "`pubspec.yaml` รายการ package และ asset",
    "`android/` `ios/` โค้ดเฉพาะแพลตฟอร์ม (แทบไม่ต้องแตะ)",
    "`test/` ไฟล์ทดสอบอัตโนมัติ",
  ] });
  panel(s, { x: 8.2, y: 1.45, w: 4.65, h: 5.35, title: "✔ Checkpoint", kind: "check", size: 18, items: [
    "แอป Counter เปิดขึ้นบน Emulator หรือ Chrome",
    "กด + แล้วตัวเลขเพิ่ม",
    "แก้ข้อความใน main.dart กด r (Hot reload) เห็นผลทันที",
    "สร้างโฟลเดอร์ `lib/models` `data` `utils` `widgets` `screens` ไว้ล่วงหน้า",
  ] });
  s.addNotes("ปัญหาที่พบบ่อย: flutter doctor ติด Android licenses (รัน flutter doctor --android-licenses) หรือ Xcode ยังไม่ได้เปิดครั้งแรก ถ้าเครื่องช้าให้รันบน Chrome ก่อน");
}

// ============================================================ STEP 1
section(1, "ธีมสีและจุดเริ่มต้นของแอป", "กำหนดสี Indigo / Sky / Amber ไว้ที่เดียวใน ThemeData และเข้าใจโครง MaterialApp → Scaffold", 40);
{
  const s = content("ความรู้ใหม่: ThemeData คือ \"ที่เดียว\" ของหน้าตาแอป", 1);
  panel(s, { x: 0.5, y: 1.45, w: 5.4, h: 5.35, title: "แนวคิด", kind: "learn", size: 19, items: [
    "`ColorScheme.fromSeed` สร้างชุดสีทั้งระบบจากสีตั้งต้น",
    "`AppBarTheme` `ElevatedButtonThemeData` `InputDecorationTheme` กำหนดค่าเริ่มต้นของ widget แต่ละชนิด",
    "ทุกหน้าได้สีและรูปทรงเดียวกันโดยไม่ต้องใส่ซ้ำ",
    "แยกไฟล์แล้ว `import 'theme.dart'` ด้วย relative path",
  ] });
  codeBox(s, `class AppColors {
  static const indigo = Color(0xFF283593); // สีหลัก
  static const sky    = Color(0xFF03A9F4); // สีรอง
  static const amber  = Color(0xFFFFB300); // สีเน้น
}

ThemeData buildAppTheme() {
  final scheme = ColorScheme.fromSeed(
    seedColor: AppColors.indigo,
    primary: AppColors.indigo,
    secondary: AppColors.sky,
    tertiary: AppColors.amber,
  );
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.indigo,
      foregroundColor: Colors.white),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size.fromHeight(48))),
    // ... cardTheme, chipTheme, bottomNavigationBarTheme
  );
}`, { x: 6.2, y: 1.45, w: 6.65, h: 5.35, title: "lib/theme.dart (ย่อ)", size: 12 });
  s.addNotes("ชี้ให้เห็น 0xFF นำหน้า = ค่า alpha ทึบ ตามด้วย RRGGBB และอธิบายว่า Size.fromHeight(48) ทำให้ปุ่มทุกปุ่มสูงเท่ากันทั้งแอป");
}
{
  const s = content("main.dart: MaterialApp → theme → home", 1);
  codeBox(s, `import 'package:flutter/material.dart';
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
}`, { x: 0.5, y: 1.45, w: 6.6, h: 5.35, title: "lib/main.dart (ชั่วคราว)", size: 12.5 });
  panel(s, { x: 7.4, y: 1.45, w: 5.45, h: 2.6, title: "✔ Checkpoint", kind: "check", size: 18, items: [
    "AppBar สีน้ำเงินเข้ม ตัวอักษรขาว",
    "พื้นหลังเทาอ่อน ไม่ใช่ขาวล้วน",
    "ไม่มีป้าย DEBUG มุมขวาบน",
  ] });
  panel(s, { x: 7.4, y: 4.25, w: 5.45, h: 2.55, title: "ท้าทาย", kind: "challenge", size: 18, items: [
    "เปลี่ยน `AppColors.indigo` เป็นสีอื่น Hot reload แล้วดูว่าอะไรเปลี่ยนตามบ้าง",
    "ลองลบ `debugShowCheckedModeBanner` ดูว่าเกิดอะไร",
  ] });
  s.addNotes("home ชั่วคราวเป็น Scaffold เปล่า เพราะยังไม่มีหน้า Login เดี๋ยว Step 3 จะเปลี่ยน");
}

// ============================================================ STEP 2
section(2, "โมเดลข้อมูลและข้อมูลจำลอง", "ออกแบบคลาส User · Equipment · Borrow ให้ตรงกับตารางฐานข้อมูล และเตรียมข้อมูลจำลอง", 50);
{
  const s = content("ความรู้ใหม่: ตกลงเรื่อง \"ข้อมูล\" ก่อนวาดหน้าจอ", 2);
  const ent = [["AppUser", ["id", "name", "studentId", "role (student/admin)"], C.indigo],
               ["Equipment", ["id", "name", "category (enum)", "total / available", "description", "imagePath?"], C.sky],
               ["Borrow", ["id", "equipmentId", "quantity", "borrowDate", "dueDate", "returnDate?"], C.amber]];
  ent.forEach(([n, f, col], i) => {
    const x = 0.5 + i * 2.75;
    s.addShape(pres.ShapeType.roundRect, { x, y: 1.5, w: 2.55, h: 0.6, fill: { color: col }, line: { color: col }, rectRadius: 0.1 });
    s.addText(n, { x, y: 1.5, w: 2.55, h: 0.6, isTextBox: true, margin: 0, fontFace: MONO, fontSize: 16, bold: true, color: i === 2 ? C.ink : C.white, align: "center", valign: "middle" });
    s.addShape(pres.ShapeType.rect, { x, y: 2.1, w: 2.55, h: 2.6, fill: { color: "F7F8FC" }, line: { color: col, width: 1.5 } });
    s.addText(f.map((t, k) => ({ text: t, options: { breakLine: k < f.length - 1 } })), { x: x + 0.15, y: 2.2, w: 2.3, h: 2.4, isTextBox: true, margin: 0, fontFace: MONO, fontSize: 12.5, color: C.ink, valign: "top", paraSpaceAfter: 4 });
  });
  s.addShape(pres.ShapeType.line, { x: 5.6, y: 3.0, w: 0.0, h: 0, line: { color: C.muted } });
  s.addText("Borrow อ้างถึง Equipment ด้วย equipmentId (เหมือน foreign key)", { x: 0.5, y: 4.85, w: 8, h: 0.4, isTextBox: true, margin: 0, fontFace: TH, fontSize: 16, color: C.muted });
  panel(s, { x: 8.8, y: 1.5, w: 4.05, h: 5.3, title: "ภาษา Dart ที่ได้ใช้", kind: "learn", size: 17, items: [
    "class + `const` constructor + named parameters `required`",
    "enhanced `enum` มีค่าประกอบ (ชื่อไทย + ไอคอน)",
    "getter คำนวณค่า `isOutOfStock` `daysLeft`",
    "`DateTime` และ `difference().inDays`",
    "`?` nullable เช่น `DateTime? returnDate`",
  ] });
  bullets(s, ["ตรงกับตาราง MySQL ในเฟส 2: `users` · `items` · `borrows`"], { x: 0.5, y: 5.4, w: 8, h: 1.2, size: 20, bullet: false });
  s.addNotes("วาด ER ง่าย ๆ บนกระดาน: users 1-n borrows n-1 items ให้เห็นว่าโมเดลใน Dart กับตารางใน MySQL คือสิ่งเดียวกัน");
}
{
  const s = content("โค้ดสำคัญ: enhanced enum และ getter", 2);
  codeBox(s, `enum EquipmentCategory {
  board('บอร์ด', Icons.developer_board),
  sensor('เซนเซอร์', Icons.sensors),
  cable('สาย', Icons.cable),
  module('โมดูล', Icons.memory),
  tool('เครื่องมือ', Icons.build);

  const EquipmentCategory(this.label, this.icon);
  final String label;
  final IconData icon;
}

class Equipment {
  final String id;
  String name;
  EquipmentCategory category;
  int total;
  int available;
  String description;
  String? imagePath;
  Equipment({required this.id, required this.name, ...});

  bool get isOutOfStock => available <= 0;
}`, { x: 0.5, y: 1.45, w: 6.2, h: 5.35, title: "lib/models/equipment.dart (ย่อ)", size: 12 });
  codeBox(s, `class Borrow {
  ...
  bool get isReturned => returnDate != null;

  /// วันที่เหลือก่อนครบกำหนด (ติดลบ = เลยกำหนด)
  int get daysLeft {
    final today = DateTime.now();
    final d0 = DateTime(today.year, today.month, today.day);
    final d1 = DateTime(dueDate.year, dueDate.month, dueDate.day);
    return d1.difference(d0).inDays;
  }

  bool get isOverdue => !isReturned && daysLeft < 0;
  bool get isDueSoon =>
      !isReturned && daysLeft >= 0 && daysLeft <= 3;
}

// mock_data.dart — วันที่สัมพัทธ์กับวันนี้
DateTime d(int offset) =>
    DateTime(now.year, now.month, now.day + offset);
Borrow(..., borrowDate: d(-5), dueDate: d(2)),`, { x: 6.95, y: 1.45, w: 5.9, h: 5.35, title: "lib/models/borrow.dart + mock_data.dart (ย่อ)", size: 12 });
  s.addNotes("ถามนักศึกษา: ทำไมตัดเวลาออก (สร้าง DateTime ใหม่จาก ปี/เดือน/วัน) ก่อน difference? — เพราะไม่งั้น 23:59 กับ 00:01 จะนับเป็นคนละวันผิด ๆ");
}
{
  const s = content("Checkpoint และไฟล์ที่ต้องมีเมื่อจบ Step 2", 2);
  codeBox(s, `lib/
├─ models/
│  ├─ user.dart        AppUser + UserRole
│  ├─ equipment.dart   Equipment + EquipmentCategory
│  └─ borrow.dart      Borrow + daysLeft
├─ data/
│  └─ mock_data.dart   8 อุปกรณ์ · 4 รายการยืม
└─ utils/
   └─ thai_date.dart   "5 ก.ย." / "5 ก.ย. 2569"`, { x: 0.5, y: 1.45, w: 6.4, h: 3.3, title: "ไฟล์ใหม่ 5 ไฟล์", size: 13.5 });
  panel(s, { x: 0.5, y: 5.0, w: 6.4, h: 1.8, title: "ท้าทาย", kind: "challenge", size: 17, items: [
    "เพิ่มอุปกรณ์จำลองอีก 2 ชิ้นในหมวด \"เครื่องมือ\"",
    "เพิ่มหมวด \"จอแสดงผล\" พร้อม `Icons.monitor`",
  ] });
  panel(s, { x: 7.2, y: 1.45, w: 5.65, h: 5.35, title: "✔ Checkpoint", kind: "check", size: 19, items: [
    "`flutter analyze` → No issues found!",
    "แอปยังหน้าตาเหมือน Step 1 (ขั้นนี้ยังไม่แตะ UI)",
    "อธิบายได้ว่า `available` ต่างจาก `total` อย่างไร",
    "อธิบายได้ว่าทำไม `returnDate` เป็น nullable",
  ] });
  s.addNotes("Step นี้ไม่มีอะไรให้ดูบนจอ ให้ใช้ flutter analyze เป็นตัวยืนยันแทน และให้นักศึกษาอธิบายโมเดลให้เพื่อนฟัง");
}

// ============================================================ STEP 3
section(3, "AppState และโครงหน้าเปล่าทุกหน้า", "สร้างชั้นข้อมูลกลางที่ทุกหน้าใช้ร่วมกัน และสร้างไฟล์หน้าจอทั้ง 8 ไฟล์เป็นโครงเปล่า", 50);
{
  const s = content("ความรู้ใหม่: ChangeNotifier + singleton", 3);
  codeBox(s, `class AppState extends ChangeNotifier {
  AppState._();                                  // ซ่อน constructor
  static final AppState instance = AppState._(); // ตัวเดียวทั้งแอป

  AppUser? _currentUser;
  final List<Equipment> _equipment = MockData.equipment();
  final List<Borrow> _borrows = MockData.borrows();

  bool get isAdmin => _currentUser?.isAdmin ?? false;
  List<Equipment> get equipment => List.unmodifiable(_equipment);

  bool borrow(Equipment item, int quantity, DateTime dueDate) {
    if (quantity <= 0 || quantity > item.available) return false;
    item.available -= quantity;
    _borrows.add(Borrow(...));
    notifyListeners();      // ← บอกทุกหน้าที่ฟังอยู่ให้วาดใหม่
    return true;
  }
}`, { x: 0.5, y: 1.45, w: 7.3, h: 4.3, title: "lib/data/app_state.dart (ย่อ)", size: 12 });
  panel(s, { x: 8.1, y: 1.45, w: 4.75, h: 4.3, title: "แนวคิด", kind: "learn", size: 18, items: [
    "`notifyListeners()` = \"ข้อมูลเปลี่ยนแล้วนะ\"",
    "หน้าจอห่อด้วย `ListenableBuilder(listenable: state)` จะ build ใหม่อัตโนมัติ",
    "`List.unmodifiable` กันหน้าจอแอบแก้ list",
    "singleton: เรียก `AppState.instance` ได้จากทุกที่",
  ] });
  panel(s, { x: 0.5, y: 5.95, w: 12.35, h: 0.85, title: "", kind: "teacher", size: 17, items: [] });
  s.addText("สำหรับผู้สอน: เปรียบ AppState เป็น \"ฐานข้อมูลชั่วคราวในหน่วยความจำ\" — ตอนต่อ MySQL จะเปลี่ยนแค่ข้างในเมธอดให้ไปเรียก API", { x: 0.75, y: 6.05, w: 12, h: 0.65, isTextBox: true, margin: 0, fontFace: TH, fontSize: 18, color: C.purple, valign: "middle" });
  s.addNotes("เทียบกับ setState: setState วาดใหม่แค่ widget ตัวเอง แต่ ChangeNotifier ทำให้หลายหน้าที่ไม่รู้จักกันอัปเดตพร้อมกันได้");
}
{
  const s = content("เทคนิค: สร้างโครงเปล่า (stub) ก่อน แล้วค่อยเติมทีละหน้า", 3);
  codeBox(s, `// lib/screens/equipment_detail_screen.dart (ชั่วคราว)
import 'package:flutter/material.dart';

class EquipmentDetailScreen extends StatelessWidget {
  final String equipmentId;      // ← พารามิเตอร์ต้องตรงกับของจริง
  const EquipmentDetailScreen({super.key, required this.equipmentId});

  @override
  Widget build(BuildContext context) =>
      Scaffold(body: Center(child: Text('Detail $equipmentId (TODO)')));
}`, { x: 0.5, y: 1.45, w: 7.6, h: 2.9, title: "ตัวอย่าง stub 1 ใน 8 ไฟล์ (ดูครบในคู่มือ)", size: 12.5 });
  codeBox(s, `login_screen.dart          LoginScreen()
register_screen.dart       RegisterScreen()
home_shell.dart            HomeShell({initialIndex})
equipment_list_screen.dart EquipmentListScreen()
equipment_detail_screen.dart EquipmentDetailScreen({required equipmentId})
equipment_form_screen.dart EquipmentFormScreen({Equipment? existing})
my_borrows_screen.dart     MyBorrowsScreen()
profile_screen.dart        ProfileScreen()`, { x: 0.5, y: 4.55, w: 7.6, h: 2.25, title: "8 ไฟล์ · 8 คลาส · constructor ที่ต้องตรง", size: 11.5 });
  panel(s, { x: 8.4, y: 1.45, w: 4.45, h: 2.6, title: "ทำไมต้อง stub?", kind: "learn", size: 17, items: [
    "หน้า Login import HomeShell · HomeShell import 3 หน้า · รายการ import รายละเอียด …",
    "ถ้าไม่มีไฟล์ปลายทาง โปรเจกต์คอมไพล์ไม่ผ่านตั้งแต่หน้าแรก",
  ] });
  panel(s, { x: 8.4, y: 4.25, w: 4.45, h: 2.55, title: "✔ Checkpoint", kind: "check", size: 17, items: [
    "เปลี่ยน `home:` ใน main.dart เป็น `const LoginScreen()`",
    "รันแล้วเห็น \"Login (TODO)\" กลางจอ",
    "`flutter analyze` ไม่มี error",
  ] });
  s.addNotes("นี่คือวิธีทำงานจริงในทีม: ตกลง interface (ชื่อคลาส + พารามิเตอร์) ก่อน แล้วแยกกันทำแต่ละหน้าได้");
}

// ============================================================ STEP 4
section(4, "หน้าเข้าสู่ระบบและสมัครสมาชิก", "ฟอร์ม Login รับข้อความ ซ่อน/แสดงรหัสผ่าน และไปหน้าหลักเมื่อสำเร็จโดยกด back กลับมาไม่ได้", 60);
{
  const s = content("ความรู้ใหม่: StatefulWidget, Controller และการนำทาง", 4);
  panel(s, { x: 0.5, y: 1.45, w: 5.6, h: 5.35, title: "แนวคิด", kind: "learn", size: 18, items: [
    "`StatefulWidget` + `setState` สลับไอคอนตา (ซ่อน/แสดงรหัสผ่าน)",
    "`TextEditingController` อ่านค่าที่พิมพ์ และต้อง `dispose()`",
    "`Navigator.push` = ซ้อนหน้าใหม่ (back ได้)",
    "`Navigator.pushReplacement` = แทนที่หน้าเดิม (back ไม่ได้) ใช้หลัง Login สำเร็จ",
    "`Form` + `TextFormField` + `validator` ตรวจข้อมูลหน้าสมัคร",
    "`SnackBar` แจ้งผลสั้น ๆ",
  ] });
  codeBox(s, `final _userCtrl = TextEditingController();
final _passCtrl = TextEditingController();
bool _obscure = true;

void _login() {
  final ok = AppState.instance.login(_userCtrl.text, _passCtrl.text);
  if (!ok) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('กรุณากรอกอีเมล/ชื่อผู้ใช้ และรหัสผ่าน')));
    return;
  }
  Navigator.of(context).pushReplacement(
    MaterialPageRoute(builder: (_) => const HomeShell()));
}

TextField(
  controller: _passCtrl,
  obscureText: _obscure,
  decoration: InputDecoration(
    labelText: 'รหัสผ่าน',
    suffixIcon: IconButton(
      icon: Icon(_obscure ? Icons.visibility_outlined
                          : Icons.visibility_off_outlined),
      onPressed: () => setState(() => _obscure = !_obscure),
    ),
  ),
),`, { x: 6.4, y: 1.45, w: 6.45, h: 5.35, title: "login_screen.dart (ย่อ)", size: 11.5 });
  s.addNotes("การ login จำลอง: ชื่อขึ้นต้นด้วย admin = แอดมิน ให้นักศึกษาลองทั้งสองแบบตั้งแต่ตอนนี้ เพราะ Step 6 จะเห็นปุ่ม + ต่างกัน");
}
{
  const s = content("โครง widget ของหน้า Login", 4);
  codeBox(s, `Scaffold
└─ SafeArea → Center → SingleChildScrollView
     └─ ConstrainedBox(maxWidth: 420)     // ไม่กว้างเกินบนแท็บเล็ต
          └─ Column (crossAxisAlignment: stretch)
               ├─ โลโก้ (Container + Icon)
               ├─ Text 'LabStock'  (32, หนา, Indigo)
               ├─ Text 'คลังอุปกรณ์แล็บ ICE'  (สีจาง)
               ├─ TextField อีเมล/ชื่อผู้ใช้
               ├─ TextField รหัสผ่าน (obscureText + ไอคอนตา)
               ├─ ElevatedButton 'เข้าสู่ระบบ'
               └─ Row: Text 'ยังไม่มีบัญชี?' + TextButton 'สมัครสมาชิก'`, { x: 0.5, y: 1.45, w: 8.0, h: 3.9, title: "widget tree", size: 12.5 });
  panel(s, { x: 0.5, y: 5.5, w: 8.0, h: 1.3, title: "", kind: "teacher", size: 17, items: [] });
  s.addText("สำหรับผู้สอน: ให้นักศึกษาวาด widget tree ของหน้านี้บนกระดาษก่อนเปิดโค้ด แล้วค่อยเทียบ — ฝึกมองหน้าจอเป็นต้นไม้", { x: 0.75, y: 5.6, w: 7.5, h: 1.1, isTextBox: true, margin: 0, fontFace: TH, fontSize: 18, color: C.purple, valign: "middle" });
  shot(s, "01_login.png", { x: 9.6, y: 1.45, h: 5.35 });
  s.addNotes("SingleChildScrollView ป้องกันคีย์บอร์ดดันจนล้น (RenderFlex overflow) ซึ่งเป็น error ที่นักศึกษาเจอบ่อยที่สุด");
}
checkSlide(4, "Checkpoint: หน้า Login และสมัครสมาชิก", [
  "หน้า Login มีโลโก้ ชื่อแอป ช่อง 2 ช่อง ปุ่ม และลิงก์สมัคร",
  "กดไอคอนตา รหัสผ่านซ่อน/แสดงสลับกัน",
  "กดเข้าสู่ระบบโดยไม่กรอก → SnackBar เตือน",
  "กรอกแล้วกด → ไปหน้า \"Home (TODO)\" กด back ไม่กลับมา Login",
  "หน้าสมัคร: กดสมัครโดยไม่กรอก → ข้อความแดงใต้ช่อง",
  "ท้าทาย: validator อีเมลต้องมี @ · ใส่โลโก้จริงด้วย `Image.asset`",
], [{ file: "01_login.png", caption: "เข้าสู่ระบบ" }, { file: "02_register.png", caption: "สมัครสมาชิก" }],
  "ให้เวลาทำ 30 นาที เดินดูทีละโต๊ะ จุดที่พลาดบ่อย: ลืม dispose controller, ใช้ push แทน pushReplacement");

// ============================================================ STEP 5
section(5, "โครงหน้าหลักและแถบเมนูด้านล่าง", "HomeShell ที่มี BottomNavigationBar สลับ 3 หน้า โดยแต่ละหน้ายังคงสถานะไว้เมื่อสลับไปมา", 40);
{
  const s = content("ความรู้ใหม่: IndexedStack + BottomNavigationBar", 5);
  codeBox(s, `class _HomeShellState extends State<HomeShell> {
  late int _index = widget.initialIndex;

  static const _pages = [
    EquipmentListScreen(),
    MyBorrowsScreen(),
    ProfileScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(index: _index, children: _pages),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _index,
        onTap: (i) => setState(() => _index = i),
        items: const [
          BottomNavigationBarItem(
              icon: Icon(Icons.grid_view_outlined), label: 'รายการ'),
          BottomNavigationBarItem(
              icon: Icon(Icons.assignment_outlined), label: 'การยืมของฉัน'),
          BottomNavigationBarItem(
              icon: Icon(Icons.person_outline), label: 'โปรไฟล์'),
        ],
      ),
    );
  }
}`, { x: 0.5, y: 1.45, w: 8.0, h: 5.35, title: "lib/screens/home_shell.dart (ย่อ)", size: 11.5 });
  panel(s, { x: 8.8, y: 1.45, w: 4.05, h: 2.9, title: "แนวคิด", kind: "learn", size: 17, items: [
    "`IndexedStack` สร้างทั้ง 3 หน้าไว้ แสดงทีละหน้า → ข้อความค้นหาไม่หายเมื่อสลับแท็บ",
    "หน้าที่ถูก push ทับ (รายละเอียด/ฟอร์ม) จะไม่มีแถบล่าง",
  ] });
  panel(s, { x: 8.8, y: 4.55, w: 4.05, h: 2.25, title: "✔ Checkpoint", kind: "check", size: 17, items: [
    "หลัง Login เห็นแถบล่าง 3 เมนู",
    "กดแล้วข้อความกลางจอเปลี่ยน (TODO ของแต่ละหน้า)",
    "ไอคอนที่เลือกเป็นสี Indigo",
  ] });
  s.addNotes("ทดลองหลัง Step 6: เปลี่ยน IndexedStack เป็น _pages[_index] แล้วพิมพ์ค้นหา สลับแท็บ กลับมา ข้อความจะหาย — ให้นักศึกษาอธิบายเหตุผล");
}

// ============================================================ STEP 6
section(6, "หน้ารายการอุปกรณ์", "กริดการ์ด ค้นหา กรองตามหมวด ป้าย \"ยืมไม่ได้\" และปุ่ม + เฉพาะแอดมิน", 70);
{
  const s = content("ความรู้ใหม่: GridView, Chip, และการกรองข้อมูล", 6);
  panel(s, { x: 0.5, y: 1.45, w: 5.3, h: 5.35, title: "แนวคิด", kind: "learn", size: 17, items: [
    "`GridView.builder` + `SliverGridDelegateWithMaxCrossAxisExtent` ปรับคอลัมน์ตามความกว้างจอเอง",
    "`ChoiceChip` ในแถวเลื่อนแนวนอน (`SingleChildScrollView`)",
    "`ListenableBuilder` ฟัง AppState",
    "`Card` + `InkWell` การ์ดกดได้",
    "กรองด้วย `where` + `toLowerCase()`",
    "แสดง widget ตามเงื่อนไข: `state.isAdmin ? FAB : null`",
    "`Expanded` ในแถวกันข้อความล้น",
  ] });
  codeBox(s, `List<Equipment> _filtered(List<Equipment> all) {
  final q = _query.trim().toLowerCase();
  return all.where((e) {
    final matchCat = _category == null || e.category == _category;
    final matchQ = q.isEmpty || e.name.toLowerCase().contains(q);
    return matchCat && matchQ;
  }).toList();
}

Expanded(
  child: GridView.builder(
    padding: const EdgeInsets.fromLTRB(16, 4, 16, 88),
    gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
      maxCrossAxisExtent: 220,
      mainAxisSpacing: 12, crossAxisSpacing: 12,
      childAspectRatio: 0.82,
    ),
    itemCount: items.length,
    itemBuilder: (_, i) => _EquipmentCard(item: items[i]),
  ),
),

floatingActionButton: state.isAdmin
    ? FloatingActionButton(
        onPressed: () => Navigator.of(context).push(
          MaterialPageRoute(builder: (_) => const EquipmentFormScreen())),
        child: const Icon(Icons.add))
    : null,`, { x: 6.1, y: 1.45, w: 6.75, h: 5.35, title: "equipment_list_screen.dart (ย่อ)", size: 11.5 });
  s.addNotes("padding ล่าง 88 ของ GridView มีไว้ให้ FAB ไม่บังการ์ดใบสุดท้าย ให้นักศึกษาลองเอาออกแล้วเลื่อนสุด");
}
{
  const s = content("โครง widget และกฎ UI ของการ์ด", 6);
  codeBox(s, `Scaffold
├─ appBar: AppBar('LabStock', actions: [🔔])
├─ body: Column
│    ├─ TextField (ค้นหา)
│    ├─ SingleChildScrollView(horizontal) → Row ของ ChoiceChip
│    └─ Expanded → GridView.builder
│           └─ Card → InkWell → Column
│                ├─ Expanded → EquipmentImage
│                └─ Text(ชื่อ) + Row[ Text('เหลือ N'), ป้าย 'ยืมไม่ได้' ]
├─ floatingActionButton: FAB '+' (เฉพาะ admin)
└─ bottomNavigationBar: (มาจาก HomeShell)`, { x: 0.5, y: 1.45, w: 7.8, h: 3.0, title: "widget tree", size: 12 });
  codeBox(s, `if (item.isOutOfStock)
  Container(
    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
    decoration: BoxDecoration(
      color: AppColors.danger,
      borderRadius: BorderRadius.circular(8)),
    child: const Text('ยืมไม่ได้',
      style: TextStyle(color: Colors.white, fontSize: 11)),
  ),`, { x: 0.5, y: 4.6, w: 7.8, h: 2.2, title: "ป้ายแดงเมื่อเหลือ 0", size: 11 });
  shot(s, "03_list_admin.png", { x: 9.6, y: 1.45, h: 5.35 });
  s.addNotes("ชี้ที่ภาพ: ค้นหา → ชิป → กริด → FAB ให้นักศึกษาชี้ว่าแต่ละส่วนตรงกับบรรทัดไหนใน tree");
}
checkSlide(6, "Checkpoint: หน้ารายการอุปกรณ์", [
  "การ์ด 8 ใบ กริด 2 คอลัมน์บนมือถือ",
  "DHT22: \"เหลือ 0\" สีแดง + ป้าย \"ยืมไม่ได้\"",
  "พิมพ์ \"ard\" เหลือแค่ Arduino · กดชิป \"สาย\" เหลือ 2 ใบ",
  "Login เป็น admin เห็นปุ่ม + สีอำพัน · ชื่ออื่นไม่เห็น",
  "แตะการ์ด → \"Detail e1 (TODO)\"",
  "ท้าทาย: เมนูเรียงลำดับด้วย `PopupMenuButton` · การ์ดที่หมดให้จางด้วย `Opacity`",
], [{ file: "03_list_admin.png", caption: "มุมมองแอดมิน" }],
  "ให้เวลา 40 นาที Step นี้ยาวที่สุด แบ่งเป็น 2 รอบ: รอบแรกให้กริดขึ้นก่อน รอบสองค่อยใส่ค้นหา/กรอง/FAB");

// ============================================================ STEP 7
section(7, "หน้ารายละเอียดอุปกรณ์และ Dialog ยืม", "รับ id จากหน้ารายการ แสดงข้อมูลชิ้นเดียว เปิด Dialog เลือกจำนวน/วันคืน แล้วบันทึกลง AppState", 70);
{
  const s = content("ความรู้ใหม่: ส่งค่าไปหน้าใหม่ และรับค่ากลับจาก Dialog", 7);
  codeBox(s, `// หน้ารายการ: ส่งแค่ id
Navigator.of(context).push(MaterialPageRoute(
  builder: (_) => EquipmentDetailScreen(equipmentId: item.id)));

// หน้ารายละเอียด: ค้นข้อมูลสดจาก AppState ด้วย id
final item = state.findEquipment(equipmentId);

// เปิด Dialog แล้ว "รอ" ค่าที่ส่งกลับ
Future<void> _showBorrowDialog(BuildContext context, Equipment item) async {
  final result = await showDialog<_BorrowRequest>(
    context: context,
    builder: (_) => _BorrowDialog(item: item),
  );
  if (result == null || !context.mounted) return;   // กดยกเลิก

  final ok = AppState.instance.borrow(item, result.quantity, result.dueDate);
  if (!context.mounted) return;
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(
      ok ? 'ยืม \${item.name} x\${result.quantity} สำเร็จ' : 'ยืมไม่สำเร็จ')));
  if (ok) Navigator.of(context).pop();              // กลับหน้ารายการ
}

// ใน Dialog: ส่งค่ากลับ
FilledButton(
  onPressed: () => Navigator.pop(context, _BorrowRequest(_qty, _due)),
  child: const Text('ยืนยันยืม'))`, { x: 0.5, y: 1.45, w: 8.1, h: 5.35, title: "equipment_detail_screen.dart (ย่อ)", size: 11.5 });
  panel(s, { x: 8.9, y: 1.45, w: 3.95, h: 5.35, title: "แนวคิด", kind: "learn", size: 17, items: [
    "ส่ง id ไม่ส่ง object → ข้อมูลสดเสมอ",
    "`showDialog<T>` คืน `Future<T?>` · null = ยกเลิก",
    "`Navigator.pop(context, value)` ส่งค่ากลับ",
    "`context.mounted` ตรวจก่อนใช้ context หลัง `await`",
    "`onPressed: null` = ปุ่มปิด (ของหมด)",
    "`showDatePicker` เลือกวันคืน",
  ] });
  s.addNotes("แพตเทิร์น await showDialog → ตรวจ null → ทำงาน → ตรวจ mounted ใช้ซ้ำในหน้าคืนของ (Step 8) และลบ (ท้าทาย Step 10)");
}
{
  const s = content("หน้ารายละเอียดและ Dialog ยืม", 7);
  codeBox(s, `Scaffold
├─ appBar: AppBar('รายละเอียดอุปกรณ์')
│     actions: [ if (isAdmin) IconButton(ดินสอ) ]
└─ body: SingleChildScrollView → Column
     ├─ ClipRRect → AspectRatio(16/10) → EquipmentImage
     ├─ Text(ชื่อ, headlineSmall)
     ├─ _InfoRow(หมวด) · _InfoRow(คงเหลือ x / y ชิ้น)
     ├─ Text(รายละเอียด)
     └─ ElevatedButton.icon('ยืมอุปกรณ์')
          onPressed: isOutOfStock ? null : _showBorrowDialog

AlertDialog (_BorrowDialog: StatefulWidget)
├─ Row: 'จำนวน'  [−]  N  [+]     (จำกัดไม่เกิน available)
├─ ListTile: 'วันคืน' + วันที่  → showDatePicker
└─ actions: ยกเลิก · ยืนยันยืม`, { x: 0.5, y: 1.45, w: 6.9, h: 5.35, title: "widget tree", size: 12 });
  shot(s, "04_detail.png", { x: 7.8, y: 1.45, h: 5.35 });
  shot(s, "05_borrow_dialog.png", { x: 10.5, y: 1.45, h: 5.35 });
  s.addNotes("Dialog ต้องเป็น StatefulWidget แยกต่างหาก เพราะจำนวนและวันที่เปลี่ยนภายใน Dialog ถ้าใช้ setState ของหน้าหลัก Dialog จะไม่วาดใหม่");
}
checkSlide(7, "Checkpoint: รายละเอียดและการยืม", [
  "แตะ Arduino เห็นรูปใหญ่ ชื่อ หมวด คงเหลือ 5 / 10 รายละเอียด",
  "แตะ DHT22 ปุ่มยืมเป็นสีเทา กดไม่ได้",
  "กดยืม → Dialog กด + ได้ไม่เกินจำนวนที่เหลือ",
  "ยืนยัน → กลับหน้ารายการ การ์ดเปลี่ยนเป็น \"เหลือ 4\" ทันที",
  "admin เห็นดินสอใน AppBar → \"Form (TODO)\"",
  "ท้าทาย: ช่อง \"เหตุผลที่ยืม\" · จำกัดวันคืนไม่เกิน 14 วัน",
], [{ file: "04_detail.png", caption: "รายละเอียด" }, { file: "05_borrow_dialog.png", caption: "Dialog ยืม" }],
  "ถามว่าทำไมการ์ดที่หน้ารายการเปลี่ยนเป็น 'เหลือ 4' ทั้งที่เราไม่ได้เขียนโค้ดอัปเดตหน้านั้นเลย → notifyListeners + ListenableBuilder");

// ============================================================ STEP 8
section(8, "หน้าการยืมของฉัน", "แท็บ กำลังยืม / ประวัติ ป้ายเตือนใกล้ครบกำหนด และปุ่มคืนของที่คืนจำนวนเข้าสต็อก", 50);
{
  const s = content("ความรู้ใหม่: TabBar และการแยก widget ย่อย", 8);
  codeBox(s, `DefaultTabController(
  length: 2,
  child: Scaffold(
    appBar: AppBar(
      title: const Text('การยืมของฉัน'),
      bottom: const TabBar(tabs: [Tab(text: 'กำลังยืม'), Tab(text: 'ประวัติ')]),
    ),
    body: ListenableBuilder(
      listenable: state,
      builder: (context, _) => TabBarView(children: [
        _BorrowList(borrows: state.activeBorrows, emptyText: 'ยังไม่มีรายการที่กำลังยืม'),
        _BorrowList(borrows: state.borrowHistory, emptyText: 'ยังไม่มีประวัติการยืม'),
      ]),
    ),
  ),
)

// ป้ายเตือนในการ์ด
Widget? badge;
if (b.isOverdue) {
  badge = _Badge(color: AppColors.danger, icon: Icons.error_outline,
                 label: 'เลยกำหนด \${-b.daysLeft} วัน');
} else if (b.isDueSoon) {
  badge = _Badge(color: Colors.orange.shade700, icon: Icons.warning_amber_rounded,
                 label: b.daysLeft == 0 ? 'ครบกำหนดวันนี้' : 'อีก \${b.daysLeft} วันครบกำหนด');
}`, { x: 0.5, y: 1.45, w: 8.3, h: 5.35, title: "my_borrows_screen.dart (ย่อ)", size: 11 });
  panel(s, { x: 9.1, y: 1.45, w: 3.75, h: 5.35, title: "แนวคิด", kind: "learn", size: 17, items: [
    "`DefaultTabController` + `TabBar` (ใน `AppBar.bottom`) + `TabBarView`",
    "`ListView.builder` รายการแนวตั้ง",
    "แยก `_BorrowList` `_BorrowCard` `_Badge` → อ่านง่าย ใช้ซ้ำ",
    "Empty state เมื่อไม่มีข้อมูล",
    "Dialog ยืนยันก่อนคืนของ",
  ] });
  s.addNotes("ตรรกะ isOverdue/isDueSoon อยู่ในโมเดล (Step 2) หน้าจอแค่เลือกสี — ตัวอย่างการแยก 'ตรรกะ' ออกจาก 'การแสดงผล'");
}
checkSlide(8, "Checkpoint: การยืมของฉัน", [
  "แท็บกำลังยืม: Arduino x1 (ป้ายส้ม อีก 2 วัน) และ Servo x2",
  "แท็บประวัติ: 2 รายการที่คืนแล้ว มีเครื่องหมายถูกเขียว",
  "กดคืนของ → ยืนยัน → ย้ายไปแท็บประวัติ และหน้ารายการได้จำนวนคืน",
  "ยืมจากหน้ารายละเอียด กลับมาแท็บนี้ เห็นรายการใหม่",
  "ท้าทาย: แก้ mock ให้มีรายการเลยกำหนด (`dueDate: d(-1)`) ดูป้ายแดง · Badge ตัวเลขบนไอคอนแท็บ",
], [{ file: "07_borrows.png", caption: "กำลังยืม" }],
  "ให้ทดสอบ flow เต็ม: ยืม → ดูในแท็บ → คืน → ดูสต็อก นี่คือ 'user story' หลักของแอป");

// ============================================================ STEP 9
section(9, "หน้าโปรไฟล์และออกจากระบบ", "แสดงผู้ใช้ปัจจุบัน เมนูรายการ และออกจากระบบแบบล้าง stack ทั้งหมด", 30);
{
  const s = content("ความรู้ใหม่: pushAndRemoveUntil และ ListTile", 9);
  codeBox(s, `void _logout(BuildContext context) {
  AppState.instance.logout();
  Navigator.of(context).pushAndRemoveUntil(
    MaterialPageRoute(builder: (_) => const LoginScreen()),
    (route) => false,        // ← ลบทุกหน้าใน stack
  );
}

ListTile(
  leading: const Icon(Icons.info_outline, color: AppColors.indigo),
  title: const Text('เกี่ยวกับแอป'),
  trailing: const Icon(Icons.chevron_right),
  onTap: () => showAboutDialog(
    context: context,
    applicationName: 'LabStock',
    applicationVersion: '1.0.0 (UI phase)',
  ),
),`, { x: 0.5, y: 1.45, w: 6.6, h: 3.9, title: "profile_screen.dart (ย่อ)", size: 12 });
  panel(s, { x: 0.5, y: 5.5, w: 6.6, h: 1.3, title: "", kind: "learn", size: 17, items: [] });
  s.addText("push = ซ้อน · pushReplacement = แทนที่ 1 หน้า · pushAndRemoveUntil = แทนที่แล้วลบทั้ง stack", { x: 0.75, y: 5.6, w: 6.2, h: 1.1, isTextBox: true, margin: 0, fontFace: TH, fontSize: 18, color: "01579B", valign: "middle" });
  panel(s, { x: 7.4, y: 1.45, w: 2.9, h: 5.35, title: "✔ Checkpoint", kind: "check", size: 16, items: [
    "ชื่อ/บทบาท/รหัสตรงกับที่ login",
    "เกี่ยวกับแอป → Dialog",
    "ออกจากระบบ → Login และ back ไม่กลับเข้าแอป",
    "ท้าทาย: เมนูประวัติ → `HomeShell(initialIndex: 1)`",
  ] });
  shot(s, "08_profile.png", { x: 10.55, y: 1.45, h: 5.35 });
  s.addNotes("Step สั้น ใช้เป็นช่วงให้คนที่ตามไม่ทันตามให้ทัน และให้คนที่เสร็จแล้วทำท้าทาย");
}

// ============================================================ STEP 10
section(10, "ฟอร์มเพิ่ม/แก้ไขอุปกรณ์ และการเลือกรูปภาพ", "ฟอร์มเดียวใช้ได้ 2 โหมด ตรวจสอบข้อมูล และเลือกรูปจากกล้อง/คลังภาพด้วย image_picker", 70);
{
  const s = content("ความรู้ใหม่: package ภายนอก และ permission", 10);
  codeBox(s, `flutter pub add image_picker`, { x: 0.5, y: 1.45, w: 7.2, h: 0.85, title: "Terminal", size: 14 });
  codeBox(s, `<key>NSCameraUsageDescription</key>
<string>ใช้กล้องเพื่อถ่ายรูปอุปกรณ์</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>ใช้คลังภาพเพื่อเลือกรูปอุปกรณ์</string>`, { x: 0.5, y: 2.45, w: 7.2, h: 1.6, title: "ios/Runner/Info.plist (เพิ่มก่อน </dict>) · Android ไม่ต้อง", size: 12 });
  codeBox(s, `Future<void> _pickImage() async {
  final source = await showModalBottomSheet<ImageSource>(   // ถ่าย / คลังภาพ
      context: context, builder: (_) => ...);
  if (source == null) return;
  try {
    final file = await ImagePicker().pickImage(source: source, maxWidth: 1200);
    if (file != null) setState(() => _imagePath = file.path);
  } catch (e) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('เลือกรูปไม่สำเร็จ: $e')));
  }
}`, { x: 0.5, y: 4.2, w: 7.2, h: 2.6, title: "equipment_form_screen.dart (ย่อ)", size: 11 });
  panel(s, { x: 8.0, y: 1.45, w: 4.85, h: 5.35, title: "แนวคิด", kind: "learn", size: 17, items: [
    "`flutter pub add` เพิ่ม dependency ใน pubspec.yaml",
    "iOS ต้องประกาศเหตุผลการขอสิทธิ์ ไม่งั้นแอปปิดตัวทันทีที่เรียกกล้อง",
    "async/await กับ `pickImage` และ try/catch ดัก error (Simulator ไม่มีกล้อง)",
    "`showModalBottomSheet` ให้ผู้ใช้เลือกแหล่งรูป",
    "`kIsWeb` ตรวจก่อนใช้ `Image.file` (ใช้บนเว็บไม่ได้)",
    "widget เดียว 2 โหมด: `Equipment? existing` null = เพิ่ม",
    "`DropdownButtonFormField` ผูกกับ enum · `inputFormatters` ตัวเลขเท่านั้น",
  ] });
  s.addNotes("แสดงตัวอย่างสดว่าถ้าไม่ใส่ Info.plist แล้วกดถ่ายรูปบนเครื่องจริง แอปจะ crash ทันที ให้จำเป็นบทเรียน");
}
{
  const s = content("ฟอร์มเดียว 2 โหมด: เพิ่ม และ แก้ไข", 10);
  codeBox(s, `class EquipmentFormScreen extends StatefulWidget {
  final Equipment? existing;      // null = โหมดเพิ่ม
  const EquipmentFormScreen({super.key, this.existing});
}

bool get _isEdit => widget.existing != null;
late final _nameCtrl = TextEditingController(text: widget.existing?.name);

void _save() {
  if (!_formKey.currentState!.validate()) return;
  final total = int.parse(_totalCtrl.text.trim());
  if (_isEdit) {
    final item = widget.existing!;
    final borrowed = item.total - item.available;   // ที่ถูกยืมอยู่
    item
      ..name = _nameCtrl.text.trim()
      ..category = _category
      ..total = total
      ..available = (total - borrowed).clamp(0, total)
      ..description = _descCtrl.text.trim();
    state.updateEquipment(item);
  } else {
    state.addEquipment(Equipment(id: 'e\${DateTime.now().millisecondsSinceEpoch}',
        name: ..., total: total, available: total, ...));
  }
  Navigator.of(context).pop();
}`, { x: 0.5, y: 1.45, w: 7.0, h: 5.35, title: "equipment_form_screen.dart (ย่อ)", size: 11 });
  shot(s, "09_form_add.png", { x: 7.85, y: 1.45, h: 5.1, caption: "โหมดเพิ่ม (ว่าง)" });
  shot(s, "06_form_edit.png", { x: 10.55, y: 1.45, h: 5.1, caption: "โหมดแก้ไข (กรอกไว้)" });
  s.addText("", { x: 7.85, y: 6.85, w: 5.2, h: 0.2, isTextBox: true, margin: 0, fontFace: TH, fontSize: 14, color: C.muted });
  s.addNotes("cascade operator (..) เป็นของใหม่สำหรับหลายคน อธิบายว่าเท่ากับเขียน item.name = ...; item.category = ...; ทีละบรรทัด");
}
checkSlide(10, "Checkpoint: ฟอร์มและรูปภาพ", [
  "admin กด + → ฟอร์มว่าง หัวข้อ \"เพิ่มอุปกรณ์\"",
  "กดบันทึกโดยไม่กรอก → เตือนใต้ช่องชื่อและจำนวน",
  "กรอกครบ → กลับหน้ารายการ เห็นการ์ดใหม่ต่อท้าย",
  "จากรายละเอียด กดดินสอ → ฟอร์มมีข้อมูลเดิม หัวข้อ \"แก้ไขอุปกรณ์\"",
  "ถ่าย/เลือกรูป → bottom sheet 2 ตัวเลือก (Simulator ใช้คลังภาพ)",
  "ท้าทาย: ปุ่มลบในโหมดแก้ไข + Dialog ยืนยัน + `removeEquipment`",
], [{ file: "09_form_add.png", caption: "เพิ่ม" }, { file: "06_form_edit.png", caption: "แก้ไข" }],
  "จุดพลาดบ่อย: ลืม initialValue ของ Dropdown ทำให้โหมดแก้ไขไม่แสดงหมวดเดิม และลืม pod install หลังเพิ่ม package บน iOS");

// ============================================================ STEP 11
section(11, "ทดสอบอัตโนมัติ สรุป และก้าวต่อไป", "เขียน widget test ตรวจ flow หลัก ทบทวนสิ่งที่เรียนรู้ และเตรียมต่อ MySQL", 40);
{
  const s = content("ความรู้ใหม่: widget test ยืนยันว่า flow ยังทำงาน", 11);
  codeBox(s, `testWidgets('login as student then navigate tabs', (tester) async {
  await tester.pumpWidget(const LabStockApp());
  expect(find.text('LabStock'), findsOneWidget);

  await tester.enterText(find.byType(TextField).first, 'somchai');
  await tester.enterText(find.byType(TextField).last, '123456');
  await tester.tap(find.widgetWithText(ElevatedButton, 'เข้าสู่ระบบ'));
  await tester.pumpAndSettle();

  expect(find.text('Arduino UNO R3'), findsOneWidget);
  expect(find.byType(FloatingActionButton), findsNothing); // นักศึกษาไม่เห็น +
  expect(find.text('ยืมไม่ได้'), findsOneWidget);          // DHT22 เหลือ 0

  await tester.tap(find.text('โปรไฟล์'));
  await tester.pumpAndSettle();
  await tester.tap(find.text('ออกจากระบบ'));
  await tester.pumpAndSettle();
  expect(find.text('เข้าสู่ระบบ'), findsOneWidget);
});`, { x: 0.5, y: 1.45, w: 8.2, h: 4.2, title: "test/widget_test.dart (ย่อ)", size: 11.5 });
  codeBox(s, `flutter analyze      # No issues found!
flutter test         # All tests passed!`, { x: 0.5, y: 5.85, w: 8.2, h: 0.95, title: "", size: 13 });
  panel(s, { x: 9.0, y: 1.45, w: 3.85, h: 5.35, title: "แนวคิด", kind: "learn", size: 17, items: [
    "`pumpWidget` สร้างแอปในหน่วยความจำ ไม่ต้องเปิด Emulator",
    "`enterText` `tap` จำลองผู้ใช้",
    "`pumpAndSettle` รอแอนิเมชันจบ",
    "`find.text` `find.byType` หา widget",
    "`expect(..., findsOneWidget)`",
    "ทดสอบเป็นตาข่ายกันพัง ตอนต่อ MySQL",
  ] });
  s.addNotes("รันสดให้ดู 1 ครั้ง แล้วแก้ข้อความปุ่มให้ผิด รันอีกครั้งให้เห็นว่า test จับได้");
}
{
  const s = content("สรุป: ทำแอปเดียว ได้ครบทุกเรื่อง", 11);
  const rows = [
    [{ text: "หมวด", options: { bold: true, color: C.white, fill: { color: C.indigo } } }, { text: "สิ่งที่ใช้ใน LabStock", options: { bold: true, color: C.white, fill: { color: C.indigo } } }],
    ["โครงสร้าง", "MaterialApp · Scaffold · AppBar · BottomNavigationBar · IndexedStack · TabBar"],
    ["แสดงผล", "GridView · ListView · Card · ListTile · CircleAvatar · Chip · Container/BoxDecoration"],
    ["รับข้อมูล", "TextField · TextFormField/validator · Dropdown · DatePicker · image_picker"],
    ["นำทาง", "push · pushReplacement · pushAndRemoveUntil · ส่งค่าผ่าน constructor · รับค่าจาก Dialog"],
    ["สถานะ", "StatefulWidget/setState · ChangeNotifier + ListenableBuilder · singleton"],
    ["Dart", "class · enhanced enum · getter · named params · async/await · where/map · cascade (..)"],
    ["คุณภาพ", "ธีมกลาง · แยก widget ย่อย · flutter analyze · widget test"],
  ];
  s.addTable(rows, { x: 0.5, y: 1.45, w: 12.35, colW: [2.2, 10.15], fontFace: TH, fontSize: 18, color: C.ink, border: { type: "solid", color: "C9CCD9", pt: 1 }, rowH: 0.62, valign: "middle", margin: 0.06 });
  s.addNotes("ให้นักศึกษาเลือก 1 หมวดที่ตัวเองยังไม่มั่นใจ แล้วกลับไปอ่านโค้ด Step ที่เกี่ยวข้องในคู่มือ");
}
{
  const s = content("ก้าวต่อไป: เฟส 2 ต่อฐานข้อมูล MySQL", 11);
  const step = (i, t, d) => {
    const y = 1.5 + i * 1.02;
    s.addShape(pres.ShapeType.ellipse, { x: 0.5, y: y + 0.12, w: 0.62, h: 0.62, fill: { color: C.amber }, line: { color: C.amber } });
    s.addText(String(i + 1), { x: 0.5, y: y + 0.12, w: 0.62, h: 0.62, isTextBox: true, margin: 0, fontFace: "Arial", fontSize: 18, bold: true, color: C.ink, align: "center", valign: "middle" });
    s.addText(t, { x: 1.35, y, w: 6.2, h: 0.45, isTextBox: true, margin: 0, fontFace: TH, fontSize: 21, bold: true, color: C.indigo });
    s.addText(runs(d, { fontFace: TH, fontSize: 17, color: C.ink }), { x: 1.35, y: y + 0.42, w: 6.2, h: 0.5, isTextBox: true, margin: 0 });
  };
  step(0, "สร้าง REST API", "PHP หรือ Node.js ครอบตาราง users / items / borrows");
  step(1, "เพิ่ม package http", "สร้าง `lib/data/api_service.dart` เรียก GET/POST/PUT");
  step(2, "แก้ AppState ให้เป็น Future", "เรียก API แล้ว `notifyListeners()` เมื่อได้ผล — หน้าจอไม่ต้องแก้");
  step(3, "เพิ่ม loading และ error", "`CircularProgressIndicator` และ SnackBar เมื่อเน็ตล่ม");
  step(4, "เก็บ session", "`shared_preferences` ไม่ต้อง login ทุกครั้ง");
  panel(s, { x: 8.0, y: 1.45, w: 4.85, h: 5.35, title: "โปรเจกต์ท้ายบท (เลือก 1)", kind: "challenge", size: 17, items: [
    "แจ้งเตือน: กระดิ่งแสดงจำนวนที่จะครบกำหนดใน 3 วัน",
    "หน้าแอดมิน: ดูรายการยืมของทุกคน อนุมัติ/ปฏิเสธ",
    "โหมดมืด: `darkTheme` + สวิตช์ในหน้าตั้งค่า",
    "ค้นหาขั้นสูง: หลายหมวดพร้อมกันด้วย `FilterChip`",
  ] });
  s.addNotes("ย้ำภาพสถาปัตยกรรม (สไลด์ 7): เพราะหน้าจอคุยกับ AppState เท่านั้น เฟส 2 จึงแก้แค่ชั้นข้อมูล");
}

// ============================================================ ปิด
{
  const s = pres.addSlide();
  s.background = { color: C.indigo };
  s.addText("ขอบคุณครับ", { x: 0.9, y: 2.2, w: 8, h: 1.2, isTextBox: true, margin: 0, fontFace: TH, fontSize: 60, bold: true, color: C.white });
  s.addText("เอกสารประกอบ: คู่มือปฏิบัติการ LabStock (PDF) มีโค้ดเต็มทุกไฟล์ + Checkpoint ทุกขั้นตอน", { x: 0.9, y: 3.5, w: 9, h: 0.6, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, color: "C5CAE9" });
  s.addText("ทดลองเข้าสู่ระบบ: ชื่อผู้ใช้ขึ้นต้นด้วย admin = แอดมิน · อื่น ๆ = นักศึกษา", { x: 0.9, y: 4.1, w: 9, h: 0.6, isTextBox: true, margin: 0, fontFace: TH, fontSize: 22, color: C.amber });
  shot(s, "08_profile.png", { x: 10.4, y: 0.7, h: 5.9 });
  footer(s, true);
}

pres.writeFile({ fileName: OUT }).then(f => console.log("saved", f, "slides:", slideNo));
