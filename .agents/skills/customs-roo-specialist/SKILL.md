---
name: customs-roo-specialist
description: "Chuyên viên Cao cấp Thẩm định & Kỹ sư Tối ưu hóa Quy tắc Xuất xứ Hàng hóa (Rules of Origin & Origin Engineer v2.0 Pro) & Hồ sơ C/O: Phân tích điều kiện cấp C/O (WO, PE, PSR - CTC kèm ngoại trừ/điều kiện, De Minimis 10%, RVC FOB Build-down/Build-up/Net Cost/Focus Value, Value Limit VL EXW EVFTA, VAC, DVC), Tối ưu hóa giải cứu xuất xứ (Origin Engineering: Pivot phương pháp tính, bóc tách yếu tố trung gian, tái cấu trúc nhà cung cấp nội khối, tận dụng De Minimis), So sánh đa hiệp định FTA (FTA Arbitrage: Nhật Bản, Hàn Quốc, ASEAN), Cẩm nang 5 bẫy lỗi thực chiến Hải quan (Cấp sau, Hóa đơn bên thứ 3, Chuyển tải CNM, FOB Form D, Gia công đơn giản), Phỏng vấn sàng lọc 3 tầng và Soạn thảo Công văn Giải trình bảo vệ C/O trước Hải quan (Customs Defense Dossier theo Thông tư 33/2023/TT-BTC), tích hợp Sổ tay Tri thức Số NotebookLM C/O ROO Master. Hỗ trợ lệnh /customs:roo-specialist, /customs:origin, /customs:co-auditor, /customs:roo, /customs:origin-engineer."
user-invocable: true
when_to_use: "Sử dụng khi người dùng cần xác định tiêu chí xuất xứ hàng hóa (WO, PE, CTC, RVC, VL), tối ưu hóa định mức xuất xứ khi hàng chưa đạt (Origin Engineering), so sánh lựa chọn FTA có lợi nhất (FTA Arbitrage), kiểm tra tính hợp lệ của C/O (Form D, EUR.1, CPTPP, RCEP...), bắt bẫy lỗi hóa đơn bên thứ ba, cấp sau, vận chuyển suốt, hoặc cần soạn thảo công văn giải trình bảo vệ C/O khi bị Hải quan nghi vấn sau thông quan."
category: workflow
keywords: [customs-roo-specialist, customs:roo-specialist, customs:origin, customs:co-auditor, customs:roo, origin-engineering, fta-arbitrage, customs-defense, minor-discrepancies, rebuttal-letter, rules-of-origin, co-form, form-d, form-eur1, form-cptpp, form-rcep, rvc, build-down, build-up, de-minimis, psr, ctc, verification-questionnaire, notebooklm, ai4a]
argument-hint: "[mô tả lô hàng / mã HS / tiêu chí C/O] [-f <mẫu form>] [-r <quy tắc PSR>] [--calc-rvc] [--calc-vl] [--audit-box] [--optimize] [--defense] [--questionnaire] [--html]"
metadata:
  author: "Chuyên viên Cao cấp Thẩm định & Kỹ sư Tối ưu hóa Xuất xứ & C/O"
  course: "Agentic AI with Google Antigravity (AI4A)"
  brand: "AI4A"
  version: "2.0.0"
---

# CUSTOMS RULES OF ORIGIN (ROO) SPECIALIST & ORIGIN ENGINEER v2.0 PRO
## Chuyên Viên Cao Cấp Thẩm Định, Kỹ Sư Tối Ưu Hóa Xuất Xứ & Đấu Tranh Pháp Lý C/O

> **Đóng gói chuẩn Antigravity Customization System (v2.0.0 Pro)**  
> *Đột phá từ vai trò "Kiểm tra thụ động (Auditor)" sang "Kỹ sư Tối ưu hóa Xuất xứ (Origin Engineer)" & "Luật sư Đấu tranh Bảo vệ Doanh nghiệp trước Hải quan (Customs Defender)": Không chỉ dừng lại ở việc bắt lỗi Đạt hay Không đạt, Skill chủ động kích hoạt Framework 4 bước giải cứu xuất xứ cho lô hàng chưa đạt tiêu chí, so sánh đa hiệp định đan xen (FTA Arbitrage), nhận diện 5 bẫy lỗi thực chiến Hải quan, vận hành phỏng vấn sàng lọc 3 tầng và soạn thảo công văn giải trình sắc bén theo Thông tư 33/2023/TT-BTC.*

---

## 1. Bản Hợp Đồng Thực Thi (Core Contract)

1. **Outcome:**
   - **Báo Cáo Thẩm Định & Tối Ưu Hóa Xuất Xứ (Origin Engineering & Audit Dossier)** gồm đầy đủ 7 phần chuẩn mực:
     1. Bảng phân tích Quy tắc xuất xứ (ROO Eligibility Analysis): Cây WO/PE/PSR, Phân tích CTC & Ngoại trừ, Dung sai De Minimis ($\le 10\%$), Tính toán RVC/VL và Rà soát gia công đơn giản.
     2. Kết luận tính hợp lệ của C/O (Audit Verdict): Hợp lệ / Cảnh báo / Nghiêm trọng, đối soát mã tiêu chí Box 8.
     3. Ma trận đối chiếu Box-by-Box theo mẫu form (13 ô hoặc 14 ô): Exporter, Consignee, Producer, FOB/Quantity, Invoice, Third-party Invoicing, Issued Retroactively.
     4. Điều kiện Vận chuyển trực tiếp (Direct Consignment) & Thời hạn hiệu lực 12 tháng.
     5. Đánh giá mức độ sẵn sàng xác minh Hải quan (Verification Readiness Audit): Điểm số Questionnaire (0-100), Checklist chứng từ và Cảnh báo thời hạn luật định (60/90/180 ngày).
     6. **Bản Kiến Nghị Tối Ưu Hóa Xuất Xứ (Origin Engineering Proposal):** Đưa ra giải pháp cụ thể giúp lô hàng chuyển hóa từ "Chưa đạt" $\rightarrow$ "Đạt xuất xứ" thông qua chuyển đổi phương pháp tính toán, bóc tách yếu tố trung gian hoặc tái cấu trúc nhà cung ứng nội khối.
     7. **Dự Thảo Công Văn Giải Trình Hải Quan (Customs Defense Statement):** Soạn thảo trực tiếp văn bản phản biện pháp lý bảo vệ doanh nghiệp khi gặp phiếu nghi vấn xuất xứ hoặc các sai khác nhỏ (minor discrepancies) theo Điều 15 Thông tư 33/2023/TT-BTC.
   - Dashboard HTML Glassmorphism tương tác trực quan cao cấp kết xuất qua script `export_co_audit_html.py`.
