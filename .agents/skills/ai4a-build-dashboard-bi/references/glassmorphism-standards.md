# AI4A Modern BI Design Standards: Glassmorphism & Dark Mode Architecture

> **Tài Liệu Kỹ Thuật Tham Chiếu Nghiệp Vụ**  
> *Quy chuẩn thiết kế giao diện Business Intelligence thế hệ mới dành cho Antigravity Agents.*

---

## 1. Trụ Cột 1: Kỹ Thuật Kính Mờ (Glassmorphism Physics)

Giao diện kính mờ tạo chiều sâu không gian (Spatial Depth) bằng cách mô phỏng đặc tính khúc xạ ánh sáng qua tấm kính mờ đặt trên nền không gian vũ trụ tối (Deep Dark Canvas).

### 1.1. Công thức Layer Kính chuẩn (Frosted Glass Stack)

```css
.glass-panel {
  /* 1. Lớp màu nền bán trong suốt (Semi-transparent background) */
  background: rgba(15, 23, 42, 0.65); /* Slate 900 với độ mờ 65% */

  /* 2. Khúc xạ & bão hòa ánh sáng phần nền phía sau */
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);

  /* 3. Viền phản quang góc xiên 1px (Specular highlight border) */
  border: 1px solid rgba(255, 255, 255, 0.08);

  /* 4. Đổ bóng bề mặt kết hợp phản chiếu ánh sáng mép trên (Top bevel) */
  box-shadow: 
    0 8px 32px 0 rgba(0, 0, 0, 0.45),
    inset 0 1px 1px 0 rgba(255, 255, 255, 0.15);

  /* 5. Bo góc thẩm mỹ công thái học */
  border-radius: 16px;

  /* 6. Tối ưu GPU Render (Chống rớt FPS) */
  contain: paint;
}
```

### 1.2. Các cấp độ Kính Mờ (Glass Hierarchy)

| Cấp Độ | Lớp Áp Dụng | Background Alpha | Backdrop Blur | Mục Đích Sử Dụng |
|---|---|---|---|---|
| **Level 0** | Dashboard Canvas | `#070a12` (Solid) | None | Nền đen sâu (Obsidian) hấp thụ ánh sáng. |
| **Level 1** | Base Glass Container | `rgba(15, 23, 42, 0.65)` | `16px` | Khung Dashboard, Bảng dữ liệu, Header. |
| **Level 2** | Elevated Card (KPI) | `rgba(30, 41, 59, 0.70)` | `20px` | Thẻ chỉ số Hero, Khung biểu đồ chính. |
| **Level 3** | Modal & Floating Menu | `rgba(15, 23, 42, 0.90)` | `24px` | Dropdown menu, Tooltip, Modal đối soát. |

---

## 2. Trụ Cột 2: Kiến Trúc Dark Mode & Phối Màu Tương Phản (High-Contrast Palette)

### 2.1. Phân cấp Màu Nền (Surface Hierarchy)
- **Canvas Base:** `#070a12` (Deep Cosmic Black) — Tạo cảm giác vô tận.
- **Card Neutral Surface:** `#0f172a` (Slate 900) — Điểm tựa mắt đọc không gây chói.
- **Card Highlight Surface:** `#1e293b` (Slate 800) — Nổi bật khi rê chuột (Hover state).

### 2.2. Phối Màu Tương Phản Chuẩn Doanh Nghiệp (Curated Neon Accents)

Tuyệt đối không dùng các mã màu RGB bão hòa thô (`#FF0000`, `#00FF00`, `#0000FF`). Phải sử dụng bộ màu Neon có kiểm soát quang phổ:

| Tên Màu | Hex Code | Ứng Dụng Nghiệp Vụ BI | Độ Tương Phản (vs Slate 900) |
|---|---|---|---|
| **Neon Cyan** | `#06b6d4` / `#22d3ee` | Doanh thu thuần, Tổng lượng đơn, Chỉ số chủ đạo | **9.2:1 (Đạt WCAG AAA)** |
| **Neon Emerald** | `#10b981` / `#34d399` | Lợi nhuận gộp, Tăng trưởng dương, Trạng thái thành công | **8.6:1 (Đạt WCAG AAA)** |
| **Neon Amber** | `#f59e0b` / `#fbbf24` | Tồn kho cảnh báo, Chi phí dự phòng, Chờ xử lý | **9.5:1 (Đạt WCAG AAA)** |
| **Neon Rose** | `#f43f5e` / `#fb7185` | Tỷ lệ hủy/đổi trả, Thâm hụt ngân sách, Cảnh báo đỏ | **5.4:1 (Đạt WCAG AA)** |
| **Electric Violet**| `#8b5cf6` / `#a78bfa` | Khách hàng mới, Giá trị vòng đời (LTV), Kênh bán lẻ | **6.1:1 (Đạt WCAG AA)** |

---

## 3. Trụ Cột 3: Bố Cục Thẻ KPI (KPI Layout Architecture)

Một thẻ KPI chuẩn doanh nghiệp phải cung cấp **3 tầng thông tin** trong vòng **3 giây quét mắt**:

```
┌─────────────────────────────────────────────────────────────┐
│ 💰  TỔNG DOANH THU                           [ +18.4% ↑ ]   │ <-- Tầng 1: Ngữ cảnh & Xu hướng
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   3,852,000,000 ₫                                           │ <-- Tầng 2: Con số then chốt (Hero)
│                                                             │
├─────────────────────────────────────────────────────────────┤
│   Mục tiêu: 3.5 Tỷ                     [ Đạt 110% • Tốt ]   │ <-- Tầng 3: Điểm quy chiếu & Đánh giá
└─────────────────────────────────────────────────────────────┘
```

1. **Header Row:** Icon nhận diện có viền kính + Tên chỉ số + Delta Badge (tỷ lệ tăng/giảm kèm icon mũi tên SVG).
2. **Hero Value Row:** Font chữ kích thước lớn (`2.2rem`), trọng lượng `800`, sử dụng thuộc tính `font-variant-numeric: tabular-nums` để tránh giật giao diện khi nhảy số.
3. **Footer Row:** Điểm quy chiếu (Benchmark kỳ trước hoặc Target kế hoạch) + Status Pill.

---

## 4. Trụ Cột 4: Hiệu Ứng Nhảy Số 60fps (Counter Animation Engine)

### 4.1. Đường Cong Giảm Tốc (Deceleration Easing)
Không sử dụng chuyển động tuyến tính (Linear motion) vì tạo cảm giác máy móc khô cứng. Sử dụng hàm **Exponential Deceleration (`easeOutExpo`)**:

$$\text{progress}(t) = 1 - 2^{-10t}$$

Đặc điểm:
- 0% - 30% thời gian: Số tăng vọt với tốc độ cao tạo cảm giác bùng nổ dữ liệu.
- 70% - 100% thời gian: Số chậm dần từng đơn vị và hạ cánh chính xác vào con số cuối cùng.

### 4.2. Tối Ưu Tần Số Quét Màn Hình
- Luôn sử dụng `requestAnimationFrame` thay vì `setInterval` / `setTimeout`.
- Tự động hủy Frame cũ (`cancelAnimationFrame`) khi người dùng bấm đổi bộ lọc thời gian liên tục.
- Sử dụng `IntersectionObserver` với ngưỡng `threshold: 0.15` để chỉ bắt đầu nhảy số khi thẻ card thực sự lọt vào màn hình của người dùng.
