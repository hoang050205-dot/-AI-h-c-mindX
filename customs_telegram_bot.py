# -*- coding: utf-8 -*-
"""
========================================================================================
CUSTOMS LEGAL TELEGRAM COPILOT (customs_telegram_bot.py) — v2.5 Multi-Doc Digest Edition
========================================================================================
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / AI4A Antigravity
Cải tiến trọng tâm:
  1. Hỗ trợ CẬP NHẬT TẤT CẢ CÁC VĂN BẢN LIÊN QUAN (Luật, Nghị định, Thông tư, Quyết định,
     Hiệp định FTA, Công văn quy phạm...) chứ không chỉ giới hạn ở 1 văn bản riêng lẻ.
  2. Tối ưu hóa Bản tin Tổng hợp (Digest Batching): Lược bỏ khối nội dung tóm tắt dài dòng
     (bỏ nội dung trọng tâm cồng kềnh) để gom 5-10+ văn bản vào danh mục tinh gọn, súc tích.
  3. Gom cụm cảnh báo mốc hiệu lực HÔM NAY (T-0) và NGÀY MAI (T-1) thành bảng tổng hợp gọn gàng.
  4. Thu thập đa nguồn: Google News RSS chuyên sâu + CSDL Pháp lý nội bộ (Registry & FTS5).
  5. Tự động hóa khi MỞ MÁY TÍNH (On-Logon), kiểm soát chặt chẽ chống gửi lặp trong ngày.
  6. Bảo mật 100% qua file .env (CUSTOMS_TELEGRAM_BOT_TOKEN / TELEGRAM_BOT_TOKEN).
========================================================================================
"""

import os
import sys
import json
import re
import html
import sqlite3
import argparse
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv

# UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent
ENV_PATH = WORKSPACE_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

CACHE_DIR = WORKSPACE_ROOT / "knowledge-base" / "legal-assets"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
SENT_ALERTS_FILE = CACHE_DIR / "sent_legal_alerts.json"
DAILY_RUN_FILE = CACHE_DIR / "last_daily_run.json"
REGISTRY_FILE = CACHE_DIR / "legal_assets_registry.json"
DB_PATH = CACHE_DIR / "customs_legal_index.sqlite"

