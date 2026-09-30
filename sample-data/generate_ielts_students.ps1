# generate_ielts_students.ps1
# Script tao file Excel thong tin hoc vien IELTS X bang OpenXML va PowerShell
[CmdletBinding()]
param (
    [string]$JsonPath = "sample-data/ielts_students_raw.json",
    [string]$OutputPath = "sample-data/IELTS_Center_X_Students.xlsx"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

if (-not (Test-Path $JsonPath)) {
    Write-Error "Khong tim thay tap tin JSON nguon: $JsonPath"
    exit 1
}

Write-Host "[INIT] Doc du lieu tu tap tin JSON: $JsonPath" -ForegroundColor Cyan
$jsonRaw = [System.IO.File]::ReadAllText((Resolve-Path $JsonPath), [System.Text.Encoding]::UTF8)
$data = $jsonRaw | ConvertFrom-Json

$students = $data.students
$classes  = $data.classes
$kpis     = $data.kpis

Write-Host "[INFO] Tim thay $($students.Count) hoc vien, $($classes.Count) lop hoc." -ForegroundColor Green

# Tao thu muc tam
$tempDir = Join-Path $env:TEMP ("ielts_excel_" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path "$tempDir\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\worksheets" -Force | Out-Null

# 1. [Content_Types].xml
$contentTypes = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>
"@
[System.IO.File]::WriteAllText("$tempDir\[Content_Types].xml", $contentTypes, [System.Text.Encoding]::UTF8)

# 2. _rels/.rels
$rootRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\_rels\.rels", $rootRels, [System.Text.Encoding]::UTF8)

# 3. xl/workbook.xml
$workbookXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Danh_Sach_Hoc_Vien" sheetId="1" r:id="rId1"/>
    <sheet name="Tong_Quan_Lop_Hoc" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\workbook.xml", $workbookXml, [System.Text.Encoding]::UTF8)

# 4. xl/_rels/workbook.xml.rels
$wbRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\_rels\workbook.xml.rels", $wbRels, [System.Text.Encoding]::UTF8)

# 5. xl/styles.xml
$stylesXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="2">
    <numFmt numFmtId="164" formatCode="0.0"/>
    <numFmt numFmtId="165" formatCode="@"/>
  </numFmts>
  <fonts count="6">
    <font><sz val="10"/><name val="Segoe UI"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF0F172A"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF15803D"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FFB45309"/><name val="Segoe UI"/></font>
    <font><b/><sz val="14"/><color rgb="FF1E3A8A"/><name val="Segoe UI"/></font>
  </fonts>
  <fills count="7">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8FAFC"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFEF3C7"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE0E7FF"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFE2E8F0"/></left>
      <right style="thin"><color rgb="FFE2E8F0"/></right>
      <top style="thin"><color rgb="FFE2E8F0"/></top>
      <bottom style="thin"><color rgb="FFE2E8F0"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="12">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0"/>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="164" fontId="2" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="164" fontId="2" fillId="3" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="4" fillId="5" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="5" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="6" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
  </cellXfs>
</styleSheet>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\styles.xml", $stylesXml, [System.Text.Encoding]::UTF8)

# 6. Sheet 1: Danh_Sach_Hoc_Vien
$sb1 = New-Object System.Text.StringBuilder
[void]$sb1.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb1.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb1.AppendLine('  <cols>')
[void]$sb1.AppendLine('    <col min="1" max="1" width="6" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="2" max="2" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="3" max="3" width="24" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="4" max="4" width="15" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="5" max="5" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="6" max="6" width="10" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="7" max="7" width="24" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="8" max="8" width="15" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="9" max="9" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="10" max="10" width="22" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="11" max="11" width="24" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="12" max="12" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="13" max="13" width="18" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="14" max="14" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('  </cols>')
[void]$sb1.AppendLine('  <sheetData>')

# Title & Subtitle
$s1TitleEsc = [System.Security.SecurityElement]::Escape($data.sheet1_title)
$s1SubEsc   = [System.Security.SecurityElement]::Escape($data.sheet1_subtitle)
[void]$sb1.AppendLine('    <row r="1" ht="32" customHeight="1">')
[void]$sb1.AppendLine("      <c r=`"A1`" t=`"inlineStr`" s=`"9`"><is><t>$s1TitleEsc</t></is></c>")
[void]$sb1.AppendLine('    </row>')
[void]$sb1.AppendLine('    <row r="2" ht="20" customHeight="1">')
[void]$sb1.AppendLine("      <c r=`"A2`" t=`"inlineStr`" s=`"0`"><is><t>$s1SubEsc</t></is></c>")
[void]$sb1.AppendLine('    </row>')
[void]$sb1.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# Headers
$headers1 = $data.sheet1_headers
[void]$sb1.AppendLine('    <row r="4" ht="28" customHeight="1">')
for ($c = 0; $c -lt $headers1.Count; $c++) {
    $colLetter = [char](65 + $c)
    $escapedH = [System.Security.SecurityElement]::Escape($headers1[$c])
    [void]$sb1.AppendLine("      <c r=`"$colLetter`4`" t=`"inlineStr`" s=`"1`"><is><t>$escapedH</t></is></c>")
}
[void]$sb1.AppendLine('    </row>')

# Student Rows
$rIdx = 5
foreach ($st in $students) {
    $isZebra = ($rIdx % 2 -eq 1)
    $sLeft   = if ($isZebra) { 3 } else { 0 }
    $sCenter = if ($isZebra) { 4 } else { 2 }
    $sBand   = if ($isZebra) { 6 } else { 5 }
    $sHocPhi = if ($st.HocPhi -eq "Đã hoàn thành") { 7 } else { 8 }

    [void]$sb1.AppendLine("    <row r=`"$rIdx`" ht=`"22`" customHeight=`"1`">")

    # A: STT
    [void]$sb1.AppendLine("      <c r=`"A$rIdx`" s=`"$sCenter`"><v>$($st.STT)</v></c>")
    # B: MaHV
    $eMaHV = [System.Security.SecurityElement]::Escape($st.MaHV)
    [void]$sb1.AppendLine("      <c r=`"B$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eMaHV</t></is></c>")
    # C: HoTen
    $eHoTen = [System.Security.SecurityElement]::Escape($st.HoTen)
    [void]$sb1.AppendLine("      <c r=`"C$rIdx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eHoTen</t></is></c>")
    # D: SDT (String)
    $eSDT = [System.Security.SecurityElement]::Escape($st.SDT)
    [void]$sb1.AppendLine("      <c r=`"D$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eSDT</t></is></c>")
    # E: NgaySinh
    $eNS = [System.Security.SecurityElement]::Escape($st.NgaySinh)
    [void]$sb1.AppendLine("      <c r=`"E$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eNS</t></is></c>")
    # F: GioiTinh
    $eGT = [System.Security.SecurityElement]::Escape($st.GioiTinh)
    [void]$sb1.AppendLine("      <c r=`"F$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eGT</t></is></c>")
    # G: Lop
    $eLop = [System.Security.SecurityElement]::Escape($st.Lop)
    [void]$sb1.AppendLine("      <c r=`"G$rIdx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eLop</t></is></c>")
    # H: MaLop
    $eML = [System.Security.SecurityElement]::Escape($st.MaLop)
    [void]$sb1.AppendLine("      <c r=`"H$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eML</t></is></c>")
    # I: Target Band
    $tbVal = [double]$st.Target
    $tbStr = $tbVal.ToString("0.0", [System.Globalization.CultureInfo]::InvariantCulture)
    [void]$sb1.AppendLine("      <c r=`"I$rIdx`" s=`"$sBand`"><v>$tbStr</v></c>")
    # J: GiangVien
    $eGV = [System.Security.SecurityElement]::Escape($st.GiangVien)
    [void]$sb1.AppendLine("      <c r=`"J$rIdx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eGV</t></is></c>")
    # K: LichHoc
    $eLH = [System.Security.SecurityElement]::Escape($st.LichHoc)
    [void]$sb1.AppendLine("      <c r=`"K$rIdx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eLH</t></is></c>")
    # L: NgayNhapHoc
    $eNNH = [System.Security.SecurityElement]::Escape($st.NgayNhapHoc)
    [void]$sb1.AppendLine("      <c r=`"L$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eNNH</t></is></c>")
    # M: HocPhi
    $eHP = [System.Security.SecurityElement]::Escape($st.HocPhi)
    [void]$sb1.AppendLine("      <c r=`"M$rIdx`" t=`"inlineStr`" s=`"$sHocPhi`"><is><t>$eHP</t></is></c>")
    # N: TrangThai
    $eTT = [System.Security.SecurityElement]::Escape($st.TrangThai)
    [void]$sb1.AppendLine("      <c r=`"N$rIdx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eTT</t></is></c>")

    [void]$sb1.AppendLine('    </row>')
    $rIdx++
}

[void]$sb1.AppendLine('  </sheetData>')
[void]$sb1.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet1.xml", $sb1.ToString(), [System.Text.Encoding]::UTF8)

# 7. Sheet 2: Tong_Quan_Lop_Hoc
$sb2 = New-Object System.Text.StringBuilder
[void]$sb2.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb2.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb2.AppendLine('  <cols>')
[void]$sb2.AppendLine('    <col min="1" max="1" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="2" max="2" width="24" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="3" max="3" width="22" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="4" max="4" width="12" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="5" max="5" width="16" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="6" max="6" width="24" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="7" max="7" width="22" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="8" max="8" width="18" customWidth="1"/>')
[void]$sb2.AppendLine('  </cols>')
[void]$sb2.AppendLine('  <sheetData>')

# Title Row Sheet 2
$s2TitleEsc = [System.Security.SecurityElement]::Escape($data.sheet2_title)
$s2SubEsc   = [System.Security.SecurityElement]::Escape($data.sheet2_subtitle)
[void]$sb2.AppendLine('    <row r="1" ht="32" customHeight="1">')
[void]$sb2.AppendLine("      <c r=`"A1`" t=`"inlineStr`" s=`"9`"><is><t>$s2TitleEsc</t></is></c>")
[void]$sb2.AppendLine('    </row>')
[void]$sb2.AppendLine('    <row r="2" ht="20" customHeight="1">')
[void]$sb2.AppendLine("      <c r=`"A2`" t=`"inlineStr`" s=`"0`"><is><t>$s2SubEsc</t></is></c>")
[void]$sb2.AppendLine('    </row>')
[void]$sb2.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# Table 1 Header
$headers2 = $data.sheet2_headers
[void]$sb2.AppendLine('    <row r="4" ht="28" customHeight="1">')
for ($c = 0; $c -lt $headers2.Count; $c++) {
    $colLetter = [char](65 + $c)
    $escapedH = [System.Security.SecurityElement]::Escape($headers2[$c])
    [void]$sb2.AppendLine("      <c r=`"$colLetter`4`" t=`"inlineStr`" s=`"1`"><is><t>$escapedH</t></is></c>")
}
[void]$sb2.AppendLine('    </row>')

$r2Idx = 5
$totalSiSo = 0
foreach ($cls in $classes) {
    $isZebra = ($r2Idx % 2 -eq 1)
    $sLeft   = if ($isZebra) { 3 } else { 0 }
    $sCenter = if ($isZebra) { 4 } else { 2 }
    $totalSiSo += [int]$cls.SiSo

    [void]$sb2.AppendLine("    <row r=`"$r2Idx`" ht=`"22`" customHeight=`"1`">")
    
    $eML = [System.Security.SecurityElement]::Escape($cls.MaLop)
    [void]$sb2.AppendLine("      <c r=`"A$r2Idx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eML</t></is></c>")
    $eTL = [System.Security.SecurityElement]::Escape($cls.TenLop)
    [void]$sb2.AppendLine("      <c r=`"B$r2Idx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eTL</t></is></c>")
    $eGV = [System.Security.SecurityElement]::Escape($cls.GiangVien)
    [void]$sb2.AppendLine("      <c r=`"C$r2Idx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eGV</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"D$r2Idx`" s=`"$sCenter`"><v>$($cls.SiSo)</v></c>")
    $eTB = [System.Security.SecurityElement]::Escape($cls.TargetBand)
    [void]$sb2.AppendLine("      <c r=`"E$r2Idx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eTB</t></is></c>")
    $eLH = [System.Security.SecurityElement]::Escape($cls.LichHoc)
    [void]$sb2.AppendLine("      <c r=`"F$r2Idx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eLH</t></is></c>")
    $eP = [System.Security.SecurityElement]::Escape($cls.Phong)
    [void]$sb2.AppendLine("      <c r=`"G$r2Idx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eP</t></is></c>")
    $eHPT = [System.Security.SecurityElement]::Escape($cls.HocPhiHoanThanh)
    [void]$sb2.AppendLine("      <c r=`"H$r2Idx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eHPT</t></is></c>")

    [void]$sb2.AppendLine('    </row>')
    $r2Idx++
}

# Total Row
[void]$sb2.AppendLine("    <row r=`"$r2Idx`" ht=`"24`" customHeight=`"1`">")
[void]$sb2.AppendLine("      <c r=`"A$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>TONG CONG</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"B$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>4 Lop Dang Van Hanh</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"C$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>4 Giang Vien</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"D$r2Idx`" s=`"11`"><v>$totalSiSo</v></c>")
[void]$sb2.AppendLine("      <c r=`"E$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>4.5 - 8.5</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"F$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>3 Ca Hoc</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"G$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>2 Co So</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"H$r2Idx`" t=`"inlineStr`" s=`"11`"><is><t>28/35 (80.0%)</t></is></c>")
[void]$sb2.AppendLine('    </row>')

# Spacing & KPI Section
$r2Idx += 2
[void]$sb2.AppendLine("    <row r=`"$r2Idx`" ht=`"26`" customHeight=`"1`">")
[void]$sb2.AppendLine("      <c r=`"A$r2Idx`" t=`"inlineStr`" s=`"10`"><is><t>Chi So Hoc Vu Cot Loi</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"B$r2Idx`" t=`"inlineStr`" s=`"10`"><is><t>Gia Tri Thuc Te</t></is></c>")
[void]$sb2.AppendLine("      <c r=`"C$r2Idx`" t=`"inlineStr`" s=`"10`"><is><t>Ghi Chu Dao Tao</t></is></c>")
[void]$sb2.AppendLine('    </row>')

foreach ($kpi in $kpis) {
    $r2Idx++
    $isZebra = ($r2Idx % 2 -eq 1)
    $sLeft   = if ($isZebra) { 3 } else { 0 }
    $sCenter = if ($isZebra) { 4 } else { 2 }
    
    $eCS = [System.Security.SecurityElement]::Escape($kpi.ChiSo)
    $eGT = [System.Security.SecurityElement]::Escape($kpi.GiaTri)
    $eGC = [System.Security.SecurityElement]::Escape($kpi.GhiChu)

    [void]$sb2.AppendLine("    <row r=`"$r2Idx`" ht=`"20`" customHeight=`"1`">")
    [void]$sb2.AppendLine("      <c r=`"A$r2Idx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eCS</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"B$r2Idx`" t=`"inlineStr`" s=`"$sCenter`"><is><t>$eGT</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"C$r2Idx`" t=`"inlineStr`" s=`"$sLeft`"><is><t>$eGC</t></is></c>")
    [void]$sb2.AppendLine('    </row>')
}

[void]$sb2.AppendLine('  </sheetData>')
[void]$sb2.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet2.xml", $sb2.ToString(), [System.Text.Encoding]::UTF8)

# 8. Dong goi file Excel .xlsx va chuan hoa slash sang OpenXML tieu chuan
$outDir = Split-Path -Path $OutputPath -Parent
if ($outDir -and -not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

if (Test-Path $OutputPath) {
    Remove-Item $OutputPath -Force
}

$rawZip = $OutputPath + ".raw.zip"
if (Test-Path $rawZip) { Remove-Item $rawZip -Force }

[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $rawZip)
Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

$src = [System.IO.Compression.ZipFile]::OpenRead($rawZip)
$dst = [System.IO.Compression.ZipFile]::Open($OutputPath, [System.IO.Compression.ZipArchiveMode]::Create)
foreach ($entry in $src.Entries) {
    $cleanName = $entry.FullName -replace '\\', '/'
    $newEntry = $dst.CreateEntry($cleanName, [System.IO.Compression.CompressionLevel]::Optimal)
    $sStream = $entry.Open()
    $dStream = $newEntry.Open()
    $sStream.CopyTo($dStream)
    $dStream.Close()
    $sStream.Close()
}
$src.Dispose()
$dst.Dispose()
Remove-Item $rawZip -Force

Write-Host "[SUCCESS] Da tao thanh cong tap tin Excel hoc vien IELTS X:" -ForegroundColor Green
Write-Host "          => $OutputPath" -ForegroundColor Yellow
Write-Host "          => Dung luong: $((Get-Item $OutputPath).Length) bytes" -ForegroundColor Gray
