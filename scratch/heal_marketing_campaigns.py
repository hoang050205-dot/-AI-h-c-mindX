import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

EXCHANGE_RATE_USD_VND = 25000
ANCHOR_DATE = datetime(2026, 9, 30)  # Thứ Tư, 30/09/2026

INPUT_PATH = os.path.join(r"c:\Minh Hoang\Antigravity học\my-workspace", "sample-data", "marketing_campaigns.xlsx")
OUTPUT_PATH = os.path.join(r"c:\Minh Hoang\Antigravity học\my-workspace", "sample-data", "marketing_campaigns_healed.xlsx")

def decode_natural_date(val, anchor=ANCHOR_DATE):
    """Quy tắc 3: Giải mã ngày tự nhiên sang YYYY-MM-DD"""
    if pd.isna(val):
        return val
    s = str(val).strip()
    
    # 1. 'Tháng sau' = Ngày 1 tháng kế tiếp
    if "tháng sau" in s.lower():
        year = anchor.year + (1 if anchor.month == 12 else 0)
        month = 1 if anchor.month == 12 else anchor.month + 1
        return f"{year:04d}-{month:02d}-01"
    
    # 2. 'Tuần tới' / 'Đầu tuần sau' = Thứ Hai tuần sau
    if "tuần tới" in s.lower() or "đầu tuần sau" in s.lower():
        days_ahead = 7 - anchor.weekday()  # Monday is 0, Wednesday is 2 -> 7 - 2 = 5 days -> 2026-10-05
        next_monday = anchor + timedelta(days=days_ahead)
        return next_monday.strftime("%Y-%m-%d")
        
    # 3. Các từ ngữ mở rộng
    if "sau lễ" in s.lower():
        return "2026-09-03"
    if "q3" in s.lower() or "cuối q3" in s.lower():
        return "2026-09-30"
    if "sau tết" in s.lower():
        return "2026-02-23"
    if "giữa tháng" in s.lower():
        return f"{anchor.year:04d}-{anchor.month:02d}-15"
    if "hết mùa hè" in s.lower():
        return "2026-08-31"
        
    return s

def run_healing():
    print(f"Reading input from: {INPUT_PATH}")
    df = pd.read_excel(INPUT_PATH, sheet_name="Marketing_Campaigns")
    initial_shape = df.shape
    print(f"Loaded {initial_shape[0]} rows and {initial_shape[1]} columns.")
    
    # Track statistics
    stats = {
        "usd_converted": 0,
        "default_currency_filled": 0,
        "active_to_paused": 0,
        "natural_dates_decoded": 0,
        "outliers_flagged": 0
    }
    
    # --- QUY TẮC 1: TIỀN TỆ ---
    # Đếm số dòng thiếu đơn vị
    missing_currency_mask = df['Currency'].isna() | (df['Currency'].astype(str).str.strip() == '')
    stats['default_currency_filled'] = int(missing_currency_mask.sum())
    df['Currency'] = df['Currency'].fillna('VND').astype(str).str.strip()
    df.loc[df['Currency'] == '', 'Currency'] = 'VND'
    
    # Đếm và quy đổi USD sang VND
    usd_mask = df['Currency'].str.upper() == 'USD'
    stats['usd_converted'] = int(usd_mask.sum())
    df.loc[usd_mask, 'Budget'] = df.loc[usd_mask, 'Budget'] * EXCHANGE_RATE_USD_VND
    df.loc[usd_mask, 'Actual_Spend'] = df.loc[usd_mask, 'Actual_Spend'] * EXCHANGE_RATE_USD_VND
    df.loc[usd_mask, 'Currency'] = 'VND'
    
    df['Budget'] = pd.to_numeric(df['Budget'], errors='coerce').fillna(0).astype('int64')
    df['Actual_Spend'] = pd.to_numeric(df['Actual_Spend'], errors='coerce').fillna(0).astype('int64')
    
    # --- QUY TẮC 2: LOGIC NGÂN SÁCH ---
    healing_notes = []
    for idx, row in df.iterrows():
        notes = []
        # Active + ngân sách/spend = 0 -> đổi sang Paused + ghi cảnh báo
        if row['Status'] == 'Active' and (row['Budget'] == 0 or row['Actual_Spend'] == 0):
            df.at[idx, 'Status'] = 'Paused'
            notes.append("ĐỔI PAUSED: Chi tiêu = 0 khi đang Active (kiểm tra tracking/giải ngân)")
            stats['active_to_paused'] += 1
            
        # Cảnh báo outlier > 1 tỷ VND
        if row['Budget'] > 1_000_000_000:
            notes.append(f"CẢNH BÁO OUTLIER: Budget > 1 tỷ VND ({row['Budget']:,} VND)")
            stats['outliers_flagged'] += 1
            
        healing_notes.append(" | ".join(notes) if notes else "Hợp lệ")
        
    df['Audit_Healing_Notes'] = healing_notes
    
    # --- QUY TẮC 3: GIẢI MÃ LỊCH TRÌNH ---
    for col in ['Start_Date', 'End_Date']:
        for idx, val in df[col].items():
            decoded = decode_natural_date(val)
            if decoded != str(val).strip():
                stats['natural_dates_decoded'] += 1
                df.at[idx, col] = decoded
                
    # Save healed file
    with pd.ExcelWriter(OUTPUT_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Healed_Campaigns", index=False)
        
    print("\n=== KẾT QUẢ CHỮA LÀNH DỮ LIỆU THỰC TẾ ===")
    print(f"1. Số dòng USD quy đổi sang VND (x25k): {stats['usd_converted']} dòng")
    print(f"2. Số dòng thiếu Currency tự động gán VND: {stats['default_currency_filled']} dòng")
    print(f"3. Số dòng Active chi tiêu 0 đổi sang Paused: {stats['active_to_paused']} dòng")
    print(f"4. Số trường ngày tự nhiên đã giải mã ISO: {stats['natural_dates_decoded']} trường")
    print(f"5. Số chiến dịch Budget > 1 tỷ VND gắn cảnh báo: {stats['outliers_flagged']} dòng")
    print(f"\nĐã xuất bản file chữa lành: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_healing()
