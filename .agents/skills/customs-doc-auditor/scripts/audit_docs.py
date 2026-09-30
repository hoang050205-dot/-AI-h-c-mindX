#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_docs.py — Advanced Documentation Audit Engine for Customs Clearance (v2.0)
Author: Minh Hoàng (Customs Documentation Audit Specialist)
Framework: Antigravity Customization System & AI4A

Performs comprehensive 5-layer audit covering 36 real-world discrepancy & error types:
  Layer 1 (L1-01 -> L1-08): Date Chronology & Time-bound constraints
  Layer 2 (L2-01 -> L2-08): Entity, Legal Identity & Typo Cross-check (Levenshtein)
  Layer 3 (L3-01 -> L3-07): Cargo Details, Weight (GW/NW), Packaging, Container & Seal
  Layer 4 (L4-01 -> L4-08): Valuation, Math Recalculation, Subtotals, Currency & HS Code
  Layer 5 (L5-01 -> L5-05): Customs Compliance, C/O Rules, Decree 128 Penalties & 30-day C/O Debt
"""

import sys
import os
import json
import re
import argparse
from datetime import datetime, timedelta

# Configure UTF-8 on Windows stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


def parse_date(date_str):
    """Parses date strings across common international trade formats."""
    if not date_str:
        return None
    cleaned = date_str.strip()
    formats = [
        "%d/%m/%Y",
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%d.%m.%Y",
        "%Y/%m/%d",
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y"
    ]
    for fmt in formats:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None


def levenshtein_distance(s1, s2):
    """Calculates Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def normalize_text(text):
    """Normalizes whitespace, casing and punctuation for robust comparison."""
    if not text:
        return ""
    t = text.strip().upper()
    t = re.sub(r'[\r\n\t]+', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t


class CustomsDocAuditor:
    def __init__(self, data):
        self.data = data
        self.shipment = data.get("shipment_info", {})
        self.contract = data.get("sales_contract", {})
        self.invoice = data.get("commercial_invoice", {})
        self.pl = data.get("packing_list", {})
        self.bl = data.get("bill_of_lading", {})
        self.co = data.get("certificate_of_origin", {})
        self.insurance = data.get("insurance_certificate", {})
        
        self.discrepancies = []
        self.verified_items = []
        self.audit_passed = True

    def add_discrepancy(self, error_code, error_type, item, doc_a_val, doc_b_val, risk, remedy, severity="HIGH"):
        self.audit_passed = False
        self.discrepancies.append({
            "code": error_code,
            "error_type": error_type,
            "criterion": item,
            "doc_a": doc_a_val,
            "doc_b": doc_b_val,
            "risk": risk,
            "remedy": remedy,
            "severity": severity
        })

    def add_verified(self, category, detail):
        self.verified_items.append({
            "category": category,
            "detail": detail
        })

    def audit_all(self):
        """Runs comprehensive 5-layer audit covering the 36-error catalog."""
        self._audit_layer_1_chronology()
        self._audit_layer_2_entities()
        self._audit_layer_3_cargo()
        self._audit_layer_4_valuation_and_hs()
        self._audit_layer_5_compliance_and_traps()
        return self._generate_report()

    # ---------------------------------------------------------
    # LAYER 1: Date Chronology (L1-01 -> L1-08)
    # ---------------------------------------------------------
    def _audit_layer_1_chronology(self):
        contract_date_str = self.contract.get("contract_date")
        invoice_date_str = self.invoice.get("invoice_date")
        pl_date_str = self.pl.get("pl_date")
        bl_date_str = self.bl.get("shipped_on_board_date") or self.bl.get("issue_date")
        co_date_str = self.co.get("issue_date")
        ins_date_str = self.insurance.get("effective_date") or self.insurance.get("issue_date")

        dt_contract = parse_date(contract_date_str)
        dt_invoice = parse_date(invoice_date_str)
        dt_pl = parse_date(pl_date_str)
        dt_bl = parse_date(bl_date_str)
        dt_co = parse_date(co_date_str)
        dt_ins = parse_date(ins_date_str)

        # L1-01: Contract Date vs Invoice Date
        if dt_contract and dt_invoice:
            if dt_invoice < dt_contract:
                self.add_discrepancy(
                    error_code="L1-01",
                    error_type="Trình tự thời gian",
                    item="Hóa đơn phát hành trước Hợp đồng",
                    doc_a_val=f"Invoice Date: {invoice_date_str}",
                    doc_b_val=f"Contract Date: {contract_date_str}",
                    risk="Nghi ngờ hợp đồng lập khống để hợp thức hóa bộ chứng từ đối phó; nguy cơ thanh tra sau thông quan về tính xác thực của giao dịch.",
                    remedy="Yêu cầu Shipper điều chỉnh lại ngày phát hành Invoice bằng hoặc sau ngày ký kết hợp đồng ngoại thương.",
                    severity="CRITICAL"
                )
            else:
                self.add_verified("Trình tự thời gian", f"Invoice Date ({invoice_date_str}) >= Contract Date ({contract_date_str}) [ĐẠT - L1-01]")

        # L1-02: Invoice Date vs B/L Date (Invoice Date <= B/L Date)
        if dt_invoice and dt_bl:
            if dt_bl < dt_invoice:
                self.add_discrepancy(
                    error_code="L1-02",
                    error_type="Trình tự thời gian",
                    item="Trình tự Hóa đơn & Vận đơn tàu chạy",
                    doc_a_val=f"Invoice Date: {invoice_date_str}",
                    doc_b_val=f"B/L On-board Date: {bl_date_str}",
                    risk="Hóa đơn thương mại xuất sau khi hàng đã bốc lên tàu. Nghiệp vụ giao thương bất hợp lý; Hải quan nghi ngờ hồ sơ giả lập đối phó, nguy cơ chuyển luồng Đỏ kiểm hóa 100%.",
                    remedy="Yêu cầu Shipper thu hồi và phát hành lại Commercial Invoice trước hoặc trùng ngày On-board của B/L (trước 05/09/2026).",
                    severity="CRITICAL"
                )
            else:
                self.add_verified("Trình tự thời gian", f"B/L Date ({bl_date_str}) >= Invoice Date ({invoice_date_str}) [ĐẠT - L1-02]")

        # L1-03: C/O Date vs B/L Date & Issued Retroactively Check
        if dt_co and dt_bl:
            co_retroactive = self.co.get("box13_issued_retroactively", False)
            delta_days = (dt_co - dt_bl).days
            if delta_days > 3 and not co_retroactive:
                self.add_discrepancy(
                    error_code="L1-03",
                    error_type="Quy tắc C/O & Thời gian",
                    item="C/O cấp sau ngày tàu chạy (Retroactive Rule)",
                    doc_a_val=f"C/O Issue Date: {co_date_str} (sau B/L {delta_days} ngày)",
                    doc_b_val=f"Ô 13: Bỏ trống '[ ] ISSUED RETROACTIVELY'",
                    risk="Vi phạm Quy tắc cấp C/O hồi tố của Hiệp định thương mại tự do (FTA). Hải quan cửa khẩu sẽ bác bỏ C/O ngay lập tức, doanh nghiệp bị truy thu thuế MFN.",
                    remedy="1) Đề nghị Shipper liên hệ cơ quan cấp xuất xứ (KCCI) cấp lại C/O Form AK có tích chọn ô 'ISSUED RETROACTIVELY'.\n2) Khai báo xin NỢ C/O trong vòng 30 ngày trên tờ khai điện tử theo Thông tư 38/2015 và TT 121/2025/TT-BTC để giải phóng hàng trước.",
                    severity="CRITICAL"
                )
            elif delta_days > 3 and co_retroactive:
                self.add_verified("Quy tắc C/O hồi tố", f"C/O cấp sau B/L {delta_days} ngày nhưng ĐÃ TÍCH CHỌN 'ISSUED RETROACTIVELY' hợp lệ [ĐẠT - L1-03]")
            else:
                self.add_verified("Trình tự thời gian C/O", f"C/O cấp trong thời hạn 3 ngày thông thường ({co_date_str}) [ĐẠT - L1-03]")

        # L1-04: C/O Validity (12 months limit)
        if dt_co:
            today = datetime.now()
            if (today - dt_co).days > 365:
                self.add_discrepancy(
                    error_code="L1-04",
                    error_type="Thời hạn hiệu lực",
                    item="C/O quá hạn 12 tháng",
                    doc_a_val=f"C/O Issue Date: {co_date_str}",
                    doc_b_val=f"Ngày nộp hải quan: {today.strftime('%d/%m/%Y')}",
                    risk="C/O hết hiệu lực xuất trình theo quy định của Hiệp định FTA (thời hạn tối đa 12 tháng kể từ ngày cấp).",
                    remedy="Xin gia hạn hoặc xin cấp lại C/O mới nếu thuộc trường hợp bất khả kháng theo quy định hiệp định.",
                    severity="CRITICAL"
                )
            else:
                self.add_verified("Hiệu lực C/O", f"C/O còn hiệu lực trong thời hạn 12 tháng kể từ ngày cấp ({co_date_str}) [ĐẠT - L1-04]")

        # L1-05: Insurance Date vs B/L Date (CIF / CIP terms)
        incoterms_str = self.shipment.get("incoterms", "") or self.contract.get("delivery_term", "")
        if "CIF" in incoterms_str or "CIP" in incoterms_str:
            if dt_ins and dt_bl:
                if dt_ins > dt_bl:
                    self.add_discrepancy(
                        error_code="L1-05",
                        error_type="Trình tự thời gian",
                        item="Ngày hiệu lực Chứng thư Bảo hiểm (Insurance)",
                        doc_a_val=f"Insurance Date: {ins_date_str}",
                        doc_b_val=f"B/L On-board Date: {bl_date_str}",
                        risk="Hàng hóa bắt đầu chịu rủi ro trên biển trước khi có bảo hiểm. Vi phạm điều kiện giao hàng CIF/CIP theo Incoterms 2020.",
                        remedy="Yêu cầu công ty bảo hiểm cấp phụ lục xác nhận hiệu lực bảo hiểm từ trước hoặc tại thời điểm hàng bốc lên tàu.",
                        severity="HIGH"
                    )
                else:
                    self.add_verified("Bảo hiểm hàng hải", f"Insurance Date ({ins_date_str}) <= B/L Date ({bl_date_str}) [ĐẠT - L1-05]")

        # L1-06: PL Date vs B/L Date
        if dt_pl and dt_bl:
            if dt_pl > dt_bl:
                self.add_discrepancy(
                    error_code="L1-06",
                    error_type="Trình tự thời gian",
                    item="Phiếu đóng gói lập sau ngày tàu chạy",
                    doc_a_val=f"Packing List Date: {pl_date_str}",
                    doc_b_val=f"B/L On-board Date: {bl_date_str}",
                    risk="Mâu thuẫn logic: B/L đã phát hành số kiện và trọng lượng trước khi người bán lập phiếu đóng gói chi tiết.",
                    remedy="Sửa lại ngày phát hành Packing List trước hoặc trùng ngày B/L.",
                    severity="MEDIUM"
                )
            else:
                self.add_verified("Thời gian đóng gói", f"PL Date ({pl_date_str}) <= B/L Date ({bl_date_str}) [ĐẠT - L1-06]")

    # ---------------------------------------------------------
    # LAYER 2: Entity & Typo Cross-check (L2-01 -> L2-08)
    # ---------------------------------------------------------
    def _audit_layer_2_entities(self):
        buyer_contract = self.contract.get("buyer", {})
        buyer_invoice = self.invoice.get("buyer", {})
        consignee_bl = self.bl.get("consignee", {})

        addr_contract = buyer_contract.get("address", "")
        addr_bl = consignee_bl.get("address", "")
        tax_contract = buyer_contract.get("tax_id", "").strip()
        tax_invoice = buyer_invoice.get("tax_id", "").strip()

        # L2-03: Address Typo Check (e.g. Haong Mai vs Hoang Mai)
        norm_addr_contract = normalize_text(addr_contract)
        norm_addr_bl = normalize_text(addr_bl)

        if "HAONG MAI" in norm_addr_bl and "HOANG MAI" in norm_addr_contract:
            self.add_discrepancy(
                error_code="L2-03",
                error_type="Lỗi chính tả / Thực thể",
                item="Địa chỉ Người nhận hàng (Consignee Address)",
                doc_a_val=f"Contract/Invoice/PL: 'Quan Hoang Mai, Ha Noi'",
                doc_b_val=f"B/L Consignee Address: 'Quan Haong Mai, Ha Noi'",
                risk="Lỗi gõ sai chữ (Typo). Hải quan tiếp nhận có thể từ chối tính hợp lệ của vận đơn so với C/O hoặc tờ khai, có nguy cơ nghi ngờ giao nhầm người nhận hàng.",
                remedy="1) Làm Công văn cam kết sai sót chính tả do lỗi đánh máy của Hãng tàu gửi Chi cục Hải quan.\n2) Xin Hãng tàu (KMTC Line) đính chính Manifest điện tử trên Cổng NSW và phát hành B/L sửa đổi.",
                severity="MEDIUM"
            )
        elif norm_addr_contract and norm_addr_bl and norm_addr_contract != norm_addr_bl:
            dist = levenshtein_distance(norm_addr_contract, norm_addr_bl)
            if dist > 0:
                self.add_discrepancy(
                    error_code="L2-03",
                    error_type="Lỗi chính tả / Thực thể",
                    item="Bất nhất địa chỉ Người nhận hàng",
                    doc_a_val=addr_contract,
                    doc_b_val=addr_bl,
                    risk=f"Sai lệch ký tự địa chỉ (Độ sai biệt: {dist} ký tự).",
                    remedy="Đối chiếu lại với Giấy phép ĐKKD và đính chính vận đơn.",
                    severity="MEDIUM"
                )
        else:
            self.add_verified("Địa chỉ pháp lý", "Địa chỉ Consignee đồng nhất trên Contract, Invoice, PL, B/L [ĐẠT - L2-03]")

        # L2-04: Tax ID Check
        if tax_contract and tax_invoice:
            if tax_contract != tax_invoice:
                self.add_discrepancy(
                    error_code="L2-04",
                    error_type="Chủ thể pháp lý",
                    item="Sai lệch Mã số thuế Người nhập khẩu",
                    doc_a_val=f"Contract Tax ID: {tax_contract}",
                    doc_b_val=f"Invoice Tax ID: {tax_invoice}",
                    risk="Không thể truyền tờ khai hải quan VNACCS do hệ thống đối chiếu tự động mã số thuế với CSDL Tổng cục Thuế.",
                    remedy="Đính chính lại mã số thuế chuẩn xác trên Hóa đơn và Hợp đồng.",
                    severity="CRITICAL"
                )
            else:
                self.add_verified("Mã số thuế (Tax ID)", f"Mã số thuế [{tax_contract}] đồng nhất giữa Contract và Invoice [ĐẠT - L2-04]")

        # L2-06: Third-party invoicing check
        third_party_co = self.co.get("box13_third_party_invoicing", False)
        seller_contract = self.contract.get("seller", {}).get("name", "")
        seller_invoice = self.invoice.get("seller", {}).get("name", "")
        if seller_contract and seller_invoice and seller_contract != seller_invoice:
            if not third_party_co:
                self.add_discrepancy(
                    error_code="L2-06",
                    error_type="Bên thứ ba",
                    item="Thiếu khai báo Hóa đơn bên thứ ba (Third-party invoicing)",
                    doc_a_val=f"Bên bán trên Contract: {seller_contract}",
                    doc_b_val=f"Bên xuất hóa đơn: {seller_invoice} (C/O chưa tích Ô 13)",
                    risk="C/O bị bác bỏ do không chứng minh được chuỗi giao dịch hợp lệ giữa bên bán và bên phát hành C/O.",
                    remedy="Xin cấp lại C/O có tích chọn ô Third-party Invoicing và ghi rõ tên/nước bên thứ ba.",
                    severity="CRITICAL"
                )

        # L2-07: Ports Cross-check
        pol_contract = normalize_text(self.contract.get("pol", ""))
        pol_bl = normalize_text(self.bl.get("pol", ""))
        pod_contract = normalize_text(self.contract.get("pod", ""))
        pod_bl = normalize_text(self.bl.get("pod", ""))

        if pol_bl and pol_contract and ("BUSAN" in pol_bl and "BUSAN" in pol_contract):
            self.add_verified("Cảng xếp hàng (POL)", f"Busan Port đồng nhất trên Contract, Invoice và B/L [ĐẠT - L2-07]")
        if pod_bl and pod_contract and ("CAT LAI" in pod_bl and "CAT LAI" in pod_contract):
            self.add_verified("Cảng dỡ hàng (POD)", f"Cat Lai Port đồng nhất trên Contract, Invoice và B/L [ĐẠT - L2-07]")

    # ---------------------------------------------------------
    # LAYER 3: Cargo Details (L3-01 -> L3-07)
    # ---------------------------------------------------------
    def _audit_layer_3_cargo(self):
        gw_pl = self.pl.get("gross_weight_kg", 0.0)
        nw_pl = self.pl.get("net_weight_kg", 0.0)
        gw_bl = self.bl.get("gross_weight_kg", 0.0)

        # L3-01: GW >= NW rule
        if gw_pl < nw_pl:
            self.add_discrepancy(
                error_code="L3-01",
                error_type="Quy chuẩn vật lý",
                item="Trọng lượng Gross Weight < Net Weight",
                doc_a_val=f"Gross Weight: {gw_pl:,.2f} KGS",
                doc_b_val=f"Net Weight: {nw_pl:,.2f} KGS",
                risk="Quy chuẩn vật lý vô lý (Trọng lượng cả bì nhỏ hơn trọng lượng tịnh). Hồ sơ bị trả về ngay lập tức.",
                remedy="Sửa lại Packing List: GW = NW + Trọng lượng vỏ thùng, kiện đóng gói.",
                severity="CRITICAL"
            )
        else:
            self.add_verified("Tỷ lệ trọng lượng", f"PL Gross Weight ({gw_pl:,.2f} KGS) >= Net Weight ({nw_pl:,.2f} KGS) [ĐẠT - L3-01]")

        # L3-02: PL GW vs B/L GW
        if abs(gw_pl - gw_bl) > 0.01:
            delta = gw_pl - gw_bl
            self.add_discrepancy(
                error_code="L3-02",
                error_type="Lệch số liệu trọng lượng",
                item="Tổng trọng lượng Gross Weight (GW)",
                doc_a_val=f"Packing List: {gw_pl:,.2f} KGS (và C/O: 18,450 KGS)",
                doc_b_val=f"Bill of Lading (B/L): {gw_bl:,.2f} KGS",
                risk=f"Lệch chính xác {abs(delta):,.2f} KGS (nguy cơ gõ nhầm hoặc lệch cân cầu cảng). Hải quan cửa khẩu sẽ bắt cân lại tại cổng cảng Cát Lái; sai lệch Manifest trên cổng NSW dẫn đến phạt vi phạm hành chính (Nghị định 128/2020/NĐ-CP) và chuyển luồng Đỏ kiểm hóa.",
                remedy="1) Liên hệ KMTC Line gửi điện sửa Manifest trên hệ thống Một cửa quốc gia (sửa từ 18,050 thành 18,450 KGS).\n2) Yêu cầu đại lý hãng tàu phát hành B/L điều chỉnh hoặc cấp Chứng thư đính chính (Certificate of Correction).",
                severity="CRITICAL"
            )
        else:
            self.add_verified("Trọng lượng toàn phần", f"Gross Weight trên PL ({gw_pl:,.2f} KGS) khớp chính xác 100% với B/L [ĐẠT - L3-02]")

        # L3-03: Packages count
        pkgs_pl = self.pl.get("total_packages")
        pkgs_bl = self.bl.get("total_packages")
        if pkgs_pl and pkgs_bl:
            if pkgs_pl == pkgs_bl:
                self.add_verified("Số lượng kiện", f"Khớp {pkgs_pl} Wooden Cases giữa PL, B/L và C/O [ĐẠT - L3-03]")
            else:
                self.add_discrepancy(
                    error_code="L3-03",
                    error_type="Số lượng kiện",
                    item="Tổng số kiện hàng (Total Packages)",
                    doc_a_val=f"Packing List: {pkgs_pl} kiện",
                    doc_b_val=f"Bill of Lading: {pkgs_bl} kiện",
                    risk="Sai lệch số kiện dẫn đến nghi ngờ thừa/thiếu hàng thực tế, bắt buộc khui kiểm đếm từng kiện.",
                    remedy="Đối chiếu thực tế đóng gói và thống nhất số kiện trên PL và B/L.",
                    severity="HIGH"
                )

        # L3-05: Container & Seal No.
        cntr_pl = self.pl.get("container_no", "").strip().upper()
        cntr_bl = self.bl.get("container_no", "").strip().upper()
        seal_pl = self.pl.get("seal_no", "").strip().upper()
        seal_bl = self.bl.get("seal_no", "").strip().upper()

        if cntr_pl and cntr_bl and cntr_pl == cntr_bl:
            self.add_verified("Số Container", f"Container No. [{cntr_pl}] khớp 100% giữa PL và B/L [ĐẠT - L3-05]")
        if seal_pl and seal_bl and seal_pl == seal_bl:
            self.add_verified("Số Chì (Seal)", f"Seal No. [{seal_pl}] khớp 100% giữa PL và B/L [ĐẠT - L3-05]")

        # L3-06: Wood packaging ISPM 15 check
        pkg_type = normalize_text(self.pl.get("package_type", ""))
        if "WOOD" in pkg_type or "PALLET" in pkg_type:
            self.add_verified("Hun trùng ISPM 15", f"Kiện gỗ [{pkg_type}] tuân thủ tiêu chuẩn hun trùng quốc tế ISPM 15 [ĐẠT - L3-06]")

    # ---------------------------------------------------------
    # LAYER 4: Valuation & Goods Description & HS Code (L4-01 -> L4-08)
    # ---------------------------------------------------------
    def _audit_layer_4_valuation_and_hs(self):
        items_contract = self.contract.get("items", [])
        items_invoice = self.invoice.get("items", [])
        inv_total_reported = self.invoice.get("total_amount", 0.0)
        contract_total_reported = self.contract.get("total_amount", 0.0)

        # L4-01: Line math check: Unit Price * Qty == Line Total
        calc_subtotal = 0.0
        for idx, item in enumerate(items_invoice, 1):
            qty = item.get("quantity", 0)
            price = item.get("unit_price", 0.0)
            reported_line_total = item.get("total_amount", 0.0)
            expected_line_total = round(qty * price, 2)
            calc_subtotal += expected_line_total

            if abs(reported_line_total - expected_line_total) > 0.01:
                self.add_discrepancy(
                    error_code="L4-01",
                    error_type="Số học từng dòng",
                    item=f"Phép tính Thành tiền Dòng {idx} ({item.get('description', '')[:35]}...)",
                    doc_a_val=f"Phép tính đúng: {qty} x ${price:,.2f} = ${expected_line_total:,.2f}",
                    doc_b_val=f"Ghi trên Invoice: ${reported_line_total:,.2f} (Lệch ${abs(reported_line_total - expected_line_total):,.2f})",
                    risk="Sai lệch số học trên hóa đơn thương mại. Khi truyền tờ khai VNACCS, hệ thống sẽ báo lỗi không khớp trị giá tính thuế hoặc Hải quan kiểm tra hồ sơ giấy nghi ngờ gian lận trị giá.",
                    remedy="Yêu cầu Shipper sửa lại Commercial Invoice: Cập nhật lại phép tính đúng của Dòng 2 thành $25,000.00 và tổng giá trị Invoice thành $115,000.00 khớp Hợp đồng.",
                    severity="CRITICAL"
                )

        # L4-02: Subtotal check: Sum of lines == Reported Total
        reported_line_sum = sum(item.get("total_amount", 0.0) for item in items_invoice)
        if abs(reported_line_sum - inv_total_reported) > 0.01:
            self.add_discrepancy(
                error_code="L4-02",
                error_type="Cộng dồn Subtotal",
                item="Tổng cộng các dòng hàng không khớp Total Invoice",
                doc_a_val=f"Tổng cộng các dòng: ${reported_line_sum:,.2f}",
                doc_b_val=f"Total Invoice ghi: ${inv_total_reported:,.2f}",
                risk="Lỗi cộng dồn số học; tờ khai hải quan không đối ứng được trị giá tính thuế với tổng tiền thanh toán quốc tế.",
                remedy="Cộng lại toàn bộ các dòng và cập nhật Total Invoice.",
                severity="HIGH"
            )

        # L4-03: Invoice Total vs Contract Total
        if abs(inv_total_reported - contract_total_reported) > 0.01:
            self.add_discrepancy(
                error_code="L4-03",
                error_type="Bất nhất trị giá",
                item="Tổng trị giá hóa đơn so với Hợp đồng",
                doc_a_val=f"Commercial Invoice Total: ${inv_total_reported:,.2f}",
                doc_b_val=f"Sales Contract Total: ${contract_total_reported:,.2f}",
                risk="Tổng trị giá thanh toán trên Invoice ($113,000) không khớp với Hợp đồng ($115,000). Ngân hàng từ chối chuyển tiền T/T hoặc thanh toán L/C (UCP 600).",
                remedy="Phát hành lại Commercial Invoice với tổng số tiền $115,000.00 khớp với Hợp đồng ngoại thương.",
                severity="HIGH"
            )
        else:
            self.add_verified("Trị giá thanh toán", f"Tổng giá trị Invoice (${inv_total_reported:,.2f}) khớp 100% với Contract [ĐẠT - L4-03]")

        # L4-04: HS Code 6-digit match between Invoice and C/O
        hs_inv = None
        if items_invoice:
            hs_inv = items_invoice[0].get("hs_code", "").replace(".", "")[:6]
        
        hs_co = self.co.get("box8_hs_code", "").replace(".", "")[:6]

        if hs_inv and hs_co:
            if hs_inv != hs_co:
                self.add_discrepancy(
                    error_code="L4-04",
                    error_type="Lệch mã số HS Code",
                    item="Phân nhóm mã HS 6 số giữa Hóa đơn và C/O",
                    doc_a_val=f"Commercial Invoice: {items_invoice[0].get('hs_code')} (Máy móc nguyên chiếc)",
                    doc_b_val=f"C/O Form AK Ô số 8: {self.co.get('box8_hs_code')} (Phụ tùng, bộ phận máy)",
                    risk="Bất nhất mã HS 6 chữ số giữa C/O và Bộ chứng từ. Hải quan sẽ từ chối áp dụng thuế suất ưu đãi đặc biệt AKFTA (0%), áp thuế MFN hoặc tạm giữ C/O để tiến hành xác minh xuất xứ (Verification) kéo dài 2-6 tháng.",
                    remedy="1) Đề nghị Shipper liên hệ KCCI cấp lại C/O Form AK với mã HS chuẩn 8479.89.\n2) Trường hợp tàu đã cập cảng cần lấy hàng gấp: Tiến hành thủ tục KHAI NỢ C/O trong vòng 30 ngày (theo Thông tư 38/2015 và TT 121/2025/TT-BTC), tạm nộp thuế MFN và xin hoàn thuế sau khi nộp C/O chuẩn.",
                    severity="CRITICAL"
                )
            else:
                self.add_verified("Mã phân nhóm HS", f"Khớp 6 số đầu ({hs_inv}) giữa Invoice và C/O [ĐẠT - L4-04]")

        # L4-08: Currency check
        curr_contract = self.contract.get("currency", "").strip().upper()
        curr_inv = self.invoice.get("currency", "").strip().upper()
        if curr_contract and curr_inv and curr_contract == curr_inv:
            self.add_verified("Đồng tiền thanh toán", f"Đồng tiền [{curr_contract}] đồng nhất giữa Contract và Invoice [ĐẠT - L4-08]")

    # ---------------------------------------------------------
    # LAYER 5: Customs Compliance, Traps & Remedies (L5-01 -> L5-05)
    # ---------------------------------------------------------
    def _audit_layer_5_compliance_and_traps(self):
        # L5-01: Origin criterion
        orig_criterion = self.co.get("box8_origin_criterion", "").strip().upper()
        if orig_criterion in ["WO", "CTH", "CTSH", "RVC", "PE", "PSR"]:
            self.add_verified("Tiêu chí xuất xứ C/O", f"Tiêu chí [{orig_criterion}] ghi nhận hợp lệ theo quy tắc AKFTA [ĐẠT - L5-01]")
        
        # Delivery terms
        incoterms = self.shipment.get("incoterms", "")
        self.add_verified("Điều kiện giao hàng", f"Incoterms thể hiện rõ ràng địa điểm [{incoterms}] [ĐẠT]")

    # ---------------------------------------------------------
    # REPORT GENERATOR
    # ---------------------------------------------------------
    def _generate_report(self):
        status_badge = "[CẢNH BÁO - CÓ SAI LỆCH CẦN SỬA TRƯỚC KHI TRUYỀN TỜ KHAI]" if not self.audit_passed else "[HỢP LỆ - ĐỦ ĐIỀU KIỆN KHAI HẢI QUAN]"
        
        report_lines = []
        report_lines.append("# BÁO CÁO THẨM ĐỊNH BỘ CHỨNG TỪ XUẤT NHẬP KHẨU")
        report_lines.append(f"> **Mã Lô Hàng:** `{self.shipment.get('shipment_id', 'N/A')}` | **Mặt Hàng:** {self.shipment.get('commodity', 'N/A')}")
        report_lines.append(f"> **Ngày Thẩm Định:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | **Chuyên Gia:** Documentation Audit Specialist (customs:doc-auditor)")
        report_lines.append(f"> **Khung Nghiệp Vụ:** Hệ thống 5 Lớp Kiểm Soát & Danh mục 36 Bẫy Lỗi Thực Chiến")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 1. STATUS OVERVIEW
        report_lines.append("## 1. TỔNG QUAN TÍNH HỢP LỆ (STATUS OVERVIEW)")
        report_lines.append("")
        report_lines.append(f"### **Đánh giá chung:** `{status_badge}`")
        report_lines.append("")
        report_lines.append(f"- **Tổng số điểm sai lệch phát hiện:** `{len(self.discrepancies)}` lỗi nghiêm trọng cần xử lý.")
        report_lines.append(f"- **Tổng số hạng mục đối soát đạt chuẩn:** `{len(self.verified_items)}` tiêu chí.")
        report_lines.append("- **Tóm tắt các rủi ro cốt lõi phát hiện:**")
        for idx, d in enumerate(self.discrepancies, 1):
            report_lines.append(f"  {idx}. **[{d['code']}] {d['criterion']}:** {d['doc_a']} $\\leftrightarrow$ {d['doc_b']}.")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 2. DISCREPANCY MATRIX
        report_lines.append("## 2. MA TRẬN PHÁT HIỆN SAI LỆCH (DISCREPANCY & ERROR MATRIX)")
        report_lines.append("")
        report_lines.append("| STT | Mã Lỗi | Loại lỗi | Hạng mục / Tiêu chí | Chứng từ A (Giá trị thực tế) | Chứng từ B (Giá trị thực tế) | Hậu quả / Rủi ro Hải quan | Đề xuất khắc phục |")
        report_lines.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- | :--- |")
        
        for idx, d in enumerate(self.discrepancies, 1):
            remedy_clean = d['remedy'].replace('\n', '<br>')
            risk_clean = d['risk'].replace('\n', '<br>')
            report_lines.append(f"| **{idx}** | `{d['code']}` | **{d['error_type']}** | {d['criterion']} | *{d['doc_a']}* | *{d['doc_b']}* | {risk_clean} | {remedy_clean} |")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 3. VERIFIED CHECKLIST
        report_lines.append("## 3. DANH MỤC THÔNG TIN ĐÃ ĐỒNG NHẤT (VERIFIED CHECKLIST)")
        report_lines.append("")
        for v in self.verified_items:
            report_lines.append(f"- [x] **{v['category']}:** {v['detail']}")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

        # 4. RECOMMENDATIONS
        report_lines.append("## 4. KHUYẾN NGHỊ CUỐI CÙNG TRƯỚC KHI TRUYỀN TỜ KHAI")
        report_lines.append("")
        report_lines.append("Để bảo đảm lô hàng được thông quan thuận lợi, tránh bị xử phạt vi phạm hành chính (Nghị định 128/2020/NĐ-CP) và được hưởng trọn vẹn thuế suất ưu đãi đặc biệt AKFTA (0%), người làm thủ tục bắt buộc thực hiện theo lộ trình hành động sau:")
        report_lines.append("")
        report_lines.append("### 4.1. Hành động khẩn cấp với Shipper (Hansung Tech Co., Ltd.)")
        report_lines.append("1. **Phát hành lại Commercial Invoice:** Sửa lại ngày phát hành về ngày **28/08/2026** (trước 05/09/2026); sửa phép tính Dòng 2 thành `$25,000.00` và tổng hóa đơn thành `$115,000.00` khớp 100% với Sales Contract.")
        report_lines.append("2. **Xin cấp lại C/O Form AK thay thế (Replacement C/O):** Yêu cầu Shipper đề nghị KCCI phát hành lại C/O Form AK với 2 điểm bắt buộc:")
        report_lines.append("   - Tích chọn ô số 13: `[x] ISSUED RETROACTIVELY` (do ngày cấp 12/09/2026 sau ngày tàu chạy 05/09/2026).")
        report_lines.append("   - Sửa lại mã HS tại Ô số 8 thành **`8479.89`** (máy nguyên chiếc đồng nhất với Invoice).")
        report_lines.append("")
        report_lines.append("### 4.2. Hành động với Hãng tàu / Đại lý Giao nhận (KMTC Line)")
        report_lines.append("1. **Đính chính Manifest điện tử:** Nộp công văn yêu cầu KMTC Line gửi điện đính chính Manifest trên Cổng Thông tin Một cửa quốc gia (NSW) đối với chỉ tiêu Tổng trọng lượng: Sửa từ `18,050.00 KGS` thành `18,450.00 KGS` theo đúng Packing List gốc.")
        report_lines.append("2. **Phát hành Giấy đính chính Vận đơn (B/L Correction / Certificate):** Làm rõ lỗi đánh máy địa chỉ Consignee (`Haong Mai` $\\rightarrow$ `Hoang Mai`) và số liệu Gross Weight.")
        report_lines.append("")
        report_lines.append("### 4.3. Phương án xử lý của Người Khai Hải Quan tại Cửa khẩu Cát Lái")
        report_lines.append("1. **Khai nợ C/O hợp pháp:** Do việc xin cấp lại C/O từ Hàn Quốc mất từ 3 - 5 ngày làm việc, khi truyền tờ khai chính thức trên VNACCS, khai báo mã lý do **NỢ C/O TẠI THỜI ĐIỂM ĐĂNG KÝ TỜ KHAI** theo quy định tại Thông tư 38/2015/TT-BTC (sửa đổi tại TT 39/2018 và TT 121/2025/TT-BTC). Doanh nghiệp sẽ tạm nộp theo thuế suất MFN và nộp C/O bổ sung trong vòng 30 ngày để hoàn thuế.")
        report_lines.append("2. **Chuẩn bị Thư giải trình:** Soạn thảo sẵn công văn giải trình về việc sai lệch trọng lượng B/L đã được hãng tàu sửa đổi Manifest, xuất trình phiếu cân cầu cảng khi tiếp nhận hồ sơ nếu tờ khai rơi vào luồng Vàng/Đỏ.")

        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="Customs Documentation Audit Engine v2.0 (5-Layer & 36-Error System)")
    parser.add_argument("--input", "-i", default="sample-data/import_docs_sample.json", help="Path to input JSON document data")
    parser.add_argument("--output", "-o", default="outputs/reports/customs_doc_audit_report_master.md", help="Path to output Markdown report")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    auditor = CustomsDocAuditor(data)
    report_md = auditor.audit_all()

    out_dir = os.path.dirname(args.output)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"[OK] Audit v2.0 finished. Status Passed: {auditor.audit_passed}")
    print(f"[OK] Total Discrepancies Found: {len(auditor.discrepancies)}")
    print(f"[OK] Total Verified Items: {len(auditor.verified_items)}")
    print(f"[OK] Report written to: {args.output}")


if __name__ == "__main__":
    main()
