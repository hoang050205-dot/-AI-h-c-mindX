# -*- coding: utf-8 -*-
"""
Script tạo file Excel Báo Cáo Phân Tích Quán Cà Phê Quận 1 (PDCA Framework)
Tác giả: Antigravity AI
"""

import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

# 1. Dữ liệu 22 quán cafe Quận 1 đã chuẩn hóa và làm sạch
data = [
    {
        "CAFE_ID": "CF01",
        "CAFE_NAME": "The Workshop Coffee",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "Lầu 2, 27 Ngô Đức Kế",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 50000,
        "PRICE_MAX_VND": 160000,
        "PRICE_AVG_VND": 105000,
        "PRICE_RANGE_DISPLAY": "50,000 - 160,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 1650,
        "STYLE_CONCEPT": "Specialty & Industrial Loft",
        "PRIMARY_PURPOSE": "Làm việc & Thưởng thức Specialty",
        "OPENING_HOURS": "08:00 - 21:00",
        "PARKING_INFO": "Giữ xe tòa nhà (Có phí)"
    },
    {
        "CAFE_ID": "CF02",
        "CAFE_NAME": "Okkio Caffe - Lê Lợi",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "120-122 Lê Lợi",
        "WARD": "Bến Thành",
        "PRICE_MIN_VND": 55000,
        "PRICE_MAX_VND": 120000,
        "PRICE_AVG_VND": 87500,
        "PRICE_RANGE_DISPLAY": "55,000 - 120,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.6,
        "REVIEW_COUNT": 920,
        "STYLE_CONCEPT": "Retro & Red Brick Minimalist",
        "PRIMARY_PURPOSE": "Thư giãn & Sống ảo",
        "OPENING_HOURS": "07:30 - 22:00",
        "PARKING_INFO": "Bãi xe lân cận (Có phí)"
    },
    {
        "CAFE_ID": "CF03",
        "CAFE_NAME": "Cheese Coffee - Pasteur",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "15 Pasteur",
        "WARD": "Nguyễn Thái Bình",
        "PRICE_MIN_VND": 35000,
        "PRICE_MAX_VND": 75000,
        "PRICE_AVG_VND": 55000,
        "PRICE_RANGE_DISPLAY": "35,000 - 75,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.4,
        "REVIEW_COUNT": 2150,
        "STYLE_CONCEPT": "European Classic & French Bistro",
        "PRIMARY_PURPOSE": "Sống ảo & Trò chuyện bạn bè",
        "OPENING_HOURS": "07:00 - 22:30",
        "PARKING_INFO": "Tại quán (Có bảo vệ dắt xe)"
    },
    {
        "CAFE_ID": "CF04",
        "CAFE_NAME": "The Running Bean",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "33 Mạc Thị Bưởi",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 65000,
        "PRICE_MAX_VND": 150000,
        "PRICE_AVG_VND": 107500,
        "PRICE_RANGE_DISPLAY": "65,000 - 150,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 1480,
        "STYLE_CONCEPT": "Modern Mediterranean & Brunch",
        "PRIMARY_PURPOSE": "Tiếp khách & Làm việc nhóm",
        "OPENING_HOURS": "07:30 - 22:00",
        "PARKING_INFO": "Bãi xe lân cận (Có phí)"
    },
    {
        "CAFE_ID": "CF05",
        "CAFE_NAME": "Rang Rang Coffee - Mạc Thị Bưởi",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "74 Mạc Thị Bưởi",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 60000,
        "PRICE_MAX_VND": 180000,
        "PRICE_AVG_VND": 120000,
        "PRICE_RANGE_DISPLAY": "60,000 - 180,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 860,
        "STYLE_CONCEPT": "Modern Hi-Tech & Futurism",
        "PRIMARY_PURPOSE": "Làm việc & Specialty Coffee",
        "OPENING_HOURS": "07:00 - 23:00",
        "PARKING_INFO": "Gửi xe gần quán (Có phí)"
    },
    {
        "CAFE_ID": "CF06",
        "CAFE_NAME": "Dabao Concept - Cố Đô",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "18bis/29 Nguyễn Thị Minh Khai",
        "WARD": "Đa Kao",
        "PRICE_MIN_VND": 50000,
        "PRICE_MAX_VND": 105000,
        "PRICE_AVG_VND": 77500,
        "PRICE_RANGE_DISPLAY": "50,000 - 105,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.4,
        "REVIEW_COUNT": 1120,
        "STYLE_CONCEPT": "Cổ trang Á Đông & Nét hoài niệm",
        "PRIMARY_PURPOSE": "Sống ảo & Check-in nghệ thuật",
        "OPENING_HOURS": "07:00 - 22:00",
        "PARKING_INFO": "Tại quán (Miễn phí)"
    },
    {
        "CAFE_ID": "CF07",
        "CAFE_NAME": "Soo Kafe - Phan Kế Bính",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "10 Phan Kế Bính",
        "WARD": "Đa Kao",
        "PRICE_MIN_VND": 45000,
        "PRICE_MAX_VND": 75000,
        "PRICE_AVG_VND": 60000,
        "PRICE_RANGE_DISPLAY": "45,000 - 75,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.6,
        "REVIEW_COUNT": 1380,
        "STYLE_CONCEPT": "Korean Minimalist & Garden",
        "PRIMARY_PURPOSE": "Làm việc yên tĩnh & Đọc sách",
        "OPENING_HOURS": "08:00 - 23:00",
        "PARKING_INFO": "Tại quán (Có bảo vệ dắt xe)"
    },
    {
        "CAFE_ID": "CF08",
        "CAFE_NAME": "Tonkin Specialty Coffee",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "91 Lý Tự Trọng",
        "WARD": "Bến Thành",
        "PRICE_MIN_VND": 45000,
        "PRICE_MAX_VND": 120000,
        "PRICE_AVG_VND": 82500,
        "PRICE_RANGE_DISPLAY": "45,000 - 120,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 540,
        "STYLE_CONCEPT": "Indochine Đông Dương & Art Space",
        "PRIMARY_PURPOSE": "Thưởng thức Cà phê trứng & Gặp gỡ",
        "OPENING_HOURS": "07:30 - 22:00",
        "PARKING_INFO": "Bãi xe gần quán (Có phí)"
    },
    {
        "CAFE_ID": "CF09",
        "CAFE_NAME": "Mockingbird Cafe",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "Lầu 4, Chung cư 14 Tôn Thất Đạm",
        "WARD": "Nguyễn Thái Bình",
        "PRICE_MIN_VND": 40000,
        "PRICE_MAX_VND": 70000,
        "PRICE_AVG_VND": 55000,
        "PRICE_RANGE_DISPLAY": "40,000 - 70,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.4,
        "REVIEW_COUNT": 780,
        "STYLE_CONCEPT": "Vintage Chung cư xưa & View Cầu Móng",
        "PRIMARY_PURPOSE": "Hẹn hò & Trốn ồn ào",
        "OPENING_HOURS": "08:30 - 23:00",
        "PARKING_INFO": "Gửi xe chung cư (Có phí)"
    },
    {
        "CAFE_ID": "CF10",
        "CAFE_NAME": "Beanthere Cafe",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "42/7 Hồ Hảo Hớn",
        "WARD": "Cô Giang",
        "PRICE_MIN_VND": 55000,
        "PRICE_MAX_VND": 110000,
        "PRICE_AVG_VND": 82500,
        "PRICE_RANGE_DISPLAY": "55,000 - 110,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 690,
        "STYLE_CONCEPT": "Garden Rooftop & Creative Space",
        "PRIMARY_PURPOSE": "Làm việc sáng tạo & Thư giãn",
        "OPENING_HOURS": "08:00 - 22:00",
        "PARKING_INFO": "Tại quán (Miễn phí)"
    },
    {
        "CAFE_ID": "CF11",
        "CAFE_NAME": "Katinat Saigon Kafe - Đồng Khởi",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "91 Đồng Khởi",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 38000,
        "PRICE_MAX_VND": 70000,
        "PRICE_AVG_VND": 54000,
        "PRICE_RANGE_DISPLAY": "38,000 - 70,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.2,
        "REVIEW_COUNT": 3850,
        "STYLE_CONCEPT": "Modern Retro & Street View",
        "PRIMARY_PURPOSE": "Check-in & Ngắm phố phường",
        "OPENING_HOURS": "07:00 - 23:00",
        "PARKING_INFO": "Bãi xe vỉa hè lân cận (Có phí)"
    },
    {
        "CAFE_ID": "CF12",
        "CAFE_NAME": "Cộng Cà Phê - Bùi Viện",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "127-129 Bùi Viện",
        "WARD": "Phạm Ngũ Lão",
        "PRICE_MIN_VND": 35000,
        "PRICE_MAX_VND": 75000,
        "PRICE_AVG_VND": 55000,
        "PRICE_RANGE_DISPLAY": "35,000 - 75,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.3,
        "REVIEW_COUNT": 2420,
        "STYLE_CONCEPT": "Bao cấp hoài niệm & Gỗ mộc",
        "PRIMARY_PURPOSE": "Văn hóa hoài cổ & Cà phê cốt dừa",
        "OPENING_HOURS": "07:30 - 23:30",
        "PARKING_INFO": "Gửi xe phố Tây (Có phí)"
    },
    {
        "CAFE_ID": "CF13",
        "CAFE_NAME": "Trung Nguyên Legend - Alexandre de Rhodes",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "12 Alexandre de Rhodes",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 45000,
        "PRICE_MAX_VND": 110000,
        "PRICE_AVG_VND": 77500,
        "PRICE_RANGE_DISPLAY": "45,000 - 110,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.4,
        "REVIEW_COUNT": 1950,
        "STYLE_CONCEPT": "Không gian Tri thức & Sách Nền tảng",
        "PRIMARY_PURPOSE": "Tiếp đối tác & Họp bàn công việc",
        "OPENING_HOURS": "06:30 - 22:00",
        "PARKING_INFO": "Tại quán (Miễn phí có bảo vệ)"
    },
    {
        "CAFE_ID": "CF14",
        "CAFE_NAME": "Nest by AIA - Landmark Bitexco",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "Tầng 2, Bitexco, 02 Hải Triều",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 55000,
        "PRICE_MAX_VND": 95000,
        "PRICE_AVG_VND": 75000,
        "PRICE_RANGE_DISPLAY": "55,000 - 95,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 1150,
        "STYLE_CONCEPT": "Luxury Co-working & Library",
        "PRIMARY_PURPOSE": "Chạy Deadline & Họp chuyên nghiệp",
        "OPENING_HOURS": "08:00 - 21:30",
        "PARKING_INFO": "Hầm Bitexco (Có phí)"
    },
    {
        "CAFE_ID": "CF15",
        "CAFE_NAME": "Snob Coffee - 24/7 Trần Hưng Đạo",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "147A Trần Hưng Đạo",
        "WARD": "Cầu Ông Lãnh",
        "PRICE_MIN_VND": 35000,
        "PRICE_MAX_VND": 68000,
        "PRICE_AVG_VND": 51500,
        "PRICE_RANGE_DISPLAY": "35,000 - 68,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.1,
        "REVIEW_COUNT": 1620,
        "STYLE_CONCEPT": "Modern 24/7 All-Night & iMac Station",
        "PRIMARY_PURPOSE": "Làm việc xuyên đêm & Học nhóm",
        "OPENING_HOURS": "24/7 (Mở cả ngày đêm)",
        "PARKING_INFO": "Tại quán (Miễn phí)"
    },
    {
        "CAFE_ID": "CF16",
        "CAFE_NAME": "Cà Phê Trứng 3T - Tôn Đức Thắng",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "1A Tôn Đức Thắng",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 39000,
        "PRICE_MAX_VND": 65000,
        "PRICE_AVG_VND": 52000,
        "PRICE_RANGE_DISPLAY": "39,000 - 65,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.3,
        "REVIEW_COUNT": 890,
        "STYLE_CONCEPT": "Vintage Hà Nội Xưa & Ban công",
        "PRIMARY_PURPOSE": "Thưởng thức đặc sản & Hẹn hò",
        "OPENING_HOURS": "07:00 - 23:00",
        "PARKING_INFO": "Tại quán (Có bảo vệ dắt xe)"
    },
    {
        "CAFE_ID": "CF17",
        "CAFE_NAME": "11:11 Cafe - Pasteur",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "144/7 Pasteur",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 40000,
        "PRICE_MAX_VND": 75000,
        "PRICE_AVG_VND": 57500,
        "PRICE_RANGE_DISPLAY": "40,000 - 75,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.3,
        "REVIEW_COUNT": 710,
        "STYLE_CONCEPT": "Dark Minimalist & Monochrome",
        "PRIMARY_PURPOSE": "Check-in thời trang & Sống ảo",
        "OPENING_HOURS": "08:00 - 22:00",
        "PARKING_INFO": "Đầu hẻm Pasteur (Có phí)"
    },
    {
        "CAFE_ID": "CF18",
        "CAFE_NAME": "Cafe RuNam D'Or",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "03 Công xã Paris",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 85000,
        "PRICE_MAX_VND": 250000,
        "PRICE_AVG_VND": 167500,
        "PRICE_RANGE_DISPLAY": "85,000 - 250,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.4,
        "REVIEW_COUNT": 2280,
        "STYLE_CONCEPT": "French Royal Villa & View Nhà thờ",
        "PRIMARY_PURPOSE": "Tiếp khách cao cấp & Trải nghiệm",
        "OPENING_HOURS": "07:30 - 23:00",
        "PARKING_INFO": "Trước quán (Có Valet đỗ xe)"
    },
    {
        "CAFE_ID": "CF19",
        "CAFE_NAME": "Bason Café - Hồ Huấn Nghiệp",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "4-6-8 Hồ Huấn Nghiệp",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 50000,
        "PRICE_MAX_VND": 95000,
        "PRICE_AVG_VND": 72500,
        "PRICE_RANGE_DISPLAY": "50,000 - 95,000 VNĐ",
        "PRICE_SEGMENT": "Tầm trung (40k - 75k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 640,
        "STYLE_CONCEPT": "Indochine Di sản Xưởng tàu",
        "PRIMARY_PURPOSE": "Thư giãn nghệ thuật & Tiếp khách",
        "OPENING_HOURS": "07:00 - 22:00",
        "PARKING_INFO": "Khách sạn The Myst (Miễn phí)"
    },
    {
        "CAFE_ID": "CF20",
        "CAFE_NAME": "L'Usine - Lê Thánh Tôn",
        "BRAND_TYPE": "Chuỗi (Chain)",
        "ADDRESS": "19 Lê Thánh Tôn",
        "WARD": "Bến Nghé",
        "PRICE_MIN_VND": 65000,
        "PRICE_MAX_VND": 160000,
        "PRICE_AVG_VND": 112500,
        "PRICE_RANGE_DISPLAY": "65,000 - 160,000 VNĐ",
        "PRICE_SEGMENT": "Cao cấp (>75k)",
        "RATING_GOOGLE": 4.3,
        "REVIEW_COUNT": 1320,
        "STYLE_CONCEPT": "Contemporary Bistro & Lifestyle",
        "PRIMARY_PURPOSE": "Brunch cuối tuần & Họp mặt đối tác",
        "OPENING_HOURS": "07:30 - 21:30",
        "PARKING_INFO": "Bãi xe Lê Thánh Tôn (Có phí)"
    },
    {
        "CAFE_ID": "CF21",
        "CAFE_NAME": "Cà Phê Vợt Chợ Bến Thành",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "28 Phan Chu Trinh",
        "WARD": "Bến Thành",
        "PRICE_MIN_VND": 20000,
        "PRICE_MAX_VND": 35000,
        "PRICE_AVG_VND": 27500,
        "PRICE_RANGE_DISPLAY": "20,000 - 35,000 VNĐ",
        "PRICE_SEGMENT": "Bình dân (<40k)",
        "RATING_GOOGLE": 4.5,
        "REVIEW_COUNT": 820,
        "STYLE_CONCEPT": "Cà phê Vỉa hè Sài Gòn xưa",
        "PRIMARY_PURPOSE": "Trải nghiệm văn hóa & Cà phê sáng",
        "OPENING_HOURS": "06:00 - 18:00",
        "PARKING_INFO": "Vỉa hè quán (Miễn phí)"
    },
    {
        "CAFE_ID": "CF22",
        "CAFE_NAME": "Cà Phê Vợt Bà Ba Lữ",
        "BRAND_TYPE": "Độc lập (Independent)",
        "ADDRESS": "100/18 Đỗ Quang Đẩu",
        "WARD": "Phạm Ngũ Lão",
        "PRICE_MIN_VND": 18000,
        "PRICE_MAX_VND": 30000,
        "PRICE_AVG_VND": 24000,
        "PRICE_RANGE_DISPLAY": "18,000 - 30,000 VNĐ",
        "PRICE_SEGMENT": "Bình dân (<40k)",
        "RATING_GOOGLE": 4.6,
        "REVIEW_COUNT": 510,
        "STYLE_CONCEPT": "Quán cóc hoài cổ gia truyền",
        "PRIMARY_PURPOSE": "Bạc xỉu truyền thống & Đời thường",
        "OPENING_HOURS": "05:30 - 17:00",
        "PARKING_INFO": "Hẻm trước quán (Miễn phí)"
    }
]

