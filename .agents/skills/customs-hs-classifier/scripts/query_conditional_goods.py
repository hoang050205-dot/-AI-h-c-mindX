import os
import sys
import re
import argparse

sys.stdout.reconfigure(encoding='utf-8')

# Matrix of Line Ministry Specialized Policies & Inspection under Decree 69/2018/ND-CP and related regulations
SPECIALIZED_POLICIES = [
    {
        "category": "Nông sản, hạt giống, ngũ cốc, thực vật sống (đậu tương, ngô, gạo, lúa mì, rau quả, gỗ)",
        "keywords": ["đậu tương", "soya", "ngô", "bắp", "gạo", "lúa", "lúa mì", "hạt", "rau", "quả", "trái cây", "gỗ", "thực vật", "seed", "grain", "hoa", "cây"],
        "legal_basis": "Nghị định 69/2018/NĐ-CP (Phụ lục III); Thông tư 30/2014/TT-BNNPTNT & Thông tư 33/2014/TT-BNNPTNT; Thông tư 15/2018/TT-BNNPTNT & Thông tư 11/2021/TT-BNNPTNT",
        "ministry": "Bộ Nông nghiệp và Phát triển Nông thôn (Cục Bảo vệ Thực vật)",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN",
        "requirements": [
            "1. Kiểm dịch thực vật nhập khẩu (Phytosanitary Inspection): Bắt buộc có Giấy chứng nhận kiểm dịch thực vật (Phyto Certificate) do cơ quan có thẩm quyền của nước xuất khẩu cấp trước khi hàng cập cảng.",
            "2. Đăng ký kiểm tra An toàn thực phẩm (nếu dùng làm thực phẩm cho người) theo Nghị định 15/2018/NĐ-CP.",
            "3. Kiểm tra danh mục sinh vật biến đổi gen (GMO): Nếu là đậu tương/ngô biến đổi gen làm thức ăn chăn nuôi, phải nằm trong Danh mục sự kiện biến đổi gen được cấp Giấy xác nhận GMO.",
            "4. Đăng ký trên Cổng thông tin Một cửa Quốc gia (NSW) trước khi tàu cập cảng."
        ],
        "risk_warning": "Nếu thiếu Giấy Phyto gốc từ nước xuất khẩu hoặc lô hàng bị nhiễm đối tượng kiểm dịch thực vật nhóm 1 (côn trùng sống, mọt Trogoderma...), hải quan sẽ không cho thông quan và buộc tái xuất trong vòng 30 ngày!"
    },
    {
        "category": "Động vật sống, thịt đông lạnh, thủy hải sản, sản phẩm từ động vật",
        "keywords": ["thịt", "bò", "lợn", "heo", "gà", "thủy sản", "cá", "tôm", "sữa", "trứng", "mỡ động vật", "động vật"],
        "legal_basis": "Nghị định 69/2018/NĐ-CP (Phụ lục III); Thông tư 25/2016/TT-BNNPTNT, Thông tư 26/2016/TT-BNNPTNT; Nghị định 15/2018/NĐ-CP",
        "ministry": "Bộ Nông nghiệp và Phát triển Nông thôn (Cục Thú y)",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN & KIỂM TRA CHUYÊN NGÀNH GẮT GAO",
        "requirements": [
            "1. Doanh nghiệp chế biến/giết mổ của nước xuất khẩu phải nằm trong Danh sách được Cục Thú y Việt Nam cấp phép xuất khẩu vào VN.",
            "2. Xin Giấy phép kiểm dịch động vật của Cục Thú y trước khi hàng rời cảng đi.",
            "3. Giấy chứng nhận kiểm dịch (Veterinary Health Certificate) gốc của nước xuất xứ.",
            "4. Lấy mẫu kiểm dịch động vật và kiểm tra An toàn thực phẩm tại cửa khẩu/cảng đến."
        ],
        "risk_warning": "Nhập từ nhà máy chưa được phê duyệt mã số vào Việt Nam sẽ bị từ chối nhập khẩu ngay lập tức!"
    },
    {
        "category": "Máy móc, thiết bị, dây chuyền công nghệ đã qua sử dụng (second-hand machinery)",
        "keywords": ["đã qua sử dụng", "cũ", "second-hand", "used", "máy móc cũ", "dây chuyền cũ", "thiết bị cũ"],
        "legal_basis": "Quyết định số 18/2019/QĐ-TTg của Thủ tướng Chính phủ; Nghị định 69/2018/NĐ-CP; Thông tư 23/2015/TT-BKHCN",
        "ministry": "Bộ Khoa học và Công nghệ",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN KHẮT KHE HOẶC BỊ CẤM",
        "requirements": [
            "1. Tuổi thiết bị không được vượt quá 10 năm tính từ năm sản xuất đến năm nhập khẩu (một số ngành đặc thù 15-20 năm).",
            "2. Sản xuất theo tiêu chuẩn phù hợp với Quy chuẩn kỹ thuật quốc gia (QCVN) hoặc Tiêu chuẩn quốc gia (TCVN) hoặc Tiêu chuẩn của các nước G7, Hàn Quốc.",
            "3. Bắt buộc nộp Chứng thư giám định máy móc, thiết bị đã qua sử dụng do Tổ chức giám định được chỉ định cấp.",
            "4. Chỉ được nhập khẩu trực tiếp phục vụ sản xuất của chính doanh nghiệp, không được nhập để thương mại bán lại."
        ],
        "risk_warning": "Thiết bị quá 10 năm tuổi thuộc diện cấm nhập khẩu tuyệt đối, bị buộc tái xuất và xử phạt hành chính theo Nghị định 128/2020/NĐ-CP!"
    },
    {
        "category": "Thiết bị điện, điện tử gia dụng & công nghệ thông tin (máy tính, điện thoại, máy giặt, điều hòa)",
        "keywords": ["máy tính", "laptop", "điện thoại", "phone", "tivi", "điều hòa", "máy giặt", "tủ lạnh", "màn hình", "pc", "linh kiện"],
        "legal_basis": "Nghị định 69/2018/NĐ-CP; Quyết định 04/2017/QĐ-TTg (Hiệu suất năng lượng); Thông tư 04/2023/TT-BTTTT; Thông tư 11/2020/TT-BKHCN",
        "ministry": "Bộ Công Thương (Nhãn năng lượng) & Bộ TT&TT (Hợp quy viễn thông) & Bộ KH&CN (Chất lượng)",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN (MỚI 100%). NẾU ĐÃ QUA SỬ DỤNG: CẤM NHẬP KHẨU TUYỆT ĐỐI!",
        "requirements": [
            "1. Hàng điện tử gia dụng/IT đã qua sử dụng thuộc Danh mục CẤM NHẬP KHẨU theo Thông tư 11/2018/TT-BTTTT.",
            "2. Hàng mới 100%: Phải đăng ký kiểm tra Hiệu suất năng lượng tối thiểu và Dán nhãn năng lượng (Bộ Công Thương).",
            "3. Thiết bị phát sóng vô tuyến (wifi, bluetooth, 4G/5G): Chứng nhận hợp quy và Công bố hợp quy (Bộ TT&TT).",
            "4. Kiểm tra chất lượng nhà nước theo QCVN (Bộ KH&CN)."
        ],
        "risk_warning": "Nghiêm cấm nhập khẩu thiết bị CNTT, điện tử đã qua sử dụng (rác thải điện tử - e-waste) dưới mọi hình thức!"
    },
    {
        "category": "Hóa chất, tiền chất công nghiệp, phân bón, thuốc bảo vệ thực vật",
        "keywords": ["hóa chất", "chemical", "axit", "dung môi", "tiền chất", "phân bón", "thuốc trừ sâu", "thuốc bảo vệ thực vật"],
        "legal_basis": "Luật Hóa chất 2007; Nghị định 113/2017/NĐ-CP & Nghị định 82/2022/NĐ-CP; Nghị định 69/2018/NĐ-CP",
        "ministry": "Bộ Công Thương (Cục Hóa chất) & Bộ NN&PTNT (Cục Bảo vệ Thực vật)",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN HOẶC GIẤY PHÉP",
        "requirements": [
            "1. Khai báo hóa chất nhập khẩu qua Cổng một cửa Quốc gia (NSW) trước khi thông quan.",
            "2. Hóa chất hạn chế sản xuất, kinh doanh: Bắt buộc có Giấy phép nhập khẩu do Bộ Công Thương cấp.",
            "3. Tiền chất công nghiệp / Tiền chất ma túy: Bắt buộc Giấy phép của Cục Hóa chất.",
            "4. Phải có Phiếu an toàn hóa chất (MSDS - Material Safety Data Sheet) bằng tiếng Việt."
        ],
        "risk_warning": "Hóa chất cấm theo Công ước Rotterdam/Stockholm hoặc Bảng 1 Công ước Cấm vũ khí hóa học bị CẤM NHẬP KHẨU tuyệt đối."
    },
    {
        "category": "Dược phẩm, mỹ phẩm, thực phẩm chức năng, thiết bị y tế",
        "keywords": ["thuốc", "dược phẩm", "mỹ phẩm", "kem", "son", "phấn", "thực phẩm chức năng", "thiết bị y tế", "khẩu trang", "băng gạc"],
        "legal_basis": "Luật Dược 2016; Nghị định 98/2021/NĐ-CP (Trang thiết bị y tế); Thông tư 06/2011/TT-BYT (Mỹ phẩm); Nghị định 69/2018/NĐ-CP",
        "ministry": "Bộ Y Tế (Cục Quản lý Dược, Vụ Trang thiết bị và Công trình y tế)",
        "status": "XUẤT NHẬP KHẨU CÓ ĐIỀU KIỆN & GIẤY PHÉP CHUYÊN NGÀNH",
        "requirements": [
            "1. Mỹ phẩm: Bắt buộc có Phiếu tiếp nhận Phiếu công bố sản phẩm mỹ phẩm do Cục Quản lý Dược cấp.",
            "2. Dược phẩm: Có Giấy đăng ký lưu hành hoặc Giấy phép nhập khẩu thuốc chưa có số đăng ký.",
            "3. Trang thiết bị y tế: Phân loại A, B, C, D; Công bố tiêu chuẩn áp dụng (Loại A, B) hoặc Đăng ký số lưu hành (Loại C, D).",
            "4. Chứng từ nguồn gốc: CFS (Certificate of Free Sale), ISO 13485."
        ],
        "risk_warning": "Mỹ phẩm, dược phẩm nhập lậu hoặc chưa công bố bị xử phạt nặng và tịch thu tiêu hủy!"
    },
    {
        "category": "Hàng tiêu dùng thông thường (Quần áo, giày dép, đồ nội thất gỗ, đồ gia dụng nhựa mới 100%)",
        "keywords": ["quần áo", "may mặc", "vải", "giày", "dép", "bàn", "ghế", "nội thất", "đồ nhựa", "thìa", "bát", "đĩa"],
        "legal_basis": "Nghị định 69/2018/NĐ-CP; Thông tư 38/2015/TT-BTC & Thông tư 39/2018/TT-BTC",
        "ministry": "Bộ Công Thương (quản lý chung)",
        "status": "ĐƯỢC PHÉP XUẤT NHẬP KHẨU TỰ DO (MỚI 100%)",
        "requirements": [
            "1. Hàng hóa mới 100% không thuộc danh mục quản lý chuyên ngành, không cần giấy phép.",
            "2. Riêng sản phẩm dệt may (vải, quần áo): Kiểm tra hàm lượng Formaldehyt và các amin thơm chuyển hóa từ thuốc nhuộm azo theo Thông tư 21/2017/TT-BCT.",
            "3. Thông quan thông thường qua VNACCS/ECUS5."
        ],
        "risk_warning": "Quần áo, hàng dệt may đã qua sử dụng thuộc danh mục CẤM NHẬP KHẨU (Nghị định 69/2018/NĐ-CP)."
    }
]

