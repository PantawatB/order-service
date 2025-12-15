# Integration Testing (Medium) — Starter

เป้าหมาย
- ฝึกทำ Integration Testing 3 แบบ: Top-down, Bottom-up, Sandwich
- ฝึกเขียน Stub/Driver/Spy
- เข้าใจการแยกส่วนบริการ (Inventory, Payment, Shipping, Email) และการรวมระบบ

วิธีเริ่มต้น
1) ติดตั้ง dependencies
   pip install -r requirements.txt
2) รันทดสอบ
   pytest -q

แบบฝึกหัดที่ต้องทำ
- ทำความเข้าใจโค้ดในไฟล์: inventory.py, payment.py, shipping.py, emailer.py, order.py
- อ่านเทสต์ตัวอย่างใน tests/ แล้ว:
  1) เพิ่มกรณีทดสอบ Top-down:
     - เขียน StubPayment ที่ล้มเหลวแบบต่างๆ
     - เพิ่ม SpyEmail ตรวจ subject/body
  2) เพิ่มกรณีทดสอบ Bottom-up:
     - เพิ่มเทสต์ reserve/release ที่ขอบเขต
  3) เพิ่มกรณีทดสอบ Sandwich:
     - ใช้ SimplePayment จริง + Email spy
     - เพิ่ม region อื่น (เช่น "US")
- สรุปสิ่งที่ค้นพบสั้นๆ (5–10 บรรทัด)

โครงร่างสถาปัตยกรรม
OrderService -> Inventory, Payment, Shipping, Email