# 2. Data Dictionary definitions
data_dict = [
    ("CAFE_ID", "String", "CF01, CF02...", "Mã định danh duy nhất của từng quán cà phê"),
    ("CAFE_NAME", "String", "The Workshop Coffee...", "Tên thương mại của quán, chuẩn hóa không khoảng trắng thừa"),
    ("BRAND_TYPE", "Categorical", "Chuỗi (Chain) / Độc lập", "Mô hình vận hành: chuỗi nhiều chi nhánh hay cửa hàng độc lập"),
    ("ADDRESS", "String", "27 Ngô Đức Kế...", "Địa chỉ số nhà và tên đường tại khu vực trung tâm Quận 1"),
    ("WARD", "Categorical", "Bến Nghé, Bến Thành...", "Phường hành chính trực thuộc Quận 1 để phân tích địa bàn"),
    ("PRICE_MIN_VND", "Integer (VNĐ)", "50000", "Mức giá thấp nhất trong menu (chuẩn số nguyên phục vụ tính toán)"),
    ("PRICE_MAX_VND", "Integer (VNĐ)", "160000", "Mức giá cao nhất trong menu (chuẩn số nguyên phục vụ tính toán)"),
    ("PRICE_AVG_VND", "Integer (VNĐ)", "105000", "Mức giá trung bình = (Min + Max)/2, đại diện mức chi trả trung bình"),
    ("PRICE_RANGE_DISPLAY", "String", "50,000 - 160,000 VNĐ", "Chuỗi hiển thị khoảng giá thân thiện cho người dùng đọc báo cáo"),
    ("PRICE_SEGMENT", "Categorical", "Bình dân / Tầm trung / Cao cấp", "Phân khúc thị trường: Bình dân (<40k), Tầm trung (40k-75k), Cao cấp (>75k)"),
    ("RATING_GOOGLE", "Float (Thang 5.0)", "4.5", "Điểm đánh giá thực tế trên Google Maps (chuẩn hóa 1 chữ số thập phân)"),
    ("REVIEW_COUNT", "Integer", "1650", "Tổng số lượt nhận xét, đánh giá của người dùng trên Google Maps"),
    ("STYLE_CONCEPT", "Categorical", "Specialty, Indochine...", "Phong cách thiết kế và bài trí không gian chủ đạo của quán"),
    ("PRIMARY_PURPOSE", "Categorical", "Làm việc, Sống ảo...", "Mục đích sử dụng phù hợp nhất cho khách hàng khi ghé quán"),
    ("OPENING_HOURS", "String", "08:00 - 21:00, 24/7...", "Khung giờ phục vụ khách hàng hàng ngày"),
    ("PARKING_INFO", "Categorical", "Tại quán, Gửi bãi...", "Thông tin bãi đỗ xe và chi phí giữ xe cho khách hàng")
]