def check_policy(query):
    clean_q = query.strip().lower()
    matched = []
    
    for item in SPECIALIZED_POLICIES:
        for kw in item["keywords"]:
            if kw in clean_q:
                matched.append(item)
                break
                
    if not matched:
        # Fallback to general policy check
        print(f"\n[?] Không phát hiện chính sách cấm/hạn chế đặc biệt tức thì cho '{query}'.")
        print("    -> Cần đối chiếu tiếp theo mã HS cụ thể trong Biểu thuế XNK 2026 và Danh mục NĐ 69/2018.")
        return

    print(f"\n{'='*95}")
    print(f" RÀ SOÁT CHÍNH SÁCH MẶT HÀNG & TÍNH HỢP PHÁP CHO: '{query}'")
    print(f"{'='*95}\n")
    
    for idx, p in enumerate(matched, 1):
        print(f"[{idx}] NHÓM HÀNG: {p['category']}")
        print(f"    - TÌNH TRẠNG PHÁP LÝ : {p['status']}")
        print(f"    - CƠ QUAN QUẢN LÝ    : {p['ministry']}")
        print(f"    - CĂN CỨ VĂN BẢN     : {p['legal_basis']}")
        print(f"    - YÊU CẦU ĐIỀU KIỆN  :")
        for req in p["requirements"]:
            print(f"      * {req}")
        print(f"    - [!] CẢNH BÁO BẪY RỦI RO:")
        print(f"      {p['risk_warning']}")
        print(f"{'-'*95}")

def main():
    parser = argparse.ArgumentParser(description="Tra cứu chính sách mặt hàng và kiểm tra chuyên ngành theo Nghị định 69/2018/NĐ-CP")
    parser.add_argument("-q", "--query", required=True, help="Tên hàng hóa hoặc loại mặt hàng cần rà soát")
    args = parser.parse_args()
    check_policy(args.query)

if __name__ == "__main__":
    main()
