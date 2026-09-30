# process_academic.ps1
# Engine tu dong hoa thu thap, lam sach du lieu hoc vien, tao Master Excel da sheet va tong hop KPI giang vien
# Tac gia: Academic Training Officer / Antigravity AI (AI4A Framework)

[CmdletBinding()]
param (
    [string]$InputPath = "",
    [string]$OutputDir = "outputs/reports",
    [string]$ExcelFileName = "Academic_Student_Grades_Master.xlsx",
    [string]$MetricsFileName = "academic_summary_metrics.json"
)

$ErrorActionPreference = "Stop"

# Load .NET Compression Assemblies
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[START] ACADEMIC TRAINING OPS PIPELINE DANG KHOI CHAY..." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Dinh vi tap du lieu dau vao
if (-not $InputPath) {
    $found = Get-ChildItem -Path "sample-data" -Filter "*raw_student*.json" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $InputPath = $found.FullName
    } else {
        Write-Error "Khong tim thay file du lieu hoc vien trong sample-data. Vui long truyen -InputPath"
        exit 1
    }
}

if (-not (Test-Path $InputPath)) {
    Write-Error "Tep nguon khong ton tai: $InputPath"
    exit 1
}

Write-Host "[INFO] Doc du lieu tu tap tin: $InputPath" -ForegroundColor Gray

# Dam bao thu muc dau ra ton tai
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# 2. Doc du lieu tho va bat dau qua trinh lam sach
$rawJsonContent = Get-Content -Path $InputPath -Raw -Encoding UTF8
$rawItems = $rawJsonContent | ConvertFrom-Json

$totalRawRecords = $rawItems.Count
Write-Host "[STAGE 1 - HARVEST] Thu thap thanh cong $totalRawRecords ban ghi tho." -ForegroundColor Green

$cleanedList = New-Object System.Collections.Generic.List[PSObject]
$seenKeys = New-Object System.Collections.Generic.HashSet[string]

$purgedGhostCount = 0
$purgedDuplicateCount = 0
$purgedCorruptedScoreCount = 0
$maskedPiiCount = 0

foreach ($row in $rawItems) {
    # 2.1 Loc ghost rows (Thieu Student_ID hoac Class_ID)
    $sId = if ($row.Student_ID) { [string]$row.Student_ID.Trim() } else { "" }
    $cId = if ($row.Class_ID) { [string]$row.Class_ID.Trim() } else { "" }
    $sName = if ($row.Student_Name) { [string]$row.Student_Name.Trim() } else { "" }

    if ([string]::IsNullOrWhiteSpace($sId) -or [string]::IsNullOrWhiteSpace($cId) -or $sName -match "Rác|Unknown") {
        $purgedGhostCount++
        continue
    }

    # 2.2 Loc ban ghi trung lap (Composite Key: Student_ID + Class_ID)
    $compositeKey = "$sId|$cId"
    if ($seenKeys.Contains($compositeKey)) {
        $purgedDuplicateCount++
        continue
    }
    $seenKeys.Add($compositeKey) | Out-Null

    # 2.3 Lam sach va ep kieu so hoc cho cac cot diem (Attendance, Midterm, Final)
    function Parse-Score([string]$val) {
        if ([string]::IsNullOrWhiteSpace($val)) { return 0.0 }
        $v = $val.Trim().ToLower()
        if ($v -match "vắng|absent|n/a|chưa nộp") { return 0.0 }
        # Loai bo text thua nhu "diem", "điểm"
        $v = $v -replace "[^\d,\.-]", ""
        $v = $v -replace ",", "."
        $outVal = 0.0
        if ([double]::TryParse($v, [System.Globalization.NumberStyles]::Any, [System.Globalization.CultureInfo]::InvariantCulture, [ref]$outVal)) {
            return $outVal
        }
        return -999.0 # Gia tri loi
    }

    $attScore = Parse-Score -val ([string]$row.Attendance)
    $midScore = Parse-Score -val ([string]$row.Midterm)
    $finScore = Parse-Score -val ([string]$row.Final)

    # Kiem tra tinh hop le cua thang diem 0 - 10
    if ($attScore -lt 0.0 -or $attScore -gt 10.0 -or `
        $midScore -lt 0.0 -or $midScore -gt 10.0 -or `
        $finScore -lt 0.0 -or $finScore -gt 10.0) {
        $purgedCorruptedScoreCount++
        continue
    }

    # 2.4 Tinh toan diem tong ket (10% CC + 30% GK + 60% CK)
    $totalScore = [Math]::Round(($attScore * 0.10) + ($midScore * 0.30) + ($finScore * 0.60), 2)

    # 2.5 Xep loai va trang thai
    $status = if ($totalScore -ge 5.0) { "PASS" } else { "FAIL" }
    $rank = if ($totalScore -ge 9.0) { "Xuất sắc" }
            elseif ($totalScore -ge 8.0) { "Giỏi" }
            elseif ($totalScore -ge 6.5) { "Khá" }
            elseif ($totalScore -ge 5.0) { "Trung bình" }
            else { "Yếu / Không Đạt" }

    # 2.6 Masking PII
    if ($row.Personal_Phone -or $row.Personal_Email) {
        $maskedPiiCount++
    }

    $item = [PSCustomObject]@{
        Class_ID       = $cId
        Course_Name    = [string]$row.Course_Name
        Teacher_Name   = [string]$row.Teacher_Name
        Student_ID     = $sId
        Student_Name   = $sName
        Attendance     = $attScore
        Midterm        = $midScore
        Final          = $finScore
        Total_Score    = $totalScore
        Grade_Rank     = $rank
        Status         = $status
    }
    $cleanedList.Add($item)
}

