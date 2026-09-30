# Báo Cáo Phân Tích Quản Trị Vận Hành & Quỹ Lương (Kỳ Tháng 03/2026)

**Thời điểm xử lý:** 2026-09-09  
**Tệp dữ liệu nguồn:** `sample-data/THỰC HÀNH_ERP_OP_BigData_200rows B3.xlsx`  
**Công cụ tự động hóa:** Custom Skill `ops:erp-processor` (PowerShell Core / OpenXML Engine)  
**Phụ trách phân tích:** Operations Analyst / AI4A Workspace  

---

## 1. Tổng Quan Chỉ Số Điều Hành (Executive KPI Summary)

| Chỉ Số Cốt Lõi | Giá Trị Số Học | Tỷ Trọng / Tỷ Lệ | Nhận Định Vận Hành |
|---|---|:---:|---|
| **Tổng số nhân sự hợp lệ** | **200 nhân viên** | 100% | Đã lọc sạch triệt để **799 dòng rác trống (ghost rows)** xuất ra từ ERP. |
| **Tổng quỹ lương cơ bản (Base)** | **3,771,713,639 VNĐ** | 100.0% | Chi phí cố định hàng tháng của 4 khối phòng ban. |
| **Tổng tiền thưởng (Bonus)** | **499,094,030 VNĐ** | **13.23%** | Tỷ lệ thưởng ở mức hợp lý (kỳ vọng 10% - 15%). |
| **Tổng tiền phạt (Penalty)** | **200,612,662 VNĐ** | **5.32%** | Khấu trừ vi phạm kỷ luật lao động và sai sót quy trình. |
| **Tổng chi trả thực lĩnh (Net)** | **4,070,195,007 VNĐ** | **107.91%** | Quỹ lương giải ngân thực tế (= Base + Bonus - Penalty). |

---

## 2. Cơ Cấu Chi Phí Theo Bộ Phận (Department Breakdown)

| Bộ Phận | Nhân Sự | Lương Cơ Bản (VNĐ) | Thưởng (VNĐ) | Phạt (VNĐ) | Thực Lĩnh (VNĐ) | Thu Nhập TB/Người | Tỷ Lệ Thưởng | Tỷ Lệ Phạt |
|---|:---:|---:|---:|---:|---:|---:|:---:|:---:|
| **HR (Nhân sự)** | 58 | 1,109,114,321 | 157,372,333 | 60,793,919 | 1,205,692,735 | 20,787,806 VNĐ | 14.19% | 5.48% |
| **Operations (Vận hành)** | 48 | 936,887,127 | 119,944,562 | 53,974,493 | 1,002,857,196 | 20,892,858 VNĐ | 12.80% | 5.76% |
| **Finance (Tài chính)** | 50 | 908,342,279 | 108,759,459 | 42,738,444 | 974,363,294 | 19,487,266 VNĐ | 11.97% | 4.70% |
| **Sales (Kinh doanh)** | 44 | 817,369,912 | 113,017,676 | 43,105,806 | 887,281,782 | 20,165,495 VNĐ | 13.83% | 5.27% |
| **Tổng cộng** | **200** | **3,771,713,639** | **499,094,030** | **200,612,662** | **4,070,195,007** | **20,350,975 VNĐ** | **13.23%** | **5.32%** |

---

## 3. Phân Tích Hiệu Suất Theo Quản Lý (Manager Breakdown)

Skill đã tự động phân tách bảng tính riêng biệt, bảo đảm tuyệt đối tính bảo mật tiền lương giữa các Quản lý:

| Quản Lý | Quy Mô Team | Tổng Lương Cơ Bản | Tổng Thưởng | Tổng Phạt | Tổng Thực Lĩnh | Thu Nhập TB | File Bàn Giao Riêng Tư |
|---|:---:|---:|---:|---:|---:|---:|---|
| **Manager_A** | 62 NV | 1,159,186,631 | 159,356,385 | 59,168,516 | 1,259,374,500 VNĐ | 20,312,492 VNĐ | [Manager_A_2026-03.xlsx](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/managers/Manager_A_2026-03.xlsx) |
| **Manager_C** | 51 NV | 1,010,803,313 | 129,704,785 | 54,318,283 | 1,086,189,815 VNĐ | 21,297,840 VNĐ | [Manager_C_2026-03.xlsx](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/managers/Manager_C_2026-03.xlsx) |
| **Manager_D** | 50 NV | 891,041,941 | 123,352,299 | 49,456,432 | 964,937,808 VNĐ | 19,298,756 VNĐ | [Manager_D_2026-03.xlsx](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/managers/Manager_D_2026-03.xlsx) |
| **Manager_B** | 37 NV | 710,681,754 | 86,680,561 | 37,669,431 | 759,692,884 VNĐ | 20,532,240 VNĐ | [Manager_B_2026-03.xlsx](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/managers/Manager_B_2026-03.xlsx) |
| **Tổng Master** | **200 NV** | **3,771,713,639** | **499,094,030** | **200,612,662** | **4,070,195,007 VNĐ** | **20,350,975 VNĐ** | [ERP_Operations_Master_2026-03.xlsx](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/outputs/reports/ERP_Operations_Master_2026-03.xlsx) |

