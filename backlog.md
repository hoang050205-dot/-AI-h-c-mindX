# Marketing Data Healing Backlog (`backlog.md`)

> **Hệ thống:** Self-Healing Marketing Data Engine  
> **Tệp thực thi:** `sample-data\marketing_campaigns.xlsx` (Xử lý trực tiếp trên file gốc)  
> **Thời gian chạy:** `2026-09-30 22:16:07`  
> **Kết quả tổng kết:** **Healed: 37 | Warning: 15 | Edge Case: 7**  

---

## 📊 1. BẢNG TỔNG HỢP CHỈ SỐ

| Chỉ số kiểm soát | Số lượng phát hiện & xử lý | Ý nghĩa nghiệp vụ |
|:---|:---:|:---|
| 🛠️ **Healed (Đã chữa lành)** | **37** | Tổng số lỗi dữ liệu (tiền tệ USD, thiếu đơn vị, ngày tự nhiên, logic chi tiêu) đã được tự động chuẩn hóa về quy chuẩn. |
| ⚠️ **Warning (Cảnh báo rủi ro)** | **15** | Các ca cần lưu ý: Chuyển Active sang Paused (8 ca) + Cảnh báo ngân sách vượt 1 tỷ VND (7 ca). |
| 🚨 **Edge Case (Ca ngoại lệ)** | **7** | Các ca ngân sách siêu lớn (> 1,000,000,000 VND) vượt khung kiểm soát chi phí thông thường 10-40 lần. |

---

## 📝 2. CHI TIẾT CÁC SỰ KIỆN HÀNH ĐỘNG (44 sự kiện)

