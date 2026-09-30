# -*- coding: utf-8 -*-
"""
========================================================================================
AUTOMATION ENGINEERING WORKFLOW: TELEGRAM AI NEWS BOT v2.0 (MÔ HÌNH OIPO NÂNG CẤP)
========================================================================================
1. OBJECTIVE:
   - Tự động hóa tổng hợp 3 tin tức AI mới nhất trong ngày từ các nguồn uy tín.
   - Dịch toàn bộ Tiêu đề (Title) và Nội dung tóm tắt (Summary) sang tiếng Việt chính xác.
   - Định dạng thông điệp trực quan có số thứ tự (1, 2, 3) mạch lạc, chuyên nghiệp.
   - Tự động tổng hợp Góc nhìn / Insight chiến lược về xu hướng phát triển công nghệ AI.
   - Hỗ trợ gửi ngay lập tức hoặc tự động lập lịch gửi lúc 10h00 sáng hàng ngày.

2. INPUT:
   - Nguồn dữ liệu: Google News RSS (AI, OpenAI, Google AI) kết hợp TechCrunch/The Verge AI.
   - Cấu hình bí mật: TELEGRAM_BOT_TOKEN và TELEGRAM_CHAT_ID được nạp từ file .env.

3. PROCESS:
   - Đọc cấu hình bảo mật từ .env bằng python-dotenv.
   - get_ai_news(limit=3): Thu thập 3 bài báo AI chất lượng cao, trích xuất title, link, summary.
   - translate_to_vi(): Dịch thuật chuẩn xác sang tiếng Việt qua REST API bằng requests (không dùng googletrans).
   - generate_ai_insight(): Phân tích chủ đề và đúc kết 2 nhận định xu hướng chiến lược.
   - format_telegram_message(): Ghép layout chuyên nghiệp chuẩn hóa ngày dd/mm/yyyy.
   - send_telegram(): Gửi tin nhắn qua Telegram Bot API bằng requests.post.

4. OUTPUT:
   - Bản tin Telegram 3 bài báo kèm tóm tắt chi tiết và insight công nghệ gửi tới Chat ID người dùng.
   - Cơ chế chạy tự động 10h00 sáng qua Windows Task Scheduler hoặc Python daemon (--schedule).
========================================================================================
"""

import os
import sys
import time
import html
import re
import argparse
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv

# Cấu hình UTF-8 cho console Windows để hiển thị tiếng Việt và emoji không bị lỗi charmap
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Nạp biến môi trường từ .env
load_dotenv()