> **Đối soát toàn vẹn (Zero-Reconciliation):** $\sum \text{File Con} = 4,070,195,007 \text{ VNĐ} = \text{File Master}$ (Độ lệch = 0 VNĐ).

---

## 4. Nhận Diện Bất Thường Vận Hành (Outlier Analysis)

### 🌟 Top 5 Nhân Sự Nhận Thưởng Cao Nhất
1. **E026 (Employee_26 - HR, Quản lý: Manager_A):** Thưởng `4,991,591 VNĐ` (Tỷ lệ thưởng **27.24%** trên lương cơ bản).
2. **E056 (Employee_56 - HR, Quản lý: Manager_A):** Thưởng `4,950,792 VNĐ` (Tỷ lệ thưởng **19.92%**).
3. **E145 (Employee_145 - HR, Quản lý: Manager_A):** Thưởng `4,939,810 VNĐ` (Tỷ lệ thưởng **21.84%**).
4. **E104 (Employee_104 - Finance, Quản lý: Manager_A):** Thưởng `4,939,656 VNĐ` (Tỷ lệ thưởng **30.90%** — cao kỷ lục).
5. **E031 (Employee_31 - HR, Quản lý: Manager_A):** Thưởng `4,925,144 VNĐ` (Tỷ lệ thưởng **18.04%**).

### ⚠️ Top 5 Nhân Sự Bị Khấu Trừ Phạt Cao Nhất
1. **E031 (Employee_31 - HR, Quản lý: Manager_A):** Phạt `1,993,943 VNĐ` (**Nghịch lý vận hành:** Vừa thuộc Top 5 Thưởng vừa đứng số 1 về Phạt).
2. **E095 (Employee_95 - HR, Quản lý: Manager_C):** Phạt `1,993,458 VNĐ`.
3. **E136 (Employee_136 - Sales, Quản lý: Manager_A):** Phạt `1,982,488 VNĐ` (Tỷ lệ phạt chiếm **13.34%** lương cơ bản).
4. **E013 (Employee_13 - HR, Quản lý: Manager_C):** Phạt `1,973,553 VNĐ` (Tỷ lệ phạt chiếm **20.30%** lương cơ bản).
5. **E186 (Employee_186 - HR, Quản lý: Manager_C):** Phạt `1,952,083 VNĐ` (Tỷ lệ phạt chiếm **21.82%** lương cơ bản).

---

## 5. Nhận Định Chiến Lược & Đề Xuất Hành Động (PDCA Act)

### 💡 3 Insights Vận Hành Cốt Lõi:
1. **Khối HR biến động thu nhập mạnh nhất:** HR chiếm tới 4/5 vị trí thưởng cao nhất và 4/5 vị trí phạt nặng nhất. Nguyên nhân có thể do KPI tuyển dụng hoặc biến động nhân sự cuối quý dẫn tới mức độ khen thưởng/chế tài dồn cục.
2. **Hiện tượng "Hai mặt" ở nhân sự E031:** E031 vừa đạt mức thưởng gần tối đa (4.92M) nhưng đồng thời lại bị phạt kịch trần (1.99M). Đây là nhân sự có năng suất đột biến nhưng tiềm ẩn sai phạm quy trình nghiêm trọng.
3. **Hiệu suất quản lý:** Manager_C có mức thu nhập bình quân nhân viên cao nhất công ty (21.3M), trong khi Manager_D có mức thu nhập bình quân thấp nhất (19.3M).

### 🎯 2 Đề Xuất Hành Động Cho Ban Điều Hành:
1. **Đối với Giám đốc Vận hành (COO):** Rà soát lại quy trình vận hành và chế tài phạt của Khối HR và Khối Sales; đặc biệt cần phỏng vấn trực tiếp Quản lý Manager_A và Manager_C về các trường hợp nhân sự bị phạt trên 20% lương (như E013, E186) để tránh rủi ro khiếu nại lao động hoặc nghỉ việc đột ngột.
2. **Đối với Trưởng phòng Nhân sự (HRD):** Hoàn thiện chính sách xét thưởng: Cân nhắc áp dụng điều kiện loại trừ — "Nhân sự vi phạm kỷ luật bị phạt trên 1.5 triệu đồng trong tháng sẽ không được xét duyệt thưởng loại A", nhằm giải quyết dứt điểm nghịch lý như trường hợp của E031.