| STT | Mã GD | Tên Chiến Dịch | Quy Tắc Áp Dụng | Phân Loại | Giá Trị Trước | Giá Trị Sau / Hành Động |
|:---:|:---:|:---|:---|:---:|:---|:---|
| 1 | `CMP002` | Google Search Brand Protection | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 2,500 USD | Spend: 1,850 USD | Budget: 62,500,000 VND | Spend: 46,250,000 VND (Tỷ giá 25,000) |
| 2 | `CMP005` | LinkedIn B2B Lead Summit | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 3,200 USD | Spend: 3,180 USD | Budget: 80,000,000 VND | Spend: 79,500,000 VND (Tỷ giá 25,000) |
| 3 | `CMP008` | YouTube Tech Review Influencer | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 4,000 USD | Spend: 0 USD | Budget: 100,000,000 VND | Spend: 0 VND (Tỷ giá 25,000) |
| 4 | `CMP012` | Google Performance Max Ecom | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 1,800 USD | Spend: 1,420 USD | Budget: 45,000,000 VND | Spend: 35,500,000 VND (Tỷ giá 25,000) |
| 5 | `CMP014` | Mobile App Install Universal | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 5,500 USD | Spend: 2,100 USD | Budget: 137,500,000 VND | Spend: 52,500,000 VND (Tỷ giá 25,000) |
| 6 | `CMP022` | Google Display Network Retargeting | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 3,500 USD | Spend: 2,750 USD | Budget: 87,500,000 VND | Spend: 68,750,000 VND (Tỷ giá 25,000) |
| 7 | `CMP030` | YouTube Bumper Ads Quick Reach | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 1,200 USD | Spend: 950 USD | Budget: 30,000,000 VND | Spend: 23,750,000 VND (Tỷ giá 25,000) |
| 8 | `CMP041` | Global Tech Expo Booth Digital Push | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 6,000 USD | Spend: 4,100 USD | Budget: 150,000,000 VND | Spend: 102,500,000 VND (Tỷ giá 25,000) |
| 9 | `CMP052` | YouTube TrueView For Action | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 2,800 USD | Spend: 2,100 USD | Budget: 70,000,000 VND | Spend: 52,500,000 VND (Tỷ giá 25,000) |
| 10 | `CMP063` | Google Discovery Feed Carousel | Quy tắc 1: Quy đổi tiền tệ USD -> VND | `HEALED` | Budget: 4,200 USD | Spend: 3,450 USD | Budget: 105,000,000 VND | Spend: 86,250,000 VND (Tỷ giá 25,000) |
| 11 | `CMP004` | SEO Content Pillar Q3 | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 12 | `CMP007` | Facebook Retargeting Catalog | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 13 | `CMP010` | Shopee 9.9 Super Shopping Day | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 14 | `CMP015` | Local Mall Experiential Booth | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 15 | `CMP016` | Affiliate Referral Commission | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 16 | `CMP025` | SEO Link Building Authority Surge | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 17 | `CMP035` | TikTok Brand Takeover TopView | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 18 | `CMP045` | Community Discord Server Onboarding | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 19 | `CMP055` | TikTok Sound Branding Audio Logo | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 20 | `CMP065` | Retail Store Window Decal Branding | Quy tắc 2: Bổ khuyết đơn vị tiền tệ thiếu | `HEALED` | Currency: (Trống / None) | Currency: VND |
| 21 | `CMP004` | SEO Content Pillar Q3 | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 22 | `CMP008` | YouTube Tech Review Influencer | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 23 | `CMP015` | Local Mall Experiential Booth | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 24 | `CMP027` | LinkedIn Enterprise Account ABM | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 25 | `CMP034` | University Tour Activation Booth | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 26 | `CMP044` | Podcast Mid-roll Host Read Sponsorship | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 27 | `CMP056` | Airport VIP Lounge Digital Screen | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 28 | `CMP067` | Gaming Streamer Product Placement | Quy tắc 3: Kiểm tra logic ngân sách | `HEALED & WARNING` | Status: Active | Actual_Spend: 0 VND | Status: Paused |
| 29 | `CMP008` | YouTube Tech Review Influencer | Quy tắc 4: Giải mã lịch trình (Start_Date) | `HEALED` | Start_Date: 'Tháng sau' | Start_Date: '2026-10-01' |
| 30 | `CMP015` | Local Mall Experiential Booth | Quy tắc 4: Giải mã lịch trình (Start_Date) | `HEALED` | Start_Date: 'Đầu tuần sau' | Start_Date: '2026-10-05' |
| 31 | `CMP032` | Facebook Lead Form Test Drive | Quy tắc 4: Giải mã lịch trình (Start_Date) | `HEALED` | Start_Date: 'Giữa tháng này' | Start_Date: '2026-09-15' |
| 32 | `CMP053` | Flash Clearance Sale Weekend | Quy tắc 4: Giải mã lịch trình (Start_Date) | `HEALED` | Start_Date: 'Tuần tới' | Start_Date: '2026-10-05' |
| 33 | `CMP003` | TikTok Dance Challenge GenZ | Quy tắc 4: Giải mã lịch trình (End_Date) | `HEALED` | End_Date: 'Sau lễ' | End_Date: '2026-09-03' |
| 34 | `CMP013` | TikTok Livestream Flash Voucher | Quy tắc 4: Giải mã lịch trình (End_Date) | `HEALED` | End_Date: 'Q3' | End_Date: '2026-09-30' |
| 35 | `CMP023` | Spring Festive Brand Giveaway | Quy tắc 4: Giải mã lịch trình (End_Date) | `HEALED` | End_Date: 'Sau Tết' | End_Date: '2026-02-23' |
| 36 | `CMP042` | Mid-Autumn Festival Gift Box Promo | Quy tắc 4: Giải mã lịch trình (End_Date) | `HEALED` | End_Date: 'Cuối Q3' | End_Date: '2026-09-30' |
| 37 | `CMP062` | Summer Travel Gear Promo | Quy tắc 4: Giải mã lịch trình (End_Date) | `HEALED` | End_Date: 'Hết mùa hè' | End_Date: '2026-08-31' |
| 38 | `CMP006` | National TVC & Highway Billboard | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 1,850,000,000 VND | Budget: 1,850,000,000 VND [Flagged] |
| 39 | `CMP011` | Mega Year-End Omnichannel Push | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 3,200,000,000 VND | Budget: 3,200,000,000 VND [Flagged] |
| 40 | `CMP026` | TVC Tet Countdown Prime Time | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 1,200,000,000 VND | Budget: 1,200,000,000 VND [Flagged] |
| 41 | `CMP036` | National Roadshow 10 Provinces | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 2,500,000,000 VND | Budget: 2,500,000,000 VND [Flagged] |
| 42 | `CMP046` | Brand Rebranding Mega Launch Event | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 1,450,000,000 VND | Budget: 1,450,000,000 VND [Flagged] |
| 43 | `CMP057` | Global Music Festival Co-sponsorship | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 4,000,000,000 VND | Budget: 4,000,000,000 VND [Flagged] |
| 44 | `CMP068` | Nationwide LED City Screen Takeover | Edge Case: Ngân sách bất thường (> 1 tỷ VND) | `WARNING & EDGE_CASE` | Budget: 1,750,000,000 VND | Budget: 1,750,000,000 VND [Flagged] |

---

## 💡 3. GHI CHÚ HÀNH ĐỘNG TIẾP THEO (ACTION ITEMS)
1. **Đội ngũ Media Buyer:** Kiểm tra lại 8 chiến dịch vừa chuyển sang `Paused` để xác minh xem đã gắn tracking pixel và nạp thẻ thanh toán quảng cáo chưa.
2. **Bộ phận Kế toán & Phê duyệt:** Thẩm định 7 chiến dịch có ngân sách > 1 tỷ VND để đảm bảo có chữ ký phê duyệt từ CMO và Ban Giám Đốc.
3. **Bộ phận Data Analytics:** Tệp dữ liệu hiện đã chuẩn hóa 100% định dạng VND và ngày ISO `YYYY-MM-DD`, sẵn sàng tích hợp trực tiếp vào Power BI, Tableau hoặc Looker Studio.