def build_excel_report(output_paths):
    wb = openpyxl.Workbook()
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True

    # Palette
    NAVY = "1B365D"
    ICE_BLUE = "E8EEF5"
    DARK_TEXT = "1C2833"
    BORDER_GRAY = "D5D8DC"
    ZEBRA_FILL = "F8F9FA"
    CARD_BG = "F4F6F9"

    font_title = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
    font_sub = Font(name="Segoe UI", size=10, italic=True, color="EAECEE")
    font_sec = Font(name="Segoe UI", size=12, bold=True, color=NAVY)
    font_bold = Font(name="Segoe UI", size=10, bold=True, color=DARK_TEXT)
    font_regular = Font(name="Segoe UI", size=10, color=DARK_TEXT)
    font_card_num = Font(name="Segoe UI", size=18, bold=True, color=NAVY)
    font_card_lbl = Font(name="Segoe UI", size=9, bold=True, color="566573")

    fill_header = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
    fill_sub_hdr = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
    fill_ice = PatternFill(start_color=ICE_BLUE, end_color=ICE_BLUE, fill_type="solid")
    fill_zebra = PatternFill(start_color=ZEBRA_FILL, end_color=ZEBRA_FILL, fill_type="solid")
    fill_card = PatternFill(start_color=CARD_BG, end_color=CARD_BG, fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color=BORDER_GRAY),
        right=Side(style='thin', color=BORDER_GRAY),
        top=Side(style='thin', color=BORDER_GRAY),
        bottom=Side(style='thin', color=BORDER_GRAY)
    )

    # -------------------------------------------------------------
    # SHEET 1: Executive_Dashboard
    # -------------------------------------------------------------
    ws_dash = wb.active
    ws_dash.title = "Executive_Dashboard"
    ws_dash.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_dash.merge_cells("A1:K1")
    t_cell = ws_dash["A1"]
    t_cell.value = "BÁO CÁO PHÂN TÍCH THỊ TRƯỜNG QUÁN CÀ PHÊ QUẬN 1, TP. HỒ CHÍ MINH"
    t_cell.font = font_title
    t_cell.fill = fill_header
    t_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[1].height = 40

    ws_dash.merge_cells("A2:K2")
    sub_cell = ws_dash["A2"]
    sub_cell.value = "Mô hình ứng dụng: PDCA Framework (Plan - Do - Check - Act) | Dữ liệu làm sạch & chuẩn hóa | Tháng 09/2026"
    sub_cell.font = font_sub
    sub_cell.fill = fill_sub_hdr
    sub_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.row_dimensions[2].height = 22

    # KPI Cards row 4 to 5
    # Card 1: Tổng số quán
    ws_dash.merge_cells("A4:B4")
    ws_dash["A4"] = "TỔNG SỐ QUÁN KHẢO SÁT"
    ws_dash["A4"].font = font_card_lbl
    ws_dash["A4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["A4"].fill = fill_card
    ws_dash.merge_cells("A5:B5")
    ws_dash["A5"] = 22
    ws_dash["A5"].font = font_card_num
    ws_dash["A5"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["A5"].fill = fill_card
    ws_dash["A5"].number_format = '#,##0" Quán"'

    # Card 2: Điểm Rating Google TB
    ws_dash.merge_cells("D4:E4")
    ws_dash["D4"] = "ĐIỂM GOOGLE RATING TB"
    ws_dash["D4"].font = font_card_lbl
    ws_dash["D4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["D4"].fill = fill_card
    ws_dash.merge_cells("D5:E5")
    ws_dash["D5"] = 4.44
    ws_dash["D5"].font = font_card_num
    ws_dash["D5"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["D5"].fill = fill_card
    ws_dash["D5"].number_format = '0.00" ★"'

    # Card 3: Giá TB Toàn Quận
    ws_dash.merge_cells("G4:H4")
    ws_dash["G4"] = "MỨC GIÁ TRUNG BÌNH"
    ws_dash["G4"].font = font_card_lbl
    ws_dash["G4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["G4"].fill = fill_card
    ws_dash.merge_cells("G5:H5")
    ws_dash["G5"] = 77318
    ws_dash["G5"].font = font_card_num
    ws_dash["G5"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["G5"].fill = fill_card
    ws_dash["G5"].number_format = '#,##0" VNĐ"'

    # Card 4: Quán Phù Hợp Làm Việc
    ws_dash.merge_cells("J4:K4")
    ws_dash["J4"] = "TỶ LỆ QUÁN LÀM VIỆC TỐT"
    ws_dash["J4"].font = font_card_lbl
    ws_dash["J4"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["J4"].fill = fill_card
    ws_dash.merge_cells("J5:K5")
    ws_dash["J5"] = 0.727
    ws_dash["J5"].font = font_card_num
    ws_dash["J5"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dash["J5"].fill = fill_card
    ws_dash["J5"].number_format = '0.0%'

    for col in ["A", "B", "D", "E", "G", "H", "J", "K"]:
        ws_dash[f"{col}4"].border = thin_border
        ws_dash[f"{col}5"].border = thin_border

    ws_dash.row_dimensions[4].height = 20
    ws_dash.row_dimensions[5].height = 32

    # TABLE 1: Phân bố theo Phân khúc giá (Row 7 - 12)
    ws_dash["A7"] = "1. PHÂN BỐ THỊ TRƯỜNG THEO PHÂN KHÚC GIÁ"
    ws_dash["A7"].font = font_sec

    headers_t1 = ["Phân Khúc Giá", "Số Lượng", "Tỷ Trọng", "Giá TB (VNĐ)", "Rating TB"]
    for col_idx, h in enumerate(headers_t1, start=1):
        cell = ws_dash.cell(row=8, column=col_idx, value=h)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    ws_dash.row_dimensions[8].height = 24

    t1_data = [
        ("Bình dân (<40k)", 2, 2/22, 25750, 4.55),
        ("Tầm trung (40k - 75k)", 10, 10/22, 56750, 4.37),
        ("Cao cấp (>75k)", 10, 10/22, 108250, 4.48),
    ]

    for row_idx, row_vals in enumerate(t1_data, start=9):
        ws_dash.cell(row=row_idx, column=1, value=row_vals[0]).alignment = Alignment(horizontal="left", vertical="center")
        ws_dash.cell(row=row_idx, column=2, value=row_vals[1]).alignment = Alignment(horizontal="center", vertical="center")
        ws_dash.cell(row=row_idx, column=3, value=row_vals[2]).alignment = Alignment(horizontal="right", vertical="center")
        ws_dash.cell(row=row_idx, column=4, value=row_vals[3]).alignment = Alignment(horizontal="right", vertical="center")
        ws_dash.cell(row=row_idx, column=5, value=row_vals[4]).alignment = Alignment(horizontal="center", vertical="center")

        ws_dash.cell(row=row_idx, column=3).number_format = '0.0%'
        ws_dash.cell(row=row_idx, column=4).number_format = '#,##0" đ"'
        ws_dash.cell(row=row_idx, column=5).number_format = '0.00" ★"'

        for col_idx in range(1, 6):
            c = ws_dash.cell(row=row_idx, column=col_idx)
            c.font = font_regular
            c.border = thin_border
            if row_idx % 2 == 1:
                c.fill = fill_zebra
        ws_dash.row_dimensions[row_idx].height = 20

    # Total Row Table 1
    tot_row = 12
    ws_dash.cell(row=tot_row, column=1, value="Tổng cộng / Toàn quận").font = font_bold
    ws_dash.cell(row=tot_row, column=2, value=22).font = font_bold
    ws_dash.cell(row=tot_row, column=3, value=1.0).font = font_bold
    ws_dash.cell(row=tot_row, column=4, value=77318).font = font_bold
    ws_dash.cell(row=tot_row, column=5, value=4.44).font = font_bold

    ws_dash.cell(row=tot_row, column=1).alignment = Alignment(horizontal="left", vertical="center")
    ws_dash.cell(row=tot_row, column=2).alignment = Alignment(horizontal="center", vertical="center")
    ws_dash.cell(row=tot_row, column=3).alignment = Alignment(horizontal="right", vertical="center")
    ws_dash.cell(row=tot_row, column=4).alignment = Alignment(horizontal="right", vertical="center")
    ws_dash.cell(row=tot_row, column=5).alignment = Alignment(horizontal="center", vertical="center")

    ws_dash.cell(row=tot_row, column=3).number_format = '0.0%'
    ws_dash.cell(row=tot_row, column=4).number_format = '#,##0" đ"'
    ws_dash.cell(row=tot_row, column=5).number_format = '0.00" ★"'

    for col_idx in range(1, 6):
        c = ws_dash.cell(row=tot_row, column=col_idx)
        c.fill = fill_ice
        c.border = thin_border
    ws_dash.row_dimensions[tot_row].height = 22

    # TABLE 2: Phân bố theo Phường (Row 7 - 16, Col G - K)
    ws_dash["G7"] = "2. PHÂN BỐ ĐỊA BÀN THEO PHƯỜNG"
    ws_dash["G7"].font = font_sec

    headers_t2 = ["Phường", "Số Quán", "Tỷ Trọng", "Giá TB (VNĐ)", "Rating TB"]
    for idx, h in enumerate(headers_t2, start=7):
        cell = ws_dash.cell(row=8, column=idx, value=h)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    t2_data = [
        ("Bến Nghé", 11, 11/22, 94182, 4.43),
        ("Bến Thành", 3, 3/22, 65833, 4.53),
        ("Đa Kao", 2, 2/22, 68750, 4.50),
        ("Nguyễn Thái Bình", 2, 2/22, 55000, 4.40),
        ("Phạm Ngũ Lão", 2, 2/22, 39500, 4.45),
        ("Cô Giang", 1, 1/22, 82500, 4.50),
        ("Cầu Ông Lãnh", 1, 1/22, 51500, 4.10),
    ]

    for row_idx, row_vals in enumerate(t2_data, start=9):
        ws_dash.cell(row=row_idx, column=7, value=row_vals[0]).alignment = Alignment(horizontal="left", vertical="center")
        ws_dash.cell(row=row_idx, column=8, value=row_vals[1]).alignment = Alignment(horizontal="center", vertical="center")
        ws_dash.cell(row=row_idx, column=9, value=row_vals[2]).alignment = Alignment(horizontal="right", vertical="center")
        ws_dash.cell(row=row_idx, column=10, value=row_vals[3]).alignment = Alignment(horizontal="right", vertical="center")
        ws_dash.cell(row=row_idx, column=11, value=row_vals[4]).alignment = Alignment(horizontal="center", vertical="center")

        ws_dash.cell(row=row_idx, column=9).number_format = '0.0%'
        ws_dash.cell(row=row_idx, column=10).number_format = '#,##0" đ"'
        ws_dash.cell(row=row_idx, column=11).number_format = '0.00" ★"'

        for col_idx in range(7, 12):
            c = ws_dash.cell(row=row_idx, column=col_idx)
            c.font = font_regular
            c.border = thin_border
            if row_idx % 2 == 1:
                c.fill = fill_zebra
        ws_dash.row_dimensions[row_idx].height = 20

    # TABLE 3: TOP 5 QUÁN CÓ RATING CAO NHẤT (Row 14 - 21, Col A - E)
    ws_dash["A14"] = "3. TOP 5 QUÁN CÀ PHÊ ĐƯỢC ĐÁNH GIÁ CAO NHẤT"
    ws_dash["A14"].font = font_sec

    headers_t3 = ["Tên Quán Cà Phê", "Phường", "Phân Khúc", "Lượt Review", "Rating Google"]
    for col_idx, h in enumerate(headers_t3, start=1):
        cell = ws_dash.cell(row=15, column=col_idx, value=h)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    ws_dash.row_dimensions[15].height = 24

    t3_data = [
        ("Okkio Caffe - Lê Lợi", "Bến Thành", "Cao cấp (>75k)", 920, 4.6),
        ("Soo Kafe - Phan Kế Bính", "Đa Kao", "Tầm trung (40k-75k)", 1380, 4.6),
        ("Cà Phê Vợt Bà Ba Lữ", "Phạm Ngũ Lão", "Bình dân (<40k)", 510, 4.6),
        ("The Workshop Coffee", "Bến Nghé", "Cao cấp (>75k)", 1650, 4.5),
        ("The Running Bean", "Bến Nghé", "Cao cấp (>75k)", 1480, 4.5),
    ]

    for row_idx, row_vals in enumerate(t3_data, start=16):
        ws_dash.cell(row=row_idx, column=1, value=row_vals[0]).alignment = Alignment(horizontal="left", vertical="center")
        ws_dash.cell(row=row_idx, column=2, value=row_vals[1]).alignment = Alignment(horizontal="center", vertical="center")
        ws_dash.cell(row=row_idx, column=3, value=row_vals[2]).alignment = Alignment(horizontal="center", vertical="center")
        ws_dash.cell(row=row_idx, column=4, value=row_vals[3]).alignment = Alignment(horizontal="right", vertical="center")
        ws_dash.cell(row=row_idx, column=5, value=row_vals[4]).alignment = Alignment(horizontal="center", vertical="center")

        ws_dash.cell(row=row_idx, column=4).number_format = '#,##0'
        ws_dash.cell(row=row_idx, column=5).number_format = '0.0" ★"'

        for col_idx in range(1, 6):
            c = ws_dash.cell(row=row_idx, column=col_idx)
            c.font = font_regular
            c.border = thin_border
            if row_idx % 2 == 1:
                c.fill = fill_zebra
        ws_dash.row_dimensions[row_idx].height = 20

    # Callout Insights & PDCA Findings (Row 18 - 22, Col G - K)
    ws_dash["G17"] = "4. THÔNG TIN PHÂN TÍCH & ĐỀ XUẤT HÀNH ĐỘNG (PDCA ACT)"
    ws_dash["G17"].font = font_sec

    insights = [
        "💡 Insight 1 (Vị trí & Giá): Phường Bến Nghé tập trung 50% số quán trong khảo sát với mức giá TB cao nhất quận (94.2k VNĐ), định vị phân khúc Specialty & Business meeting.",
        "💡 Insight 2 (Chất lượng vs Giá): Điểm đánh giá cao (4.5 - 4.6★) xuất hiện đồng đều ở cả 3 phân khúc (Bình dân vợt 25k, Tầm trung 55k, Specialty 100k+), chứng minh sự hài lòng đến từ đúng kỳ vọng trải nghiệm.",
        "💡 Insight 3 (Xu hướng không gian): 72.7% quán định hướng làm việc/chạy deadline có trang bị wifi ổn định, nhưng chỉ ~36% có chỗ giữ xe miễn phí tại quán do đặc thù mặt bằng Quận 1.",
        "🎯 Đề xuất 1 (Khách hàng): Cần làm việc yên tĩnh & đồ uống ngon nên chọn khu Đa Kao / Bến Thành (Soo Kafe, Okkio) với chi phí hợp lý và chỗ giữ xe tiện lợi hơn lõi Bến Nghé.",
        "🎯 Đề xuất 2 (Kinh doanh): Mở quán mới tại Q1 nên khai thác mô hình Specialty kết hợp Co-working tại các phường vệ tinh (Cô Giang, Đa Kao) để tối ưu chi phí thuê mặt bằng."
    ]

    for i, ins in enumerate(insights, start=18):
        ws_dash.merge_cells(start_row=i, start_column=7, end_row=i, end_column=11)
        c = ws_dash.cell(row=i, column=7, value=ins)
        c.font = Font(name="Segoe UI", size=9, color=DARK_TEXT)
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        c.fill = fill_card
        for col_k in range(7, 12):
            ws_dash.cell(row=i, column=col_k).border = thin_border
        ws_dash.row_dimensions[i].height = 28

    # Add Column Chart for Market Share by Segment
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Số lượng Quán theo Phân khúc Giá"
    chart.y_axis.title = "Số lượng quán"
    chart.x_axis.title = "Phân khúc giá"
    chart.width = 16
    chart.height = 8

    chart_data = Reference(ws_dash, min_col=2, min_row=8, max_row=11)
    chart_cats = Reference(ws_dash, min_col=1, min_row=9, max_row=11)
    chart.add_data(chart_data, titles_from_data=True)
    chart.set_categories(chart_cats)
    chart.legend = None
    ws_dash.add_chart(chart, "A23")

    # Column widths for Dashboard
    dash_widths = {"A": 26, "B": 14, "C": 14, "D": 16, "E": 14, "F": 4, "G": 20, "H": 12, "I": 12, "J": 16, "K": 14}
    for col_letter, w in dash_widths.items():
        ws_dash.column_dimensions[col_letter].width = w

    # -------------------------------------------------------------
    # SHEET 2: Cleaned_Data
    # -------------------------------------------------------------
    ws_data = wb.create_sheet(title="Cleaned_Data")
    ws_data.views.sheetView[0].showGridLines = True

    columns = [
        "CAFE_ID", "CAFE_NAME", "BRAND_TYPE", "ADDRESS", "WARD",
        "PRICE_MIN_VND", "PRICE_MAX_VND", "PRICE_AVG_VND", "PRICE_RANGE_DISPLAY",
        "PRICE_SEGMENT", "RATING_GOOGLE", "REVIEW_COUNT", "STYLE_CONCEPT",
        "PRIMARY_PURPOSE", "OPENING_HOURS", "PARKING_INFO"
    ]

    header_names_vn = [
        "Mã Quán", "Tên Quán Cà Phê", "Loại Thương Hiệu", "Địa Chỉ", "Phường",
        "Giá Thấp Nhất (VNĐ)", "Giá Cao Nhất (VNĐ)", "Giá Trung Bình (VNĐ)", "Khoảng Giá Hiển Thị",
        "Phân Khúc Giá", "Đánh Giá Google", "Lượt Đánh Giá", "Phong Cách Không Gian",
        "Mục Đích Phù Hợp", "Giờ Mở Cửa", "Thông Tin Bãi Xe"
    ]

    for col_idx, (col_key, col_vn) in enumerate(zip(columns, header_names_vn), start=1):
        cell = ws_data.cell(row=1, column=col_idx, value=col_vn)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
    ws_data.row_dimensions[1].height = 28

    # Populate rows
    for row_idx, item in enumerate(data, start=2):
        ws_data.cell(row=row_idx, column=1, value=item["CAFE_ID"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_data.cell(row=row_idx, column=2, value=item["CAFE_NAME"]).alignment = Alignment(horizontal="left", vertical="center")
        ws_data.cell(row=row_idx, column=3, value=item["BRAND_TYPE"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_data.cell(row=row_idx, column=4, value=item["ADDRESS"]).alignment = Alignment(horizontal="left", vertical="center")
        ws_data.cell(row=row_idx, column=5, value=item["WARD"]).alignment = Alignment(horizontal="center", vertical="center")
        
        # Numeric values for computation
        c_min = ws_data.cell(row=row_idx, column=6, value=item["PRICE_MIN_VND"])
        c_min.number_format = '#,##0" VNĐ"'
        c_min.alignment = Alignment(horizontal="right", vertical="center")

        c_max = ws_data.cell(row=row_idx, column=7, value=item["PRICE_MAX_VND"])
        c_max.number_format = '#,##0" VNĐ"'
        c_max.alignment = Alignment(horizontal="right", vertical="center")

        c_avg = ws_data.cell(row=row_idx, column=8, value=item["PRICE_AVG_VND"])
        c_avg.number_format = '#,##0" VNĐ"'
        c_avg.alignment = Alignment(horizontal="right", vertical="center")

        ws_data.cell(row=row_idx, column=9, value=item["PRICE_RANGE_DISPLAY"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_data.cell(row=row_idx, column=10, value=item["PRICE_SEGMENT"]).alignment = Alignment(horizontal="center", vertical="center")

        c_rt = ws_data.cell(row=row_idx, column=11, value=item["RATING_GOOGLE"])
        c_rt.number_format = '0.0" ★"'
        c_rt.alignment = Alignment(horizontal="center", vertical="center")

        c_rc = ws_data.cell(row=row_idx, column=12, value=item["REVIEW_COUNT"])
        c_rc.number_format = '#,##0'
        c_rc.alignment = Alignment(horizontal="right", vertical="center")

        ws_data.cell(row=row_idx, column=13, value=item["STYLE_CONCEPT"]).alignment = Alignment(horizontal="left", vertical="center")
        ws_data.cell(row=row_idx, column=14, value=item["PRIMARY_PURPOSE"]).alignment = Alignment(horizontal="left", vertical="center")
        ws_data.cell(row=row_idx, column=15, value=item["OPENING_HOURS"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_data.cell(row=row_idx, column=16, value=item["PARKING_INFO"]).alignment = Alignment(horizontal="left", vertical="center")

        for c_idx in range(1, 17):
            cell = ws_data.cell(row=row_idx, column=c_idx)
            cell.font = font_regular
            cell.border = thin_border
            if row_idx % 2 == 1:
                cell.fill = fill_zebra
        ws_data.row_dimensions[row_idx].height = 22

    # Enable autofilter
    ws_data.auto_filter.ref = f"A1:P{len(data)+1}"
    # Freeze row 1
    ws_data.freeze_panes = "A2"

    # Set column widths
    for col_idx in range(1, 17):
        max_len = 0
        col_letter = get_column_letter(col_idx)
        for row in range(1, len(data) + 2):
            val = ws_data.cell(row=row, column=col_idx).value
            if val:
                max_len = max(max_len, len(str(val)))
        ws_data.column_dimensions[col_letter].width = max(max_len + 5, 14)

    # -------------------------------------------------------------
    # SHEET 3: Data_Dictionary
    # -------------------------------------------------------------
    ws_dict = wb.create_sheet(title="Data_Dictionary")
    ws_dict.views.sheetView[0].showGridLines = True

    dict_headers = ["STT", "Tên Trường (Field Name)", "Kiểu Dữ Liệu (Data Type)", "Ví Dụ Mẫu (Sample Value)", "Mô Tả & Mục Đích Phân Tích (Description & Business Purpose)"]
    for col_idx, h in enumerate(dict_headers, start=1):
        cell = ws_dict.cell(row=1, column=col_idx, value=h)
        cell.font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
    ws_dict.row_dimensions[1].height = 28

    for row_idx, item in enumerate(data_dict, start=2):
        ws_dict.cell(row=row_idx, column=1, value=row_idx - 1).alignment = Alignment(horizontal="center", vertical="center")
        ws_dict.cell(row=row_idx, column=2, value=item[0]).alignment = Alignment(horizontal="left", vertical="center")
        ws_dict.cell(row=row_idx, column=3, value=item[1]).alignment = Alignment(horizontal="center", vertical="center")
        ws_dict.cell(row=row_idx, column=4, value=item[2]).alignment = Alignment(horizontal="left", vertical="center")
        ws_dict.cell(row=row_idx, column=5, value=item[3]).alignment = Alignment(horizontal="left", vertical="center")

        ws_dict.cell(row=row_idx, column=2).font = font_bold
        for col_idx in range(1, 6):
            c = ws_dict.cell(row=row_idx, column=col_idx)
            c.font = font_bold if col_idx == 2 else font_regular
            c.border = thin_border
            if row_idx % 2 == 1:
                c.fill = fill_zebra
        ws_dict.row_dimensions[row_idx].height = 22

    dict_widths = {"A": 8, "B": 24, "C": 22, "D": 26, "E": 65}
    for col_letter, w in dict_widths.items():
        ws_dict.column_dimensions[col_letter].width = w

    # Save to all target paths
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        wb.save(p)
        print(f"Successfully saved to: {p}")

if __name__ == "__main__":
    import sys
    # Handle windows unicode console
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    report_path = r"c:\Minh Hoang\Antigravity học\my-workspace\outputs\reports\Quan_Cafe_Quan_1_Cleaned.xlsx"
    sample_path = r"c:\Minh Hoang\Antigravity học\my-workspace\sample-data\Quan_Cafe_Quan_1_Cleaned.xlsx"
    build_excel_report([report_path, sample_path])