$validStudentCount = $cleanedList.Count
$totalPurged = $purgedGhostCount + $purgedDuplicateCount + $purgedCorruptedScoreCount

Write-Host "[STAGE 2 - CLEANSE] Ket qua lam sach du lieu:" -ForegroundColor Yellow
Write-Host "  - So ban ghi hop le: $validStudentCount" -ForegroundColor Green
Write-Host "  - Ghost rows da loai bo: $purgedGhostCount" -ForegroundColor Gray
Write-Host "  - Ban ghi trung lap da loai bo: $purgedDuplicateCount" -ForegroundColor Gray
Write-Host "  - Ban ghi diem ngoai pham vi (0-10): $purgedCorruptedScoreCount" -ForegroundColor Gray
Write-Host "  - Ho so da duoc bao mat PII: $maskedPiiCount" -ForegroundColor Gray

# 3. Tong hop chi so KPI theo tung Giang vien
$teachersGroup = $cleanedList | Group-Object -Property Teacher_Name
$teacherKpiList = New-Object System.Collections.Generic.List[PSObject]

foreach ($tg in $teachersGroup) {
    $tName = $tg.Name
    $students = $tg.Group
    $count = $students.Count
    $cId = ($students | Select-Object -ExpandProperty Class_ID -Unique) -join ", "
    $courseName = ($students | Select-Object -ExpandProperty Course_Name -Unique) -join ", "

    $passedCount = ($students | Where-Object { $_.Status -eq "PASS" }).Count
    $failedCount = $count - $passedCount
    $passRate = [Math]::Round(($passedCount / $count) * 100, 1)

    $avgAtt = [Math]::Round(($students | Measure-Object -Property Attendance -Average).Average, 2)
    $avgMid = [Math]::Round(($students | Measure-Object -Property Midterm -Average).Average, 2)
    $avgFin = [Math]::Round(($students | Measure-Object -Property Final -Average).Average, 2)
    $avgTotal = [Math]::Round(($students | Measure-Object -Property Total_Score -Average).Average, 2)

    # Phan loai rank (Bao dam luon la so nguyen int)
    $countXS = @($students | Where-Object { $_.Grade_Rank -eq "Xuất sắc" }).Count
    $countGioi = @($students | Where-Object { $_.Grade_Rank -eq "Giỏi" }).Count
    $countKha = @($students | Where-Object { $_.Grade_Rank -eq "Khá" }).Count
    $countTB = @($students | Where-Object { $_.Grade_Rank -eq "Trung bình" }).Count
    $countYeu = @($students | Where-Object { $_.Grade_Rank -eq "Yếu / Không Đạt" }).Count

    $goodExcellentPct = [Math]::Round((($countXS + $countGioi) / $count) * 100, 1)

    # Tinh Do lech chuan (Standard Deviation) de xem do phan hoa
    $varianceSum = 0.0
    foreach ($s in $students) {
        $varianceSum += [Math]::Pow(($s.Total_Score - $avgTotal), 2)
    }
    $stdDev = if ($count -gt 1) { [Math]::Round([Math]::Sqrt($varianceSum / $count), 2) } else { 0.0 }

    # Danh gia so bo
    $pedagogicalNote = if ($passRate -lt 80.0) { "Cảnh báo tỷ lệ rớt cao; phân hóa mạnh" }
                       elseif ($goodExcellentPct -ge 70.0 -and $stdDev -lt 0.6) { "Cảnh báo lạm phát điểm (chấm quá dễ)" }
                       elseif ($passRate -ge 90.0) { "Hiệu suất đào tạo rất tốt; phổ điểm chuẩn" }
                       else { "Đạt chuẩn yêu cầu đào tạo" }

    $tKpi = [PSCustomObject]@{
        Teacher_Name       = $tName
        Class_ID           = $cId
        Course_Name        = $courseName
        Student_Count      = $count
        Passed_Count       = $passedCount
        Failed_Count       = $failedCount
        Pass_Rate_Pct      = $passRate
        Avg_Attendance     = $avgAtt
        Avg_Midterm        = $avgMid
        Avg_Final          = $avgFin
        Avg_Total_Score    = $avgTotal
        Excellent_Count    = $countXS
        Good_Count         = $countGioi
        Fair_Count         = $countKha
        Avg_Rank_Count     = $countTB
        Weak_Rank_Count    = $countYeu
        Good_Excellent_Pct = $goodExcellentPct
        Std_Dev            = $stdDev
        Pedagogical_Note   = $pedagogicalNote
    }
    $teacherKpiList.Add($tKpi)
}

