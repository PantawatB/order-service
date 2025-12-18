# A2.2: Handout for Integration Testing & Automation of Order Service

เป้าหมาย
- ฝึกทำ Integration Testing 3 แบบ: Top-down, Bottom-up, Sandwich
- ฝึกเขียน Stub/Driver/Spy
- พิสูจน์ได้ว่าระบบตอบสนองถูกต้อง ไม่เกิดความผิดพลาด
- การทำให้เทสต์รันอัตโนมัติบน CI อย่างเป็นระบบ
---

เครื่องมือ
- Real component (ดู High-level call graph ด้านล่าง)
- Automation
     - pytest	   รัน test อัตโนมัติ
     - Stub	      ควบคุมพฤติกรรม component
     - Spy	      ตรวจว่าถูกเรียกหรือไม่

วิธีเริ่มต้น
1) ติดตั้ง dependencies (pytest ในกรณีนี้)
   pip install -r requirements.txt
2) รันทดสอบ
   pytest -q

ต่อไป แบบฝึกหัดที่ต้องทำ
- ทำความเข้าใจโค้ดในไฟล์: inventory.py, payment.py, shipping.py, emailer.py, order.py
- ทำเทสต์ครบ 3 แบบ: Top-down, Bottom-up, Sandwich โดย ใส่ markers บนไฟล์/ฟังก์ชันทดสอบให้ตรงหมวด 
     - อ่านเทสต์ตัวอย่างใน tests/ แล้ว:
            1) เพิ่มกรณีทดสอบ Top-down:
               - เขียน StubPayment ที่ล้มเหลวแบบต่างๆ
               - เพิ่ม SpyEmail ตรวจ subject/body
            2) เพิ่มกรณีทดสอบ Bottom-up:
               - เพิ่มเทสต์ reserve/release ที่ขอบเขต
            3) เพิ่มกรณีทดสอบ Sandwich:
               - ใช้ SimplePayment จริง + Email spy
               - เพิ่ม region อื่น (เช่น "US")
- สำหรับแต่ละแบบ สร้าง stub/spy เขียนเทสต์ แล้วรัน
- Automation: ทำผ่าน GitHub Actions (CI)
     - รันเฉพาะหมวดได้ เช่น pytest -m topdown -q
     - รันพร้อม coverage
- ส่ง URL ของ GitHub Repo สำหรับส่งงาน ที่มี folder ตรงกับหมายเลขงาน (เช่น AT2-2) ในนั้นมีไฟล์เทสต์ทั้งหมดและไฟล์​ตอบคำถาม (เช่น AT2-2-ANSWER.md) ในทุกไฟล์ที่ส่งขอให้มีรหัสนศ.ของคนทำ
     1. สิ่งที่ค้นพบว่าระบบไม่เป็นไปตามที่คาดหวังไว้ หรือปัญหาที่ไม่คิดว่าจะเจอ (อย่างต่ำ 5 บรรทัด)
     2. การทดสอบโค้ดนี้แบบอัตโนมัติ มีข้อดี ข้อเสียอะไรบ้าง
     3. ขั้นตอนการทำให้เทสต์รันอัตโนมัติอย่างเป็นระบบที่ทำในกิจกรรมนี้ คืออะไร
     4. ชุดทดสอบตั้งต้น ได้ coverage เท่าไร เมื่อเพิ่มกรณีทดสอบแล้ว ได้ coverage เท่าไร
     5. เป็นไปได้ไหมที่จะทำให้ได้ 100% integration test coverage ให้เหตุผล (อย่างต่ำ 3-4 บรรทัด)
-  

### High-Level Call Graph
OrderService  
├── InventoryRepository  
│       ├── reserve()  
│       └── release()  
│  
├── ShippingService  
│   └── cost()  
│  
├── PaymentGateway  
│   └── charge()  
│  
└── EmailService  
    └── send()
--- 
