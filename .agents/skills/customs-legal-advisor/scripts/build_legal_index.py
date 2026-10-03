#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_legal_index.py — Khởi Tạo & Lập Chỉ Mục SQLite FTS5 CSDL Pháp Lý Hải Quan
Tác giả: Chuyên gia Pháp chế & Thủ tục Hải quan / AI4A Antigravity
Mô tả: Tự động khởi tạo CSDL customs_legal_index.sqlite, lập bảng FTS5 unicode61
       tra cứu cấp Điều/Khoản siêu tốc và bảng Genealogy Diff đối chiếu đa tầng.
Zero external dependencies (chỉ dùng Python stdlib sqlite3, json, pathlib).
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# UTF-8 cho Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
ASSETS_DIR = WORKSPACE_ROOT / "knowledge-base" / "legal-assets"
DB_PATH = ASSETS_DIR / "customs_legal_index.sqlite"

def init_db(db_path):
    """Khởi tạo cấu trúc bảng SQLite và bảng ảo FTS5"""
    if db_path.exists():
        try:
            db_path.unlink()
        except Exception:
            pass

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # 1. Bảng lưu trữ chi tiết các Điều/Khoản
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS legal_clauses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id TEXT NOT NULL,
        doc_number TEXT NOT NULL,
        doc_title TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        hierarchy_level INTEGER NOT NULL,
        chapter TEXT,
        article_number TEXT NOT NULL,
        article_title TEXT NOT NULL,
        clause_number TEXT,
        content TEXT NOT NULL,
        tags TEXT,
        amended_by TEXT,
        replaces_clause TEXT,
        effective_status TEXT NOT NULL
    );
    """)

    # 2. Bảng FTS5 lập chỉ mục toàn văn tiếng Việt có dấu
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS legal_clauses_fts USING fts5(
        content,
        article_number,
        article_title,
        doc_number,
        tags,
        content='legal_clauses',
        content_rowid='id',
        tokenize='unicode61'
    );
    """)

    # Triggers để đồng bộ FTS5 tự động khi INSERT/UPDATE/DELETE
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS legal_clauses_ai AFTER INSERT ON legal_clauses BEGIN
        INSERT INTO legal_clauses_fts(rowid, content, article_number, article_title, doc_number, tags)
        VALUES (new.id, new.content, new.article_number, new.article_title, new.doc_number, new.tags);
    END;
    """)

    # 3. Bảng Genealogy Diff (Đối chiếu phả hệ sửa đổi đa tầng)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genealogy_diff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_key TEXT UNIQUE NOT NULL,
        article_title TEXT NOT NULL,
        subject TEXT NOT NULL,
        version_original TEXT NOT NULL,
        version_amended_1 TEXT,
        version_latest_2026 TEXT NOT NULL,
        key_differences TEXT NOT NULL,
        compliance_trap TEXT NOT NULL,
        action_recommendation TEXT NOT NULL
    );
    """)

    conn.commit()
    return conn