# Cấu hình Token (Ưu tiên CUSTOMS_BOT, fallback về BOT chung nếu chưa cấu hình)
BOT_TOKEN = os.getenv("CUSTOMS_TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("CUSTOMS_TELEGRAM_CHAT_ID") or os.getenv("TELEGRAM_CHAT_ID", "")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def load_sent_cache():
    if SENT_ALERTS_FILE.exists():
        try:
            with open(SENT_ALERTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"sent_doc_numbers": [], "last_updated": ""}
    return {"sent_doc_numbers": [], "last_updated": ""}

def save_sent_cache(cache):
    cache["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SENT_ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def check_already_run_today():
    """Kiểm tra xem bot đã thực hiện lần quét trong ngày hôm nay chưa"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if DAILY_RUN_FILE.exists():
        try:
            with open(DAILY_RUN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("last_run_date") == today_str:
                    return True, data.get("last_run_time", "")
        except Exception:
            pass
    return False, ""

def mark_run_today():
    """Ghi nhận ngày chạy hôm nay"""
    now = datetime.now()
    data = {
        "last_run_date": now.strftime("%Y-%m-%d"),
        "last_run_time": now.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(DAILY_RUN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def send_telegram_message(text, reply_markup=None):
    """Gửi tin nhắn Telegram chuẩn định dạng HTML"""
    if not BOT_TOKEN or not CHAT_ID:
        print("[CẢNH BÁO] Chưa cấu hình CUSTOMS_TELEGRAM_BOT_TOKEN hoặc CUSTOMS_TELEGRAM_CHAT_ID trong .env")
        print(f"Nội dung dự kiến gửi:\n{text}")
        return False

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    try:
        resp = requests.post(TELEGRAM_API_URL, json=payload, timeout=15)
        if resp.status_code == 200:
            return True
        else:
            print(f"[LỖI TELEGRAM] Status {resp.status_code}: {resp.text}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"[LỖI KẾT NỐI TELEGRAM] {e}", file=sys.stderr)
        return False

def get_tracked_documents_from_db():
    """Lấy danh sách toàn bộ văn bản và ngày hiệu lực từ CSDL pháp lý nội bộ"""
    docs = []
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for d in data.get("documents", []):
                    docs.append({
                        "doc_number": d.get("doc_number"),
                        "type": d.get("type", "Văn bản"),
                        "title": d.get("title"),
                        "authority": d.get("issuing_authority"),
                        "issue_date": d.get("issue_date"),
                        "effective_date": d.get("effective_date"),
                        "category": d.get("category", "#HaiQuan"),
                        "link": "https://vanban.chinhphu.vn",
                        "status": d.get("status")
                    })
        except Exception as e:
            print(f"[CẢNH BÁO] Không đọc được registry: {e}")
    return docs

def check_effective_dates(target_date=None):
    """
    Kiểm tra danh mục các văn bản:
    1. Hôm nay có hiệu lực (T-0)
    2. Ngày mai bắt đầu có hiệu lực (T-1)
    """
    today = target_date or datetime.now().date()
    tomorrow = today + timedelta(days=1)
    today_str = today.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    docs = get_tracked_documents_from_db()
    today_effective = []
    tomorrow_effective = []

    for d in docs:
        eff_raw = d.get("effective_date", "")
        match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", eff_raw)
        if match:
            y, m, day = match.groups()
            eff_iso = f"{int(y):04d}-{int(m):02d}-{int(day):02d}"
            
            if eff_iso == today_str:
                today_effective.append(d)
            elif eff_iso == tomorrow_str:
                tomorrow_effective.append(d)

    return today_effective, tomorrow_effective

def enrich_legal_document(title, desc="", link=""):
    """
    Phân tích và trích xuất thông tin định danh của văn bản pháp lý XNK:
    - Loại văn bản: Luật, Nghị định, Thông tư, Quyết định, Hiệp định FTA, Công văn...
    - Số hiệu văn bản (Regex)
    - Cơ quan ban hành ước tính
    - Lĩnh vực nghiệp vụ (#ThuếXNK, #ThủTụcHảiQuan, #FTA, #C_O...)
    - Trích yếu súc tích (1 dòng, bỏ râu ria)
    """
    clean_title = re.sub(r"<[^>]+>", "", title).strip()
    # Loại bỏ tên nguồn tin tức ở cuối tiêu đề (VD: - Báo Chính phủ, - VnExpress...)
    if " - " in clean_title:
        clean_title = clean_title.rsplit(" - ", 1)[0].strip()

    full_text = f"{clean_title} {desc}".lower()

    # 1. Nhận diện Số hiệu văn bản
    num_match = re.search(r"\b(\d+/\d{4}/[A-ZĐ-]+|\d+/[A-ZĐ-]+|[A-ZĐ-]+/\d{4})\b", clean_title)
    doc_num = num_match.group(1) if num_match else ""

    # 2. Nhận diện Loại văn bản
    if "luật" in full_text or "quốc hội" in full_text:
        doc_type = "Luật"
    elif "nghị định" in full_text or "/nđ-cp" in full_text:
        doc_type = "Nghị định"
    elif "thông tư" in full_text or "/tt-btc" in full_text or "/tt-bct" in full_text:
        doc_type = "Thông tư"
    elif "quyết định" in full_text or "/qđ-" in full_text:
        doc_type = "Quyết định"
    elif "hiệp định" in full_text or "fta" in full_text:
        doc_type = "Hiệp định FTA"
    elif "công văn" in full_text or "/tchq-" in full_text:
        doc_type = "Công văn"
    elif "nghị quyết" in full_text or "/nq-" in full_text:
        doc_type = "Nghị quyết"
    else:
        doc_type = "Văn bản XNK"

    # Nếu không có số hiệu dạng chuẩn, lấy cụm từ đại diện
    if not doc_num:
        if doc_type == "Hiệp định FTA":
            # Bắt tên FTA nếu có
            fta_match = re.search(r"\b(EVFTA|CPTPP|RCEP|VKFTA|VIFTA|UKVFTA|AANZFTA|ACFTA)\b", clean_title, re.IGNORECASE)
            doc_num = fta_match.group(1).upper() if fta_match else "Hiệp định Mới"
        else:
            doc_num = "Ban hành mới"

    # 3. Nhận diện Cơ quan ban hành
    if "bộ tài chính" in full_text or "btc" in full_text:
        auth = "Bộ Tài chính"
    elif "hải quan" in full_text or "tchq" in full_text:
        auth = "Tổng cục Hải quan"
    elif "bộ công thương" in full_text or "bct" in full_text:
        auth = "Bộ Công Thương"
    elif "nông nghiệp" in full_text or "nn&ptnt" in full_text:
        auth = "Bộ NN&PTNT"
    elif "quốc hội" in full_text:
        auth = "Quốc hội"
    elif "thủ tướng" in full_text or "ttg" in full_text:
        auth = "Thủ tướng Chính phủ"
    elif "chính phủ" in full_text or "nđ-cp" in full_text:
        auth = "Chính phủ"
    else:
        auth = "Cơ quan Nhà nước"

    # 4. Nhận diện Lĩnh vực nghiệp vụ
    tags = []
    if any(k in full_text for k in ["thuế", "gtgt", "vat", "thuế xnk", "biểu thuế"]):
        tags.append("#ThuếXNK")
    if any(k in full_text for k in ["thủ tục", "hồ sơ", "khai báo", "vnaccs", "luồng"]):
        tags.append("#ThủTụcHảiQuan")
    if any(k in full_text for k in ["xuất xứ", "c/o", "co form", "nguồn gốc"]):
        tags.append("#XuấtXứCO")
    if any(k in full_text for k in ["giấy phép", "chuyên ngành", "kiểm dịch", "đăng kiểm"]):
        tags.append("#QuảnLýChuyênNgành")
    if any(k in full_text for k in ["fta", "hiệp định", "ưu đãi", "đối tác"]):
        tags.append("#HiệpĐịnhFTA")
    if not tags:
        tags.append("#ChínhSáchXNK")

    category = " ".join(tags)

    return {
        "doc_number": doc_num,
        "type": doc_type,
        "title": clean_title,
        "authority": auth,
        "category": category,
        "link": link or "https://vanban.chinhphu.vn",
        "effective_date": "Xem chi tiết tại văn bản gốc"
    }

def format_effective_date_digest(docs, alert_type="T-0"):
    """
    Định dạng Danh mục Tổng hợp Văn bản có hiệu lực (T-0 hoặc T-1)
    - Loại bỏ nội dung trọng tâm dài dòng để gom nhiều văn bản vào 1 tin gọn gàng.
    - Hiển thị theo danh sách số học trực quan (1️⃣, 2️⃣, 3️⃣...).
    """
    now = datetime.now()
    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    if alert_type == "T-0":
        header_title = "🔔 <b>DANH MỤC VĂN BẢN XNK CÓ HIỆU LỰC HÔM NAY (T-0)</b> 🔔"
        date_str = now.strftime("%d/%m/%Y")
        sub_title = f"📅 <b>Áp dụng chính thức từ hôm nay: {date_str}</b>\n<i>Tổng hợp {len(docs)} văn bản bắt đầu có hiệu lực thi hành:</i>"
        note = "⚠️ <b>LƯU Ý DOANH NGHIỆP:</b>\n• Yêu cầu bộ phận Chứng từ & Khai báo rà soát ngay trước khi truyền tờ khai VNACCS!"
    else:
        header_title = "⏳ <b>DANH MỤC VĂN BẢN XNK CÓ HIỆU LỰC NGÀY MAI (T-1)</b> ⏳"
        date_str = (now + timedelta(days=1)).strftime("%d/%m/%Y")
        sub_title = f"📅 <b>Mốc áp dụng: Ngày mai ({date_str})</b>\n<i>Chuẩn bị áp dụng {len(docs)} văn bản từ ngày mai:</i>"
        note = "💡 <b>VIỆC CẦN LÀM HÔM NAY:</b>\n• Rà soát các lô hàng dự kiến truyền tờ khai vào ngày mai để áp dụng đúng quy định!"

    lines = [
        header_title,
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        sub_title,
        ""
    ]

    for idx, d in enumerate(docs):
        icon = num_emojis[idx] if idx < len(num_emojis) else f"[{idx+1}]"
        doc_type = html.escape(d.get("type", "Văn bản"))
        doc_num = html.escape(d.get("doc_number", "Số hiệu"))
        auth = html.escape(d.get("authority", "Cơ quan"))
        title = html.escape(d.get("title", ""))
        link = d.get("link", "https://vanban.chinhphu.vn")

        item_str = (
            f"{icon} <b>[{doc_type}] {doc_num}</b> — <i>{auth}</i>\n"
            f"• <b>Trích yếu:</b> {title}\n"
            f"• 🔗 <a href=\"{link}\">Xem toàn văn văn bản gốc</a>\n"
        )
        lines.append(item_str)

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(note)

    return "\n".join(lines)

def format_new_docs_digest(docs_batch, batch_index=1, total_batches=1):
    """
    Định dạng Bản tin Điểm tin Đa Văn bản Mới ban hành (Compact Digest):
    - Đã LƯỢC BỎ nội dung trọng tâm dài dòng theo yêu cầu người dùng.
    - Cập nhật TẤT CẢ các loại văn bản liên quan (Luật, NĐ, TT, QĐ, FTA, CV...).
    - Mỗi văn bản chỉ gồm 3-4 dòng thông tin mấu chốt + link tải văn bản gốc.
    """
    now_str = datetime.now().strftime("%d/%m/%Y")
    batch_suffix = f" (Phần {batch_index}/{total_batches})" if total_batches > 1 else ""
    num_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    lines = [
        f"🚨 <b>ĐIỂM TIN PHÁP LÝ XNK MỚI BAN HÀNH{batch_suffix}</b> 🚨",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📅 <i>Cập nhật: {now_str} • Gồm {len(docs_batch)} văn bản liên quan</i>\n"
    ]

    for idx, d in enumerate(docs_batch):
        icon = num_emojis[idx] if idx < len(num_emojis) else f"[{idx+1}]"
        doc_type = html.escape(d.get("type", "Văn bản"))
        doc_num = html.escape(d.get("doc_number", "Ban hành mới"))
        auth = html.escape(d.get("authority", "Cơ quan ban hành"))
        title = html.escape(d.get("title", ""))
        eff_date = html.escape(d.get("effective_date", "Xem tại văn bản gốc"))
        category = html.escape(d.get("category", "#ChínhSáchXNK"))
        link = d.get("link", "https://vanban.chinhphu.vn")

        item_str = (
            f"{icon} <b>[{doc_type}] {doc_num}</b> — <i>{auth}</i>\n"
            f"• <b>Trích yếu:</b> {title}\n"
            f"• <b>Hiệu lực:</b> <code>{eff_date}</code> • <b>Lĩnh vực:</b> {category}\n"
            f"• 🔗 <a href=\"{link}\">Xem toàn văn văn bản gốc</a>\n"
        )
        lines.append(item_str)

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("💡 <i>Bấm vào liên kết từng văn bản để tra cứu chi tiết toàn văn.</i>")

    return "\n".join(lines)

def fetch_online_customs_news(limit_per_feed=8):
    """
    Quét tự động nguồn tin tức & văn bản mới đa dạng từ Google News RSS Việt Nam.
    Truy vấn đa tầng phủ kín: Luật, Nghị định, Thông tư, Quyết định, Biểu thuế, Hiệp định FTA.
    """
    queries = [
        'hải quan OR xuất nhập khẩu OR "thuế xuất khẩu" OR "thuế nhập khẩu"',
        '"nghị định" OR "thông tư" hải quan OR "biểu thuế"',
        '"hiệp định thương mại" OR "FTA" Việt Nam OR "C/O xuất xứ"'
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    collected = []
    seen_titles = set()

    for q in queries:
        encoded_q = urllib.parse.quote(q)
        feed_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=vi&gl=VN&ceid=VN:vi"
        try:
            resp = requests.get(feed_url, headers=headers, timeout=10)
            if resp.status_code != 200:
                continue

            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:limit_per_feed]:
                title = item.findtext("title", "")
                link = item.findtext("link", "")
                pub_date = item.findtext("pubDate", "")
                desc = item.findtext("description", "")

                # Chuẩn hóa fingerprint để loại bỏ bài trùng
                fingerprint = re.sub(r"[^a-zA-Z0-9\u00C0-\u024F\u1EA0-\u1EF9]", "", title.lower())[:45]
                if not fingerprint or fingerprint in seen_titles:
                    continue
                seen_titles.add(fingerprint)

                enriched = enrich_legal_document(title, desc, link)
                if pub_date:
                    enriched["issue_date"] = pub_date[:16]
                collected.append(enriched)
        except Exception as e:
            # Ghi nhận lỗi nếu mạng gặp sự cố nhưng không ngắt chương trình
            continue

    return collected

def execute_daily_workflow(force=False, dry_run=False):
    """
    Quy trình vận hành buổi sáng khi mở máy (On-Logon):
    1. Kiểm tra trạng thái Tạm dừng / Đã chạy hôm nay.
    2. Cảnh báo T-0 (Hôm nay có hiệu lực) dạng Danh mục tổng hợp.
    3. Cảnh báo T-1 (Ngày mai có hiệu lực) dạng Danh mục tổng hợp.
    4. Quét và gửi Bản tin Đa Văn bản Mới (Digest Batching, không tóm tắt dài dòng).
    5. Đánh dấu mốc chạy duy nhất trong ngày.
    """
    disabled_flag = CACHE_DIR / "bot_disabled.flag"
    if disabled_flag.exists() and not force:
        print("ℹ️ [TẠM DỪNG] Bot đang ở trạng thái Tạm dừng (Disabled). Dùng setup_customs_scheduler.ps1 -Enable để bật lại.")
        return

    already_run, run_time = check_already_run_today()
    if already_run and not force:
        print(f"ℹ️ [BỎ QUA] Hôm nay ({datetime.now().strftime('%d/%m/%Y')}) Bot đã hoàn thành lần quét lúc {run_time}.")
        print("Bot chỉ kích hoạt 1 lần duy nhất trong ngày khi bạn mở máy để tránh làm phiền.")
        print("Nếu muốn chạy lại ngay lập tức, sử dụng cờ: --force")
        return

    print("=" * 70)
    print(f"🚀 KÍCH HOẠT QUY TRÌNH BUỔI SÁNG CUSTOMS LEGAL TELEGRAM BOT (v2.5)")
    print(f"⏰ Thời điểm: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)

    alerts_sent = 0
    sent_cache = load_sent_cache()
    sent_list = sent_cache.get("sent_doc_numbers", [])

    # 1. Cảnh báo Hiệu lực T-0 (Hôm nay)
    t0_docs, t1_docs = check_effective_dates()
    if t0_docs:
        print(f"🔔 Phát hiện {len(t0_docs)} văn bản CHÍNH THỨC CÓ HIỆU LỰC HÔM NAY (T-0)!")
        msg_t0 = format_effective_date_digest(t0_docs, alert_type="T-0")
        if dry_run:
            print(f"[DRY-RUN T-0]:\n{msg_t0}\n")
        else:
            if send_telegram_message(msg_t0):
                alerts_sent += 1
    else:
        print("✓ Không có văn bản nào bắt đầu có hiệu lực vào hôm nay (T-0).")

    # 2. Cảnh báo Hiệu lực T-1 (Ngày mai)
    if t1_docs:
        print(f"⏳ Phát hiện {len(t1_docs)} văn bản SẼ CÓ HIỆU LỰC VÀO NGÀY MAI (T-1)!")
        msg_t1 = format_effective_date_digest(t1_docs, alert_type="T-1")
        if dry_run:
            print(f"[DRY-RUN T-1]:\n{msg_t1}\n")
        else:
            if send_telegram_message(msg_t1):
                alerts_sent += 1
    else:
        print("✓ Không có văn bản nào bắt đầu có hiệu lực vào ngày mai (T-1).")

    # 3. Quét tất cả các văn bản liên quan mới ban hành
    print("📡 Đang quét các văn bản XNK liên quan mới ban hành (Luật, NĐ, TT, QĐ, FTA)...")
    online_docs = fetch_online_customs_news()

    # Lọc bài mới chưa gửi
    unsent_docs = []
    for doc in online_docs:
        doc_key = doc.get("title", "")
        fingerprint = re.sub(r"[^a-zA-Z0-9\u00C0-\u024F\u1EA0-\u1EF9]", "", doc_key.lower())[:45]
        if fingerprint in sent_list:
            continue
        unsent_docs.append((fingerprint, doc))

    if unsent_docs:
        print(f"✓ Tìm thấy {len(unsent_docs)} văn bản pháp lý XNK mới chưa gửi.")
        # Chia thành các batch tối đa 5 văn bản / tin nhắn để đọc thoáng mắt
        batch_size = 5
        batches = [unsent_docs[i:i + batch_size] for i in range(0, len(unsent_docs), batch_size)]
        total_batches = len(batches)

        for b_idx, batch in enumerate(batches, start=1):
            docs_in_batch = [item[1] for item in batch]
            msg_digest = format_new_docs_digest(docs_in_batch, batch_index=b_idx, total_batches=total_batches)

            if dry_run:
                print(f"[DRY-RUN VĂN BẢN MỚI BATCH {b_idx}/{total_batches}]:\n{msg_digest}\n")
            else:
                ok = send_telegram_message(msg_digest)
                if ok:
                    alerts_sent += 1
                    for fp, _ in batch:
                        sent_list.append(fp)
    else:
        print("✓ Chưa có văn bản XNK mới nào trong lần quét này.")

    # Cập nhật cache & đánh dấu ngày chạy
    if not dry_run:
        sent_cache["sent_doc_numbers"] = sent_list[-300:]  # Giữ tối đa 300 bản ghi gần nhất
        save_sent_cache(sent_cache)
        mark_run_today()
        print(f"✅ Hoàn thành quy trình buổi sáng! Đã gửi {alerts_sent} bản tin về Telegram.")
    else:
        print("✅ Hoàn thành kiểm tra thử nghiệm (Dry-run mode). Không gửi dữ liệu thật.")

def send_demo_alerts():
    """
    Gửi bản tin mẫu nghiệm thu chuẩn format mới:
    - 1 Bản tin Tổng hợp Đa Văn bản (Gồm 4 loại văn bản: Nghị định, Thông tư, Quyết định, Hiệp định FTA).
    - 1 Danh mục Hiệu lực Đa Văn bản (T-0 Hôm nay áp dụng).
    - ĐÃ BỎ hoàn toàn nội dung trọng tâm dài dòng, giao diện thanh thoát, trực quan.
    """
    print("🚀 Đang gửi 2 tin nhắn mẫu theo chuẩn CẬP NHẬT ĐA VĂN BẢN (Digest) về Telegram...")

    # Mẫu 1: Bản tin Điểm tin Đa Văn bản mới (4 loại văn bản khác nhau)
    demo_new_docs = [
        {
            "type": "Nghị định",
            "doc_number": "174/2025/NĐ-CP",
            "authority": "Chính phủ",
            "title": "Chính sách giảm thuế giá trị gia tăng 2% (xuống 8%) khâu nhập khẩu và nội địa",
            "effective_date": "01/07/2025",
            "category": "#ThuếXNK #GiảmThuếVAT",
            "link": "https://vanban.chinhphu.vn"
        },
        {
            "type": "Thông tư",
            "doc_number": "121/2025/TT-BTC",
            "authority": "Bộ Tài chính",
            "title": "Sửa đổi toàn diện thủ tục hải quan số, khai báo e-C/O và giám sát phối hợp cảng biển",
            "effective_date": "01/02/2026",
            "category": "#ThủTụcHảiQuan #HồSơSố",
            "link": "https://vanban.chinhphu.vn"
        },
        {
            "type": "Quyết định",
            "doc_number": "505/QĐ-TCHQ",
            "authority": "Tổng cục Hải quan",
            "title": "Ban hành quy trình chuẩn về soi chiếu container và kiểm tra thực tế hàng hóa luồng Đỏ",
            "effective_date": "15/03/2026",
            "category": "#KiểmTraHảiQuan #PhânLuồng",
            "link": "https://vanban.chinhphu.vn"
        },
        {
            "type": "Hiệp định FTA",
            "doc_number": "VIFTA (VN - Israel)",
            "authority": "Bộ Công Thương",
            "title": "Biểu thuế xuất nhập khẩu ưu đãi đặc biệt và quy tắc xuất xứ hàng hóa giai đoạn 2026-2030",
            "effective_date": "01/01/2026",
            "category": "#HiệpĐịnhFTA #XuấtXứCO",
            "link": "https://vanban.chinhphu.vn"
        }
    ]

    msg_digest = format_new_docs_digest(demo_new_docs, batch_index=1, total_batches=1)
    ok1 = send_telegram_message(msg_digest)

    # Mẫu 2: Danh mục Văn bản có hiệu lực hôm nay (T-0 Đa Văn bản)
    demo_t0_docs = [
        {
            "type": "Thông tư",
            "doc_number": "121/2025/TT-BTC",
            "authority": "Bộ Tài chính",
            "title": "Bãi bỏ việc nộp e-C/O giấy; liên thông số tiếp nhận NSW trực tiếp trên VNACCS",
            "link": "https://vanban.chinhphu.vn"
        },
        {
            "type": "Quyết định",
            "doc_number": "28/2026/QĐ-TTg",
            "authority": "Thủ tướng Chính phủ",
            "title": "Danh mục phế liệu được phép nhập khẩu từ nước ngoài làm nguyên liệu sản xuất",
            "link": "https://vanban.chinhphu.vn"
        }
    ]

    msg_t0 = format_effective_date_digest(demo_t0_docs, alert_type="T-0")
    ok2 = send_telegram_message(msg_t0)

    if ok1 and ok2:
        print("✅ GỬI THÀNH CÔNG 2 BẢN TIN MẪU ĐA VĂN BẢN! Vui lòng kiểm tra Telegram của bạn.")
    else:
        print("⚠️ Có lỗi khi gửi tin qua Telegram. Vui lòng kiểm tra lại CUSTOMS_TELEGRAM_BOT_TOKEN trong file .env.")

def main():
    parser = argparse.ArgumentParser(description="Customs Legal Telegram Copilot — Cảnh Báo Pháp Lý XNK Đa Văn Bản")
    parser.add_argument("--on-logon", action="store_true", help="Chế độ kích hoạt khi mở máy tính (chỉ chạy 1 lần/ngày)")
    parser.add_argument("--force", action="store_true", help="Bắt buộc chạy dù hôm nay đã chạy rồi")
    parser.add_argument("--dry-run", action="store_true", help="Chạy kiểm thử xem trước tin nhắn mà không gửi Telegram")
    parser.add_argument("--send-demo", action="store_true", help="Gửi 2 bản tin mẫu (Đa văn bản mới & Mốc hiệu lực) về Telegram")
    parser.add_argument("--status", action="store_true", help="Kiểm tra trạng thái cấu hình và CSDL")

    args = parser.parse_args()

    if args.status:
        print("=" * 60)
        print("📊 TRẠNG THÁI CUSTOMS LEGAL TELEGRAM COPILOT (v2.5)")
        print("=" * 60)
        has_token = bool(BOT_TOKEN)
        has_chat = bool(CHAT_ID)
        token_display = BOT_TOKEN[:6] + "..." + BOT_TOKEN[-4:] if len(BOT_TOKEN) > 10 else ("Đã cấu hình" if has_token else "CHƯA CẤU HÌNH")
        print(f"• Tệp cấu hình:       {ENV_PATH}")
        print(f"• Bot Token:          {token_display}")
        print(f"• Chat ID:            {CHAT_ID if has_chat else 'CHƯA CẤU HÌNH'}")
        
        already_run, run_time = check_already_run_today()
        print(f"• Trạng thái hôm nay: {'ĐÃ CHẠY lúc ' + run_time if already_run else 'CHƯA CHẠY'}")
        
        docs = get_tracked_documents_from_db()
        print(f"• CSDL Pháp lý:       Đang theo dõi {len(docs)} văn bản nội bộ")
        t0, t1 = check_effective_dates()
        print(f"• Hiệu lực hôm nay (T-0): {len(t0)} văn bản")
        print(f"• Hiệu lực ngày mai (T-1): {len(t1)} văn bản")
        print("=" * 60)
        return

    if args.send_demo:
        send_demo_alerts()
        return

    # Chạy mặc định hoặc on-logon
    execute_daily_workflow(force=args.force, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
