# build_ielts_academic_master.ps1
# Engine tao Master Excel 4 Sheet va xuat JSON Metrics cho IELTS Center X
[CmdletBinding()]
param (
    [string]$JsonPath = "sample-data/ielts_academic_enriched.json",
    [string]$OutputDir = "outputs/reports",
    [string]$ExcelName = "IELTS_Center_X_Cleaned_Master.xlsx",
    [string]$MetricsName = "ielts_academic_summary_metrics.json"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[INIT] LOADING ENRICHED DATA FROM: $JsonPath" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path $JsonPath)) {
    Write-Error "Data file not found: $JsonPath"
    exit 1
}

$rawText = [System.IO.File]::ReadAllText((Resolve-Path $JsonPath), [System.Text.Encoding]::UTF8)
$data = $rawText | ConvertFrom-Json

$ui = $data.ui_strings
$metrics = $data.summary_metrics
$classes = $data.classes
$students = $data.students
$atRiskList = $data.at_risk_list
$dataDict = $data.data_dictionary

Write-Host "[DATA] Loaded $($students.Count) students, $($classes.Count) classes." -ForegroundColor Green

# 1. Output summary metrics JSON
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}
$metricsJsonPath = Join-Path $OutputDir $MetricsName
$rawText | Set-Content -Path $metricsJsonPath -Encoding UTF8
Write-Host "[METRICS] Saved metrics JSON to: $metricsJsonPath" -ForegroundColor Green

