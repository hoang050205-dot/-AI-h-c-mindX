import os
import sys
import re
import argparse

sys.stdout.reconfigure(encoding='utf-8')

# Comprehensive Specialized Permits & Licensing Matrix under Decree 69/2018/ND-CP and Sectoral Laws
PERMITS_DATABASE = [
    {
        "category": "Nông sản, hạt giống, ngũ cốc, thức ăn chăn nuôi & sinh vật biến đổi gen (GMO)",
        "keywords": ["đậu tương", "soya", "ngô", "bắp", "gạo", "lúa", "lúa mì", "hạt giống", "seed", "thực vật", "nông sản", "thức ăn chăn nuôi", "ngũ cốc"],
        "hs_patterns": ["^1201", "^1005", "^1001", "^1006", "^2304", "^1209"],
        "ministry": "Bộ Nông nghiệp và Phát triển Nông thôn (Cục Bảo vệ Thực vật & Cục Trồng trọt)",
        "legal_bases": [
            "Nghị định số 69/2018/NĐ-CP (Phụ lục III - Danh mục hàng hóa XNK theo giấy phép, theo điều kiện)",
            "Luật Quản lý ngoại thương số 05/2017/QH14",
            "Luật Bảo vệ và Kiểm dịch thực vật số 41/2013/QH13",
            "Luật Trồng trọt số 31/2018/QH14 & Nghị định số 94/2019/NĐ-CP",
            "Nghị định số 15/2018/NĐ-CP quy định chi tiết thi hành Luật An toàn thực phẩm",
            "Nghị định số 69/2010/NĐ-CP & Nghị định số 108/2011/NĐ-CP về an toàn sinh học đối với sinh vật biến đổi gen (GMO)",
            "Thông tư số 30/2014/TT-BNNPTNT & Thông tư số 33/2014/TT-BNNPTNT quy định về kiểm dịch thực vật nhập khẩu",
            "Thông tư số 15/2018/TT-BNNPTNT & Thông tư số 11/2021/TT-BNNPTNT ban hành Bảng mã HS danh mục vật thể thuộc diện kiểm dịch thực vật"
        ],
        "permits": [
            {
                "permit_name": "Giấy phép Nhập khẩu Giống cây trồng",
                "issuing_authority": "Cục Trồng trọt — Bộ NN&PTNT",
                "applicable_condition": "BẮT BUỘC nếu nhập khẩu hạt giống đậu tương (Mã HS 1201.10.00) để gieo trồng nhân giống.",
                "exempt_condition": "MIỄN GIẤY PHÉP nếu là hạt đậu tương thương phẩm (Mã HS 1201.90.00) nhập khẩu để tiêu dùng, ép dầu thực vật, hoặc chế biến thức ăn chăn nuôi.",
                "timing": "Phải có Giấy phép trước khi ký kết hợp đồng thương mại và trước khi hàng rời cảng xuất khẩu.",
                "submission_method": "Nộp hồ sơ trực tuyến qua Cổng dịch vụ công của Bộ NN&PTNT hoặc Cổng Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Giấy phép Kiểm dịch Thực vật Nhập khẩu (Import Phytosanitary Permit)",
                "issuing_authority": "Cục Bảo vệ Thực vật — Bộ NN&PTNT",
                "applicable_condition": "Bắt buộc đối với giống cây trồng, sinh vật có ích hoặc vật thể thuộc diện kiểm dịch có nguy cơ cao mang dịch hại kiểm dịch thực vật của Việt Nam.",
                "exempt_condition": "Đậu tương thương phẩm từ các quốc gia/vùng đã được phân tích nguy cơ dịch hại (PRA) và mở cửa thị trường (như Mỹ, Brazil, Canada) không cần xin Giấy phép trước, nhưng BẮT BUỘC phải làm thủ tục Kiểm dịch thực vật tại cửa khẩu đến.",
                "timing": "Xin cấp trước khi xuất hàng từ nước xuất khẩu.",
                "submission_method": "Cổng thông tin Một cửa Quốc gia (NSW) tại vnsw.gov.vn."
            },
            {
                "permit_name": "Giấy xác nhận Sinh vật Biến đổi Gen (GMO) đủ điều kiện làm Thực phẩm / Thức ăn chăn nuôi",
                "issuing_authority": "Bộ Nông nghiệp và Phát triển Nông thôn",
                "applicable_condition": "BẮT BUỘC đối với đậu tương hoặc ngô biến đổi gen (Genetically Modified Organism - GMO). Sự kiện chuyển gen cụ thể của lô hàng phải nằm trong Danh mục sự kiện biến đổi gen đã được Bộ NN&PTNT cấp Giấy xác nhận.",
                "exempt_condition": "Hàng hóa là nông sản tự nhiên thuần chủng (Non-GMO) kèm theo Chứng nhận Non-GMO hoặc Giấy kiểm nghiệm không phát hiện biến đổi gen.",
                "timing": "Sự kiện GMO phải được cấp Giấy xác nhận và công bố trên cổng thông tin trước thời điểm nhập khẩu.",
                "submission_method": "Kiểm tra đối chiếu mã sự kiện GMO đã cấp phép trên hệ thống dữ liệu của Cục Bảo vệ thực vật."
            },
            {
                "permit_name": "Giấy tiếp nhận Đăng ký Kiểm dịch Thực vật & An toàn Thực phẩm Nhập khẩu",
                "issuing_authority": "Chi cục Kiểm dịch Thực vật Vùng (thuộc Cục BVTV)",
                "applicable_condition": "BẮT BUỘC cho 100% lô hàng nông sản thực vật nhập khẩu ở khâu làm thủ tục hải quan.",
                "exempt_condition": "Không miễn trừ.",
                "timing": "Đăng ký tối thiểu 24h - 48h trước khi tàu/phương tiện vận chuyển cập cảng.",
                "submission_method": "Đăng ký trực tuyến trên Cổng Một cửa Quốc gia (NSW) để lấy Mã số hồ sơ khai báo tờ khai VNACCS."
            }
        ],
        "mandatory_certificates": [
            "Giấy chứng nhận Kiểm dịch Thực vật (Phytosanitary Certificate) bản gốc do Cơ quan Kiểm dịch nước xuất khẩu cấp (bắt buộc).",
            "Giấy chứng nhận An toàn thực phẩm / Health Certificate của cơ quan có thẩm quyền nước xuất xứ.",
            "Giấy chứng nhận kiểm định chất lượng giống (nếu khai mã giống 1201.10.00).",
            "Bản công bố hợp quy thức ăn chăn nuôi hoặc Giấy đăng ký kiểm tra chất lượng thức ăn chăn nuôi nhập khẩu (nếu dùng làm TĂCN)."
        ],
        "penalties_and_risks": "Nếu nhập khẩu hạt giống mà không có Giấy phép của Cục Trồng trọt, hoặc đậu tương biến đổi gen chưa được cấp phép sự kiện GMO, hoặc thiếu Giấy Phyto gốc từ nước xuất xứ: Cơ quan Hải quan và Kiểm dịch sẽ lập biên bản đình chỉ thông quan, phạt tiền từ 30.000.000 đến 100.000.000 VNĐ theo Nghị định 128/2020/NĐ-CP và BUỘC TÁI XUẤT trong vòng 30 ngày."
    },
    {
        "category": "Động vật sống, thịt đông lạnh, thủy hải sản & sản phẩm nguồn gốc động vật",
        "keywords": ["thịt", "bò", "heo", "lợn", "gà", "thủy sản", "cá", "tôm", "hải sản", "sữa", "trứng", "mỡ động vật", "động vật sống"],
        "hs_patterns": ["^01", "^02", "^03", "^04", "^05"],
        "ministry": "Bộ Nông nghiệp và Phát triển Nông thôn (Cục Thú y)",
        "legal_bases": [
            "Nghị định số 69/2018/NĐ-CP (Phụ lục III)",
            "Luật Thú y số 79/2015/QH13",
            "Thông tư số 25/2016/TT-BNNPTNT & Thông tư số 26/2016/TT-BNNPTNT về kiểm dịch động vật, sản phẩm động vật",
            "Nghị định số 15/2018/NĐ-CP về an toàn thực phẩm"
        ],
        "permits": [
            {
                "permit_name": "Phê duyệt Danh sách Cơ sở Giết mổ/Chế biến đủ điều kiện xuất khẩu vào Việt Nam",
                "issuing_authority": "Cục Thú y — Bộ NN&PTNT",
                "applicable_condition": "Nhà máy/cơ sở sản xuất tại nước ngoài phải có tên và mã code được Cục Thú y thẩm định và đăng tải công khai trên website Cục Thú y.",
                "exempt_condition": "Không có ngoại lệ đối với sản phẩm động vật thương mại.",
                "timing": "Phải kiểm tra và xác nhận mã code nhà máy trước khi giao kết hợp đồng ngoại thương.",
                "submission_method": "Tra cứu cơ sở dữ liệu trực tuyến tại cucthuy.gov.vn."
            },
            {
                "permit_name": "Giấy phép Kiểm dịch Động vật / Sản phẩm động vật Nhập khẩu",
                "issuing_authority": "Cục Thú y — Bộ NN&PTNT",
                "applicable_condition": "BẮT BUỘC doanh nghiệp phải nộp Đơn đăng ký kiểm dịch nhập khẩu và được Cục Thú y cấp Văn bản đồng ý kiểm dịch trước khi hàng rời cảng đi.",
                "exempt_condition": "Không miễn trừ.",
                "timing": "Trước khi xuất hàng từ nước xuất khẩu.",
                "submission_method": "Cổng thông tin Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Giấy chứng nhận Kiểm dịch Động vật (Veterinary Health Certificate)",
                "issuing_authority": "Cơ quan thú y có thẩm quyền của nước xuất khẩu",
                "applicable_condition": "Bản gốc đi kèm lô hàng, chứng nhận nguồn gốc xuất xứ sạch bệnh và an toàn vệ sinh dịch tễ.",
                "exempt_condition": "Không miễn trừ.",
                "timing": "Cấp cùng thời điểm phát hành bộ chứng từ vận tải.",
                "submission_method": "Nộp bản gốc cho Chi cục Thú y Vùng tại cảng đến."
            }
        ],
        "mandatory_certificates": [
            "Văn bản đồng ý kiểm dịch của Cục Thú y.",
            "Giấy Health Certificate bản gốc của nước xuất xứ.",
            "Giấy đăng ký kiểm dịch động vật và an toàn thực phẩm trên NSW."
        ],
        "penalties_and_risks": "Nhập khẩu từ cơ sở chưa được cấp phép hoặc không có Giấy phép kiểm dịch sẽ bị từ chối nhập khẩu ngay lập tức, phạt tiền nặng và buộc tiêu hủy hoặc tái xuất."
    },
    {
        "category": "Máy móc, thiết bị, dây chuyền công nghệ đã qua sử dụng (Second-hand)",
        "keywords": ["đã qua sử dụng", "cũ", "second-hand", "used", "máy móc cũ", "dây chuyền cũ", "thiết bị cũ"],
        "hs_patterns": ["^84", "^85", "^87", "^90"],
        "ministry": "Bộ Khoa học và Công nghệ (Vụ Đánh giá, Thẩm định và Giám định Công nghệ)",
        "legal_bases": [
            "Quyết định số 18/2019/QĐ-TTg ngày 19/04/2019 của Thủ tướng Chính phủ quy định việc nhập khẩu máy móc, thiết bị, dây chuyền công nghệ đã qua sử dụng",
            "Nghị định số 69/2018/NĐ-CP của Chính phủ",
            "Thông tư số 23/2015/TT-BKHCN của Bộ Khoa học và Công nghệ"
        ],
        "permits": [
            {
                "permit_name": "Chứng thư Giám định Máy móc, Thiết bị đã qua sử dụng",
                "issuing_authority": "Tổ chức giám định được Bộ KH&CN chỉ định hoặc thừa nhận",
                "applicable_condition": "BẮT BUỘC cho toàn bộ máy móc, thiết bị đơn chiếc đã qua sử dụng nhập khẩu. Chứng thư phải xác nhận tuổi thiết bị không quá 10 năm và đáp ứng tiêu chuẩn an toàn, tiết kiệm năng lượng, bảo vệ môi trường.",
                "exempt_condition": "Chỉ miễn trừ trường hợp tạm nhập tái xuất phục vụ thi công dự án hoặc gia công rồi tái xuất.",
                "timing": "Thực hiện giám định tại nước xuất khẩu trước khi xếp hàng hoặc giám định tại cửa khẩu/cảng đến của Việt Nam.",
                "submission_method": "Nộp bản chính chứng thư giám định cho cơ quan hải quan khi làm thủ tục thông quan."
            },
            {
                "permit_name": "Văn bản Chấp thuận Nhập khẩu Dây chuyền công nghệ đã qua sử dụng",
                "issuing_authority": "Bộ Khoa học và Công nghệ",
                "applicable_condition": "BẮT BUỘC đối với dây chuyền công nghệ đồng bộ đã qua sử dụng.",
                "exempt_condition": "Không miễn trừ.",
                "timing": "Trước khi ký hợp đồng nhập khẩu và chuyển giao công nghệ.",
                "submission_method": "Nộp hồ sơ thẩm định công nghệ tại Bộ Khoa học và Công nghệ."
            }
        ],
        "mandatory_certificates": [
            "Chứng thư giám định của tổ chức giám định được chỉ định.",
            "Tài liệu kỹ thuật, năm sản xuất từ nhà chế tạo gốc.",
            "Cam kết trực tiếp sử dụng cho mục đích sản xuất của doanh nghiệp (nghiêm cấm nhập khẩu để bán lại thương mại)."
        ],
        "penalties_and_risks": "Thiết bị có tuổi đời trên 10 năm thuộc diện CẤM NHẬP KHẨU TUYỆT ĐỐI. Nếu vi phạm sẽ bị xử phạt theo Nghị định 128/2020/NĐ-CP và buộc tái xuất trong vòng 30 ngày."
    },
    {
        "category": "Hóa chất, tiền chất công nghiệp, dung môi & vật liệu nổ",
        "keywords": ["hóa chất", "chemical", "axit", "tiền chất", "dung môi", "phân bón", "thuốc bảo vệ thực vật"],
        "hs_patterns": ["^28", "^29", "^31", "^38"],
        "ministry": "Bộ Công Thương (Cục Hóa chất)",
        "legal_bases": [
            "Luật Hóa chất số 06/2007/QH12",
            "Nghị định số 113/2017/NĐ-CP & Nghị định số 82/2022/NĐ-CP quy định chi tiết Luật Hóa chất",
            "Nghị định số 69/2018/NĐ-CP của Chính phủ"
        ],
        "permits": [
            {
                "permit_name": "Giấy phép Nhập khẩu Hóa chất hạn chế sản xuất, kinh doanh",
                "issuing_authority": "Bộ Công Thương (Cục Hóa chất)",
                "applicable_condition": "BẮT BUỘC đối với các hóa chất thuộc Phụ lục II Nghị định 113/2017/NĐ-CP.",
                "exempt_condition": "Hóa chất sản xuất, kinh doanh có điều kiện (Phụ lục I) chỉ cần Khai báo hóa chất.",
                "timing": "Trước khi mở tờ khai hải quan.",
                "submission_method": "Cổng thông tin Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Giấy phép Nhập khẩu Tiền chất Công nghiệp (Tiền chất ma túy)",
                "issuing_authority": "Cục Hóa chất — Bộ Công Thương",
                "applicable_condition": "BẮT BUỘC cho từng lô hàng chứa tiền chất công nghiệp nhóm 1 và nhóm 2.",
                "exempt_condition": "Không miễn trừ.",
                "timing": "Có giấy phép trước khi đưa hàng về cảng.",
                "submission_method": "Cổng Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Giấy xác nhận Khai báo Hóa chất Nhập khẩu",
                "issuing_authority": "Cục Hóa chất (Hệ thống cấp mã tự động qua NSW)",
                "applicable_condition": "BẮT BUỘC cho toàn bộ hóa chất thuộc Phụ lục V Nghị định 113/2017/NĐ-CP.",
                "exempt_condition": "Hóa chất dưới 1kg làm mẫu thử, hóa chất là thành phần mỹ phẩm, dược phẩm đã được quản lý chuyên ngành.",
                "timing": "Trước khi thông quan hàng hóa.",
                "submission_method": "Cổng NSW: Hệ thống tự động phản hồi Giấy xác nhận có mã số tiếp nhận trong vòng vài phút."
            }
        ],
        "mandatory_certificates": [
            "Phiếu an toàn hóa chất (MSDS) đầy đủ tiếng Việt.",
            "Giấy phép nhập khẩu tiền chất / Giấy xác nhận khai báo hóa chất NSW."
        ],
        "penalties_and_risks": "Không khai báo hóa chất bị phạt tiền từ 20-50 triệu VNĐ; nhập lậu hóa chất hạn chế bị truy cứu trách nhiệm hình sự."
    },
    {
        "category": "Dược phẩm, mỹ phẩm, thực phẩm chức năng & trang thiết bị y tế",
        "keywords": ["thuốc", "dược phẩm", "mỹ phẩm", "thực phẩm chức năng", "thực phẩm bảo vệ sức khỏe", "thiết bị y tế", "trang thiết bị y tế"],
        "hs_patterns": ["^30", "^3304", "^3305", "^9018", "^9019", "^9021", "^9022"],
        "ministry": "Bộ Y Tế (Cục Quản lý Dược, Vụ Trang thiết bị y tế, Cục An toàn thực phẩm)",
        "legal_bases": [
            "Luật Dược số 105/2016/QH13 & Nghị định số 54/2017/NĐ-CP",
            "Thông tư số 06/2011/TT-BYT quy định về quản lý mỹ phẩm",
            "Nghị định số 98/2021/NĐ-CP & Nghị định số 07/2023/NĐ-CP về quản lý trang thiết bị y tế",
            "Nghị định số 15/2018/NĐ-CP về an toàn thực phẩm"
        ],
        "permits": [
            {
                "permit_name": "Phiếu tiếp nhận Phiếu công bố sản phẩm Mỹ phẩm",
                "issuing_authority": "Cục Quản lý Dược — Bộ Y Tế",
                "applicable_condition": "BẮT BUỘC cho 100% sản phẩm mỹ phẩm nhập khẩu thương mại.",
                "exempt_condition": "Hàng mẫu thử nghiệm nghiên cứu không bán ra thị trường (phải có công văn giải trình).",
                "timing": "Phải có Phiếu tiếp nhận có số công bố còn hiệu lực (5 năm) trước khi khai hải quan.",
                "submission_method": "Cổng Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Số lưu hành Trang thiết bị Y tế (Loại A, B, C, D) / Giấy phép Nhập khẩu TTBYT",
                "issuing_authority": "Bộ Y Tế (Vụ Trang thiết bị và Công trình y tế)",
                "applicable_condition": "BẮT BUỘC: Phiếu tiếp nhận công bố tiêu chuẩn áp dụng (Loại A, B) hoặc Giấy chứng nhận đăng ký lưu hành (Loại C, D).",
                "exempt_condition": "Nhập khẩu phục vụ nghiên cứu, viện trợ nhân đạo cần giấy phép riêng.",
                "timing": "Trước khi ký hợp đồng và nhập khẩu hàng hóa.",
                "submission_method": "Hệ thống dịch vụ công trực tuyến quản lý trang thiết bị y tế dmec.moh.gov.vn."
            },
            {
                "permit_name": "Giấy tiếp nhận Bản công bố sản phẩm Thực phẩm chức năng / Bảo vệ sức khỏe",
                "issuing_authority": "Cục An toàn thực phẩm — Bộ Y Tế",
                "applicable_condition": "BẮT BUỘC cho thực phẩm bảo vệ sức khỏe, thực phẩm dinh dưỡng y học.",
                "exempt_condition": "Không miễn trừ đối với hàng kinh doanh.",
                "timing": "Hoàn tất thủ tục công bố trước khi nhập khẩu.",
                "submission_method": "Cổng Một cửa Quốc gia (NSW)."
            }
        ],
        "mandatory_certificates": [
            "Giấy chứng nhận lưu hành tự do (CFS - Certificate of Free Sale) hợp pháp hóa lãnh sự.",
            "Giấy chứng nhận hệ thống quản lý chất lượng ISO 13485 (cho TTBYT).",
            "Số tiếp nhận công bố còn hiệu lực."
        ],
        "penalties_and_risks": "Nhập khẩu mỹ phẩm, dược phẩm hoặc trang thiết bị y tế không có số đăng ký/giấy phép lưu hành sẽ bị phạt tiền kịch khung và buộc tiêu hủy hàng hóa."
    },
    {
        "category": "Thiết bị viễn thông, phát sóng vô tuyến & hiệu suất năng lượng",
        "keywords": ["máy tính", "laptop", "điện thoại", "phát sóng", "thu phát", "wifi", "bluetooth", "điều hòa", "máy giặt", "tủ lạnh", "màn hình"],
        "hs_patterns": ["^8415", "^8418", "^8450", "^8517", "^8528"],
        "ministry": "Bộ Thông tin và Truyền thông & Bộ Công Thương",
        "legal_bases": [
            "Thông tư số 04/2023/TT-BTTTT & Thông tư số 02/2024/TT-BTTTT về hợp quy thiết bị viễn thông",
            "Quyết định số 04/2017/QĐ-TTg của Thủ tướng Chính phủ về dán nhãn năng lượng",
            "Thông tư số 36/2016/TT-BCT quy định dán nhãn năng lượng"
        ],
        "permits": [
            {
                "permit_name": "Giấy phép Nhập khẩu Thiết bị phát, thu-phát sóng vô tuyến điện",
                "issuing_authority": "Cục Tần số vô tuyến điện — Bộ TT&TT",
                "applicable_condition": "Bắt buộc đối với các thiết bị phát sóng đặc thù, trạm phát sóng viễn thông chuyên dụng.",
                "exempt_condition": "Thiết bị phát sóng cự ly ngắn (Wifi, Bluetooth, RFID...) tuân thủ điều kiện kỹ thuật theo Thông tư 08/2021/TT-BTTTT chỉ cần Chứng nhận hợp quy, không cần xin giấy phép nhập khẩu riêng.",
                "timing": "Trước khi làm thủ tục hải quan.",
                "submission_method": "Cổng Một cửa Quốc gia (NSW)."
            },
            {
                "permit_name": "Giấy tiếp nhận Đăng ký Dán nhãn Năng lượng",
                "issuing_authority": "Vụ Tiết kiệm năng lượng và Phát triển bền vững — Bộ Công Thương",
                "applicable_condition": "BẮT BUỘC cho thiết bị điện gia dụng (điều hòa, tủ lạnh, máy giặt, tivi, màn hình máy tính...).",
                "exempt_condition": "Không áp dụng cho linh kiện tháo rời chưa thành thiết bị hoàn chỉnh.",
                "timing": "Sau khi có kết quả thử nghiệm hiệu suất năng lượng đạt chuẩn.",
                "submission_method": "Cổng dịch vụ công Bộ Công Thương."
            }
        ],
        "mandatory_certificates": [
            "Giấy chứng nhận Hợp quy (Do Tổ chức chứng nhận được chỉ định cấp).",
            "Thông báo tiếp nhận Bản công bố hợp quy của Cục Viễn thông.",
            "Phiếu thử nghiệm Hiệu suất năng lượng tối thiểu."
        ],
        "penalties_and_risks": "Nghiêm cấm nhập khẩu thiết bị CNTT, điện tử đã qua sử dụng (CẤM TUYỆT ĐỐI). Hàng mới 100% không chứng nhận hợp quy sẽ không được giải tỏa thông quan."
    },
    {
        "category": "Hàng tiêu dùng, công nghiệp thông thường (Không thuộc diện giấy phép chuyên ngành)",
        "keywords": ["quần áo", "may mặc", "giày", "dép", "bàn", "ghế", "nội thất", "đồ nhựa", "sắt thép thông thường"],
        "hs_patterns": ["^61", "^62", "^64", "^9403", "^3926"],
        "ministry": "Bộ Công Thương (quản lý ngoại thương thông thường)",
        "legal_bases": [
            "Luật Quản lý ngoại thương số 05/2017/QH14",
            "Nghị định số 69/2018/NĐ-CP của Chính phủ",
            "Thông tư số 38/2015/TT-BTC & Thông tư số 39/2018/TT-BTC của Bộ Tài chính"
        ],
        "permits": [
            {
                "permit_name": "Không yêu cầu Giấy phép Nhập khẩu Chuyên ngành",
                "issuing_authority": "Doanh nghiệp tự do kinh doanh xuất nhập khẩu theo quy định Luật Doanh nghiệp",
                "applicable_condition": "Áp dụng cho mọi doanh nghiệp có đăng ký kinh doanh hợp pháp tại Việt Nam.",
                "exempt_condition": "Được phép nhập khẩu tự do không cần xin giấy phép trước.",
                "timing": "Làm thủ tục hải quan bình thường khi hàng đến cảng.",
                "submission_method": "Khai báo tờ khai hải quan điện tử VNACCS/ECUS5."
            }
        ],
        "mandatory_certificates": [
            "Bộ hồ sơ hải quan thương mại thông thường (Hóa đơn thương mại, Packing list, Vận tải đơn, C/O).",
            "Ghi nhãn hàng hóa nhập khẩu theo đúng Nghị định 111/2021/NĐ-CP (sửa đổi Nghị định 43/2017/NĐ-CP)."
        ],
        "penalties_and_risks": "Rủi ro chính là ghi sai nhãn mác xuất xứ hoặc thiếu nhãn phụ tiếng Việt sẽ bị xử phạt từ 2-60 triệu VNĐ theo Nghị định 119/2017/NĐ-CP."
    }
]

