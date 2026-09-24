const _thaiMonths = [
  'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
  'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.',
];

/// แปลงวันที่เป็นข้อความสั้น ๆ แบบไทย เช่น "5 ก.ย."
String thaiShortDate(DateTime d) => '${d.day} ${_thaiMonths[d.month - 1]}';

/// แบบเต็ม พ.ศ. เช่น "5 ก.ย. 2569"
String thaiFullDate(DateTime d) =>
    '${d.day} ${_thaiMonths[d.month - 1]} ${d.year + 543}';