# 2. Build OpenXML Workbook (4 Sheets)
$tempDir = Join-Path $env:TEMP ("ielts_master_" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path "$tempDir\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\worksheets" -Force | Out-Null

# 2.1 [Content_Types].xml
$contentTypes = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet4.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>
"@
[System.IO.File]::WriteAllText("$tempDir\[Content_Types].xml", $contentTypes, [System.Text.Encoding]::UTF8)

# 2.2 _rels/.rels
$rootRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\_rels\.rels", $rootRels, [System.Text.Encoding]::UTF8)

# 2.3 xl/workbook.xml
$workbookXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Executive_Dashboard" sheetId="1" r:id="rId1"/>
    <sheet name="Cleaned_Students_Master" sheetId="2" r:id="rId2"/>
    <sheet name="Teacher_KPI_Summary" sheetId="3" r:id="rId3"/>
    <sheet name="Data_Dictionary" sheetId="4" r:id="rId4"/>
  </sheets>
</workbook>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\workbook.xml", $workbookXml, [System.Text.Encoding]::UTF8)

# 2.4 xl/_rels/workbook.xml.rels
$wbRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet4.xml"/>
  <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\_rels\workbook.xml.rels", $wbRels, [System.Text.Encoding]::UTF8)

# 2.5 xl/styles.xml
$stylesXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="3">
    <numFmt numFmtId="164" formatCode="0.0"/>
    <numFmt numFmtId="165" formatCode="@"/>
    <numFmt numFmtId="166" formatCode="0.0%"/>
  </numFmts>
  <fonts count="9">
    <font><sz val="10"/><name val="Segoe UI"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF0F172A"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF15803D"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FFB45309"/><name val="Segoe UI"/></font>
    <font><b/><sz val="14"/><color rgb="FF1E3A8A"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FFBE123C"/><name val="Segoe UI"/></font>
    <font><b/><sz val="18"/><color rgb="FF1E3A8A"/><name val="Segoe UI"/></font>
    <font><sz val="9"/><color rgb="FF64748B"/><name val="Segoe UI"/></font>
  </fonts>
  <fills count="9">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8FAFC"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFEF3C7"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE0E7FF"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFE4E6"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF1F5F9"/></patternFill></fill>
  </fills>
  <borders count="3">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFE2E8F0"/></left>
      <right style="thin"><color rgb="FFE2E8F0"/></right>
      <top style="thin"><color rgb="FFE2E8F0"/></top>
      <bottom style="thin"><color rgb="FFE2E8F0"/></bottom>
    </border>
    <border>
      <left style="medium"><color rgb="FF3B82F6"/></left>
      <right style="medium"><color rgb="FF3B82F6"/></right>
      <top style="medium"><color rgb="FF3B82F6"/></top>
      <bottom style="medium"><color rgb="FF3B82F6"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="18">
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
    <xf numFmtId="0" fontId="6" fillId="7" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="7" fillId="6" borderId="2" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="8" fillId="6" borderId="0" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="8" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="left" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="left" vertical="center"/></xf>
  </cellXfs>
</styleSheet>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\styles.xml", $stylesXml, [System.Text.Encoding]::UTF8)

function Escape-Xml([string]$text) {
    if ([string]::IsNullOrEmpty($text)) { return "" }
    return [System.Security.SecurityElement]::Escape($text)
}

# ==============================================================================
# 2.6 Sheet 1: Executive_Dashboard
# ==============================================================================
$sb1 = New-Object System.Text.StringBuilder
[void]$sb1.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb1.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb1.AppendLine('  <cols>')
[void]$sb1.AppendLine('    <col min="1" max="1" width="5" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="2" max="2" width="22" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="3" max="3" width="25" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="4" max="4" width="12" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="5" max="5" width="16" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="6" max="6" width="16" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="7" max="7" width="16" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="8" max="8" width="18" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="9" max="9" width="18" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="10" max="10" width="40" customWidth="1"/>')
[void]$sb1.AppendLine('  </cols>')
[void]$sb1.AppendLine('  <sheetData>')

# Title
[void]$sb1.AppendLine('    <row r="1" ht="32" customHeight="1">')
$t1 = Escape-Xml $ui.sheet1_title
[void]$sb1.AppendLine("      <c r=`"B1`" t=`"inlineStr`" s=`"9`"><is><t>$t1</t></is></c>")
[void]$sb1.AppendLine('    </row>')
[void]$sb1.AppendLine('    <row r="2" ht="20" customHeight="1">')
$sub1 = Escape-Xml $ui.sheet1_subtitle
[void]$sb1.AppendLine("      <c r=`"B2`" t=`"inlineStr`" s=`"0`"><is><t>$sub1</t></is></c>")
[void]$sb1.AppendLine('    </row>')
[void]$sb1.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# KPI Cards
$vTotal = "$($metrics.total_students) HV"
$vPass = "$($metrics.overall_pass_rate_pct)%"
$vMock = "$($metrics.overall_avg_mock_band) Band"
$vTuition = "$($metrics.tuition_completion_pct)%"

[void]$sb1.AppendLine('    <row r="4" ht="32" customHeight="1">')
[void]$sb1.AppendLine("      <c r=`"B4`" t=`"inlineStr`" s=`"12`"><is><t>$vTotal</t></is></c>")
[void]$sb1.AppendLine("      <c r=`"C4`" s=`"12`"/>")
[void]$sb1.AppendLine("      <c r=`"D4`" t=`"inlineStr`" s=`"12`"><is><t>$vPass</t></is></c>")
[void]$sb1.AppendLine("      <c r=`"E4`" s=`"12`"/>")
[void]$sb1.AppendLine("      <c r=`"F4`" t=`"inlineStr`" s=`"12`"><is><t>$vMock</t></is></c>")
[void]$sb1.AppendLine("      <c r=`"G4`" s=`"12`"/>")
[void]$sb1.AppendLine("      <c r=`"H4`" t=`"inlineStr`" s=`"12`"><is><t>$vTuition</t></is></c>")
[void]$sb1.AppendLine("      <c r=`"I4`" s=`"12`"/>")
[void]$sb1.AppendLine('    </row>')

$c1Label = Escape-Xml $ui.card1_label
$c2Label = Escape-Xml $ui.card2_label
$c3Label = Escape-Xml $ui.card3_label
$c4Label = Escape-Xml $ui.card4_label

[void]$sb1.AppendLine('    <row r="5" ht="18" customHeight="1">')
[void]$sb1.AppendLine("      <c r=`"B5`" t=`"inlineStr`" s=`"13`"><is><t>$c1Label</t></is></c>")
[void]$sb1.AppendLine('      <c r="C5" s="13"/>')
[void]$sb1.AppendLine("      <c r=`"D5`" t=`"inlineStr`" s=`"13`"><is><t>$c2Label</t></is></c>")
[void]$sb1.AppendLine('      <c r="E5" s="13"/>')
[void]$sb1.AppendLine("      <c r=`"F5`" t=`"inlineStr`" s=`"13`"><is><t>$c3Label</t></is></c>")
[void]$sb1.AppendLine('      <c r="G5" s="13"/>')
[void]$sb1.AppendLine("      <c r=`"H5`" t=`"inlineStr`" s=`"13`"><is><t>$c4Label</t></is></c>")
[void]$sb1.AppendLine('      <c r="I5" s="13"/>')
[void]$sb1.AppendLine('    </row>')
[void]$sb1.AppendLine('    <row r="6" ht="15" customHeight="1"/>')

# Section 1 Header: Teacher Performance
[void]$sb1.AppendLine('    <row r="7" ht="24" customHeight="1">')
$sec1 = Escape-Xml $ui.sec1_title
[void]$sb1.AppendLine("      <c r=`"B7`" t=`"inlineStr`" s=`"9`"><is><t>$sec1</t></is></c>")
[void]$sb1.AppendLine('    </row>')

$tHeaders = $ui.t_headers
$colLetters = @("B","C","D","E","F","G","H","I","J")
[void]$sb1.AppendLine('    <row r="8" ht="26" customHeight="1">')
for ($i=0; $i -lt $tHeaders.Count; $i++) {
    $cl = $colLetters[$i]
    $thEsc = Escape-Xml $tHeaders[$i]
    [void]$sb1.AppendLine("      <c r=`"$cl`8`" t=`"inlineStr`" s=`"1`"><is><t>$thEsc</t></is></c>")
}
[void]$sb1.AppendLine('    </row>')

$r = 9
foreach ($c in $classes) {
    $isZ = ($r % 2 -eq 1)
    $sL = if ($isZ) { 3 } else { 0 }
    $sC = if ($isZ) { 4 } else { 2 }
    $sB = if ($isZ) { 6 } else { 5 }
    $sBadge = if ($c.PassRatePct -ge 90) { 7 } elseif ($c.PassRatePct -ge 80) { 10 } else { 8 }

    $gv = Escape-Xml $c.GiangVien
    $lop = Escape-Xml $c.TenLop
    $att = "$($c.ChuyenCanTB)%"
    $hw = "$($c.BTVNTB)%"
    $pass = "$($c.PassRatePct)%"
    $hp = Escape-Xml $c.TuitionStatusText
    $nd = Escape-Xml $c.NhanDinh

    [void]$sb1.AppendLine("    <row r=`"$r`" ht=`"24`" customHeight=`"1`">")
    [void]$sb1.AppendLine("      <c r=`"B$r`" t=`"inlineStr`" s=`"$sL`"><is><t>$gv</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"C$r`" t=`"inlineStr`" s=`"$sL`"><is><t>$lop</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"D$r`" s=`"$sC`"><v>$($c.SiSo)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"E$r`" t=`"inlineStr`" s=`"$sC`"><is><t>$att</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"F$r`" t=`"inlineStr`" s=`"$sC`"><is><t>$hw</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"G$r`" s=`"$sB`"><v>$($c.MockBandTB)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"H$r`" t=`"inlineStr`" s=`"$sBadge`"><is><t>$pass</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"I$r`" t=`"inlineStr`" s=`"$sC`"><is><t>$hp</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"J$r`" t=`"inlineStr`" s=`"$sL`"><is><t>$nd</t></is></c>")
    [void]$sb1.AppendLine('    </row>')
    $r++
}

# Section 2 Header: At-Risk Students
[void]$sb1.AppendLine('    <row r="14" ht="15" customHeight="1"/>')
[void]$sb1.AppendLine('    <row r="15" ht="24" customHeight="1">')
$sec2 = Escape-Xml $ui.sec2_title
[void]$sb1.AppendLine("      <c r=`"B15`" t=`"inlineStr`" s=`"9`"><is><t>$sec2</t></is></c>")
[void]$sb1.AppendLine('    </row>')

$wHeaders = $ui.w_headers
$wCols = @("B","C","D","E","F","G","H","I","J")
[void]$sb1.AppendLine('    <row r="16" ht="26" customHeight="1">')
for ($i=0; $i -lt $wHeaders.Count; $i++) {
    $cl = $wCols[$i]
    $whEsc = Escape-Xml $wHeaders[$i]
    [void]$sb1.AppendLine("      <c r=`"$cl`16`" t=`"inlineStr`" s=`"1`"><is><t>$whEsc</t></is></c>")
}
[void]$sb1.AppendLine('    </row>')

$wr = 17
foreach ($st in $atRiskList) {
    $mHv = Escape-Xml $st.MaHV
    $hTen = Escape-Xml $st.HoTen
    $lop = Escape-Xml $st.Lop
    $gv = Escape-Xml $st.GiangVien
    $lyDo = Escape-Xml $st.LyDo

    [void]$sb1.AppendLine("    <row r=`"$wr`" ht=`"24`" customHeight=`"1`">")
    [void]$sb1.AppendLine("      <c r=`"B$wr`" t=`"inlineStr`" s=`"2`"><is><t>$mHv</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"C$wr`" t=`"inlineStr`" s=`"0`"><is><t>$hTen</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"D$wr`" t=`"inlineStr`" s=`"0`"><is><t>$lop</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"E$wr`" t=`"inlineStr`" s=`"0`"><is><t>$gv</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"F$wr`" s=`"5`"><v>$($st.Mock)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"G$wr`" s=`"5`"><v>$($st.Target)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"H$wr`" s=`"11`"><v>$($st.Delta)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"I$wr`" t=`"inlineStr`" s=`"11`"><is><t>CAN CAN THIEP</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"J$wr`" t=`"inlineStr`" s=`"0`"><is><t>$lyDo</t></is></c>")
    [void]$sb1.AppendLine('    </row>')
    $wr++
}

[void]$sb1.AppendLine('  </sheetData>')
[void]$sb1.AppendLine('  <mergeCells count="4">')
[void]$sb1.AppendLine('    <mergeCell ref="B4:C4"/>')
[void]$sb1.AppendLine('    <mergeCell ref="B5:C5"/>')
[void]$sb1.AppendLine('    <mergeCell ref="D4:E4"/>')
[void]$sb1.AppendLine('    <mergeCell ref="D5:E5"/>')
[void]$sb1.AppendLine('  </mergeCells>')
[void]$sb1.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet1.xml", $sb1.ToString(), [System.Text.Encoding]::UTF8)

# ==============================================================================
# 2.7 Sheet 2: Cleaned_Students_Master
# ==============================================================================
$sb2 = New-Object System.Text.StringBuilder
[void]$sb2.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb2.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb2.AppendLine('  <cols>')
[void]$sb2.AppendLine('    <col min="1" max="1" width="6" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="2" max="2" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="3" max="3" width="24" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="4" max="4" width="15" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="5" max="5" width="13" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="6" max="6" width="8" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="7" max="7" width="10" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="8" max="8" width="15" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="9" max="9" width="22" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="10" max="10" width="20" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="11" max="11" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="12" max="12" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="13" max="13" width="10" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="14" max="14" width="10" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="15" max="15" width="10" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="16" max="16" width="10" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="17" max="17" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="18" max="18" width="12" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="19" max="19" width="12" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="20" max="20" width="18" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="21" max="21" width="18" customWidth="1"/>')
[void]$sb2.AppendLine('  </cols>')
[void]$sb2.AppendLine('  <sheetData>')

# Title
[void]$sb2.AppendLine('    <row r="1" ht="32" customHeight="1">')
$t2 = Escape-Xml $ui.sheet2_title
[void]$sb2.AppendLine("      <c r=`"A1`" t=`"inlineStr`" s=`"9`"><is><t>$t2</t></is></c>")
[void]$sb2.AppendLine('    </row>')
[void]$sb2.AppendLine('    <row r="2" ht="20" customHeight="1">')
$sub2 = Escape-Xml $ui.sheet2_subtitle
[void]$sb2.AppendLine("      <c r=`"A2`" t=`"inlineStr`" s=`"0`"><is><t>$sub2</t></is></c>")
[void]$sb2.AppendLine('    </row>')
[void]$sb2.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# Headers
$s2Headers = $ui.s2_headers
$s2ColLetters = @("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U")

[void]$sb2.AppendLine('    <row r="4" ht="28" customHeight="1">')
for ($c = 0; $c -lt $s2Headers.Count; $c++) {
    $cl = $s2ColLetters[$c]
    $hEsc = Escape-Xml $s2Headers[$c]
    [void]$sb2.AppendLine("      <c r=`"$cl`4`" t=`"inlineStr`" s=`"1`"><is><t>$hEsc</t></is></c>")
}
[void]$sb2.AppendLine('    </row>')

$rIdx = 5
foreach ($st in $students) {
    $isZ = ($rIdx % 2 -eq 1)
    $sL = if ($isZ) { 3 } else { 0 }
    $sC = if ($isZ) { 4 } else { 2 }
    $sScore = if ($isZ) { 6 } else { 5 }
    $sStatus = if ($st.Status -eq "Đúng lộ trình") { 7 } elseif ($st.Status -eq "Vượt kỳ vọng") { 10 } else { 11 }
    $sHP = if ($st.HocPhi -eq "Đã hoàn thành") { 7 } else { 8 }

    $mHV = Escape-Xml $st.MaHV
    $hTen = Escape-Xml $st.HoTen
    $sdt = Escape-Xml $st.SDT_Mask
    $ns = Escape-Xml $st.NgaySinh
    $gt = Escape-Xml $st.GioiTinh
    $mLop = Escape-Xml $st.MaLop
    $tLop = Escape-Xml $st.TenLop
    $gv = Escape-Xml $st.GiangVien
    $att = "$($st.ChuyenCan)%"
    $hw = "$($st.BTVN)%"
    $stt = Escape-Xml $st.Status
    $hp = Escape-Xml $st.HocPhi

    [void]$sb2.AppendLine("    <row r=`"$rIdx`" ht=`"22`" customHeight=`"1`">")
    [void]$sb2.AppendLine("      <c r=`"A$rIdx`" s=`"$sC`"><v>$($st.STT)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"B$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$mHV</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"C$rIdx`" t=`"inlineStr`" s=`"$sL`"><is><t>$hTen</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"D$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$sdt</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"E$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$ns</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"F$rIdx`" s=`"$sC`"><v>$($st.Tuoi)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"G$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$gt</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"H$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$mLop</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"I$rIdx`" t=`"inlineStr`" s=`"$sL`"><is><t>$tLop</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"J$rIdx`" t=`"inlineStr`" s=`"$sL`"><is><t>$gv</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"K$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$att</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"L$rIdx`" t=`"inlineStr`" s=`"$sC`"><is><t>$hw</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"M$rIdx`" s=`"$sScore`"><v>$($st.Lis)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"N$rIdx`" s=`"$sScore`"><v>$($st.Read)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"O$rIdx`" s=`"$sScore`"><v>$($st.Wri)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"P$rIdx`" s=`"$sScore`"><v>$($st.Spe)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"Q$rIdx`" s=`"$sScore`"><v>$($st.MockBand)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"R$rIdx`" s=`"$sScore`"><v>$($st.Target)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"S$rIdx`" s=`"$sScore`"><v>$($st.Delta)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"T$rIdx`" t=`"inlineStr`" s=`"$sStatus`"><is><t>$stt</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"U$rIdx`" t=`"inlineStr`" s=`"$sHP`"><is><t>$hp</t></is></c>")
    [void]$sb2.AppendLine('    </row>')
    $rIdx++
}

[void]$sb2.AppendLine('  </sheetData>')
[void]$sb2.AppendLine("  <autoFilter ref=`"A4:U$($rIdx-1)`"/>")
[void]$sb2.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet2.xml", $sb2.ToString(), [System.Text.Encoding]::UTF8)

# ==============================================================================
# 2.8 Sheet 3: Teacher_KPI_Summary
# ==============================================================================
$sb3 = New-Object System.Text.StringBuilder
[void]$sb3.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb3.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb3.AppendLine('  <cols>')
[void]$sb3.AppendLine('    <col min="1" max="1" width="20" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="2" max="2" width="24" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="3" max="3" width="14" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="4" max="4" width="8" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="5" max="5" width="14" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="6" max="6" width="14" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="7" max="7" width="13" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="8" max="8" width="10" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="9" max="9" width="10" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="10" max="10" width="10" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="11" max="11" width="10" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="12" max="12" width="16" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="13" max="13" width="14" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="14" max="14" width="18" customWidth="1"/>')
[void]$sb3.AppendLine('    <col min="15" max="15" width="45" customWidth="1"/>')
[void]$sb3.AppendLine('  </cols>')
[void]$sb3.AppendLine('  <sheetData>')

# Title
[void]$sb3.AppendLine('    <row r="1" ht="32" customHeight="1">')
$t3 = Escape-Xml $ui.sheet3_title
[void]$sb3.AppendLine("      <c r=`"A1`" t=`"inlineStr`" s=`"9`"><is><t>$t3</t></is></c>")
[void]$sb3.AppendLine('    </row>')
[void]$sb3.AppendLine('    <row r="2" ht="20" customHeight="1">')
$sub3 = Escape-Xml $ui.sheet3_subtitle
[void]$sb3.AppendLine("      <c r=`"A2`" t=`"inlineStr`" s=`"0`"><is><t>$sub3</t></is></c>")
[void]$sb3.AppendLine('    </row>')
[void]$sb3.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# Headers
$s3Headers = $ui.s3_headers
$s3ColLetters = @("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O")

[void]$sb3.AppendLine('    <row r="4" ht="28" customHeight="1">')
for ($c = 0; $c -lt $s3Headers.Count; $c++) {
    $cl = $s3ColLetters[$c]
    $hEsc = Escape-Xml $s3Headers[$c]
    [void]$sb3.AppendLine("      <c r=`"$cl`4`" t=`"inlineStr`" s=`"1`"><is><t>$hEsc</t></is></c>")
}
[void]$sb3.AppendLine('    </row>')

$r3 = 5
foreach ($c in $classes) {
    $isZ = ($r3 % 2 -eq 1)
    $sL = if ($isZ) { 3 } else { 0 }
    $sC = if ($isZ) { 4 } else { 2 }
    $sB = if ($isZ) { 6 } else { 5 }
    $sBadge = if ($c.PassRatePct -ge 90) { 7 } elseif ($c.PassRatePct -ge 80) { 10 } else { 8 }

    $gv = Escape-Xml $c.GiangVien
    $lop = Escape-Xml $c.TenLop
    $trg = Escape-Xml $c.TargetBand
    $att = "$($c.ChuyenCanTB)%"
    $hw = "$($c.BTVNTB)%"
    $pass = "$($c.PassRatePct)%"
    $atRiskStr = "$($c.AtRiskCount) HV"
    $sAtRiskBadge = if ($c.AtRiskCount -eq 0) { 7 } elseif ($c.AtRiskCount -eq 1) { 8 } else { 11 }
    $hp = Escape-Xml $c.TuitionStatusText
    $nd = Escape-Xml $c.NhanDinh

    [void]$sb3.AppendLine("    <row r=`"$r3`" ht=`"26`" customHeight=`"1`">")
    [void]$sb3.AppendLine("      <c r=`"A$r3`" t=`"inlineStr`" s=`"$sL`"><is><t>$gv</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"B$r3`" t=`"inlineStr`" s=`"$sL`"><is><t>$lop</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"C$r3`" t=`"inlineStr`" s=`"$sC`"><is><t>$trg</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"D$r3`" s=`"$sC`"><v>$($c.SiSo)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"E$r3`" t=`"inlineStr`" s=`"$sC`"><is><t>$att</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"F$r3`" t=`"inlineStr`" s=`"$sC`"><is><t>$hw</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"G$r3`" s=`"$sB`"><v>$($c.MockBandTB)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"H$r3`" s=`"$sB`"><v>$($c.LisTB)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"I$r3`" s=`"$sB`"><v>$($c.ReadTB)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"J$r3`" s=`"$sB`"><v>$($c.WriTB)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"K$r3`" s=`"$sB`"><v>$($c.SpeTB)</v></c>")
    [void]$sb3.AppendLine("      <c r=`"L$r3`" t=`"inlineStr`" s=`"$sBadge`"><is><t>$pass</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"M$r3`" t=`"inlineStr`" s=`"$sAtRiskBadge`"><is><t>$atRiskStr</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"N$r3`" t=`"inlineStr`" s=`"$sC`"><is><t>$hp</t></is></c>")
    [void]$sb3.AppendLine("      <c r=`"O$r3`" t=`"inlineStr`" s=`"$sL`"><is><t>$nd</t></is></c>")
    [void]$sb3.AppendLine('    </row>')
    $r3++
}

[void]$sb3.AppendLine('  </sheetData>')
[void]$sb3.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet3.xml", $sb3.ToString(), [System.Text.Encoding]::UTF8)

# ==============================================================================
# 2.9 Sheet 4: Data_Dictionary
# ==============================================================================
$sb4 = New-Object System.Text.StringBuilder
[void]$sb4.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb4.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb4.AppendLine('  <cols>')
[void]$sb4.AppendLine('    <col min="1" max="1" width="6" customWidth="1"/>')
[void]$sb4.AppendLine('    <col min="2" max="2" width="22" customWidth="1"/>')
[void]$sb4.AppendLine('    <col min="3" max="3" width="15" customWidth="1"/>')
[void]$sb4.AppendLine('    <col min="4" max="4" width="18" customWidth="1"/>')
[void]$sb4.AppendLine('    <col min="5" max="5" width="45" customWidth="1"/>')
[void]$sb4.AppendLine('    <col min="6" max="6" width="30" customWidth="1"/>')
[void]$sb4.AppendLine('  </cols>')
[void]$sb4.AppendLine('  <sheetData>')

# Title
[void]$sb4.AppendLine('    <row r="1" ht="32" customHeight="1">')
$t4 = Escape-Xml $ui.sheet4_title
[void]$sb4.AppendLine("      <c r=`"A1`" t=`"inlineStr`" s=`"9`"><is><t>$t4</t></is></c>")
[void]$sb4.AppendLine('    </row>')
[void]$sb4.AppendLine('    <row r="2" ht="20" customHeight="1">')
$sub4 = Escape-Xml $ui.sheet4_subtitle
[void]$sb4.AppendLine("      <c r=`"A2`" t=`"inlineStr`" s=`"0`"><is><t>$sub4</t></is></c>")
[void]$sb4.AppendLine('    </row>')
[void]$sb4.AppendLine('    <row r="3" ht="10" customHeight="1"/>')

# Headers
$dictHeaders = $ui.s4_headers
$dictCols = @("A","B","C","D","E","F")
[void]$sb4.AppendLine('    <row r="4" ht="28" customHeight="1">')
for ($c = 0; $c -lt $dictHeaders.Count; $c++) {
    $cl = $dictCols[$c]
    $hEsc = Escape-Xml $dictHeaders[$c]
    [void]$sb4.AppendLine("      <c r=`"$cl`4`" t=`"inlineStr`" s=`"1`"><is><t>$hEsc</t></is></c>")
}
[void]$sb4.AppendLine('    </row>')

$dr = 5
foreach ($di in $dataDict) {
    $isZ = ($dr % 2 -eq 1)
    $sL = if ($isZ) { 3 } else { 0 }
    $sC = if ($isZ) { 4 } else { 2 }

    $col = Escape-Xml $di.Col
    $type = Escape-Xml $di.Type
    $samp = Escape-Xml $di.Sample
    $desc = Escape-Xml $di.Desc
    $rule = Escape-Xml $di.Rule

    [void]$sb4.AppendLine("    <row r=`"$dr`" ht=`"22`" customHeight=`"1`">")
    [void]$sb4.AppendLine("      <c r=`"A$dr`" s=`"$sC`"><v>$($di.STT)</v></c>")
    [void]$sb4.AppendLine("      <c r=`"B$dr`" t=`"inlineStr`" s=`"$sL`"><is><t>$col</t></is></c>")
    [void]$sb4.AppendLine("      <c r=`"C$dr`" t=`"inlineStr`" s=`"$sC`"><is><t>$type</t></is></c>")
    [void]$sb4.AppendLine("      <c r=`"D$dr`" t=`"inlineStr`" s=`"$sC`"><is><t>$samp</t></is></c>")
    [void]$sb4.AppendLine("      <c r=`"E$dr`" t=`"inlineStr`" s=`"$sL`"><is><t>$desc</t></is></c>")
    [void]$sb4.AppendLine("      <c r=`"F$dr`" t=`"inlineStr`" s=`"$sL`"><is><t>$rule</t></is></c>")
    [void]$sb4.AppendLine('    </row>')
    $dr++
}

[void]$sb4.AppendLine('  </sheetData>')
[void]$sb4.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet4.xml", $sb4.ToString(), [System.Text.Encoding]::UTF8)

# 2.10 Package ZIP into final XLSX
$targetExcelReport = Join-Path $OutputDir $ExcelName
$targetExcelSample = "sample-data/$ExcelName"

if (Test-Path $targetExcelReport) { Remove-Item $targetExcelReport -Force }
if (Test-Path $targetExcelSample) { Remove-Item $targetExcelSample -Force }

$zipFile = Join-Path $env:TEMP ("ielts_pack_" + [System.Guid]::NewGuid().ToString("N") + ".zip")
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $zipFile, [System.IO.Compression.CompressionLevel]::Optimal, $false)

Copy-Item $zipFile -Destination $targetExcelReport -Force
Copy-Item $zipFile -Destination $targetExcelSample -Force

Remove-Item $zipFile -Force -ErrorAction SilentlyContinue
Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "[EXCEL] Generated Master Excel successfully at:" -ForegroundColor Cyan
Write-Host "  -> $targetExcelReport" -ForegroundColor White
Write-Host "  -> $targetExcelSample" -ForegroundColor White
Write-Host "[SUCCESS] ACADEMIC OPS PIPELINE COMPLETED SUCCESSFULLY!" -ForegroundColor Green