def search_permits(query, hs_code=None):
    clean_q = query.strip().lower()
    results = []
    
    # Match by HS code pattern first
    if hs_code:
        clean_hs = hs_code.replace(".", "").strip()
        for item in PERMITS_DATABASE:
            for pattern in item.get("hs_patterns", []):
                if re.search(pattern, clean_hs):
                    results.append(item)
                    break

    # Match by keyword
    for item in PERMITS_DATABASE:
        if item in results:
            continue
        for kw in item["keywords"]:
            if kw in clean_q or clean_q in kw:
                results.append(item)
                break
                
    if not results:
        # Default to general category
        results.append(PERMITS_DATABASE[-1])
        
    return results

def main():
    parser = argparse.ArgumentParser(description="Tra cứu Giấy phép Nhập khẩu & Thủ tục Quản lý Chuyên ngành Nghị định 69/2018/NĐ-CP")
    parser.add_argument("-q", "--query", required=True, help="Tên hàng hóa cần tra cứu (ví dụ: 'đậu tương', 'máy tính', 'thịt bò')")
    parser.add_argument("--hs", default=None, help="Mã số HS hàng hóa (ví dụ: '1201.90.00')")
    args = parser.parse_args()

    matches = search_permits(args.query, args.hs)
    print("=" * 100)
    print(f" KẾT QUẢ TRA CỨU GIẤY PHÉP NHẬP KHẨU & QUẢN LÝ CHUYÊN NGÀNH CHO: '{args.query}' (Mã HS: {args.hs or 'Chưa xác định'})")
    print("=" * 100)

    for i, match in enumerate(matches, 1):
        print(f"\n[{i}] NHÓM QUẢN LÝ: {match['category'].upper()}")
        print(f"    - Cơ quan chủ quản: {match['ministry']}")
        print("    - Căn cứ pháp lý quy định:")
        for law in match["legal_bases"][:3]:
            print(f"      + {law}")
        print("\n    - DANH MỤC GIẤY PHÉP / XÁC NHẬN CHUYÊN NGÀNH CẦN THIẾT:")
        for p in match["permits"]:
            print(f"      * 【{p['permit_name']}】")
            print(f"        - Thẩm quyền cấp : {p['issuing_authority']}")
            print(f"        - Điều kiện áp dụng: {p['applicable_condition']}")
            print(f"        - Điều kiện miễn trừ: {p['exempt_condition']}")
            print(f"        - Thời điểm xin   : {p['timing']}")
            print(f"        - Hình thức nộp  : {p['submission_method']}")
            print("        " + "-" * 70)
        print("\n    - CHỨNG TỪ CHUYÊN NGÀNH BẮT BUỘC:")
        for cert in match["mandatory_certificates"]:
            print(f"      ✔ {cert}")
        print(f"\n    - CẢNH BÁO BẪY RỦI RO & XỬ PHẠT:")
        print(f"      ⚠️ {match['penalties_and_risks']}")
        print("=" * 100)

if __name__ == "__main__":
    main()