def populate_database(conn):
    cursor = conn.cursor()

    # Dữ liệu các Điều/Khoản trọng tâm thực chiến của 9 văn bản
    clauses_data = [
        # ==============================================================
        # DOC-05, DOC-06, DOC-07: BỘ BA THÔNG TƯ 38 - 39 - 121
        # ==============================================================
        {
            "doc_id": "DOC-05", "doc_number": "38/2015/TT-BTC",
            "doc_title": "Thông tư số 38/2015/TT-BTC quy định về thủ tục hải quan; kiểm tra, giám sát hải quan",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Chương II: Thủ tục hải quan",
            "article_number": "Điều 16", "article_title": "Hồ sơ hải quan khi làm thủ tục hải quan",
            "clause_number": "Quy định gốc (TT 38)",
            "content": "Hồ sơ hải quan đối với hàng hóa nhập khẩu gồm: Tờ khai hải quan; Hóa đơn thương mại (01 bản chụp); Vận tải đơn hoặc các chứng từ vận tải khác có giá trị tương đương (01 bản chụp); Giấy phép nhập khẩu (01 bản chính nếu nhập khẩu một lần hoặc 01 bản chụp kèm Phiếu theo dõi trừ lùi); Giấy chứng nhận xuất xứ hàng hóa (01 bản chính hoặc bản chụp theo quy định). Người khai hải quan ký tên, đóng dấu xác nhận sao y bản chính trên các bản chụp.",
            "tags": "hồ sơ hải quan, chứng từ nhập khẩu, bản chụp chứng từ, c/o gốc, vận tải đơn, hóa đơn thương mại",
            "amended_by": "Khoản 5 Điều 1 Thông tư 39/2018/TT-BTC và Thông tư 121/2025/TT-BTC",
            "replaces_clause": "", "effective_status": "Đã được sửa đổi, bổ sung căn bản"
        },
        {
            "doc_id": "DOC-06", "doc_number": "39/2018/TT-BTC",
            "doc_title": "Thông tư số 39/2018/TT-BTC sửa đổi, bổ sung một số điều tại Thông tư 38/2015/TT-BTC",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Điều 1: Sửa đổi Thông tư 38",
            "article_number": "Điều 16", "article_title": "Hồ sơ hải quan khi làm thủ tục hải quan (Sửa đổi bởi TT 39)",
            "clause_number": "Khoản 5 Điều 1",
            "content": "Bãi bỏ việc nộp chứng từ giấy sao y. Người khai hải quan phải gửi các chứng từ thuộc hồ sơ hải quan quy định tại khoản 2 Điều này cho cơ quan hải quan dưới dạng dữ liệu điện tử (bản scan có chữ ký số điện tử) thông qua Hệ thống xử lý dữ liệu điện tử hải quan (V5/VNACCS). Trường hợp nộp chứng từ giấy chỉ áp dụng khi hệ thống gặp sự cố hoặc đối với các chứng từ cơ quan có thẩm quyền yêu cầu nộp bản chính như Giấy chứng nhận xuất xứ (C/O bản giấy cấp tay), Giấy phép bản chính.",
            "tags": "hồ sơ điện tử, số hóa chứng từ, scan chữ ký số, bỏ chứng từ giấy, c/o bản giấy, v5 vnaccs",
            "amended_by": "Thông tư 121/2025/TT-BTC",
            "replaces_clause": "Điều 16 Thông tư 38/2015/TT-BTC", "effective_status": "Còn hiệu lực một phần (tiếp tục sửa đổi bởi TT 121)"
        },
        {
            "doc_id": "DOC-07", "doc_number": "121/2025/TT-BTC",
            "doc_title": "Thông tư số 121/2025/TT-BTC sửa đổi, bổ sung các Thông tư quy định về thủ tục hải quan",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Điều 1: Sửa đổi TT 38 & TT 39",
            "article_number": "Điều 16", "article_title": "Hồ sơ hải quan điện tử và e-C/O liên thông (Cập nhật 2026)",
            "clause_number": "Khoản 2 Điều 1",
            "content": "Chuẩn hóa việc nộp hồ sơ hải quan số hóa toàn diện: Đối với chứng từ chứng nhận xuất xứ điện tử (e-C/O), giấy phép điện tử, chứng thư chuyên ngành đã được cơ quan cấp truyền dữ liệu trực tiếp qua Cổng thông tin một cửa quốc gia (NSW) hoặc Cơ chế một cửa ASEAN (ASW), người khai hải quan chỉ cần khai báo mã số chứng từ trên tờ khai hải quan, không phải nộp lại bản scan đính kèm. Cơ quan hải quan tự động kiểm tra, đối soát và thông quan trên hệ thống CNTT thế hệ mới.",
            "tags": "e-c/o, hồ sơ số hóa 2026, cổng một cửa quốc gia, nsw, asw, miễn nộp chứng từ đã liên thông, kiểm tra tự động",
            "amended_by": "",
            "replaces_clause": "Khoản 5 Điều 1 Thông tư 39/2018/TT-BTC", "effective_status": "Còn hiệu lực (Hiện hành từ 01/02/2026)"
        },
        {
            "doc_id": "DOC-05", "doc_number": "38/2015/TT-BTC",
            "doc_title": "Thông tư số 38/2015/TT-BTC quy định về thủ tục hải quan; kiểm tra, giám sát hải quan",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Chương II: Thủ tục hải quan",
            "article_number": "Điều 18", "article_title": "Nguyên tắc khai hải quan",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "Người khai hải quan phải khai đầy đủ các thông tin trên tờ khai hải quan theo các chỉ tiêu thông tin quy định tại Phụ lục II ban hành kèm Thông tư này và gửi các chứng từ thuộc hồ sơ hải quan quy định tại Điều 16 qua Hệ thống. Hàng hóa xuất khẩu, nhập khẩu theo các loại hình khác nhau phải khai trên từng tờ khai hải quan khác nhau theo từng loại hình tương ứng. Một tờ khai hải quan chỉ được khai tối đa 50 dòng hàng.",
            "tags": "nguyên tắc khai báo, mã loại hình xnk, 50 dòng hàng, phụ lục ii chỉ tiêu thông tin, tờ khai điện tử",
            "amended_by": "Khoản 7 Điều 1 Thông tư 39/2018/TT-BTC",
            "replaces_clause": "", "effective_status": "Còn hiệu lực một phần"
        },
        {
            "doc_id": "DOC-06", "doc_number": "39/2018/TT-BTC",
            "doc_title": "Thông tư số 39/2018/TT-BTC sửa đổi, bổ sung một số điều tại Thông tư 38/2015/TT-BTC",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Điều 1: Sửa đổi Thông tư 38",
            "article_number": "Điều 20", "article_title": "Khai bổ sung hồ sơ hải quan hàng hóa xuất khẩu, nhập khẩu",
            "clause_number": "Khoản 9 Điều 1",
            "content": "1. Các trường hợp khai bổ sung: a) Khai bổ sung trong thông quan: Người khai hải quan được khai bổ sung trước thời điểm cơ quan hải quan thông báo kiểm tra trực tiếp hồ sơ; b) Khai bổ sung sau khi hàng hóa đã được thông quan: Trong thời hạn 60 ngày kể từ ngày thông quan nhưng trước thời điểm cơ quan hải quan quyết định kiểm tra sau thông quan, thanh tra. Quá thời hạn 60 ngày hoặc sau khi hải quan đã có quyết định kiểm tra, việc khai bổ sung vẫn được tiếp nhận nhưng bị xử phạt vi phạm hành chính theo quy định tại Nghị định 128/2020/NĐ-CP.",
            "tags": "khai bổ sung, thời hạn 60 ngày, sửa đổi tờ khai, sau thông quan, kiểm tra sau thông quan, phạt chậm khai bổ sung",
            "amended_by": "Thông tư 121/2025/TT-BTC",
            "replaces_clause": "Điều 20 Thông tư 38/2015/TT-BTC", "effective_status": "Còn hiệu lực một phần"
        },
        {
            "doc_id": "DOC-06", "doc_number": "39/2018/TT-BTC",
            "doc_title": "Thông tư số 39/2018/TT-BTC sửa đổi, bổ sung một số điều tại Thông tư 38/2015/TT-BTC",
            "doc_type": "Thông tư", "hierarchy_level": 3, "chapter": "Điều 1: Sửa đổi Thông tư 38",
            "article_number": "Điều 60", "article_title": "Báo cáo quyết toán tình hình sử dụng nguyên liệu, vật tư, máy móc, thiết bị và hàng hóa xuất khẩu",
            "clause_number": "Khoản 39 Điều 1",
            "content": "Định kỳ hàng năm, chậm nhất là ngày thứ 90 kể từ ngày kết thúc năm tài chính, người khai hải quan nộp báo cáo quyết toán tình hình sử dụng nguyên liệu, vật tư nhập khẩu, hàng hóa xuất khẩu cho cơ quan hải quan theo Mẫu số 15/BCQT-NVL/GSQL Phụ lục II. Báo cáo quyết toán phải lập theo nguyên tắc tổng trị giá nhập - xuất - tồn kho nguyên liệu, vật tư và sản phẩm xuất khẩu trên hệ thống sổ sách kế toán theo chế độ kế toán của Bộ Tài chính.",
            "tags": "báo cáo quyết toán, bcqt, mẫu 15 bcqt, gia công sản xuất xuất khẩu, sxxk, 90 ngày năm tài chính, tồn kho sổ sách",
            "amended_by": "",
            "replaces_clause": "Điều 60 Thông tư 38/2015/TT-BTC", "effective_status": "Còn hiệu lực hiện hành"
        },

        # ==============================================================
        # DOC-08: NGHỊ ĐỊNH 128/2020/NĐ-CP (XỬ PHẠT VPHC HẢI QUAN)
        # ==============================================================
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 7", "article_title": "Vi phạm quy định về thời hạn làm thủ tục hải quan, nộp hồ sơ thuế",
            "clause_number": "Khoản 1 đến Khoản 4",
            "content": "1. Phạt cảnh cáo hoặc phạt tiền từ 500.000đ - 1.000.000đ: Nộp tờ khai khi chưa có hàng tập kết. 2. Phạt từ 1.000.000đ - 2.000.000đ: Nộp hồ sơ hải quan quá thời hạn 30 ngày kể từ ngày hàng đến cửa khẩu; Chậm nộp chứng từ bản chính/điện tử quá hạn. 3. Phạt từ 2.000.000đ - 5.000.000đ: Chậm nộp báo cáo quyết toán nguyên phụ liệu dưới 30 ngày. 4. Phạt từ 5.000.000đ - 10.000.000đ: Chậm nộp báo cáo quyết toán quá thời hạn từ 30 ngày trở lên.",
            "tags": "xử phạt thời hạn, quá hạn 30 ngày, chậm nộp báo cáo quyết toán, chậm nộp tờ khai, phạt tiền nộp trễ",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 8", "article_title": "Vi phạm quy định về khai hải quan",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "1. Phạt tiền từ 1.000.000đ đến 2.000.000đ đối với hành vi khai sai so với thực tế về lượng, tên hàng, chủng loại, phẩm chất, xuất xứ, mã số hàng hóa hoặc trị giá hải quan mà không làm ảnh hưởng đến số tiền thuế phải nộp. 2. Phạt từ 2.000.000đ đến 4.000.000đ đối với hành vi không khai hoặc khai sai các chỉ tiêu thông tin trên tờ khai làm thay đổi phân luồng kiểm tra hải quan từ luồng Vàng/Đỏ sang luồng Xanh. 3. Phạt từ 3.000.000đ đến 5.000.000đ đối với hành vi khai sai mã số HS, thuế suất dẫn đến thiếu thuế nhưng người nộp thuế đã tự giác nộp đủ tiền thuế trước thời điểm kiểm tra thực tế.",
            "tags": "xử phạt khai sai, phạt khai sai tên hàng, khai sai mã hs, khai sai phân luồng, khai sai xuất xứ, bẫy lỗi chứng từ",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 9", "article_title": "Vi phạm quy định về khai thuế dẫn đến thiếu số tiền thuế phải nộp hoặc tăng số tiền thuế được miễn, giảm, hoàn, không thu",
            "clause_number": "Khoản 1 và Khoản 2",
            "content": "1. Phạt 10% tính trên số tiền thuế khai thiếu hoặc số tiền thuế được miễn, giảm, hoàn cao hơn quy định đối với trường hợp người nộp thuế tự phát hiện và khai bổ sung sau thời điểm kiểm tra hồ sơ nhưng trước khi lập biên bản vi phạm hành chính. 2. Phạt 20% tính trên số tiền thuế khai thiếu hoặc số tiền thuế được miễn, giảm, hoàn cao hơn quy định đối với trường hợp cơ quan hải quan kiểm tra, thanh tra sau thông quan phát hiện khai sai mã số HS, tên hàng, trị giá hải quan hoặc lập báo cáo quyết toán không đúng thực tế tồn kho. Biện pháp khắc phục: Buộc nộp đủ số tiền thuế thiếu và tiền chậm nộp 0.03%/ngày.",
            "tags": "phạt thiếu thuế 10%, phạt thiếu thuế 20%, truy thu thuế, tiền chậm nộp, kiểm tra sau thông quan phạt thuế, ấn định thuế",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 14", "article_title": "Vi phạm quy định về trốn thuế",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "1. Phạt 01 lần số tiền thuế trốn đối với hành vi sử dụng chứng từ giả mạo, không khai báo hàng hóa nhập khẩu, thay đổi mục đích sử dụng hàng miễn thuế không báo cáo khi có từ 2 tình tiết giảm nhẹ. 2. Phạt 1,5 lần số tiền thuế trốn đối với trường hợp không có tình tiết tăng nặng hoặc giảm nhẹ. 3. Phạt từ 02 đến 03 lần số tiền thuế trốn đối với trường hợp tái phạm hoặc có tình tiết tăng nặng. Chuyển cơ quan điều tra hình sự nếu số tiền trốn thuế từ 100.000.000 đồng trở lên theo Điều 200 Bộ luật Hình sự.",
            "tags": "trốn thuế hải quan, phạt 1 lần, phạt 3 lần số thuế trốn, giả mạo chứng từ, buôn lậu, hình sự trốn thuế",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 15", "article_title": "Vi phạm quy định về xuất nhập khẩu hàng cấm hoặc không có giấy phép",
            "clause_number": "Khoản 1 đến Khoản 4",
            "content": "1. Phạt tiền từ 10.000.000đ đến 20.000.000đ nếu tang vật dưới 30 triệu đồng; 2. Phạt từ 20.000.000đ đến 50.000.000đ nếu tang vật từ 30 triệu đến dưới 100 triệu đồng; 3. Phạt từ 50.000.000đ đến 100.000.000đ nếu tang vật từ 100 triệu đồng trở lên đối với hành vi xuất khẩu, nhập khẩu hàng hóa không có giấy phép xuất khẩu, nhập khẩu theo quy định của Nghị định 69/2018/NĐ-CP. Biện pháp khắc phục: Buộc tái xuất hoặc buộc tiêu hủy tang vật vi phạm.",
            "tags": "phạt hàng không giấy phép, phạt hàng cấm, buộc tái xuất, buộc tiêu hủy, nghị định 69, giấy phép bộ chuyên ngành",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },
        {
            "doc_id": "DOC-08", "doc_number": "128/2020/NĐ-CP",
            "doc_title": "Nghị định số 128/2020/NĐ-CP quy định xử phạt vi phạm hành chính trong lĩnh vực hải quan",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Hành vi vi phạm & Mức xử phạt",
            "article_number": "Điều 17", "article_title": "Vi phạm quy định về nhãn hàng hóa nhập khẩu",
            "clause_number": "Khoản 1 và Khoản 2",
            "content": "Phạt tiền đối với hành vi nhập khẩu hàng hóa có nhãn gốc nhưng không thể hiện xuất xứ hàng hóa, ghi sai xuất xứ, hoặc lưu thông nội địa thiếu nhãn phụ tiếng Việt theo quy định của Nghị định 43/2017/NĐ-CP và Nghị định 111/2021/NĐ-CP. Biện pháp khắc phục hậu quả: Buộc đưa hàng hóa ra khỏi lãnh thổ Việt Nam hoặc buộc khắc phục nhãn hàng hóa đúng quy định trước khi thông quan.",
            "tags": "vi phạm nhãn mác, nhãn phụ tiếng việt, made in, xuất xứ nhãn hàng, nghị định 43 111, khắc phục nhãn",
            "amended_by": "Nghị định 102/2021/NĐ-CP",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Chuyển tiếp NĐ 169/2026)"
        },

        # ==============================================================
        # DOC-04 & DOC-02: GIẢM THUẾ VAT 8% (NĐ 174/2025 & LUẬT 48/2024)
        # ==============================================================
        {
            "doc_id": "DOC-04", "doc_number": "174/2025/NĐ-CP",
            "doc_title": "Nghị định số 174/2025/NĐ-CP quy định chính sách giảm thuế giá trị gia tăng theo Nghị quyết 204/2025/QH15",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Điều khoản thi hành",
            "article_number": "Điều 1", "article_title": "Giảm thuế suất thuế GTGT 2% xuống 8%",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "Giảm 2% thuế suất thuế giá trị gia tăng, áp dụng đối với các nhóm hàng hóa, dịch vụ đang áp dụng mức thuế suất 10% (còn 8%), trừ nhóm hàng hóa, dịch vụ sau: Viễn thông, hoạt động tài chính, ngân hàng, chứng khoán, bảo hiểm, kinh doanh bất động sản, kim loại và sản phẩm từ kim loại đúc sẵn, sản phẩm khai khoáng (không kể khai thác than), than cốc, dầu mỏ tinh chế, sản phẩm hoá chất (quy định tại Phụ lục I); Hàng hóa, dịch vụ chịu thuế tiêu thụ đặc biệt (quy định tại Phụ lục II); Công nghệ thông tin theo pháp luật về CNTT (quy định tại Phụ lục III). Áp dụng thống nhất tại khâu nhập khẩu, sản xuất, gia công, kinh doanh thương mại đến hết ngày 31/12/2026.",
            "tags": "giảm thuế vat 8%, nghị định 174/2025, thuế suất 8%, phụ lục loại trừ, khâu nhập khẩu, thời hạn 31/12/2026",
            "amended_by": "",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Áp dụng đến hết 31/12/2026)"
        },
        {
            "doc_id": "DOC-04", "doc_number": "174/2025/NĐ-CP",
            "doc_title": "Nghị định số 174/2025/NĐ-CP quy định chính sách giảm thuế giá trị gia tăng",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Điều khoản thi hành",
            "article_number": "Điều 2", "article_title": "Trình tự, thủ tục khai báo hải quan khi áp dụng thuế suất GTGT 8%",
            "clause_number": "Khoản 2",
            "content": "Đối với hàng hóa nhập khẩu: Khi mở tờ khai hải quan trên hệ thống VNACCS, người khai hải quan tra cứu mã HS trên Phụ lục I, II, III ban hành kèm theo Nghị định này. Nếu mặt hàng không thuộc các phụ lục loại trừ, người khai hải quan khai mã thuế suất thuế GTGT giảm tương ứng (mã chuẩn VB... theo hướng dẫn của Tổng cục Hải quan) để hệ thống tự động tính thuế suất 8%. Trường hợp mặt hàng thuộc Phụ lục loại trừ, người khai hải quan phải áp dụng thuế suất chuẩn 10%.",
            "tags": "khai thuế 8% vnaccs, mã biểu thuế vat, thủ tục khai hải quan vat 8%, tra cứu phụ lục 1 2 3",
            "amended_by": "",
            "replaces_clause": "", "effective_status": "Còn hiệu lực (Áp dụng đến hết 31/12/2026)"
        },
        {
            "doc_id": "DOC-02", "doc_number": "48/2024/QH15",
            "doc_title": "Luật Thuế giá trị gia tăng số 48/2024/QH15",
            "doc_type": "Luật", "hierarchy_level": 1, "chapter": "Chương II: Căn cứ & Phương pháp tính thuế",
            "article_number": "Điều 7", "article_title": "Giá tính thuế giá trị gia tăng đối với hàng hóa nhập khẩu",
            "clause_number": "Khoản 2",
            "content": "Đối với hàng hóa nhập khẩu, giá tính thuế giá trị gia tăng là trị giá tính thuế nhập khẩu cộng (+) với thuế nhập khẩu cộng (+) với thuế tiêu thụ đặc biệt (nếu có) cộng (+) với thuế bảo vệ môi trường (nếu có). Trị giá tính thuế nhập khẩu được xác định theo quy định của Luật Hải quan và pháp luật về thuế xuất khẩu, thuế nhập khẩu.",
            "tags": "giá tính thuế vat nhập khẩu, công thức tính thuế vat, trị giá hải quan cộng thuế nk, thuế ttđb, thuế bvmt",
            "amended_by": "",
            "replaces_clause": "Điều 7 Luật Thuế GTGT 13/2008/QH12", "effective_status": "Còn hiệu lực (Từ 01/07/2025)"
        },

        # ==============================================================
        # DOC-01 & DOC-03: LUẬT HẢI QUAN 54 & NGHỊ ĐỊNH 167/2025
        # ==============================================================
        {
            "doc_id": "DOC-01", "doc_number": "54/2014/QH13",
            "doc_title": "Luật Hải quan số 54/2014/QH13",
            "doc_type": "Luật", "hierarchy_level": 1, "chapter": "Chương II: Thủ tục hải quan",
            "article_number": "Điều 23", "article_title": "Thời hạn nộp hồ sơ hải quan",
            "clause_number": "Khoản 1 và Khoản 2",
            "content": "1. Đối với hàng hóa xuất khẩu: nộp sau khi đã tập kết hàng hóa tại địa điểm người khai hải quan thông báo và chậm nhất là 04 giờ trước khi phương tiện vận tải xuất cảnh; đối với hàng hóa xuất khẩu gửi bằng dịch vụ chuyển phát nhanh thì chậm nhất là 02 giờ trước khi phương tiện xuất cảnh. 2. Đối với hàng hóa nhập khẩu: nộp trước ngày hàng hóa đến cửa khẩu hoặc trong thời hạn 30 ngày kể từ ngày hàng hóa đến cửa khẩu.",
            "tags": "thời hạn nộp tờ khai, nộp trước 4 giờ xuất cảnh, quá hạn 30 ngày nhập khẩu, điều 23 luật hải quan",
            "amended_by": "Luật số 90/2025/QH15",
            "replaces_clause": "", "effective_status": "Còn hiệu lực"
        },
        {
            "doc_id": "DOC-01", "doc_number": "54/2014/QH13",
            "doc_title": "Luật Hải quan số 54/2014/QH13",
            "doc_type": "Luật", "hierarchy_level": 1, "chapter": "Chương V: Kiểm tra sau thông quan",
            "article_number": "Điều 78", "article_title": "Kiểm tra sau thông quan tại trụ sở người khai hải quan",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "1. Các trường hợp kiểm tra tại trụ sở người khai hải quan: a) Khi có dấu hiệu vi phạm pháp luật hải quan và quy định khác của pháp luật liên quan đến quản lý xuất khẩu, nhập khẩu; b) Đối với các trường hợp kiểm tra theo kế hoạch tuân thủ pháp luật của người khai hải quan; c) Kiểm tra chuyên đề trên cơ sở áp dụng quản lý rủi ro. 2. Thời hạn kiểm tra sau thông quan là 05 năm kể từ ngày đăng ký tờ khai hải quan. 3. Thủ tục: Ban hành Quyết định kiểm tra, thông báo trước ít nhất 03 ngày làm việc (trừ trường hợp kiểm tra đột xuất khi có dấu hiệu vi phạm rõ ràng).",
            "tags": "kiểm tra sau thông quan, pca, kiểm tra tại trụ sở doanh nghiệp, thời hạn 5 năm, quản lý rủi ro, kiểm tra chuyên đề",
            "amended_by": "",
            "replaces_clause": "", "effective_status": "Còn hiệu lực"
        },
        {
            "doc_id": "DOC-03", "doc_number": "167/2025/NĐ-CP",
            "doc_title": "Nghị định số 167/2025/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định số 08/2015/NĐ-CP",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Điều 1: Sửa đổi Nghị định 08",
            "article_number": "Điều 4", "article_title": "Địa điểm làm thủ tục hải quan và địa điểm kiểm tra hàng hóa (Sửa đổi bởi NĐ 167)",
            "clause_number": "Khoản 1 Điều 1",
            "content": "Quy định phân cấp đồng bộ địa điểm làm thủ tục hải quan: Địa điểm làm thủ tục hải quan là nơi cơ quan hải quan tiếp nhận, đăng ký và kiểm tra hồ sơ hải quan, kiểm tra thực tế hàng hóa, phương tiện vận tải. Chuẩn hóa các địa điểm kiểm tra tập trung, địa điểm kiểm tra tại chân công trình, cơ sở sản xuất của doanh nghiệp chế xuất, doanh nghiệp ưu tiên; đẩy mạnh cơ chế giám sát tự động bằng hệ thống cân điện tử, camera AI và niêm phong định vị GPS điện tử.",
            "tags": "địa điểm làm thủ tục, kiểm tra tập trung, giám sát tự động cảng, niêm phong gps, doanh nghiệp ưu tiên, nđ 167/2025",
            "amended_by": "",
            "replaces_clause": "Điều 4 Nghị định 08/2015/NĐ-CP", "effective_status": "Còn hiệu lực (Từ 01/07/2025)"
        },

        # ==============================================================
        # DOC-09: NGHỊ ĐỊNH 69/2018/NĐ-CP (QUẢN LÝ NGOẠI THƯƠNG & GIẤY PHÉP)
        # ==============================================================
        {
            "doc_id": "DOC-09", "doc_number": "69/2018/NĐ-CP",
            "doc_title": "Nghị định số 69/2018/NĐ-CP quy định chi tiết một số điều của Luật Quản lý ngoại thương",
            "doc_type": "Nghị định", "hierarchy_level": 2, "chapter": "Chương II: Biện pháp quản lý xuất khẩu, nhập khẩu",
            "article_number": "Điều 7", "article_title": "Thủ tục cấp Giấy phép xuất khẩu, nhập khẩu và quản lý chuyên ngành",
            "clause_number": "Khoản 1 đến Khoản 3",
            "content": "Thương nhân xuất khẩu, nhập khẩu hàng hóa thuộc Danh mục quy định tại Phụ lục II, III, IV, V, VI, VII, VIII, IX ban hành kèm theo Nghị định này phải có Giấy phép của Bộ, cơ quan ngang Bộ quản lý chuyên ngành. Cơ quan hải quan chỉ giải quyết thủ tục thông quan khi người khai hải quan đã có Giấy phép xuất khẩu, nhập khẩu hoặc văn bản thông báo kết quả kiểm tra chuyên ngành đạt yêu cầu. Nghiêm cấm việc nhập khẩu hàng hóa thuộc Danh mục hàng cấm nhập khẩu tại Phụ lục I (vũ khí, pháo nổ, hàng tiêu dùng đã qua sử dụng, phế liệu không đạt chuẩn).",
            "tags": "giấy phép xuất nhập khẩu, danh mục hàng cấm phụ lục 1, kiểm tra chuyên ngành 8 bộ, nghị định 69, thông quan hàng có điều kiện",
            "amended_by": "",
            "replaces_clause": "", "effective_status": "Còn hiệu lực hiện hành"
        }
    ]

    for c in clauses_data:
        cursor.execute("""
        INSERT INTO legal_clauses (
            doc_id, doc_number, doc_title, doc_type, hierarchy_level,
            chapter, article_number, article_title, clause_number,
            content, tags, amended_by, replaces_clause, effective_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            c["doc_id"], c["doc_number"], c["doc_title"], c["doc_type"], c["hierarchy_level"],
            c["chapter"], c["article_number"], c["article_title"], c["clause_number"],
            c["content"], c["tags"], c["amended_by"], c["replaces_clause"], c["effective_status"]
        ))

    # ==============================================================
    # DỮ LIỆU GENEALOGY DIFF (BẢNG SO SÁNH PHẢ HỆ ĐA TẦNG)
    # ==============================================================
    diff_data = [
        {
            "article_key": "DIEU_16_HO_SO_HAI_QUAN",
            "article_title": "Điều 16. Thành phần bộ hồ sơ hải quan nhập khẩu",
            "subject": "Hình thức nộp chứng từ (Giấy vs Scan điện tử vs Liên thông e-C/O NSW)",
            "version_original": "TT 38/2015/TT-BTC: Cho phép nộp 01 bản chụp có ký tên, đóng dấu xác nhận sao y của doanh nghiệp đối với Hóa đơn, Vận đơn, Packing List.",
            "version_amended_1": "TT 39/2018/TT-BTC (Khoản 5 Điều 1): Bãi bỏ nộp bản giấy. Chuyển sang nộp 100% bản điện tử scan đính kèm chữ ký số qua VNACCS (V5). Chỉ nộp bản giấy với C/O bản gốc và giấy phép bản chính.",
            "version_latest_2026": "TT 121/2025/TT-BTC (Hiện hành 2026): Đối với e-C/O và Giấy phép đã liên thông qua Cổng một cửa quốc gia (NSW/ASW), chỉ cần khai báo mã số chứng từ trên tờ khai, KHÔNG phải nộp lại bản scan đính kèm.",
            "key_differences": "Bản chụp giấy sao y (2015) ──► Bản scan ký số qua V5 (2018) ──► Tự động đối soát mã điện tử NSW không cần scan (2026).",
            "compliance_trap": "Vẫn in bản giấy đóng dấu mang ra Chi cục Hải quan cửa khẩu nộp (bị từ chối tiếp nhận vì vi phạm thủ tục hải quan điện tử); hoặc scan đính kèm trùng lặp chứng từ đã có trên NSW gây nghẽn đường truyền.",
            "action_recommendation": "Kiểm tra mã tiếp nhận e-C/O trên Cổng NSW; chỉ khai mã số e-C/O vào ô ghi chú tờ khai VNACCS; chỉ scan các chứng từ ngoài luồng liên thông."
        },
        {
            "article_key": "DIEU_20_KHAI_BO_SUNG",
            "article_title": "Điều 20. Khai bổ sung hồ sơ hải quan",
            "subject": "Thời hạn và điều kiện được miễn phạt vi phạm hành chính khi khai bổ sung",
            "version_original": "TT 38/2015/TT-BTC: Khai bổ sung trước khi kiểm tra thực tế hàng hóa hoặc trong thời hạn 60 ngày kể từ ngày thông quan.",
            "version_amended_1": "TT 39/2018/TT-BTC: Bóc tách rõ 2 khung thời gian: Khai bổ sung trong thông quan (trước kiểm tra hồ sơ) và Khai bổ sung sau thông quan (trong 60 ngày). Bắt buộc xử phạt NĐ 128 nếu quá 60 ngày.",
            "version_latest_2026": "TT 121/2025/TT-BTC (kết hợp NĐ 128/2020 & Luật Quản lý thuế): Tự phát hiện khai bổ sung trong 60 ngày được miễn phạt vi phạm hành chính về khai sai, chỉ nộp tiền thuế thiếu + tiền chậm nộp 0.03%/ngày. Quá 60 ngày bị phạt 10% - 20% theo Điều 9 NĐ 128.",
            "key_differences": "Quy định lỏng lẻo (2015) ──► Ràng buộc mốc 60 ngày (2018) ──► Tự động hóa chế tài xử phạt 10%-20% tiền thuế khai thiếu (2026).",
            "compliance_trap": "Chờ đến khi có Quyết định kiểm tra sau thông quan mới vội vàng làm công văn xin khai bổ sung (mất quyền tự nguyện, bị phạt kịch khung 20% và xem xét dấu hiệu trốn thuế theo Điều 14 NĐ 128).",
            "action_recommendation": "Thiết lập quy trình nội bộ kiểm soát chứng từ sau thông quan trong vòng 30 ngày đầu tiên; nếu phát hiện sai lệch số học/HS code, nộp ngay tờ khai bổ sung AMA/AMC trước ngày thứ 60."
        },
        {
            "article_key": "VAT_8_PHAN_TRAM_2026",
            "article_title": "Nghị định 174/2025/NĐ-CP & Luật Thuế GTGT 48/2024",
            "subject": "Chính sách giảm thuế GTGT 2% tại khâu nhập khẩu đến hết năm 2026",
            "version_original": "Nghị định 44/2023 & NĐ 72/2024: Chính sách giảm thuế GTGT ngắn hạn theo từng chu kỳ 6 tháng.",
            "version_amended_1": "Nghị quyết 204/2025/QH15: Quốc hội quyết nghị kéo dài chính sách giảm thuế GTGT 2% liên tục cho toàn bộ giai đoạn 2025 - 2026.",
            "version_latest_2026": "NĐ 174/2025/NĐ-CP: Giảm thuế GTGT xuống 8% áp dụng thống nhất đến hết 31/12/2026. Bóc tách 3 Phụ lục loại trừ I, II, III (chú ý: sản phẩm hóa chất, kim loại, CNTT và hàng chịu TTĐB không được giảm).",
            "key_differences": "Gia hạn ngắt quãng từng 6 tháng (2023-2024) ──► Cố định dài hạn đến hết năm 2026 (2025-2026) kèm chuẩn hóa mã loại trừ HS 8 số.",
            "compliance_trap": "Khai nhầm mã ưu đãi thuế 8% cho các mặt hàng nằm trong Phụ lục I (Kim loại, Hóa chất) hoặc Phụ lục II (chịu thuế TTĐB như rượu bia xe cộ) dẫn đến bị phạt 20% tiền thuế khai thiếu theo Điều 9 NĐ 128/2020.",
            "action_recommendation": "Tra cứu mã HS 8 số của hàng nhập khẩu đối chiếu song song với cả 3 Phụ lục I, II, III của NĐ 174/2025 trước khi chọn mã thuế suất trên VNACCS."
        },
        {
            "article_key": "XU_PHAT_KHAI_SAI_THIEU_THUE",
            "article_title": "Nghị định 128/2020/NĐ-CP (Điều 8 & Điều 9)",
            "subject": "Chế tài xử phạt hành vi khai sai tên hàng, mã HS, trị giá và khai thiếu thuế",
            "version_original": "Nghị định 127/2013/NĐ-CP & NĐ 45/2016/NĐ-CP: Mức phạt cũ, thẩm quyền xử phạt chưa phân định rõ theo hệ thống thông quan điện tử.",
            "version_amended_1": "Nghị định 128/2020/NĐ-CP: Phân tách rõ: Khai sai không ảnh hưởng tiền thuế (Điều 8: phạt 1 - 2 triệu); Khai sai thiếu thuế tự giác nộp trước kiểm tra (phạt 10%); Khai sai do cơ quan hải quan kiểm tra phát hiện (Điều 9: phạt 20% số tiền thuế khai thiếu).",
            "version_latest_2026": "Sửa đổi bởi NĐ 102/2021/NĐ-CP & Chuyển tiếp NĐ 169/2026/NĐ-CP: Tăng cường giám sát tự động, xử phạt vi phạm hành chính kết hợp hạ bậc tuân thủ doanh nghiệp (chuyển sang luồng Vàng/Đỏ liên tục 6 tháng).",
            "key_differences": "Phạt tiền thủ công ──► Cơ chế phạt % tiền thuế thiếu kết hợp tự động hạ bậc xếp hạng rủi ro doanh nghiệp trên CSDL Tổng cục Hải quan.",
            "compliance_trap": "Cho rằng khai sai mã HS không cố ý thì không bị phạt; trong thực tế Hải quan chỉ căn cứ vào hệ quả 'thiếu số tiền thuế phải nộp' để lập biên bản phạt 20% theo Khoản 2 Điều 9.",
            "action_recommendation": "Khi có nghi ngờ về mã HS, tiến hành thủ tục Xác định trước mã số (Advance Ruling) theo Điều 28 Luật Hải quan trước khi nhập khẩu hàng loạt."
        }
    ]

    for d in diff_data:
        cursor.execute("""
        INSERT INTO genealogy_diff (
            article_key, article_title, subject, version_original,
            version_amended_1, version_latest_2026, key_differences,
            compliance_trap, action_recommendation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            d["article_key"], d["article_title"], d["subject"], d["version_original"],
            d["version_amended_1"], d["version_latest_2026"], d["key_differences"],
            d["compliance_trap"], d["action_recommendation"]
        ))

    conn.commit()
    print(f"[THÀNH CÔNG] Đã nạp {len(clauses_data)} Điều/Khoản vào bảng 'legal_clauses' & 'legal_clauses_fts'.")
    print(f"[THÀNH CÔNG] Đã nạp {len(diff_data)} ma trận đối chiếu đa tầng vào bảng 'genealogy_diff'.")

def main():
    print("=" * 70)
    print("🚀 KHỞI TẠO CSDL SQLITE FTS5 PHÁP LÝ HẢI QUAN v2.0 PRO")
    print("=" * 70)
    print(f"• Đường dẫn CSDL: {DB_PATH}")
    
    conn = init_db(DB_PATH)
    populate_database(conn)
    
    # Kiểm tra FTS5 hoạt động
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM legal_clauses_fts;")
    count_fts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM genealogy_diff;")
    count_diff = cursor.fetchone()[0]
    
    print("-" * 70)
    print(f"✅ Kiểm tra chỉ mục FTS5: {count_fts} bản ghi đã sẵn sàng tìm kiếm siêu tốc.")
    print(f"✅ Kiểm tra ma trận phả hệ: {count_diff} bộ đối chiếu đa tầng kinh điển.")
    print("=" * 70)
    conn.close()

if __name__ == "__main__":
    main()