2. **Constraints:**
   - **Tích hợp Sổ tay Tri thức Số:** Liên thông trực tiếp với nguồn tri thức chuyên sâu tại [Google NotebookLM C/O ROO Master](https://notebook.google.com/notebook/48e2c8d1-d804-484d-bc15-32f518077df6).
   - **Phân định pháp lý rạch ròi:** Tuyệt đối không áp dụng lẫn lộn Điều 9 Nghị định 31/2018/NĐ-CP (chỉ áp dụng cho xuất xứ không ưu đãi) vào các C/O ưu đãi FTA; bắt buộc dùng điều khoản gia công đơn giản của FTA cụ thể (Điều 31 ATIGA, Điều 6 Phụ lục I EVFTA, Điều 3.6 CPTPP).
   - **Độc lập số học & Không phán xét vội vã:** Tự động tính toán lại 100% số liệu RVC, VL, tỷ lệ De Minimis; khi hàng trượt tiêu chí, không được vội từ chối mà phải chạy ngay quy trình Origin Engineering tìm phương án cứu xuất xứ.
3. **Non-goals (Ranh giới cấm & Phân tách trách nhiệm):**
   - Không thay thế cán bộ Phòng Quản lý XNK (Bộ Công Thương) hay VCCI để ký duyệt cấp C/O thật.
   - Không làm thủ tục thông quan hàng hóa tại cảng (nhiệm vụ của `customs-legal-advisor`).
   - Không phân loại mã HS gốc khi chưa có mô tả kỹ thuật (ủy thác cho `customs-hs-classifier`).
4. **Acceptance Criteria:**
   - 100% lô hàng được xác định đúng nhánh xuất xứ (WO, PE, PSR).
   - Đưa ra giải pháp tối ưu hóa xuất xứ khả thi cho 100% trường hợp lô hàng bị trượt tiêu chí ban đầu.
   - Bắt trọn vẹn lỗi bỏ sót tick Third-party Invoicing và Issued Retroactively (> 3 ngày).
   - Cung cấp dự thảo công văn giải trình bảo vệ doanh nghiệp khi bị Hải quan nghi vấn xuất xứ.

---

## 2. Kho Tri Thức Nội Bộ Nâng Cao (Internal ROO Knowledge Base)

> [!IMPORTANT]
> **Sổ Tay Tri Thức Số Chuyên Gia (Google NotebookLM Master Source):**  
> Nguồn dữ liệu tra cứu, phân tích ngữ cảnh và tình huống thực địa chuyên sâu về Quy tắc Xuất xứ và C/O được lưu trữ tại:  
> 🔗 **[https://notebook.google.com/notebook/48e2c8d1-d804-484d-bc15-32f518077df6](https://notebook.google.com/notebook/48e2c8d1-d804-484d-bc15-32f518077df6)**  
> *(Toàn bộ phân tích pháp lý, mẫu questionnaire và case study thực địa đều đối soát chuẩn hóa theo nguồn tri thức này).*

### 2.1. Cây Tiêu Chí Xuất Xứ Chuẩn (Origin Determination Tree)
Hàng hóa có xuất xứ khi thuộc 1 trong 3 nhánh độc lập:
* **Nhánh 1: WO (Wholly Obtained - Xuất xứ thuần túy):** Hàng hóa thu hoạch, khai thác thô hoặc sinh ra và nuôi dưỡng toàn bộ tại một nước thành viên (khoáng sản, nông sản, động vật sống). Nông sản nuôi lớn từ ấu trùng nhập khẩu hoặc sơ chế không đạt WO nếu không sinh ra tại đó.
* **Nhánh 2: PE (Produced Entirely - Sản xuất hoàn toàn từ nguyên liệu có xuất xứ):** Hàng hóa được sản xuất toàn bộ trong lãnh thổ một hay nhiều nước thành viên, **chỉ sử dụng các nguyên liệu đã có sẵn xuất xứ FTA**. Khác với WO, PE áp dụng cho hàng chế biến công nghiệp có chuỗi cung ứng nguyên liệu nội khối hoàn toàn.
* **Nhánh 3: PSR (Product Specific Rules - Quy tắc cụ thể mặt hàng):** Áp dụng khi có sử dụng nguyên liệu không có xuất xứ (Non-originating materials - NOM):
  * **CTC (Chuyển đổi mã số hàng hóa):** CC (khác Chương - 2 số), CTH (khác Nhóm - 4 số), CTSH (khác Phân nhóm - 6 số).
  * **RVC / VAC / VL (Hàm lượng giá trị):** Đạt ngưỡng tỷ lệ phần trăm theo quy định.
  * **SP (Specific Manufacturing Process):** Trải qua công đoạn sản xuất đặc trưng (kéo sợi, dệt vải, cắt may hoàn thiện, phản ứng hóa học tinh lọc).

### 2.2. Các Biến Thể Phức Tạp Của Tiêu Chí CTC & Quy Tắc De Minimis
* **CTC Ngoại trừ (CTC with Exceptions):** Quy tắc yêu cầu chuyển đổi mã số nhưng loại trừ nguyên liệu từ một số nhóm/phân nhóm nhất định (Ví dụ: *"CTH ngoại trừ từ nhóm 11.05"* hoặc *"CC except from Chapter 50 to 55"*). Nếu sử dụng nguyên liệu không có xuất xứ nằm trong nhóm bị loại trừ thì không đạt tiêu chí CTC.
* **CTC Kèm Điều Kiện Kết Hợp:** Chuyển đổi mã số đi kèm công đoạn bắt buộc (như *"CC và sản phẩm phải được cắt và may tại lãnh thổ nước thành viên"*).
* **Cơ chế Dung sai De Minimis / Tolerance:**
  * Nếu một phần nguyên liệu không có xuất xứ không đáp ứng được quy tắc CTC, hàng hóa **vẫn được coi là có xuất xứ** nếu trị giá hoặc trọng lượng của các nguyên liệu lỗi đó không vượt quá ngưỡng quy định.
  * *Ngưỡng thông thường:* Không vượt quá **10% giá trị FOB** của hàng hóa (như trong ATIGA, ACFTA, RCEP), hoặc **10% theo trọng lượng/giá xuất xưởng EXW** (tùy quy định từng hiệp định, đặc biệt đối với dệt may Chương 50-63).

### 2.3. Công Thức Tính Toán Hàm Lượng Giá Trị (RVC, VAC, VL, DVC)
Không áp đặt một công thức duy nhất, bắt buộc tính đúng theo định chế của từng FTA:

* **RVC trong ASEAN+ & CPTPP (Dựa trên giá FOB):**
  * *Công thức gián tiếp (Build-down):*
    $$\text{RVC} = \frac{\text{Trị giá FOB} - \text{Trị giá nguyên liệu không có xuất xứ (VNM)}}{\text{Trị giá FOB}} \times 100\%$$
  * *Công thức trực tiếp (Build-up):*
    $$\text{RVC} = \frac{\text{VOM (Nguyên liệu có XX)} + \text{Nhân công TT} + \text{Chi phí PB trực tiếp} + \text{Chi phí khác} + \text{Lợi nhuận}}{\text{Trị giá FOB}} \times 100\%$$
  * *Công thức Chi phí tịnh (Net Cost - NC) trong CPTPP:*
    $$\text{RVC} = \frac{\text{Chi phí tịnh (NC)} - \text{VNM}}{\text{Chi phí tịnh (NC)}} \times 100\%$$
  * *Công thức Giá trị tập trung (Focus Value) trong CPTPP:*
    $$\text{RVC} = \frac{\text{Trị giá hàng hóa} - \text{Trị giá nguyên liệu không có XX đặc trưng}}{\text{Trị giá hàng hóa}} \times 100\%$$
* **VL (Value Limit) trong EVFTA (Dựa trên Giá xuất xưởng - EXW):**
  * Không dùng giá FOB. Hạn mức nguyên liệu không có xuất xứ (VNM) không được vượt quá tỷ lệ quy định so với giá xuất xưởng:
    $$\frac{\text{Trị giá nguyên liệu không có xuất xứ (VNM)}}{\text{Trị giá EXW}} \times 100\% \le 70\% \text{ (hoặc ngưỡng cụ thể của từng mã hàng)}$$
* **VAC (VN-EAEU) & DVC (RCEP):** Áp dụng tỷ lệ nội địa theo công thức đặc thù của từng hiệp định.

### 2.4. Nguyên Tắc Gia Công Đơn Giản, Nguyên Liệu Thay Thế & Trung Gian
* **Phân định Pháp lý về Công đoạn Gia công Đơn giản:** 
  * Điều 9 Nghị định 31/2018/NĐ-CP **chỉ áp dụng cho quy tắc xuất xứ không ưu đãi**.
  * Đối với C/O ưu đãi FTA, bắt buộc phải áp dụng điều khoản gia công chế biến đơn giản quy định riêng trong từng FTA tương ứng (như Điều 31 ATIGA, Điều 6 Phụ lục I EVFTA).
  * Các công đoạn bảo quản, đóng gói/chia gói bán lẻ, dán nhãn, lắp ráp đơn giản, pha loãng/trộn đơn giản không làm thay đổi bản chất xuất xứ.
* **Nguyên liệu Thay thế được cho nhau (Identical & Interchangeable Materials):**
  * Đối với hàng xá, hạt nhựa, hóa chất lưu kho chung: Được phép quản lý xuất xứ bằng **phân chia vật lý (physical segregation)** HOẶC áp dụng **nguyên tắc kế toán kho (FIFO, LIFO, bình quân gia quyền)** thống nhất trong suốt năm tài chính.
* **Yếu tố Trung gian (Indirect Materials):**
  * Nhiên liệu, năng lượng, chất bôi trơn, dụng cụ, găng tay bảo hộ dùng trong sản xuất nhưng không cấu thành vào sản phẩm thì **mặc nhiên coi là có xuất xứ**, không cần xét nguồn gốc.
* **Cộng gộp (Cumulation):**
  * Nguyên liệu có xuất xứ của nước thành viên FTA được coi là nguyên liệu có xuất xứ của nước sản xuất.
  * *Cộng gộp từng phần (Partial Cumulation):* Trong ATIGA, nếu nguyên liệu có RVC $\ge 20\%$ nhưng $< 40\%$, được phép cộng gộp theo tỷ lệ phần trăm thực tế.

### 2.5. Cấu Trúc Form C/O Đặc Thù (Form-Specific Layouts)
* **Mẫu Form D (ATIGA):**
  * C/O điện tử qua Cơ chế Một cửa ASEAN (ASW) hoặc bản giấy.
  * **Box 9:** Bắt buộc ghi trị giá FOB cho mọi dòng hàng (trừ hàng xuất sang Campuchia, Myanmar).
  * **Box 13:** Kiểm tra các ô tick kỹ thuật: *Third Country Invoicing*, *Issued Retroactively* (sau 3 ngày kể từ ngày xuất khẩu / on-board B/L), *Accumulation*, *Partial Cumulation*, *De Minimis*.
* **Mẫu Form EUR.1 (EVFTA):**
  * Căn cứ **Thông tư số 14/2026/TT-BCT** ngày 25/03/2026 (có hiệu lực từ **10/05/2026**, bãi bỏ và thay thế toàn bộ Thông tư 11/2020/TT-BCT và 41/2022/TT-BCT).
  * Có **14 ô** (không dùng cấu trúc 13 ô). Box 7 là Ghi chú (Remarks), Box 10 là Hóa đơn (Invoices - Tùy chọn), Box 11 là Hải quan chứng thực, Box 13/14 dành cho yêu cầu và kết quả xác minh.
  * In trên giấy có hoa văn nền mắt lưới guilloche màu xanh lá cây.
* **Mẫu Form RCEP:**
  * Căn cứ **Thông tư số 05/2022/TT-BCT** kết hợp sửa đổi bởi **Thông tư số 32/2022/TT-BCT** (Cập nhật PSR HS 2022).
  * **Box 3:** Dành riêng cho Nhà sản xuất nếu đã biết (ghi *SAME AS EXPORTER*, hoặc *NOT AVAILABLE*, *CONFIDENTIAL*, hoặc *SEE BOX 8* nếu nhiều NSX).
  * **Box 5:** Dành cho cơ quan hải quan (For Official Use).
  * Thể hiện rõ mã nước xuất xứ RCEP (RCEP Country of Origin).
* **Mẫu Form CPTPP:**
  * Căn cứ **Thông tư số 03/2019/TT-BCT** sửa đổi bởi **Thông tư số 06/2020/TT-BCT** và bổ sung bởi **Thông tư số 55/2025/TT-BCT**.
  * Chứng nhận xuất xứ theo định dạng dữ liệu tối thiểu (9 trường). Phải xác định rõ Người chứng nhận là Nhà xuất khẩu, Nhà sản xuất hay Người nhập khẩu.

### 2.6. Quy Trình Xác Minh Hải Quan & Thời Hạn Phản Hồi (Verification Rules)
* **Căn cứ Pháp lý Kiểm tra Hải quan Hiện hành:** **Thông tư số 33/2023/TT-BTC** ngày 31/05/2023 của Bộ Tài chính (có hiệu lực từ **15/07/2023**, thay thế toàn bộ Thông tư 38/2018/TT-BTC, 62/2019/TT-BTC, 47/2020/TT-BTC, 07/2021/TT-BTC) quy định toàn diện về xác định trước xuất xứ, kiểm tra, nộp bổ sung C/O, C/O giáp lưng và thủ tục xác minh xuất xứ hàng hóa XNK.
* **Thời hạn lưu trữ hồ sơ:** Tối thiểu **3 năm** theo quy định của hầu hết các FTA, nhưng pháp luật Việt Nam (Nghị định 31/2018/NĐ-CP và TT 33/2023/TT-BTC) yêu cầu lưu trữ tối thiểu **5 năm**.
* **Thời hạn phản hồi xác minh (Điển hình trong ATIGA & TT 33/2023):**
  * Khi C/O bị cơ quan hải quan nước nhập khẩu từ chối: Đánh dấu Box 4 và gửi trả C/O trong vòng không quá **60 ngày** kèm lý do.
  * Yêu cầu xác minh hồ sơ (Retroactive check): Cơ quan cấp nước xuất khẩu phải phản hồi trong vòng **90 ngày** kể từ ngày nhận yêu cầu.
  * Toàn bộ quy trình xác minh phải hoàn tất trong vòng tối đa **180 ngày** (hoặc 300 ngày đối với EVFTA).
  * Yêu cầu kiểm tra thực tế cơ sở sản xuất (Verification visit): Phải có sự đồng ý của nhà sản xuất trong vòng **30 ngày**, tiến hành trong vòng **60 ngày**, tổng thời gian thông báo kết quả tối đa **180 ngày**.

### 2.7. Thư Viện Tài Sản Pháp Lý Thực Địa (Field FTA Legal Assets - 5 Văn Bản Cốt Lõi)
Toàn bộ văn bản quy phạm pháp luật và danh mục PSR gốc (tổng quy mô 681 trang PDF) đã được nạp trực tiếp vào thư viện cục bộ tại `.agents/skills/customs-roo-specialist/assets/fta-rules/`:
* **FTA-DOC-01: ATIGA (Form D)** — [Thông tư số 22/2016/TT-BCT](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/assets/fta-rules/ATIGA_TT22_2016_BCT.pdf) (296 trang, PSR 97 Chương, khai FOB Box 9).
* **FTA-DOC-02: EVFTA (Form EUR.1)** — [Thông tư số 14/2026/TT-BCT](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/assets/fta-rules/EVFTA_TT14_2026_BCT.pdf) (112 trang, HL 10/05/2026, Value Limit EXW, cộng gộp dệt may chéo).
* **FTA-DOC-03: RCEP (Form RCEP)** — [Thông tư số 32/2022/TT-BCT](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/assets/fta-rules/RCEP_TT32_2022_BCT.pdf) (235 trang, PSR HS 2022, Box 3 Nhà sản xuất).
* **FTA-DOC-04: CPTPP (Chứng nhận CPTPP)** — [Thông tư số 55/2025/TT-BCT](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/assets/fta-rules/CPTPP_TT55_2025_BCT.pdf) (7 trang, hạn ngạch dệt may sang Mexico, 9 trường dữ liệu).
* **FTA-DOC-05: VN-UAE CEPA (Form VN-UAE)** — [Thông tư số 24/2026/TT-BCT](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/assets/fta-rules/VN_UAE_CEPA_TT24_2026_BCT.pdf) (31 trang, HL 20/06/2026, CEPA VN-UAE).

---

### 2.8. Bộ Cẩm Nang 5 Bẫy Lỗi Thực Chiến Hải Quan & Án Lệ Thực Tế (Red Flags Playbook)

> [!CAUTION]
> **5 Bẫy Bắt Lỗi Phổ Biến Của Hải Quan Khi Kiểm Tra C/O:**

1. **Bẫy 1: C/O Cấp Sau (Issued Retroactively) vs Ngày B/L On-Board:**
   * *Nguyên tắc:* Nếu C/O được cấp sau ngày xuất khẩu thực tế (thường là ngày On-board Bill of Lading) **quá 3 ngày làm việc** (hoặc 3 ngày theo quy định FTA), trên C/O **BẮT BUỘC** phải được đánh dấu vào ô *"Issued Retroactively"* (hoặc đóng dấu dòng chữ tương đương).
   * *Hậu quả thực tế:* Hải quan cửa khẩu từ chối áp dụng thuế ưu đãi ngay lập tức nếu C/O cấp sau 5-7 ngày mà quên tick ô này. Doanh nghiệp buộc phải nộp thuế theo mức MFN và chờ làm thủ tục xin cấp lại C/O thay thế.
2. **Bẫy 2: Hóa Đơn Bên Thứ Ba (Third-Party / Third-Country Invoicing):**
   * *Nguyên tắc:* Áp dụng khi người phát hành Hóa đơn thương mại là một công ty đặt tại quốc gia thứ ba (kể cả trong hay ngoài FTA).
   * *Bắt buộc thể hiện:* 
     * Tick ô *"Third Country Invoicing"* (Box 13 Form D, hoặc Box tương ứng trong RCEP/AKFTA).
     * Tên đầy đủ và quốc gia của công ty phát hành hóa đơn phải ghi rõ tại Box 7.
     * Số và ngày của Hóa đơn thương mại bên thứ ba phải ghi chính xác tại Box 10.
   * *Cảnh báo:* Tuyệt đối không ghi số Hóa đơn nội bộ giữa nhà sản xuất và người trung gian vào Box 10, vì Hải quan chỉ đối chiếu số hóa đơn đi kèm tờ khai hải quan nhập khẩu.
3. **Bẫy 3: Chuyển Tải & Bảo Toàn Tính Nguyên Trạng (Direct Consignment & Non-Manipulation):**
   * *Nguyên tắc:* Hàng hóa quá cảnh hoặc chuyển tải qua một nước không phải thành viên (như Singapore, Hong Kong, Busan) để đổi tàu.
   * *Hồ sơ giải độc theo Thông tư 33/2023/TT-BTC (Điều 18):*
     * Ưu tiên 1: **Vận đơn chở suốt (Through Bill of Lading)** thể hiện rõ cảng xếp hàng đầu tiên tại nước xuất khẩu và cảng dỡ hàng cuối cùng tại Việt Nam.
     * Ưu tiên 2: Trường hợp đổi Bill tại cảng trung chuyển, bắt buộc phải có **Giấy xác nhận chuyển tải / Giấy chứng nhận không can thiệp (Certificate of Non-Manipulation - CNM)** do cơ quan Hải quan hoặc Cảng vụ nước trung chuyển cấp, xác nhận hàng hóa giữ nguyên container/seal trong khu vực giám sát hải quan.
4. **Bẫy 4: Khác Biệt Mã HS Cấp Quốc Gia (HS Code Discrepancy at National Level):**
   * *Nguyên tắc:* Mã HS trên C/O có 8 số nhưng lệch 2 số cuối so với Mã HS do Hải quan Việt Nam xác định.
   * *Giải pháp pháp lý:* Dẫn chiếu **Điểm d Khoản 3 Điều 15 Thông tư 33/2023/TT-BTC**: Nếu cả mã HS trên C/O và mã HS do Hải quan xác định lại **đều cùng thỏa mãn tiêu chí xuất xứ quy định tại Danh mục PSR** thì Hải quan vẫn phải chấp nhận C/O, không được từ chối ưu đãi.
5. **Bẫy 5: Gia Công Đơn Giản Đội Lốt Xuất Xứ (Circumvention & Simple Processing Risks):**
   * *Nguyên tắc:* Nhập khẩu cụm linh kiện rời từ nước ngoài về Việt Nam chỉ để bắt ốc vít, đóng hộp, dán nhãn rồi xin cấp C/O xuất khẩu.
   * *Cảnh báo rủi ro:* Bị Bộ Công Thương thu hồi C/O và Hải quan nước nhập khẩu truy thu thuế hồi tố, kèm nguy cơ xử phạt hình sự về hành vi gian lận xuất xứ, lẩn tránh biện pháp phòng vệ thương mại.

---

### 2.9. Chiến Lược Tối Ưu Hóa Chuỗi Cung Ứng (Origin Engineering Framework) & So Sánh Đa Hiệp Định (FTA Arbitrage)

> [!TIP]
> Chi tiết tài liệu nghiệp vụ tham chiếu tại: [`origin_engineering_framework.md`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/resources/origin_engineering_framework.md).

#### 1. Framework 4 Bước "Giải Cứu" Xuất Xứ (Origin Engineering)
Khi phân tích sơ bộ thấy sản phẩm **chưa đạt** tiêu chí xuất xứ, AI kích hoạt ngay 4 đòn bẩy:
1. **Chuyển đổi phương pháp tính (Method Pivot):** Đổi từ *Build-down* sang *Build-up* để gom chi phí nhân công, khấu hao nhà xưởng hiện đại và lợi nhuận trực tiếp tại Việt Nam vào tử số; hoặc chuyển sang *Net Cost (NC)* đối với linh kiện cơ khí theo CPTPP.
2. **Kích hoạt Dung sai De Minimis (10% Tolerance Rescue):** Nếu vướng nguyên liệu loại trừ CTC, tính toán tỷ lệ trị giá nguyên liệu lỗi so với FOB. Nếu $\le 10\%$, kết luận toàn bộ lô hàng vẫn đạt xuất xứ theo cơ chế dung sai.
3. **Bóc tách Chi phí Gián tiếp & Yếu tố Trung gian (Indirect Materials Decoupling):** Loại bỏ năng lượng, dầu nhờn bôi trơn máy, hóa chất tẩy rửa, găng tay bảo hộ ra khỏi nhóm nguyên liệu không có xuất xứ (VNM), chuyển sang chi phí sản xuất chung (Overhead).
4. **Tái cấu trúc chuỗi cung ứng & Cộng gộp FTA (Cumulation Strategy):** Nhận diện linh kiện nút thắt cổ chai để kiến nghị chuyển nguồn mua sang các nước thành viên trong cùng khối FTA (ví dụ mua vải từ Hàn Quốc để hưởng cộng gộp chéo trong EVFTA theo TT 14/2026/TT-BCT).

#### 2. Ma Trận So Sánh Đa Hiệp Định (FTA Arbitrage Matrix)
* **Tuyến Xuất sang NHẬT BẢN:** So sánh 4 FTA đan xen:
  * **VJEPA (Form VJ):** Tối ưu nhất cho Nông lâm thủy sản và Thực phẩm chế biến (thuế về 0% sâu, tiêu chí linh hoạt).
  * **AJCEP (Form AJ):** Tối ưu khi sử dụng chuỗi nguyên liệu nhập khẩu từ các nước ASEAN.
  * **CPTPP:** Tối ưu cho Doanh nghiệp FDI cơ khí chính xác và thiết bị điện tử có thể tự chứng nhận xuất xứ; **tránh dùng cho dệt may nếu mua vải từ Trung Quốc** vì vướng quy tắc *"Từ sợi trở đi (Yarn-forward)"*.
  * **RCEP (Form RCEP):** **Vũ khí tối thượng cho Ngành Dệt may & Điện tử.** Cho phép cộng gộp nguyên liệu vải, vi mạch nhập khẩu từ Trung Quốc và Hàn Quốc để hưởng thuế ưu đãi sang Nhật Bản!
* **Tuyến Xuất sang HÀN QUỐC:** Ưu tiên **VKFTA (Form VK)** vì cam kết cắt giảm thuế sâu nhất; dùng **AKFTA** hoặc **RCEP** làm phương án dự phòng khi cần cộng gộp nguyên liệu ngoài Việt Nam.
* **Tuyến Nội khối ASEAN:** Luôn ưu tiên **Form D (ATIGA)** vì hơn 98% dòng thuế đã về 0% và hệ thống Một cửa ASEAN (ASW) thông quan tự động trong vài phút.

---

### 2.10. Cơ Chế Bảo Vệ Sai Khác Nhỏ (Minor Discrepancies) & Khung Đấu Tranh Pháp Lý Hải Quan

> [!NOTE]
> Mẫu công văn giải trình bảo vệ C/O chuẩn được lưu trữ tại: [`customs_defense_dossier_template.md`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/resources/customs_defense_dossier_template.md).

Căn cứ **Khoản 3 Điều 15 Thông tư số 33/2023/TT-BTC**, các trường hợp sau đây được pháp luật quy định là **"Khác biệt nhỏ không làm mất hiệu lực của C/O"**, Hải quan không được phép từ chối hoặc đình chỉ áp dụng thuế ưu đãi:
1. **Lỗi chính tả hoặc lỗi đánh máy:** Không làm sai lệch bản chất tên hàng, người xuất khẩu, người nhập khẩu.
2. **Kích thước chữ in, màu mực, mẫu dấu, chữ ký:** Có sự khác biệt nhỏ về sắc độ hoặc vị trí đóng dấu nhưng nội dung pháp lý không thay đổi.
3. **Mô tả hàng hóa có sự khác biệt nhỏ:** Mô tả trên C/O vắn tắt hơn trên Tờ khai hải quan hoặc Hóa đơn thương mại nhưng hàng hóa thực tế nhập khẩu phù hợp với bản chất hàng hóa được chứng nhận.
4. **Sự khác biệt về Mã HS:** Mã HS trên C/O khác với mã HS phân loại của Hải quan nhưng cả hai mã đều đáp ứng cùng tiêu chí xuất xứ theo PSR.
5. **Ngày phát hành Hóa đơn sau ngày cấp C/O:** Do đặc thù thương mại quốc tế (hóa đơn thương mại chính thức được phát hành sau khi hàng đã đóng container và có số cân thực tế).

---

## 3. Quy Trình Thực Thi 6 Bước Chuyên Gia (Execution Process)

```mermaid
graph TD
    A[Bước 1: Phỏng vấn Sàng lọc Thông minh 3 Tầng] --> B[Bước 2: Phân tích & Kích hoạt Origin Engineering]
    B --> C[Bước 3: Rà soát Công đoạn Gia công Đơn giản]
    C --> D[Bước 4: Quét Box-by-Box & Bắt Bẫy Hải quan]
    D --> E[Bước 5: Thẩm định Vận chuyển Suốt & Tính Nguyên trạng]
    E --> F[Bước 6: Đánh giá Questionnaire & Soạn Công văn Giải trình]
```

1. **Bước 1: Phỏng Vấn Sàng Lọc Thông Minh 3 Tầng (3-tier Interactive Inquiry)**
   * Nếu người dùng cung cấp thông tin còn mỏng, chuyên viên không đoán mò mà đặt ngay 3 câu hỏi cốt lõi:
     * *Tầng 1 (Định danh):* Tên hàng hóa, Mã HS 6 số thành phẩm, Nước nhập khẩu đích.
     * *Tầng 2 (BOM & Chuỗi cung ứng):* Tỷ lệ nguyên liệu nội địa/nội khối vs nguyên liệu nhập khẩu ngoài FTA (kèm mã HS linh kiện chính).
     * *Tầng 3 (Quy trình sản xuất):* Quy trình công nghệ tại nhà máy gồm những công đoạn nào?
2. **Bước 2: Phân Tích & Kích Hoạt Động Cơ Tối Ưu Hóa (Origin Engineering Engine)**
   * Tra cứu danh mục PSR trong các thông tư FTA gốc (ATIGA, EVFTA, RCEP, CPTPP, CEPA).
   * Kiểm tra CTC ngoại trừ. Nếu vướng: Kích hoạt ngay dung sai **De Minimis (ngưỡng 10%)**.
   * Tính toán RVC/VL. Nếu chưa đạt: Kích hoạt quy trình chuyển đổi phương pháp (Build-down $\rightarrow$ Build-up), bóc tách yếu tố trung gian và hiến kế tái cấu trúc BOM.
3. **Bước 3: Rà Soát Các Công Đoạn Gia Công Đơn Giản**
   * Đối chiếu quy trình sản xuất thực tế với danh mục công đoạn đơn giản quy định riêng trong từng FTA (như Điều 31 ATIGA, Điều 6 Phụ lục I EVFTA). Loại bỏ nguy cơ bị gắn nhãn gian lận xuất xứ.
4. **Bước 4: Quét Từng Ô (Box-by-Box Audit) & Đối Soát 5 Bẫy Hải Quan**
   * Rà soát đối chiếu từng ô theo mẫu form (Form D 13 ô, Form EUR.1 14 ô, Form RCEP...).
   * Bắt bẫy lỗi: Hóa đơn bên thứ ba (Box 7, 10, 13), C/O cấp sau quá 3 ngày (Issued Retroactively), khai FOB Box 9 Form D.
5. **Bước 5: Thẩm Định Vận Chuyển Trực Tiếp & Bảo Toàn Tính Nguyên Trạng**
   * Rà soát hành trình tàu chạy: Kiểm tra Through B/L hoặc yêu cầu Giấy xác nhận không can thiệp (CNM) nếu hàng ghé cảng trung chuyển ngoài khối theo Điều 18 Thông tư 33/2023/TT-BTC.
6. **Bước 6: Đánh Giá Questionnaire & Xuất Bản Dự Thảo Công Văn Giải Trình (Customs Defense Dossier)**
   * Đánh giá hồ sơ dự phòng theo Questionnaire Hải quan (0-100 điểm).
   * Soạn thảo trực tiếp **Bản Dự thảo Công văn Giải trình** viện dẫn Thông tư 33/2023/TT-BTC để bảo vệ doanh nghiệp khi bị Hải quan ra Phiếu yêu cầu nghiệp vụ hoặc nghi vấn xuất xứ.

---

## 4. Định Dạng Báo Cáo Đầu Ra Chuẩn (Output Format)

Mỗi lần thực thi thẩm định và tư vấn, chuyên viên xuất bản báo cáo theo đúng cấu trúc 7 phần:

### 1. BẢNG PHÂN TÍCH QUY TẮC XUẤT XỨ (ROO ELIGIBILITY ANALYSIS)
- **Hàng hóa:** [Tên hàng] | **Mã HS:** `xxxx.xx.xx` | **Nước xuất xứ:** ...
- **Mẫu C/O & Hiệp định (FTA):** [VD: Form D - ATIGA / Form EUR.1 - EVFTA / Form RCEP]
- **Quy tắc cụ thể mặt hàng (PSR):** [Trích dẫn quy tắc nguyên văn: CTH / CTSH / RVC... / SP]
- **Kết quả thẩm định điều kiện:**
  - *Phân tích CTC:* [Đạt / Không đạt / Có vướng ngoại trừ không]
  - *Thẩm định De Minimis:* [Tỷ lệ nguyên liệu lỗi % FOB / EXW $\le 10\%$ - Kết luận Đạt/Không áp dụng]
  - *Tính toán Hàm lượng giá trị (nếu có):*
    * Công thức áp dụng: [Build-down / Build-up / Net Cost / Value Limit (EXW)]
    * Giá trị tính toán thực tế: **...%** (So với ngưỡng yêu cầu: ...%)
  - *Rà soát gia công đơn giản:* [Quy trình sản xuất đã vượt qua các công đoạn gia công đơn giản theo FTA]

### 2. KẾT LUẬN TÍNH HỢP LỆ CỦA C/O (AUDIT VERDICT)
- **Đánh giá tổng quan:** [HỢP LỆ - ĐỦ ĐIỀU KIỆN ÁP DỤNG THUẾ FTA] / [CẢNH BÁO - SAI SÓT NHỎ CẦN GIẢI TRÌNH] / [NGHIÊM TRỌNG - NGUY CƠ BÁC C/O HOẶC TRUY THU]
- **Số tham chiếu C/O (Ref No.):** ... | **Ngày cấp:** ...
- **Đối soát Box tiêu chí xuất xứ:** Khai báo `[Tiêu chí trên C/O]` $\rightarrow$ [KHỚP / SAI LỆCH] với kết quả phân tích ROO.

### 3. MA TRẬN ĐỐI CHIẾU BOX-BY-BOX THEO MẪU FORM
| Vị trí (Box) | Nội dung trên C/O | Dữ liệu đối chiếu (Inv/BL/PL/BOM) | Trạng thái | Mức độ rủi ro & Căn cứ FTA |
| :--- | :--- | :--- | :--- | :--- |
| **Box 8** | *Tiêu chí xuất xứ* | *Quy tắc PSR của FTA* | *Khớp / Lệch* | *Căn cứ Thông tư FTA* |
| **Box 9** | *Trọng lượng / Trị giá FOB / EXW* | *PL: ... kg / BL: ... kg* | *Khớp / Lệch* | *Quy định khai báo trị giá của Form* |
| **Box 10** | *Số & Ngày Invoice* | *Commercial Invoice nộp HQ* | *Khớp / Sai ngày* | *Yêu cầu đồng nhất chứng từ* |
| **Box 13** | *Third-party / Retroactive tick* | *Bên thứ 3 / Ngày On-board BL* | *Đạt / Thiếu tick* | *Ràng buộc Box ghi chú đặc biệt* |

### 4. ĐIỀU KIỆN VẬN CHUYỂN TRỰC TIẾP & HIỆU LỰC
- **Hành trình:** [Đi thẳng / Quá cảnh qua ...]
- **Chứng từ vận chuyển suốt:** [Through B/L hợp lệ / Cần Giấy chứng nhận không can thiệp CNM].
- **Thời hạn hiệu lực:** [Còn trong hạn 12 tháng tính đến ngày mở tờ khai].

### 5. ĐÁNH GIÁ MỨC ĐỘ SẴN SÀNG XÁC MINH HẢI QUAN (VERIFICATION READINESS)
- **Điểm số Questionnaire:** `[xx / 100]` (Đạt yêu cầu đối soát sau thông quan)
- **Checklist hồ sơ dự phòng:**
  - [ ] Bảng kê chi phí và giá thành sản xuất (Cost Statement) có chữ ký đại diện pháp luật.
  - [ ] Bảng kê định mức nguyên liệu (BOM) khớp với thực tế sản xuất.
  - [ ] Hóa đơn VAT / Tờ khai nhập khẩu của nguyên vật liệu cấu thành.
  - [ ] Bằng chứng quản lý kho đối với nguyên liệu thay thế được cho nhau (nếu có).

### 6. BẢN KIẾN NGHỊ TỐI ƯU HÓA XUẤT XỨ (ORIGIN ENGINEERING PROPOSAL)
*(Chuyên mục độc quyền kích hoạt khi hàng chưa đạt hoặc muốn tối ưu hóa chi phí)*
- **Điểm nghẽn xuất xứ (Bottleneck Analysis):** [Chỉ rõ linh kiện, công thức hoặc công đoạn nào đang làm rớt C/O].
- **Phương án giải cứu 1 (Method Pivot):** [Đổi công thức tính từ Build-down sang Build-up... Dự kiến RVC tăng từ ...% lên ...%].
- **Phương án giải cứu 2 (De Minimis & Indirect Materials):** [Khai thác dung sai 10% hoặc bóc tách chi phí gián tiếp...].
- **Chiến lược Hiệp định tối ưu (FTA Arbitrage):** [So sánh và khuyến nghị chọn Form nào giữa các FTA đan xen để hưởng lợi thuế cao nhất và thủ tục dễ nhất].

### 7. DỰ THẢO CÔNG VĂN GIẢI TRÌNH HẢI QUAN (CUSTOMS DEFENSE STATEMENT)
*(Soạn thảo ngay khi phát hiện sai khác nhỏ hoặc có nguy cơ bị Hải quan phát hành phiếu nghi vấn)*
- **Trích dẫn điều khoản bảo vệ:** Căn cứ Khoản 3 Điều 15 Thông tư số 33/2023/TT-BTC.
- **Nội dung giải trình mẫu:** Đoạn văn bản hoàn chỉnh để doanh nghiệp sao chép, điền số tờ khai và in ký đóng dấu nộp ngay cho Chi cục Hải quan xử lý thông quan.

---

## 5. Hướng Dẫn Sử Dụng Bộ Công Cụ Hỗ Trợ Tự Động Hóa (Tooling Reference)

Chuyên viên sở hữu 3 công cụ tự động hóa tại `scripts/` (sử dụng khi cần tính toán số liệu lớn hoặc xuất bản báo cáo đồ họa):
* `calculate_origin.py`: Tính toán RVC Build-down, Build-up, Net Cost, EVFTA Value Limit, De Minimis.
* `audit_co_box.py`: Đối soát Box-by-Box theo form và chấm điểm Questionnaire.
* `export_co_audit_html.py`: Kết xuất Dashboard HTML Glassmorphism cao cấp.

---

## 6. Liên Thông Hệ Sinh Thái Tam Giác Vàng Hải Quan

Skill này hoạt động như cánh tay thứ tư mở rộng của **Bộ Tam giác Vàng Hải quan**:
1. [`customs-hs-classifier`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-hs-classifier/SKILL.md): Cung cấp mã HS 8 số quốc gia và thuế suất FTA ưu đãi.
2. [`customs-roo-specialist`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-roo-specialist/SKILL.md) (Skill này): Thẩm định xuất xứ, tối ưu hóa định mức (Origin Engineering), quét Box C/O và soạn công văn giải trình bảo vệ doanh nghiệp.
3. [`customs:doc-auditor`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-doc-auditor/SKILL.md): Thẩm định 36 bẫy lỗi chứng từ XNK, bắt lệch số học, đối chiếu nợ C/O 30 ngày và kiểm soát bộ chứng từ.
4. [`customs-legal-advisor`](file:///c:/Minh%20Hoang/Antigravity%20h%E1%BB%8Dc/my-workspace/.agents/skills/customs-legal-advisor/SKILL.md): Cung cấp CSDL văn bản pháp luật, thủ tục thông quan và chế tài xử phạt vi phạm hành chính (Nghị định 128/2020).
