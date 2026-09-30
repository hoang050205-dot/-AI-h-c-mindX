import os
import sys
import re
import argparse

sys.stdout.reconfigure(encoding='utf-8')

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(skill_dir, 'assets')
txt_path = os.path.join(assets_dir, 'Phu_luc_II_Sau_quy_tac_tong_quat_GRI.txt')

RULES_MAP = {
    "1": ("QUI TẮC 1", "Phân loại theo câu chữ của Nhóm (Heading) và Chú giải Phần/Chương. Tên tiêu đề chỉ để tham khảo."),
    "2": ("QUI TẮC 2", "GRI 2(a): Hàng chưa hoàn chỉnh/tháo rời. GRI 2(b): Hỗn hợp, hợp chất của nguyên liệu/chất."),
    "2A": ("QUI TẮC 2 (a)", "Hàng hóa chưa hoàn chỉnh, chưa hoàn thiện (có đặc trưng cơ bản) hoặc tháo rời, chưa lắp ráp."),
    "2B": ("QUI TẮC 2 (b)", "Hỗn hợp và hợp chất của các nguyên liệu hoặc các chất."),
    "3": ("QUI TẮC 3", "Phân loại hàng hóa thoạt nhìn vào từ 2 nhóm trở lên: 3(a) Cụ thể nhất -> 3(b) Đặc tính cơ bản -> 3(c) Nhóm có thứ tự sau cùng."),
    "3A": ("QUI TẮC 3 (a)", "Nhóm có mô tả cụ thể, đặc trưng nhất được ưu tiên hơn nhóm mô tả khái quát."),
    "3B": ("QUI TẮC 3 (b)", "Hàng hóa hỗn hợp, nhiều bộ phận hoặc dạng bộ để bán lẻ: Phân loại theo thành phần/bộ phận tạo nên ĐẶC TÍNH CƠ BẢN (Essential Character)."),
    "3C": ("QUI TẮC 3 (c)", "Phân loại vào nhóm có số thứ tự đánh số cuối cùng trong các nhóm tương đương."),
    "4": ("QUI TẮC 4", "Hàng hóa không thể phân loại theo GRI 1-3 thì phân loại vào nhóm hàng hóa GIỐNG CHÚNG NHẤT."),
    "5": ("QUI TẮC 5", "GRI 5(a): Bao bì, hộp, túi chuyên dụng đi kèm. GRI 5(b): Bao bì đóng gói thông thường."),
    "5A": ("QUI TẮC 5 (a)", "Bao bì, túi xách, hộp chuyên dụng thiết kế riêng cho sản phẩm (ví dụ bao đàn guitar, hộp kính thiên văn, bao máy ảnh)."),
    "5B": ("QUI TẮC 5 (b)", "Bao bì thông thường đi kèm đóng gói hàng hóa (trừ bao bì có thể dùng lặp lại nhiều lần)."),
    "6": ("QUI TẮC 6", "Phân loại ở cấp độ phân nhóm 6 số và 8 số: Chỉ so sánh giữa các phân nhóm cùng cấp độ gạch (-).")
}

def query_rule(rule_key):
    if not os.path.exists(txt_path):
        print(f"Error: Text companion not found at {txt_path}")
        return

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    norm_key = rule_key.strip().upper().replace("GRI", "").replace("QUI TẮC", "").replace("QUY TẮC", "").replace(" ", "")
    
    rule_info = RULES_MAP.get(norm_key)
    if not rule_info:
        # Fallback to general search
        search_keyword(rule_key)
        return

    rule_title, rule_summary = rule_info
    print(f"\n{'='*95}")
    print(f" 6 QUY TẮC TỔNG QUÁT HS (GRI) — {rule_title}")
    print(f"{'='*95}\n")
    print(f"[*] TÓM TẮT ĐỊNH HƯỚNG: {rule_summary}\n")
    
    # Extract text block around this rule
    pattern = re.compile(re.escape(rule_title) + r".*?(?=QUI TẮC \d|$)", re.DOTALL | re.IGNORECASE)
    match = pattern.search(content)
    if match:
        raw_text = match.group(0).strip()
        # Print excerpt (up to 2000 chars)
        print("[-] CĂN CỨ VĂN BẢN GỐC & CHÚ GIẢI CHI TIẾT (EXPLANATORY NOTES):")
        lines = raw_text.split('\n')
        for l in lines[:35]:
            if l.strip():
                print(f"    {l.strip()}")
        if len(lines) > 35:
            print("    [... trích xuất rút gọn, xem toàn văn tại Phụ lục II ...]")
    else:
        print(f"[-] Đã định danh nguyên tắc {rule_title}. Vui lòng xem toàn văn tại Phụ lục II.")
    print(f"\n{'-'*95}")

def search_keyword(keyword):
    if not os.path.exists(txt_path):
        print(f"Error: Text companion not found at {txt_path}")
        return

    with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    clean_kw = keyword.strip()
    matches = []
    for idx, line in enumerate(lines):
        if re.search(re.escape(clean_kw), line, re.IGNORECASE):
            # Take context of 2 lines before and after
            start = max(0, idx - 1)
            end = min(len(lines), idx + 2)
            snippet = " ".join([l.strip() for l in lines[start:end] if l.strip()])
            matches.append((idx + 1, snippet))
            if len(matches) >= 5:
                break

    print(f"\n{'='*95}")
    print(f" KẾT QUẢ TÌM KIẾM CHÚ GIẢI 6 QUY TẮC GRI CHO TỪ KHÓA: '{keyword}' ({len(matches)} đoạn trích)")
    print(f"{'='*95}\n")
    for i, (line_no, snippet) in enumerate(matches, 1):
        print(f"[{i}] Đoạn trích tại dòng {line_no}:")
        print(f"    \"{snippet[:350]}...\"\n")
    print(f"{'-'*95}")

def main():
    parser = argparse.ArgumentParser(description="Tra cứu 6 Quy tắc Tổng quát HS (GRI 1-6) và Chú giải Explanatory Notes")
    parser.add_argument("-r", "--rule", help="Số quy tắc (1, 2, 2a, 2b, 3, 3a, 3b, 3c, 4, 5, 5a, 5b, 6)")
    parser.add_argument("-k", "--keyword", help="Từ khóa nghiệp vụ (ví dụ: 'tháo rời', 'đặc tính cơ bản', 'bán lẻ')")
    args = parser.parse_args()

    if args.rule:
        query_rule(args.rule)
    elif args.keyword:
        search_keyword(args.keyword)
    else:
        print("Vui lòng chỉ định -r [1-6] hoặc -k [từ khóa]. Sử dụng --help để xem chi tiết.")

if __name__ == "__main__":
    main()
