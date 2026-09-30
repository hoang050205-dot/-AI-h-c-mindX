---
name: ai4a:build-dashboard-BI
description: "Chuyên gia Thiết kế & Xây dựng Business Intelligence Dashboard Đẳng cấp: kiến tạo giao diện BI chuẩn doanh nghiệp thế hệ mới tích hợp Glassmorphism, Dark Mode chiều sâu, cấu trúc KPI khoa học, bảng màu tương phản cao (WCAG compliant) và hiệu ứng nhảy số (Counter Animation) mượt mà 60fps. Hỗ trợ lệnh /ai4a:build-dashboard-BI hoặc /build-dashboard-bi."
user-invocable: true
when_to_use: "Sử dụng khi người dùng yêu cầu thiết kế, xây dựng, nâng cấp Dashboard BI, trực quan hóa dữ liệu kinh doanh/vận hành, tạo giao diện web báo cáo tương tác thời gian thực chuẩn Glassmorphism Dark Mode với KPI cards, biểu đồ động và hiệu ứng số nhảy."
category: workflow
keywords: [ai4a:build-dashboard-BI, build-dashboard-bi, dashboard, bi, business-intelligence, glassmorphism, dark-mode, kpi-layout, count-up, counter-animation, chartjs, data-visualization, ai4a]
argument-hint: "[dữ liệu hoặc yêu cầu] [--kpi] [--chart] [--theme] [--export-html]"
metadata:
  author: "MT Đức Thuận & AI4A Team"
  brand: "AI4A"
  course: "Agentic AI with Google Antigravity"
  version: "1.0.0"
---

# AI4A: BUILD DASHBOARD BI
## Chuyên Gia Thiết Kế & Xây Dựng Dashboard Business Intelligence Thế Hệ Mới

> **Đóng gói & Chuẩn hóa bởi MT Đức Thuận & AI4A Team**  
> *Dành tặng học viên chương trình Agentic AI with Google Antigravity (AI4A)*  
> *Bộ tiêu chuẩn thiết kế Dashboard doanh nghiệp đỉnh cao: Kính mờ (Glassmorphism), Dark Mode chiều sâu, Bố cục KPI 3 tầng, Bảng màu tương phản chuẩn WCAG và Hiệu ứng số nhảy 60fps.*

---

## 1. Bản Hợp Đồng Thực Thi (Core Contract)

1. **Outcome:**
   - Tạo ra Dashboard Business Intelligence chuẩn chỉnh cấp độ Executive dưới dạng web tương tác độc lập (Standalone Single-File HTML hoặc Modular Web App).
   - Tích hợp trọn vẹn **5 trụ cột mỹ thuật hiện đại**:
     1. **Glassmorphism:** Hiệu ứng thẻ kính mờ nhiều lớp, viền phản quang mép trên (specular bevel) và gradient orb nền.
     2. **Dark Mode Chiều Sâu:** Nền không gian đen vũ trụ (`#070a12`), bề mặt kính phiến đá (`#0f172a` / `#1e293b`), loại bỏ hoàn toàn mỏi mắt.
     3. **KPI Layout Khoa Học:** Grid 4 cột tự co giãn, mỗi thẻ gồm Icon chủ đề, Số Hero nổi bật, Delta Badge (tăng/giảm %) và Điểm quy chiếu mục tiêu.
     4. **Phối Màu Tương Phản:** Sử dụng bảng màu Neon có kiểm soát (Cyan, Emerald, Amber, Rose, Electric Violet), đạt độ tương phản WCAG 2.1 AA/AAA.
     5. **Hiệu Ứng Số Nhảy (Counter Animation):** 60fps mượt mà qua `requestAnimationFrame`, đường cong giảm tốc `easeOutExpo`, định dạng phân tách tiền tệ VNĐ/USD tự động.
   - Xuất file báo cáo HTML tại `outputs/reports/` và lưu trữ dữ liệu nguồn sạch sẽ.

2. **Constraints:**
   - **Zero-dependency runtime:** Mặc định sinh file HTML nhúng thẳng CSS & JS để mở xem trực tiếp trên mọi trình duyệt mà không cần cài đặt Node.js hay môi trường server phức tạp.
   - **Bảo toàn hiệu năng:** Tối ưu hóa render bằng `contain: paint`, `backdrop-filter: blur(16px-24px)` và xử lý `requestAnimationFrame` có cơ chế hủy frame tránh giật lag.
   - **Tuân thủ quy chuẩn Workspace:** Không ghi đè các thành phần cũ, ghi chép nhật ký PDCA đầy đủ.

3. **Non-goals:**
   - Không bắt buộc người dùng phụ thuộc vào nền tảng trả phí bên thứ 3 (PowerBI Pro, Tableau Server Cloud).
   - Không ép buộc cài đặt framework nặng (Next.js/React) cho các bài toán xuất báo cáo dashboard tĩnh hoặc định kỳ.

