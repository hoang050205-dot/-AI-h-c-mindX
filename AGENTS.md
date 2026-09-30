# My Workspace — Quy Tắc Vận Hành

## Dự Án
**Personal Agentic Workspace** — Không gian làm việc AI cá nhân được xây dựng xuyên suốt khóa học Agentic AI with Google Antigravity.

## Chủ Sở Hữu
- **Tên:** {{ten_hoc_vien}}
- **Lĩnh vực:** {{linh_vuc_chuyen_mon}} _(VD: Marketing, Kế Toán, Nhân Sự, Kinh Doanh...)_
- **Mục tiêu tự động hóa:** {{muc_tieu_chinh}} _(VD: Tự động hóa báo cáo tuần, lên lịch nội dung, phân tích dữ liệu khách hàng...)_

## Sứ Mệnh Workspace
{{mo_ta_workspace}} _(VD: Workspace hỗ trợ tôi tự động hóa các công việc lặp lại trong [lĩnh vực], tạo ra các output chuyên nghiệp và có hệ thống.)_

## Quy Tắc Vận Hành (Rules)

### Quy tắc 1 — Tích lũy, không phá vỡ
Mỗi buổi học, tôi CHỈ thêm mới vào workspace. Không xóa bỏ hoặc thay thế các thành phần đã tạo trừ khi có lý do audit rõ ràng.

### Quy tắc 2 — PDCA bắt buộc
Mọi thay đổi quan trọng phải được ghi vào `docs/pdca-log.md`. Format: Plan → Do → Check → Act.

### Quy tắc 3 — Workspace checkpoint
Sau mỗi buổi học, tôi đọc bridge guide tương ứng và hoàn thành ít nhất 1 workspace checkpoint.

### Quy tắc 4 — Output vào đúng thư mục
- Draft content → `outputs/drafts/`
- Báo cáo → `outputs/reports/`
- Dữ liệu thực hành → `sample-data/`

### Quy tắc 5 — Bảo mật
Không đưa API key, mật khẩu, dữ liệu khách hàng thật vào workspace này.

## Lịch Sử Phát Triển

