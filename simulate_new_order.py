#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Công cụ Giả lập Phát sinh Đơn hàng Mới (Simulate Realtime Order)
Công ty TNHH Alpha
Chức năng:
  - Thêm một giao dịch ngẫu nhiên vào file sales_data.xlsx
  - Giúp kiểm chứng tính năng Polling 2 giây và Hiệu ứng số nhảy 60fps trên Dashboard
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import os
import random
from datetime import datetime
import pandas as pd

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_data.xlsx")

def simulate_new_order():
    if not os.path.exists(FILE_PATH):
        print(f"LỖI: Không tìm thấy file {FILE_PATH}")
        return

    df = pd.read_excel(FILE_PATH)
    next_id_num = len(df) + 1
    order_id = f"ORD{next_id_num:04d}"

    categories = [
        {"danh_muc": "Thuc Pham", "ten_sp": "San Pham Thuc Pham Cao Cap", "ma_sp": "SP888", "don_gia": 25000000},
        {"danh_muc": "Dien Tu", "ten_sp": "Thiet Bi Thong Minh Alpha", "ma_sp": "SP999", "don_gia": 35000000},
        {"danh_muc": "Thoi Trang", "ten_sp": "Bo Su Tap Cong So Alpha Luxury", "ma_sp": "SP777", "don_gia": 18000000},
        {"danh_muc": "Gia Dung", "ten_sp": "Gia Dung Tien Ich Premium", "ma_sp": "SP666", "don_gia": 15000000}
    ]
    chosen = random.choice(categories)
    qty = random.randint(10, 40)
    revenue = qty * chosen["don_gia"]
    discount = int(revenue * 0.05)
    net_revenue = revenue - discount
    cost_goods = int(revenue * 0.52)
    ship_fee = random.choice([200000, 300000, 500000])
    total_cost = cost_goods + ship_fee
    profit = net_revenue - total_cost

    new_row = {
        "Ma_Don_Hang": order_id,
        "Ngay_Giao_Dich": datetime.now().strftime("%Y-%m-%d"),
        "Thang": datetime.now().strftime("%Y-%m"),
        "Nam": datetime.now().year,
        "Khu_Vuc": random.choice(["Mien Nam", "Mien Trung", "Mien Bac"]),
        "Tinh_Thanh": random.choice(["TP. Ho Chi Minh", "Ha Noi", "Da Nang", "Can Tho"]),
        "Ten_Khach_Hang": f"Khach Hang VIP {next_id_num}",
        "Nhom_Khach_Hang": random.choice(["B2B", "B2C"]),
        "Danh_Muc_San_Pham": chosen["danh_muc"],
        "Ma_San_Pham": chosen["ma_sp"],
        "Ten_San_Pham": chosen["ten_sp"],
        "So_Luong": qty,
        "Don_Gia": chosen["don_gia"],
        "Doanh_Thu": revenue,
        "Chiet_Khau": discount,
        "Doanh_Thu_Thuan": net_revenue,
        "Chi_Phi_Gia_Von": cost_goods,
        "Chi_Phi_Van_Chuyen": ship_fee,
        "Tong_Chi_Phi": total_cost,
        "Loi_Nhuan": profit
    }

    df_updated = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df_updated.to_excel(FILE_PATH, index=False)

    print("=" * 60)
    print(f"✅ ĐÃ PHÁT SINH THÀNH CÔNG ĐƠN HÀNG MỚI: {order_id}")
    print(f"📦 Sản phẩm: {chosen['ten_sp']} ({chosen['danh_muc']}) x {qty}")
    print(f"💰 Doanh thu thuần: +{net_revenue:,} ₫")
    print(f"📉 Chi phí:         +{total_cost:,} ₫")
    print(f"📈 Lợi nhuận ròng:  +{profit:,} ₫")
    print(f"📊 Tổng số đơn hiện tại trong Excel: {len(df_updated)}")
    print("=" * 60)
    print("👉 Hãy quan sát Web Dashboard tại http://localhost:9090")
    print("   Các con số và biểu đồ sẽ tự động nhảy số sau 2 giây!")

if __name__ == "__main__":
    simulate_new_order()