4. **Acceptance Criteria:**
   - File Dashboard hiển thị trọn vẹn hiệu ứng số nhảy khi tải trang hoặc khi chuyển bộ lọc thời gian.
   - 100% các thành phần trực quan (thẻ KPI, biểu đồ Chart.js, bảng dữ liệu) phản hồi mượt mà trên cả Desktop, Tablet và Mobile.
   - Bảng màu tương phản cao, chữ sắc nét, thông số phân định rõ ràng.

---

## 2. Bộ Tiêu Chuẩn Thiết Kế 5 Trụ Cột (5-Pillar BI Design System)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       5 TRỤ CỘT THIẾT KẾ DASHBOARD BI                       │
├───────────────────┬───────────────────┬───────────────────┬─────────────────┤
│ 1. GLASSMORPHISM  │ 2. DARK MODE SÂU  │ 3. KPI 3 TẦNG     │ 4. CONTRAST     │
│ • blur(16px-24px) │ • Base: #070a12   │ • Top: Icon+Delta │ • Neon Cyan     │
│ • Border: 1px     │ • Panel: #0f172a  │ • Mid: Hero 2.2rem│ • Neon Emerald  │
│ • Top Specular    │ • Elevated Card   │ • Bot: Benchmark  │ • Neon Amber    │
│ • Ambient Orbs    │ • WCAG AA/AAA     │ • Tabular nums    │ • Neon Rose     │
├───────────────────┴───────────────────┴───────────────────┴─────────────────┤
│ 5. COUNTER ENGINE: 60fps • easeOutExpo • RequestAnimationFrame • Observer   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Trụ cột 1 — Glassmorphism (Kính Mờ Hiện Đại)
- **Nền card:** `rgba(15, 23, 42, 0.65)` phối hợp cùng `backdrop-filter: saturate(180%) blur(16px)`.
- **Viền phản quang (Specular Bevel):** Viền bao quanh `1px solid rgba(255, 255, 255, 0.08)`, kết hợp đổ bóng nổi mép trên `box-shadow: inset 0 1px 1px 0 rgba(255, 255, 255, 0.15)`.
- **Ánh sáng nền (Ambient Glow Orbs):** Tích hợp 2–3 khối cầu mờ kích thước lớn (`filter: blur(100px)`) trôi lững lờ ở tầng nền phía sau, tạo cảm giác bề mặt kính trong suốt nhìn xuyên thấu không gian.

### Trụ cột 2 — Dark Mode Chiều Sâu (Canvas Hierarchy)
- Tránh màu đen tuyền `#000000` đơn điệu. Thay vào đó sử dụng hệ thống sắc độ đen ánh xanh (Deep Cosmic & Slate):
  - Nền toàn trang: `#070a12` (Cosmic Void)
  - Khung bao / Nền phụ: `#0b0f19` (Canvas Base)
  - Thẻ card kính: `rgba(15, 23, 42, 0.65)` (Slate 900 Glass)
  - Nút bấm / Input: `rgba(30, 41, 59, 0.70)` (Slate 800 Glass)

### Trụ cột 3 — Bố Cục Thẻ KPI 3 Tầng (KPI Layout)
Mỗi thẻ KPI được thiết kế để truyền tải trọn vẹn thông điệp chỉ trong 3 giây:
1. **Tầng 1 (Định danh & Xu thế):** Icon chủ đề trong hộp kính + Tiêu đề chỉ số + Huy hiệu biến động (Delta Badge xanh `+18.4% ↑` hoặc đỏ `-3.2% ↓`).
2. **Tầng 2 (Con số trung tâm):** Hero number nổi bật kích thước `2.2rem`, font chữ `tabular-nums` để số cố định chiều ngang khi đang nhảy.
3. **Tầng 3 (Quy chuẩn đối chiếu):** Điểm chuẩn mục tiêu (Benchmark/Target) + Huy hiệu trạng thái (Status Pill: Vượt kế hoạch, Ổn định, Cần chú ý).

### Trụ cột 4 — Bảng Phối Màu Tương Phản Cao (Curated Neon Palette)
- **Neon Cyan (`#06b6d4`):** Đại diện cho Doanh thu, Khối lượng giao dịch, Chỉ số chủ đạo.
- **Neon Emerald (`#10b981`):** Đại diện cho Lợi nhuận, Tăng trưởng dương, Tỷ lệ hoàn thành đạt/vượt.
- **Neon Amber (`#f59e0b`):** Đại diện cho Tồn kho cảnh báo, Chi phí vận hành, Hạng mục chờ duyệt.
- **Neon Rose (`#f43f5e`):** Đại diện cho Tỷ lệ đổi trả/hủy đơn, Thâm hụt ngân sách, Cảnh báo rủi ro.
- **Electric Violet (`#8b5cf6`):** Đại diện cho Giá trị vòng đời khách hàng (LTV), Kênh bán hàng B2B.

### Trụ cột 5 — Hiệu Ứng Số Nhảy 60fps (Counter Engine)
- Sử dụng thuật toán **`easeOutExpo`**: $f(t) = 1 - 2^{-10t}$. Số tăng tốc cực nhanh ở đầu và giảm tốc mượt mà khi tiến sát số đích.
- Hỗ trợ đầy đủ định dạng số Việt Nam (`3.852.000.000 ₫`), số quốc tế (`$1,250,000`), tỷ lệ phần trăm (`98.5%`).
- Kết hợp `IntersectionObserver`: Tự động kích hoạt khi người dùng cuộn đến vị trí thẻ card.