# 4. Xuat File Master Excel (Da Sheet) bang System.IO.Compression & OpenXML
$targetExcelPath = Join-Path $OutputDir $ExcelFileName
if (Test-Path $targetExcelPath) { Remove-Item $targetExcelPath -Force }

Write-Host "[STAGE 3 - EXCEL ENGINE] Dang sinh file Excel Master da sheet..." -ForegroundColor Yellow

$tempDir = Join-Path $env:TEMP ("academic_excel_" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path "$tempDir\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\worksheets" -Force | Out-Null

# 4.1 [Content_Types].xml
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

# 4.2 _rels/.rels
$rootRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\_rels\.rels", $rootRels, [System.Text.Encoding]::UTF8)

# 4.3 xl/workbook.xml
$workbookXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Student_Grades_Cleaned" sheetId="1" r:id="rId1"/>
    <sheet name="Teacher_KPI_Summary" sheetId="2" r:id="rId2"/>
  </sheets>
</workbook>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\workbook.xml", $workbookXml, [System.Text.Encoding]::UTF8)

# 4.4 xl/_rels/workbook.xml.rels
$wbRels = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\_rels\workbook.xml.rels", $wbRels, [System.Text.Encoding]::UTF8)

# 4.5 xl/styles.xml
$stylesXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="2">
    <numFmt numFmtId="164" formatCode="0.00"/>
    <numFmt numFmtId="165" formatCode="0.0%"/>
  </numFmts>
  <fonts count="4">
    <font><sz val="10"/><name val="Segoe UI"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF0F172A"/><name val="Segoe UI"/></font>
    <font><b/><sz val="10"/><color rgb="FF16A34A"/><name val="Segoe UI"/></font>
  </fonts>
  <fills count="5">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1E293B"/></patternFill></fill> <!-- 2: Header Navy -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8FAFC"/></patternFill></fill> <!-- 3: Zebra -->
    <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></patternFill></fill> <!-- 4: Pass Light Green -->
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
  <cellXfs count="8">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0"/> <!-- 0: Plain text -->
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf> <!-- 1: Header -->
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="right"/></xf> <!-- 2: Decimal 0.00 -->
    <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="right"/></xf> <!-- 3: Percent -->
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center"/></xf> <!-- 4: Center Text -->
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0"/> <!-- 5: Zebra Text -->
    <xf numFmtId="164" fontId="0" fillId="3" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="right"/></xf> <!-- 6: Zebra Decimal -->
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyAlignment="1"><alignment horizontal="center"/></xf> <!-- 7: Pass Green Status -->
  </cellXfs>
</styleSheet>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\styles.xml", $stylesXml, [System.Text.Encoding]::UTF8)

# 4.6 Sheet 1: Student_Grades_Cleaned
$sb1 = New-Object System.Text.StringBuilder
[void]$sb1.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb1.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb1.AppendLine('  <cols>')
[void]$sb1.AppendLine('    <col min="1" max="1" width="6" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="2" max="2" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="3" max="3" width="28" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="4" max="4" width="25" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="5" max="5" width="14" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="6" max="6" width="24" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="7" max="10" width="12" customWidth="1"/>')
[void]$sb1.AppendLine('    <col min="11" max="12" width="16" customWidth="1"/>')
[void]$sb1.AppendLine('  </cols>')
[void]$sb1.AppendLine('  <sheetData>')

# Header Row Sheet 1
$headers1 = @("STT", "Mã Lớp", "Tên Khóa Học", "Giảng Viên Phụ Trách", "Mã Học Viên", "Họ Tên Học Viên", "Chuyên Cần", "Giữa Kỳ", "Cuối Kỳ", "Tổng Kết", "Xếp Loại", "Trạng Thái")
[void]$sb1.AppendLine('    <row r="1" ht="28" customHeight="1">')
for ($c = 0; $c -lt $headers1.Count; $c++) {
    $colL = [char](65 + $c)
    $hEsc = [System.Security.SecurityElement]::Escape($headers1[$c])
    [void]$sb1.AppendLine("      <c r=`"$colL`1`" t=`"inlineStr`" s=`"1`"><is><t>$hEsc</t></is></c>")
}
[void]$sb1.AppendLine('    </row>')

$rIdx = 2
$stt = 1
foreach ($st in $cleanedList) {
    $isZebra = ($rIdx % 2 -eq 1)
    [void]$sb1.AppendLine("    <row r=`"$rIdx`" ht=`"20`" customHeight=`"1`">")

    # STT (Center)
    $sText = if ($isZebra) { 5 } else { 4 }
    [void]$sb1.AppendLine("      <c r=`"A$rIdx`" s=`"$sText`"><v>$stt</v></c>")

    # Class_ID, Course_Name, Teacher_Name, Student_ID, Student_Name
    $cEsc = [System.Security.SecurityElement]::Escape($st.Class_ID)
    $crsEsc = [System.Security.SecurityElement]::Escape($st.Course_Name)
    $tEsc = [System.Security.SecurityElement]::Escape($st.Teacher_Name)
    $sidEsc = [System.Security.SecurityElement]::Escape($st.Student_ID)
    $snEsc = [System.Security.SecurityElement]::Escape($st.Student_Name)

    [void]$sb1.AppendLine("      <c r=`"B$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$cEsc</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"C$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$crsEsc</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"D$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$tEsc</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"E$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$sidEsc</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"F$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$snEsc</t></is></c>")

    # Attendance, Midterm, Final, Total_Score (Decimals)
    $sDec = if ($isZebra) { 6 } else { 2 }
    [void]$sb1.AppendLine("      <c r=`"G$rIdx`" s=`"$sDec`"><v>$($st.Attendance)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"H$rIdx`" s=`"$sDec`"><v>$($st.Midterm)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"I$rIdx`" s=`"$sDec`"><v>$($st.Final)</v></c>")
    [void]$sb1.AppendLine("      <c r=`"J$rIdx`" s=`"$sDec`"><v>$($st.Total_Score)</v></c>")

    # Grade_Rank & Status
    $rankEsc = [System.Security.SecurityElement]::Escape($st.Grade_Rank)
    $statEsc = [System.Security.SecurityElement]::Escape($st.Status)
    $sStat = if ($st.Status -eq "PASS") { 7 } else { 4 }

    [void]$sb1.AppendLine("      <c r=`"K$rIdx`" t=`"inlineStr`" s=`"$sText`"><is><t>$rankEsc</t></is></c>")
    [void]$sb1.AppendLine("      <c r=`"L$rIdx`" t=`"inlineStr`" s=`"$sStat`"><is><t>$statEsc</t></is></c>")

    [void]$sb1.AppendLine('    </row>')
    $rIdx++
    $stt++
}
[void]$sb1.AppendLine('  </sheetData>')
[void]$sb1.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet1.xml", $sb1.ToString(), [System.Text.Encoding]::UTF8)

# 4.7 Sheet 2: Teacher_KPI_Summary
$sb2 = New-Object System.Text.StringBuilder
[void]$sb2.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
[void]$sb2.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
[void]$sb2.AppendLine('  <cols>')
[void]$sb2.AppendLine('    <col min="1" max="1" width="26" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="2" max="2" width="28" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="3" max="7" width="12" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="8" max="10" width="16" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="11" max="11" width="14" customWidth="1"/>')
[void]$sb2.AppendLine('    <col min="12" max="12" width="38" customWidth="1"/>')
[void]$sb2.AppendLine('  </cols>')
[void]$sb2.AppendLine('  <sheetData>')

$headers2 = @("Giảng Viên", "Môn Phụ Trách", "Sĩ Số", "Đạt (Pass)", "Rớt (Fail)", "Tỷ Lệ Pass (%)", "Điểm TB Lớp", "Điểm TB Giữa Kỳ", "Điểm TB Cuối Kỳ", "Tỷ Lệ Giỏi/XS (%)", "Độ Phân Hóa", "Đánh Giá Sư Phạm")
[void]$sb2.AppendLine('    <row r="1" ht="28" customHeight="1">')
for ($c = 0; $c -lt $headers2.Count; $c++) {
    $colL = [char](65 + $c)
    $hEsc = [System.Security.SecurityElement]::Escape($headers2[$c])
    [void]$sb2.AppendLine("      <c r=`"$colL`1`" t=`"inlineStr`" s=`"1`"><is><t>$hEsc</t></is></c>")
}
[void]$sb2.AppendLine('    </row>')

$rIdx2 = 2
foreach ($tk in $teacherKpiList) {
    $isZebra = ($rIdx2 % 2 -eq 1)
    $sText = if ($isZebra) { 5 } else { 4 }
    $sDec = if ($isZebra) { 6 } else { 2 }

    [void]$sb2.AppendLine("    <row r=`"$rIdx2`" ht=`"22`" customHeight=`"1`">")

    $tEsc = [System.Security.SecurityElement]::Escape($tk.Teacher_Name)
    $cEsc = [System.Security.SecurityElement]::Escape($tk.Course_Name)
    $noteEsc = [System.Security.SecurityElement]::Escape($tk.Pedagogical_Note)

    [void]$sb2.AppendLine("      <c r=`"A$rIdx2`" t=`"inlineStr`" s=`"$sText`"><is><t>$tEsc</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"B$rIdx2`" t=`"inlineStr`" s=`"$sText`"><is><t>$cEsc</t></is></c>")
    [void]$sb2.AppendLine("      <c r=`"C$rIdx2`" s=`"$sText`"><v>$($tk.Student_Count)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"D$rIdx2`" s=`"$sText`"><v>$($tk.Passed_Count)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"E$rIdx2`" s=`"$sText`"><v>$($tk.Failed_Count)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"F$rIdx2`" s=`"$sDec`"><v>$($tk.Pass_Rate_Pct)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"G$rIdx2`" s=`"$sDec`"><v>$($tk.Avg_Total_Score)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"H$rIdx2`" s=`"$sDec`"><v>$($tk.Avg_Midterm)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"I$rIdx2`" s=`"$sDec`"><v>$($tk.Avg_Final)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"J$rIdx2`" s=`"$sDec`"><v>$($tk.Good_Excellent_Pct)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"K$rIdx2`" s=`"$sDec`"><v>$($tk.Std_Dev)</v></c>")
    [void]$sb2.AppendLine("      <c r=`"L$rIdx2`" t=`"inlineStr`" s=`"$sText`"><is><t>$noteEsc</t></is></c>")

    [void]$sb2.AppendLine('    </row>')
    $rIdx2++
}
[void]$sb2.AppendLine('  </sheetData>')
[void]$sb2.AppendLine('</worksheet>')
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet2.xml", $sb2.ToString(), [System.Text.Encoding]::UTF8)

# 4.8 Dong goi Zip va chuan hoa slash sang OpenXML tieu chuan
[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $targetExcelPath)
Remove-Item $tempDir -Recurse -Force

$tempZip = $targetExcelPath + ".tmp"
if (Test-Path $tempZip) { Remove-Item $tempZip -Force }
$src = [System.IO.Compression.ZipFile]::OpenRead($targetExcelPath)
$dst = [System.IO.Compression.ZipFile]::Open($tempZip, [System.IO.Compression.ZipArchiveMode]::Create)
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
Remove-Item $targetExcelPath -Force
Move-Item $tempZip $targetExcelPath

Write-Host "[SUCCESS] Da tao thanh cong Excel Master da sheet tai: $targetExcelPath" -ForegroundColor Green

# 5. Xuat Metrics JSON phuc vu Agent Lap Bao Cao
$overallPassed = ($cleanedList | Where-Object { $_.Status -eq "PASS" }).Count
$overallPassRate = [Math]::Round(($overallPassed / $validStudentCount) * 100, 1)
$overallAvg = [Math]::Round(($cleanedList | Measure-Object -Property Total_Score -Average).Average, 2)
$overallGoodEx = [Math]::Round((($cleanedList | Where-Object { $_.Grade_Rank -in @("Xuất sắc", "Giỏi") }).Count / $validStudentCount) * 100, 1)

$metricsObj = [PSCustomObject]@{
    Generated_At           = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    Raw_Records_Count      = $totalRawRecords
    Valid_Student_Count    = $validStudentCount
    Purged_Ghost_Count     = $purgedGhostCount
    Purged_Duplicate_Count = $purgedDuplicateCount
    Purged_Invalid_Score   = $purgedCorruptedScoreCount
    Masked_PII_Count       = $maskedPiiCount
    Overall_Classes_Count  = $teachersGroup.Count
    Overall_Passed_Count   = $overallPassed
    Overall_Pass_Rate_Pct  = $overallPassRate
    Overall_Avg_Score      = $overallAvg
    Overall_Good_Ex_Pct    = $overallGoodEx
    Master_Excel_File      = $targetExcelPath
    Teachers_KPI           = $teacherKpiList
}

$metricsJsonPath = Join-Path $OutputDir $MetricsFileName
[System.IO.File]::WriteAllText($metricsJsonPath, ($metricsObj | ConvertTo-Json -Depth 6), [System.Text.Encoding]::UTF8)
Write-Host "[SUCCESS] Da xuat chi so phan tich JSON tai: $metricsJsonPath" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[DONE] PIPELINE HOAN TAT 100% TIEN TRINH!" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