def clean_html_text(raw_html: str) -> str:
    """Làm sạch các thẻ HTML và giải mã ký tự thực thể (HTML entities)."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^<]+?>", "", raw_html)
    text = html.unescape(text)
    # Loại bỏ các đoạn boilerplate thường gặp ở cuối RSS
    text = re.sub(r"The post .* appeared first on .*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_ai_news(limit: int = 3) -> list:
    """
    [INPUT / PROCESS]: Lấy danh sách 3 tin tức AI mới nhất, chất lượng cao từ các RSS feed.
    Kết hợp TechCrunch AI, The Verge AI và Google News RSS để đảm bảo có tóm tắt chi tiết.
    
    Returns:
        list[dict]: Danh sách các tin tức gồm 'title', 'summary', 'link', 'source'.
    """
    rss_feeds = [
        ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
        ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
        ("Google News RSS", "https://news.google.com/rss/search?q=Artificial+Intelligence+OR+OpenAI+OR+Google+AI&hl=en-US&gl=US&ceid=US:en")
    ]

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    }

    collected_items = []
    seen_fingerprints = set()

    for feed_name, feed_url in rss_feeds:
        if len(collected_items) >= limit:
            break
        try:
            resp = requests.get(feed_url, headers=headers, timeout=12)
            if resp.status_code != 200:
                continue

            root = ET.fromstring(resp.content)
            
            # Xử lý cả định dạng RSS chuẩn và Atom feed
            entries = root.findall(".//item")
            if not entries:
                entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            for entry in entries:
                title_node = entry.find("title")
                if title_node is None:
                    title_node = entry.find("{http://www.w3.org/2005/Atom}title")
                
                raw_title = clean_html_text(title_node.text if title_node is not None else "")
                if not raw_title:
                    continue

                # Loại bỏ hậu tố nguồn ở cuối tiêu đề nếu có
                clean_title = raw_title
                if " - " in clean_title:
                    clean_title = clean_title.rsplit(" - ", 1)[0].strip()

                # Kiểm tra trùng lặp tiêu đề
                fingerprint = re.sub(r"[^a-zA-Z0-9]", "", clean_title.lower())[:35]
                if fingerprint in seen_fingerprints:
                    continue
                seen_fingerprints.add(fingerprint)

                # Trích xuất đường link
                link_node = entry.find("link")
                if link_node is None:
                    link_node = entry.find("{http://www.w3.org/2005/Atom}link")
                
                link = ""
                if link_node is not None:
                    link = link_node.text or link_node.get("href", "")
                link = link.strip()

                # Trích xuất đoạn tóm tắt nội dung
                desc_node = entry.find("description")
                if desc_node is None:
                    desc_node = entry.find("{http://www.w3.org/2005/Atom}summary")
                
                raw_desc = clean_html_text(desc_node.text if desc_node is not None else "")
                
                # Nếu không có tóm tắt hoặc tóm tắt trùng tiêu đề, bổ sung tóm tắt theo ngữ cảnh
                if not raw_desc or raw_desc == clean_title or len(raw_desc) < 20:
                    raw_desc = f"Diễn biến công nghệ và cập nhật mới nhất từ {feed_name}."
                else:
                    # Giới hạn tóm tắt trong khoảng 1-2 câu gọn gàng
                    sentences = re.split(r"(?<=[.!?])\s+", raw_desc)
                    raw_desc = " ".join(sentences[:2]).strip()

                collected_items.append({
                    "title": clean_title,
                    "summary": raw_desc,
                    "link": link,
                    "source": feed_name
                })

                if len(collected_items) >= limit:
                    break

        except Exception as e:
            print(f"[Cảnh báo] Lỗi khi nạp dữ liệu từ nguồn {feed_name}: {e}")

    return collected_items[:limit]


def translate_to_vi(text: str) -> str:
    """
    [PROCESS]: Dịch văn bản tiếng Anh sang tiếng Việt bằng REST API qua requests.
    Tuyệt đối không dùng thư viện googletrans.
    Sử dụng endpoint Google Dict REST nhẹ (qua requests) kết hợp MyMemory API và Google GTX dự phòng.
    """
    if not text:
        return ""

    clean_text = clean_html_text(text)

    # Phương án 1: Google Dict REST API (nhanh, chuẩn xác cao, dùng requests thuần)
    try:
        dict_url = "https://clients5.google.com/translate_a/t"
        params = {
            "client": "dict-chrome-ex",
            "sl": "auto",
            "tl": "vi",
            "q": clean_text
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        res = requests.get(dict_url, params=params, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list) and len(data) > 0:
                item = data[0]
                if isinstance(item, list) and len(item) > 0:
                    translated = item[0]
                    if translated and isinstance(translated, str):
                        return clean_html_text(translated)
                elif isinstance(item, str):
                    return clean_html_text(item)
    except Exception as e:
        print(f"[Cảnh báo dịch - Google Dict]: {e}")

    # Phương án 2: MyMemory Translated API
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": clean_text, "langpair": "en|vi"}
        res = requests.get(url, params=params, timeout=8)
        if res.status_code == 200:
            data = res.json()
            translated = data.get("responseData", {}).get("translatedText")
            if translated and not translated.startswith("MYMEMORY WARNING"):
                return clean_html_text(translated)
    except Exception as e:
        print(f"[Cảnh báo dịch - MyMemory]: {e}")

    # Phương án 3: Google Translate Public GTX REST API
    try:
        gtx_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "vi",
            "dt": "t",
            "q": clean_text
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(gtx_url, params=params, headers=headers, timeout=8)
        if res.status_code == 200:
            data = res.json()
            translated = "".join([part[0] for part in data[0] if part[0]])
            if translated:
                return clean_html_text(translated)
    except Exception as e:
        print(f"[Cảnh báo dịch - Fallback]: {e}")

    # Nếu tất cả các phương án đều lỗi mạng, giữ nguyên văn bản gốc
    return clean_text


def generate_ai_insight(news_items: list) -> str:
    """
    [PROCESS]: Phân tích tổng thể các sự kiện công nghệ trong 3 bản tin
    và sinh ra phần nhận xét/insight xu hướng AI súc tích, thực tiễn.
    """
    all_text = " ".join([f"{item.get('title', '')} {item.get('summary', '')}" for item in news_items]).lower()

    insights = []

    # Nhận diện các chủ đề then chốt
    if any(k in all_text for k in ["ipo", "valuation", "fund", "billion", "sequoia", "invest", "public"]):
        insights.append(
            "Định giá các startup AI và kỳ lân công nghệ tiếp tục tăng trưởng nóng, tuy nhiên các công ty đầu ngành đang thận trọng hơn trong kế hoạch IPO để củng cố mô hình doanh thu bền vững."
        )

    if any(k in all_text for k in ["chip", "hardware", "nvidia", "micron", "semiconductor", "compute"]):
        insights.append(
            "Hạ tầng tính toán và năng lực bán dẫn vẫn là mắt xích cốt lõi, thúc đẩy làn sóng đầu tư hạ tầng trung tâm dữ liệu và chip thế hệ mới trên toàn cầu."
        )

    if any(k in all_text for k in ["slow", "safety", "pace", "risk", "governance", "regulation", "caution", "hack"]):
        insights.append(
            "An toàn mô hình và quản trị rủi ro AI (frontier safety) đang trở thành ưu tiên chiến lược của các CEO hàng đầu nhằm kiểm soát tốc độ phát triển và tuân thủ pháp lý."
        )

    if any(k in all_text for k in ["agent", "autonomous", "enterprise", "workflow", "data layer", "robot"]):
        insights.append(
            "Làn sóng AI đang chuyển dịch mạnh mẽ sang tự động hóa chuyên sâu (AI Agents & dữ liệu robot), mở ra kỷ nguyên doanh nghiệp vận hành tự chủ bằng dữ liệu."
        )

    # Nếu không khớp nhóm cụ thể, cung cấp insight tổng quan chất lượng cao
    if not insights:
        insights.append(
            "Hệ sinh thái AI toàn cầu đang chuyển đổi mạnh mẽ từ giai đoạn thử nghiệm mô hình sang giai đoạn tối ưu hóa giá trị ứng dụng thực tiễn trong kinh doanh."
        )
        insights.append(
            "Các tổ chức và chuyên gia cần chủ động cập nhật kỹ năng tự động hóa và quản trị dữ liệu để nắm bắt cơ hội tăng trưởng."
        )

    # Đảm bảo có đúng 2 gạch đầu dòng insight cô đọng
    formatted_insights = "\n".join([f"· {ins}" for ins in insights[:2]])
    return formatted_insights


def format_telegram_message(news_items: list, insight: str) -> str:
    """
    [PROCESS]: Định dạng bản tin theo cấu trúc chuyên nghiệp, có số thứ tự rõ ràng (1, 2, 3),
    tiêu đề, tóm tắt nội dung tiếng Việt, link nguồn và hộp insight xu hướng.
    """
    today_str = datetime.now().strftime("%d/%m/%Y")
    number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

    lines = [
        f"🚀 BẢN TIN TRÍ TUỆ NHÂN TẠO HÔM NAY — {today_str}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    ]

    for idx, item in enumerate(news_items):
        num_icon = number_emojis[idx] if idx < len(number_emojis) else f"[{idx+1}]"
        title_vi = item.get("title_vi", item.get("title", ""))
        summary_vi = item.get("summary_vi", item.get("summary", ""))
        link = item.get("link", "")

        block = (
            f"{num_icon} {title_vi}\n"
            f"📝 Tóm tắt: {summary_vi}\n"
            f"🔗 Nguồn: {link}\n"
        )
        lines.append(block)

    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("💡 GÓC NHÌN & INSIGHT XU HƯỚNG AI:")
    lines.append(insight)
    lines.append("\n#AI #OpenAI #GoogleAI #TechTrends #TinCongNghe")

    return "\n".join(lines)


def send_telegram(message: str, bot_token: str = None, chat_id: str = None) -> bool:
    """
    [OUTPUT]: Gửi tin nhắn đến Telegram chat thông qua Telegram Bot API bằng requests.post.
    """
    token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
    target_chat = chat_id or os.getenv("TELEGRAM_CHAT_ID")

    if not token or not target_chat:
        print("[Lỗi bảo mật] Thiếu TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env!")
        return False

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": str(target_chat).strip(),
        "text": message,
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(api_url, json=payload, timeout=15)
        result = response.json()

        if response.status_code == 200 and result.get("ok"):
            print(f"[Thành công] Đã gửi thông báo đến Telegram Chat ID: {target_chat}")
            return True
        else:
            description = result.get("description", "Không có mô tả chi tiết")
            print(f"[Lỗi Telegram API] Mã lỗi: {response.status_code} | Mô tả: {description}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[Lỗi kết nối mạng khi gửi Telegram]: {e}")
        return False


def run_daily_briefing() -> bool:
    """
    [ORCHESTRATION]: Thực hiện một chu trình tổng hợp, dịch thuật và gửi bản tin AI hoàn chỉnh.
    """
    print("\n" + "=" * 70)
    print(f"🚀 BẮT ĐẦU WORKFLOW ĐIỂM TIN AI CHUYÊN NGHIỆP — {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 70)

    # 1. Kiểm tra cấu hình bảo mật .env
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("❌ Lỗi: Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong file .env!")
        return False

    masked_token = token[:10] + "..." + token[-5:] if len(token) > 15 else "***"
    print(f"🔒 [Bảo mật .env] Token: {masked_token} | Chat ID: {chat_id}")

    # 2. Thu thập 3 tin AI chất lượng cao
    print("\n📡 [1/4 - Input] Đang thu thập 3 tin tức AI mới nhất...")
    news_items = get_ai_news(limit=3)
    if not news_items:
        print("❌ Lỗi: Không thể lấy dữ liệu tin tức từ các nguồn RSS.")
        return False

    print(f"  ➜ Đã thu thập thành công {len(news_items)} bản tin AI.")

    # 3. Dịch sang tiếng Việt (cả Tiêu đề và Nội dung tóm tắt)
    print("\n🌐 [2/4 - Process] Đang dịch tiêu đề và nội dung tóm tắt sang tiếng Việt...")
    for idx, item in enumerate(news_items, 1):
        print(f"  ➜ Đang dịch tin {idx}/{len(news_items)}: '{item['title'][:40]}...'")
        item["title_vi"] = translate_to_vi(item["title"])
        item["summary_vi"] = translate_to_vi(item["summary"])

    # 4. Phân tích insight xu hướng
    print("\n💡 [3/4 - Process] Đang phân tích và tạo insight xu hướng AI...")
    insight_text = generate_ai_insight(news_items)

    # 5. Định dạng thông điệp Telegram
    message = format_telegram_message(news_items, insight_text)
    print("\n📝 [Preview Bản Tin Chuẩn Bị Gửi]:")
    print("-" * 55)
    print(message)
    print("-" * 55)

    # 6. Gửi bản tin qua Telegram
    print("\n📤 [4/4 - Output] Đang gửi thông báo vào Telegram Chat...")
    success = send_telegram(message, bot_token=token, chat_id=chat_id)

    if success:
        print("\n🎉 HOÀN TẤT CHU TRÌNH GỬI BẢN TIN AI THÀNH CÔNG!")
    else:
        print("\n⚠️ Chu trình hoàn tất nhưng gặp lỗi khi gửi Telegram.")
    print("=" * 70)
    return success


def run_scheduler_daemon(target_hour: int = 10, target_minute: int = 0):
    """
    [SCHEDULER DAEMON]: Vòng lặp chờ gửi bản tin vào đúng 10h00 sáng mỗi ngày.
    """
    print("\n" + "=" * 70)
    print(f"⏰ KÍCH HOẠT CHẾ ĐỘ LẬP LỊCH TỰ ĐỘNG: Gửi đều đặn lúc {target_hour:02d}:{target_minute:02d} sáng hàng ngày")
    print("=" * 70)
    print("Bot đang chạy ở chế độ nền (Daemon). Nhấn Ctrl+C để dừng.\n")

    while True:
        now = datetime.now()
        target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

        # Nếu thời gian 10h00 hôm nay đã qua, đặt lịch cho 10h00 ngày mai
        if now >= target_time:
            target_time += timedelta(days=1)

        wait_seconds = (target_time - now).total_seconds()
        next_run_str = target_time.strftime("%d/%m/%Y lúc %H:%M:%S")
        print(f"⏳ Bản tin tiếp theo sẽ được gửi vào: {next_run_str} (Còn ~{wait_seconds/3600:.1f} giờ nữa)")

        # Ngủ cho đến thời điểm kích hoạt
        time.sleep(min(wait_seconds, 3600))  # Kiểm tra lại mỗi giờ hoặc đến giờ hẹn
        
        # Nếu đã đến hoặc vượt qua giờ hẹn (trong khoảng dung sai 2 phút), kích hoạt gửi tin
        current_check = datetime.now()
        if current_check >= target_time - timedelta(minutes=1) and current_check <= target_time + timedelta(minutes=5):
            print(f"\n🔔 ĐÃ ĐẾN GIỜ HẸN ({target_hour:02d}:{target_minute:02d} AM)! Bắt đầu gửi bản tin...")
            run_daily_briefing()
            # Ngủ 120 giây để tránh gửi trùng trong cùng 1 phút
            time.sleep(120)


def main():
    parser = argparse.ArgumentParser(description="Telegram AI News Bot - Phiên bản Tự động hóa Chuyên nghiệp")
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Chạy ở chế độ lập lịch ngầm tự động gửi vào 10:00 sáng hàng ngày"
    )
    parser.add_argument(
        "--hour",
        type=int,
        default=10,
        help="Giờ kích hoạt gửi tin (mặc định: 10)"
    )
    parser.add_argument(
        "--minute",
        type=int,
        default=0,
        help="Phút kích hoạt gửi tin (mặc định: 0)"
    )
    args = parser.parse_args()

    if args.schedule:
        run_scheduler_daemon(target_hour=args.hour, target_minute=args.minute)
    else:
        # Chế độ gửi ngay lập tức (phục vụ test hoặc kích hoạt từ Windows Task Scheduler)
        run_daily_briefing()


if __name__ == "__main__":
    main()