---

## 3. Quy Trình Vận Hành 4 Bước (4-Step Workflow)

Khi nhận lệnh xây dựng Dashboard, Agent tuân thủ nghiêm ngặt 4 bước:

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│     BƯỚC 1      │     │      BƯỚC 2      │     │      BƯỚC 3      │     │     BƯỚC 4      │
│  Data Audit &   │ ──> │   Spatial Grid   │ ──> │  Engine Binding  │ ──> │ Visual Polish & │
│   KPI Scoping   │     │  & Layout Specs  │     │   & Analytics    │     │  Export Report  │
└─────────────────┘     └──────────────────┘     └──────────────────┘     └─────────────────┘
```

### Bước 1: Data Audit & KPI Scoping (Rà soát dữ liệu & Xác lập chỉ số)
- Tiếp nhận tập dữ liệu (Excel, CSV, JSON hoặc truy vấn database).
- Xác định rõ 4 chỉ số sinh tồn (Vital Signs) của doanh nghiệp để đưa vào 4 Hero KPI Cards.
- Tính toán giá trị kỳ hiện tại, kỳ trước, tỷ lệ % tăng trưởng (delta) và mục tiêu kế hoạch.

### Bước 2: Spatial Grid & Layout Specs (Quy hoạch không gian)
- Thiết lập cấu trúc bố cục Dashboard theo tỷ lệ vàng:
  - Header: Tên Dashboard, trạng thái Live Sync, Bộ lọc thời gian (Today / 7D / 30D / Quarter / Year).
  - Row 1: 4 Thẻ KPI Hero Cards (Grid 1fr 1fr 1fr 1fr).
  - Row 2: Khung Biểu đồ Chính (2fr Biểu đồ xu hướng đa trục + 1fr Biểu đồ cơ cấu bánh Donut).
  - Row 3: Bảng dữ liệu chi tiết có tìm kiếm nhanh (Search Filter) và phân loại trạng thái.

### Bước 3: Engine Binding & Analytics (Gắn kết động lực học & Biểu đồ)
- Tích hợp thư viện `bi-counter-engine.js` vào các thẻ số với các thuộc tính `data-counter`, `data-counter-suffix`, `data-counter-separator`.
- Cấu hình biểu đồ Chart.js theo phong cách Dark Mode kính mờ: Nền trong suốt, viền Neon, gradient fill mờ nhạt dần về đáy.

### Bước 4: Visual Polish & Export Report (Kiểm định mỹ thuật & Xuất bản)
- Đóng gói toàn bộ CSS và JS vào 1 file HTML standalone (Zero dependencies) bằng công cụ Python:
  ```bash
  python .agents/skills/ai4a-build-dashboard-bi/scripts/generate_bi_dashboard.py --demo --output outputs/reports/Executive_BI_Dashboard.html
  ```
- Kiểm tra tính tương thích trên trình duyệt và ghi chép nhật ký PDCA.

---

## 4. Bộ Công Cụ & Tài Nguyên Sẵn Có Trong Skill

Skill tích hợp sẵn bộ tài nguyên tại thư mục nội bộ:

1. **`resources/bi-design-system.css`:** Bộ Design Tokens hoàn chỉnh cho Glassmorphism, Dark Mode, KPI layout, animations.
2. **`resources/bi-counter-engine.js`:** Module JS thuần (< 4KB) xử lý hiệu ứng nhảy số 60fps mượt mà.
3. **`resources/dashboard-template.html`:** Khung template mẫu chuẩn doanh nghiệp.
4. **`scripts/generate_bi_dashboard.py`:** Công cụ CLI Python chuyển đổi JSON/CSV sang Dashboard HTML tự động.
5. **`references/glassmorphism-standards.md`:** Sổ tay tra cứu thông số quang học, tương phản WCAG và tối ưu GPU.

---

## 5. Danh Mục Kiểm Tra Nghiệm Thu (Acceptance Checklist)

Trước khi bàn giao kết quả Dashboard cho người dùng, hãy đối chiếu:
- [ ] Giao diện có hiệu ứng kính mờ (Backdrop blur) nhìn xuyên thấu các khối cầu phát sáng nền hay không?
- [ ] Nền trang có đúng chuẩn Deep Slate Dark Mode (`#070a12` / `#0f172a`), không gây chói mắt?
- [ ] Các con số KPI có hiệu ứng nhảy số 60fps mượt mà từ 0 đến giá trị đích khi tải trang không?
- [ ] Mỗi thẻ KPI có đủ 3 tầng thông tin: Icon/Tên, Số Hero, Delta % tăng trưởng và Benchmark không?
- [ ] Màu sắc biểu đồ có tuân thủ bảng màu tương phản cao (Cyan, Emerald, Amber, Rose, Violet) không?
- [ ] File HTML xuất ra có thể mở trực tiếp (double click) xem trơn tru mà không cần cài server không?