| Buổi | Ngày | Thêm gì vào workspace | Ghi chú |
|:----:|------|----------------------|---------|
| 1 | {{ngay}} | Tạo workspace, viết AGENTS.md | |
| 2 | 06/09/2026 | Làm sạch dữ liệu, tạo Dashboard Excel & Báo cáo Insights (PDCA) | MINDX_Sales_Dashboard_Cleaned.xlsx, pdca-log.md #01 |
| 2 (Thực hành) | 06/09/2026 | Thu thập, làm sạch & phân tích 22 quán cafe Quận 1 theo mô hình PDCA | Quan_Cafe_Quan_1_Cleaned.xlsx, pdca-log.md #02 |
| 3 | 09/09/2026 | Kiểm tra & Audit toàn diện Skill ai4a:brainstorm theo chuẩn Antigravity | ai4a-brainstorm-audit.md, pdca-log.md #03 |
| 3 (Thực hành) | 09/09/2026 | Đóng gói Skill ops:erp-processor: quét 799 dòng rác, tách 4 file Manager, xuất Master & Báo cáo | ops:erp-processor, pdca-log.md #04 |
| 4 | 11/09/2026 | Đóng gói Skill academic:training-ops: thu thập dữ liệu rải rác, chuẩn hóa Excel Master, xuất Báo cáo Giảng viên | academic:training-ops, pdca-log.md #05 |
| 4 (Thực hành) | 11/09/2026 | Brainstorm & Tạo file Excel dữ liệu học viên IELTS X (35 HV, 2 sheet, Dashboard KPI) | IELTS_Center_X_Students.xlsx, pdca-log.md #06 |
| 5 | 11/09/2026 | Chuẩn hóa Master Excel 4 sheet, phân tích 4 Giảng viên & xuất Báo cáo IELTS X | IELTS_Center_X_Cleaned_Master.xlsx, pdca-log.md #07 |
| 6 | 13/09/2026 | Quy trình tính lương C-Suite ngành Y (OIPO), Master Excel 24M & Báo cáo HĐQT | Medical_CSuite_Payroll_24Months_Master.xlsx, pdca-log.md #08 |
| 7 | 13/09/2026 | Automation Bot điểm tin AI Telegram OIPO: RSS Google News, dịch REST API, bảo mật .env | send_telegram.py, pdca-log.md #09 |
| 7 (Nâng cấp) | 13/09/2026 | Nâng cấp Bot AI v2.0: 3 tin tức, dịch tiêu đề & tóm tắt, insight xu hướng, lập lịch 10h sáng | setup_scheduler.ps1, pdca-log.md #10 |
| 8 | 13/09/2026 | Đóng gói Skill customs:doc-auditor: đối chiếu 5 loại chứng từ XNK, bắt 6 bẫy lỗi số học/pháp lý & xuất Báo cáo | customs:doc-auditor, pdca-log.md #11 |
| 9 | 16/09/2026 | Đóng gói Skill customs:legal-advisor & CSDL Pháp lý Cục bộ (7 văn bản), vận hành 2 giai đoạn (Search & Brief -> Analysis & Workflow) | customs:legal-advisor, pdca-log.md #12 |
| 11 | 16/09/2026 | Đóng gói Skill customs:doc-auditor: engine 5 lớp kiểm soát, phát hiện 7 bẫy lỗi số học/chính tả/thời gian, xuất Báo cáo Thẩm định Master | customs:doc-auditor, pdca-log.md #14 |
| 12 | 16/09/2026 | AI Finance Agent: kiểm duyệt chi tiêu theo rule (>500k), tự động đẩy dữ liệu sang Google Sheets qua Web App REST API | send_to_sheet.py, pdca-log.md #15 |
| 12 (Thực hành) | 17/09/2026 | Enterprise Expense Sync Agent: đồng bộ 2 Google Sheets bằng OAuth 2.0, chèn nối tiếp không ghi đè, chống trùng lặp SyncStatus | sync_expenses.py, pdca-log.md #16 |
| 13 | 20/09/2026 | Đóng gói Skill ai4a:build-dashboard-BI: bộ chuẩn Glassmorphism, Deep Dark Mode, KPI 3 tầng, Neon Contrast, hiệu ứng nhảy số 60fps & Generator CLI | ai4a:build-dashboard-BI, pdca-log.md #17 |
| 13 (Thực hành) | 20/09/2026 | Realtime BI Dashboard Alpha Corp (server port 9090, polling 2s, Glassmorphism Dark Mode) & Đóng gói an toàn export_dashboard.py (HTML tĩnh, nén WinRAR mật khẩu Hoang0502) | server_dashboard.py, export_dashboard.py, pdca-log.md #18 |
| 13 (Nâng cao) | 20/09/2026 | Realtime BI Web Dashboard Beta Solutions: API raw data, Client-side reactive filter (Quý & Phòng ban), 3 thẻ KPI 3 tầng, Cột ghép & Donut, Polling 2s | server_beta_dashboard.py, beta_solutions_bi_dashboard.html, pdca-log.md #19 |
| Bảo trì | 21/09/2026 | Tạm dừng bot tin tức 10h sáng (State: Disabled), nâng cấp setup_scheduler.ps1 (-Disable, -Enable, -Status) | setup_scheduler.ps1, pdca-log.md #20 |
| Tuyển dụng | 22/09/2026 | Bộ 5 slide tiếng Anh Vinamilk SC Ops Intern 2026: xuất bản PPTX, PDF Vector 16:9 & HTML Deck | Vinamilk_Supply_Chain_Operations_PhamMinhHoang.pptx, .pdf, pdca-log.md #21 |
| Thực hành | 28/09/2026 | Kết xuất Biểu đồ Phân tích Cơ cấu Sản phẩm C.P. (Singapore, EU, China): 300 DPI PNG, SVG Vector, Excel Clustered Column Chart | CP_Product_Mix_Singapore_EU_China.xlsx, .png, pdca-log.md #22 |
| Chuyên đề BĐS | 30/09/2026 | Đóng gói Skill real-estate:lead-scoring & Web App Streamlit st.data_editor (Human-in-the-loop, AI Scoring Agent) | lead_scoring_skill.md, app_lead_scoring.py, pdca-log.md #23 |
| Nâng cấp BĐS | 30/09/2026 | Nâng cấp Web App Streamlit v2.0 Pro (5 Tabs, BI Analytics Altair, Export Excel openpyxl, Call/Zalo) & Đồng bộ Git | app_lead_scoring.py, requirements.txt, pdca-log.md #24 |









