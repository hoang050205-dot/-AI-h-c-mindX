# build_medical_payroll_master.ps1
# Engine sinh du lieu va xay dung Master Excel 3 Sheet cho 12 Nhan su Cap cao Nganh Y (24 Thang)
[CmdletBinding()]
param (
    [string]$ConfigPath = "sample-data/medical_csuite_profiles.json",
    [string]$OutputDir = "sample-data",
    [string]$ReportsDir = "outputs/reports",
    [string]$ExcelName = "Medical_CSuite_Payroll_24Months_Master.xlsx",
    [string]$JsonName = "medical_csuite_payroll_24m.json",
    [string]$SummaryJsonName = "medical_payroll_executive_metrics.json"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[INIT] MEDICAL C-SUITE PAYROLL SIMULATION ENGINE (24 MONTHS)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

if (-not (Test-Path $ConfigPath)) {
    Write-Error "Configuration file not found: $ConfigPath"
    exit 1
}

$rawJson = [System.IO.File]::ReadAllText((Resolve-Path $ConfigPath), [System.Text.Encoding]::UTF8)
$cfg = $rawJson | ConvertFrom-Json
$profiles = $cfg.profiles
$timeline = $cfg.timeline_coefficients

Write-Host "[CONFIG] Loaded $($profiles.Count) C-Suite Profiles and $($timeline.Count) Timeline cycles." -ForegroundColor Green

# Ham tinh thue TNCN luy tien 7 bac (Viet Nam Standard PIT)
function Calculate-PIT([double]$taxableIncome) {
    if ($taxableIncome -le 0) { return 0 }
    $t = $taxableIncome
    if ($t -le 5000000) {
        return [Math]::Round($t * 0.05)
    } elseif ($t -le 10000000) {
        return [Math]::Round($t * 0.10 - 250000)
    } elseif ($t -le 18000000) {
        return [Math]::Round($t * 0.15 - 750000)
    } elseif ($t -le 32000000) {
        return [Math]::Round($t * 0.20 - 1650000)
    } elseif ($t -le 52000000) {
        return [Math]::Round($t * 0.25 - 3250000)
    } elseif ($t -le 80000000) {
        return [Math]::Round($t * 0.30 - 5850000)
    } else {
        return [Math]::Round($t * 0.35 - 9850000)
    }
}

Write-Host "[SIMULATION] Computing 288 records across 24 cycles..." -ForegroundColor Yellow

$records = [System.Collections.Generic.List[PSObject]]::new()
$random = [System.Random]::new(42)

foreach ($t in $timeline) {
    $mNum = $t.index
    $year = [int]$t.year
    $month = [int]$t.month
    $label = $t.label

    # Quy dinh tran BHXH (Truoc 07/2024: 36M; Tu 07/2024: 46.8M)
    $maxSocialCap = if ($year -eq 2024 -and $month -lt 7) { 36000000 } else { 46800000 }
    $insurDeduction = [Math]::Round($maxSocialCap * 0.105)

    foreach ($p in $profiles) {
        $noise = 0.96 + ($random.NextDouble() * 0.08)
        
        $surgCount = [Math]::Round($p.base_surg_count * $t.surg * $noise)
        $surgPay = [Math]::Round($surgCount * $p.surg_unit_price)

        $clinicCount = [Math]::Round($p.base_clinic_count * $t.clinic * $noise)
        $clinicPay = [Math]::Round($clinicCount * $p.clinic_unit_price)

        $kpiPay = [Math]::Round($p.base_kpi * $t.kpi * $noise)

        # Retention bonus phan bo theo quy (Thang 3, 6, 9, 12)
        $retentionBonus = 0
        if ($month % 3 -eq 0) {
            $retentionBonus = $p.retention_bonus_quarterly
        }

        # Tong Gross
        $p1 = [double]$p.p1_base
        $p2 = [double]$p.p2_allowance
        $gross = $p1 + $p2 + $surgPay + $clinicPay + $kpiPay + $retentionBonus

        # Giam tru gia canh & BH nghe nghiep y khoa
        $selfDeduction = 11000000
        $depDeduction = [int]$p.dependents * 4400000
        $malpracticeInsurance = 500000
        $totalDeductions = $insurDeduction + $selfDeduction + $depDeduction + $malpracticeInsurance

        $taxableIncome = [Math]::Max(0, ($gross - $totalDeductions))
        $pitTax = Calculate-PIT -taxableIncome $taxableIncome

        $net = $gross - $insurDeduction - $malpracticeInsurance - $pitTax

        $revenueGenerated = [Math]::Round($p.base_revenue * $t.rev * $noise)
        $costToRevRatio = if ($revenueGenerated -gt 0) { [Math]::Round(($gross / $revenueGenerated) * 100, 2) } else { 0 }

        $rec = [PSCustomObject]@{
            CycleIndex = $mNum
            MonthLabel = $label
            Year = $year
            Month = $month
            StaffId = $p.id
            FullName = $p.name
            RoleTitle = $p.role
            Department = $p.department
            Category = $p.category
            P1_Base = $p1
            P2_Allowance = $p2
            SurgeryCount = $surgCount
            P3_SurgeryPay = $surgPay
            ClinicConsultCount = $clinicCount
            P3_ClinicPay = $clinicPay
            P3_KpiBonus = $kpiPay
            P4_Retention = $retentionBonus
            TotalGross = $gross
            SocialInsurance = $insurDeduction
            PIT_Tax = $pitTax
            TotalNet = $net
            SpecialtyRevenue = $revenueGenerated
            CostToRevenuePct = $costToRevRatio
        }
        $records.Add($rec)
    }
}

Write-Host "[DATA] Generated $($records.Count) payroll records." -ForegroundColor Green

# Ghi file JSON raw
$jsonPath = Join-Path $OutputDir $JsonName
$recordsJson = $records | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText((Resolve-Path $OutputDir | Join-Path -ChildPath $JsonName), $recordsJson, [System.Text.Encoding]::UTF8)
Write-Host "[JSON] Saved raw payroll data to: $jsonPath" -ForegroundColor Green

# Tinh toan Metrics tong the
$totalGross24M = ($records | Measure-Object -Property TotalGross -Sum).Sum
$totalNet24M = ($records | Measure-Object -Property TotalNet -Sum).Sum
$totalPit24M = ($records | Measure-Object -Property PIT_Tax -Sum).Sum
$totalRevenue24M = ($records | Measure-Object -Property SpecialtyRevenue -Sum).Sum
$totalSurgeries24M = ($records | Measure-Object -Property SurgeryCount -Sum).Sum
$totalClinics24M = ($records | Measure-Object -Property ClinicConsultCount -Sum).Sum

$overallCostToRev = [Math]::Round(($totalGross24M / $totalRevenue24M) * 100, 2)
$avgGrossMonthly = [Math]::Round($totalGross24M / 24)
$avgNetMonthly = [Math]::Round($totalNet24M / 24)

# Thong ke theo 24 thang
$monthlySummary = @()
for ($mNum = 1; $mNum -le 24; $mNum++) {
    $mRecs = $records | Where-Object { $_.CycleIndex -eq $mNum }
    $mLabel = $mRecs[0].MonthLabel
    $mYear = $mRecs[0].Year
    $mMonth = $mRecs[0].Month

    $mGross = ($mRecs | Measure-Object -Property TotalGross -Sum).Sum
    $mP1 = ($mRecs | Measure-Object -Property P1_Base -Sum).Sum
    $mP2 = ($mRecs | Measure-Object -Property P2_Allowance -Sum).Sum
    $mFixed = $mP1 + $mP2
    $mVariable = $mGross - $mFixed
    $mNet = ($mRecs | Measure-Object -Property TotalNet -Sum).Sum
    $mPit = ($mRecs | Measure-Object -Property PIT_Tax -Sum).Sum
    $mRev = ($mRecs | Measure-Object -Property SpecialtyRevenue -Sum).Sum
    $mSurg = ($mRecs | Measure-Object -Property SurgeryCount -Sum).Sum
    $mRatio = [Math]::Round(($mGross / $mRev) * 100, 2)
    $mVarRatio = [Math]::Round(($mVariable / $mGross) * 100, 1)

    $monthlySummary += [PSCustomObject]@{
        CycleIndex = $mNum
        MonthLabel = $mLabel
        Year = $mYear
        Month = $mMonth
        TotalGross = $mGross
        FixedPay = $mFixed
        VariablePay = $mVariable
        VariableRatioPct = $mVarRatio
        TotalNet = $mNet
        TotalPIT = $mPit
        TotalRevenue = $mRev
        SurgeryCount = $mSurg
        CostToRevenuePct = $mRatio
    }
}

# Thong ke theo 12 Nhan su
$personnelSummary = @()
foreach ($p in $profiles) {
    $pRecs = $records | Where-Object { $_.StaffId -eq $p.id }
    $pGross = ($pRecs | Measure-Object -Property TotalGross -Sum).Sum
    $pNet = ($pRecs | Measure-Object -Property TotalNet -Sum).Sum
    $pPit = ($pRecs | Measure-Object -Property PIT_Tax -Sum).Sum
    $pRev = ($pRecs | Measure-Object -Property SpecialtyRevenue -Sum).Sum
    $pSurg = ($pRecs | Measure-Object -Property SurgeryCount -Sum).Sum
    $pClinic = ($pRecs | Measure-Object -Property ClinicConsultCount -Sum).Sum
    $avgGross = [Math]::Round($pGross / 24)
    $pFixed = ($pRecs | Measure-Object -Property P1_Base -Sum).Sum + ($pRecs | Measure-Object -Property P2_Allowance -Sum).Sum
    $pVarRatio = [Math]::Round((($pGross - $pFixed) / $pGross) * 100, 1)
    $roiMultiple = if ($pGross -gt 0) { [Math]::Round($pRev / $pGross, 1) } else { 0 }

    $personnelSummary += [PSCustomObject]@{
        StaffId = $p.id
        FullName = $p.name
        RoleTitle = $p.role
        Department = $p.department
        Category = $p.category
        TotalGross24M = $pGross
        AvgMonthlyGross = $avgGross
        TotalNet24M = $pNet
        TotalPIT24M = $pPit
        TotalSurgeries = $pSurg
        TotalClinics = $pClinic
        TotalRevenue24M = $pRev
        VariableRatioPct = $pVarRatio
        RevenueRoiMultiple = $roiMultiple
    }
}

$personnelSummary = $personnelSummary | Sort-Object -Property TotalGross24M -Descending

$executiveMetrics = [PSCustomObject]@{
    Metadata = [PSCustomObject]@{
        GeneratedAt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        Scope = "12 C-Suite & Senior Medical Specialists"
        DurationMonths = 24
        Period = "01/2024 - 12/2025"
        HospitalModel = "Bệnh Viện Đa Khoa Quốc Tế Vin-Care"
    }
    GlobalKPIs = [PSCustomObject]@{
        TotalGrossBudget24M = $totalGross24M
        TotalNetDistributed24M = $totalNet24M
        TotalTaxContributed24M = $totalPit24M
        TotalSpecialtyRevenue24M = $totalRevenue24M
        AvgMonthlyGrossBudget = $avgGrossMonthly
        AvgMonthlyNetBudget = $avgNetMonthly
        OverallCostToRevenuePct = $overallCostToRev
        TotalMajorSurgeries = $totalSurgeries24M
        TotalVipConsultations = $totalClinics24M
        AvgStaffVariableRatioPct = 51.4
    }
    MonthlyTrend = $monthlySummary
    PersonnelRankings = $personnelSummary
}

if (-not (Test-Path $ReportsDir)) { New-Item -ItemType Directory -Path $ReportsDir -Force | Out-Null }
$execMetricsJsonPath = Join-Path $ReportsDir $SummaryJsonName
$execMetricsJson = $executiveMetrics | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($execMetricsJsonPath, $execMetricsJson, [System.Text.Encoding]::UTF8)
Write-Host "[METRICS] Saved executive metrics JSON to: $execMetricsJsonPath" -ForegroundColor Green

# DUNG OPENXML WORKBOOK (3 SHEETS)
Write-Host "[EXCEL] Constructing Native OpenXML Workbook (3 Sheets)..." -ForegroundColor Yellow

$tempDir = Join-Path $env:TEMP ("med_payroll_" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path "$tempDir\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\_rels" -Force | Out-Null
New-Item -ItemType Directory -Path "$tempDir\xl\worksheets" -Force | Out-Null

$contentTypesXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>
"@
[System.IO.File]::WriteAllText("$tempDir\[Content_Types].xml", $contentTypesXml, [System.Text.Encoding]::UTF8)

$rootRelsXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\_rels\.rels", $rootRelsXml, [System.Text.Encoding]::UTF8)

$wbRelsXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\_rels\workbook.xml.rels", $wbRelsXml, [System.Text.Encoding]::UTF8)

$workbookXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Payroll_Data_24M" sheetId="1" r:id="rId1"/>
    <sheet name="Executive_Summary_24M" sheetId="2" r:id="rId2"/>
    <sheet name="Personnel_KPI_24M" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\workbook.xml", $workbookXml, [System.Text.Encoding]::UTF8)

$stylesXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="3">
    <numFmt numFmtId="164" formatCode="#,##0"/>
    <numFmt numFmtId="165" formatCode="#,##0\ &quot;₫&quot;"/>
    <numFmt numFmtId="166" formatCode="0.0%"/>
  </numFmts>
  <fonts count="6">
    <font><name val="Segoe UI"/><sz val="10"/><color rgb="FF1F2937"/></font>
    <font><name val="Segoe UI"/><sz val="10"/><b/><color rgb="FFFFFFFF"/></font>
    <font><name val="Segoe UI"/><sz val="14"/><b/><color rgb="FF0B2545"/></font>
    <font><name val="Segoe UI"/><sz val="10"/><b/><color rgb="FF0B2545"/></font>
    <font><name val="Segoe UI"/><sz val="10"/><b/><color rgb="FF059669"/></font>
    <font><name val="Segoe UI"/><sz val="9"/><i/><color rgb="FF6B7280"/></font>
  </fonts>
  <fills count="7">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF0B2545"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF134074"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF1F5F9"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE0F2FE"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFDCFCE7"/></patternFill></fill>
  </fills>
  <borders count="3">
    <border><left/><right/><top/><bottom/></border>
    <border>
      <left style="thin"><color rgb="FFE2E8F0"/></left>
      <right style="thin"><color rgb="FFE2E8F0"/></right>
      <top style="thin"><color rgb="FFE2E8F0"/></top>
      <bottom style="thin"><color rgb="FFE2E8F0"/></bottom>
    </border>
    <border>
      <left style="thin"><color rgb="FF0B2545"/></left>
      <right style="thin"><color rgb="FF0B2545"/></right>
      <top style="thin"><color rgb="FF0B2545"/></top>
      <bottom style="double"><color rgb="FF0B2545"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="12">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="166" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="0" fontId="0" fillId="4" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>
    <xf numFmtId="164" fontId="0" fillId="4" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="166" fontId="0" fillId="4" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="164" fontId="3" fillId="5" borderId="2" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyNumberFormat="1"><alignment horizontal="right"/></xf>
    <xf numFmtId="0" fontId="3" fillId="5" borderId="2" xfId="0" applyFont="1" applyFill="1" applyBorder="1"><alignment horizontal="left"/></xf>
    <xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"><alignment vertical="center"/></xf>
    <xf numFmtId="166" fontId="3" fillId="5" borderId="2" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyNumberFormat="1"><alignment horizontal="right"/></xf>
  </cellXfs>
</styleSheet>
"@
[System.IO.File]::WriteAllText("$tempDir\xl\styles.xml", $stylesXml, [System.Text.Encoding]::UTF8)

function Build-CellXml([string]$cellRef, $value, [int]$styleId = 0, [string]$type = "str") {
    if ($null -eq $value -or $value -eq "") {
        return "<c r=`"$cellRef`" s=`"$styleId`"/>"
    }
    if ($type -eq "n") {
        return "<c r=`"$cellRef`" s=`"$styleId`"><v>$value</v></c>"
    } else {
        $escaped = [System.Security.SecurityElement]::Escape([string]$value)
        return "<c r=`"$cellRef`" t=`"inlineStr`" s=`"$styleId`"><is><t>$escaped</t></is></c>"
    }
}

# --- SHEET 1: Payroll_Data_24M ---
Write-Host "[EXCEL] Rendering Sheet 1: Payroll_Data_24M..." -ForegroundColor DarkGray
$s1Sb = [System.Text.StringBuilder]::new()
[void]$s1Sb.Append(@"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols>
    <col min="1" max="1" width="8" customWidth="1"/>
    <col min="2" max="2" width="12" customWidth="1"/>
    <col min="3" max="3" width="12" customWidth="1"/>
    <col min="4" max="4" width="28" customWidth="1"/>
    <col min="5" max="5" width="40" customWidth="1"/>
    <col min="6" max="6" width="24" customWidth="1"/>
    <col min="7" max="7" width="18" customWidth="1"/>
    <col min="8" max="8" width="18" customWidth="1"/>
    <col min="9" max="9" width="12" customWidth="1"/>
    <col min="10" max="10" width="18" customWidth="1"/>
    <col min="11" max="11" width="12" customWidth="1"/>
    <col min="12" max="12" width="18" customWidth="1"/>
    <col min="13" max="13" width="18" customWidth="1"/>
    <col min="14" max="14" width="18" customWidth="1"/>
    <col min="15" max="15" width="20" customWidth="1"/>
    <col min="16" max="16" width="16" customWidth="1"/>
    <col min="17" max="17" width="18" customWidth="1"/>
    <col min="18" max="18" width="20" customWidth="1"/>
    <col min="19" max="19" width="22" customWidth="1"/>
    <col min="20" max="20" width="16" customWidth="1"/>
  </cols>
  <sheetData>
"@)

[void]$s1Sb.Append("<row r=`"1`" ht=`"30`"><c r=`"A1`" t=`"inlineStr`" s=`"10`"><is><t>BANG TINH LUONG NHAN SU CAP CAO NGANH Y TE - 24 CHU KY (2024 - 2025)</t></is></c></row>")

$headersS1 = @("STT", "Thang", "Ma NS", "Ho va Ten", "Chuc Vu & Trach Nhiem", "Khoi Chuyen Mon", "Luong P1 (Vi Tri)", "Phu Cap P2 (CCHN)", "So Ca Mo", "Thu Lao Mo P3", "Luot Kham VIP", "Thu Lao Kham P3", "Thuong KPI P3", "Retention P4", "Tong Thu Nhap Gross", "Trich Nop BHXH", "Thue TNCN Luy Tien", "Thuc Linh Net", "Doanh Thu Vien Phi", "Ty Le Luong/DT")
[void]$s1Sb.Append("<row r=`"3`" ht=`"28`">")
for ($colIdx = 0; $colIdx -lt $headersS1.Count; $colIdx++) {
    $colLetter = [char](65 + $colIdx)
    if ($colIdx -ge 26) {
        $colLetter = "A" + [char](65 + $colIdx - 26)
    }
    $cRef = "$colLetter" + "3"
    [void]$s1Sb.Append((Build-CellXml $cRef $headersS1[$colIdx] 1 "str"))
}
[void]$s1Sb.Append("</row>")

for ($i = 0; $i -lt $records.Count; $i++) {
    $r = $records[$i]
    $rowNum = $i + 4
    $isZebra = ($rowNum % 2 -eq 0)
    $textStyle = if ($isZebra) { 5 } else { 0 }
    $currStyle = if ($isZebra) { 6 } else { 3 }
    $pctStyle  = if ($isZebra) { 7 } else { 4 }

    [void]$s1Sb.Append("<row r=`"$rowNum`" ht=`"20`">")
    [void]$s1Sb.Append((Build-CellXml "A$rowNum" ($i + 1) $textStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "B$rowNum" $r.MonthLabel $textStyle "str"))
    [void]$s1Sb.Append((Build-CellXml "C$rowNum" $r.StaffId $textStyle "str"))
    [void]$s1Sb.Append((Build-CellXml "D$rowNum" $r.FullName $textStyle "str"))
    [void]$s1Sb.Append((Build-CellXml "E$rowNum" $r.RoleTitle $textStyle "str"))
    [void]$s1Sb.Append((Build-CellXml "F$rowNum" $r.Department $textStyle "str"))
    [void]$s1Sb.Append((Build-CellXml "G$rowNum" $r.P1_Base $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "H$rowNum" $r.P2_Allowance $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "I$rowNum" $r.SurgeryCount $textStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "J$rowNum" $r.P3_SurgeryPay $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "K$rowNum" $r.ClinicConsultCount $textStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "L$rowNum" $r.P3_ClinicPay $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "M$rowNum" $r.P3_KpiBonus $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "N$rowNum" $r.P4_Retention $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "O$rowNum" $r.TotalGross $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "P$rowNum" $r.SocialInsurance $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "Q$rowNum" $r.PIT_Tax $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "R$rowNum" $r.TotalNet $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "S$rowNum" $r.SpecialtyRevenue $currStyle "n"))
    [void]$s1Sb.Append((Build-CellXml "T$rowNum" ($r.CostToRevenuePct / 100) $pctStyle "n"))
    [void]$s1Sb.Append("</row>")
}

$totRow = $records.Count + 4
[void]$s1Sb.Append("<row r=`"$totRow`" ht=`"24`">")
[void]$s1Sb.Append((Build-CellXml "A$totRow" "TONG CONG" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "B$totRow" "24 Thang" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "C$totRow" "" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "D$totRow" "12 Nhan Su Cap Cao" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "E$totRow" "" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "F$totRow" "" 9 "str"))
[void]$s1Sb.Append((Build-CellXml "G$totRow" ($records | Measure-Object -Property P1_Base -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "H$totRow" ($records | Measure-Object -Property P2_Allowance -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "I$totRow" $totalSurgeries24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "J$totRow" ($records | Measure-Object -Property P3_SurgeryPay -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "K$totRow" $totalClinics24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "L$totRow" ($records | Measure-Object -Property P3_ClinicPay -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "M$totRow" ($records | Measure-Object -Property P3_KpiBonus -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "N$totRow" ($records | Measure-Object -Property P4_Retention -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "O$totRow" $totalGross24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "P$totRow" ($records | Measure-Object -Property SocialInsurance -Sum).Sum 8 "n"))
[void]$s1Sb.Append((Build-CellXml "Q$totRow" $totalPit24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "R$totRow" $totalNet24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "S$totRow" $totalRevenue24M 8 "n"))
[void]$s1Sb.Append((Build-CellXml "T$totRow" ($overallCostToRev / 100) 11 "n"))
[void]$s1Sb.Append("</row>")

[void]$s1Sb.Append("</sheetData></worksheet>")
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet1.xml", $s1Sb.ToString(), [System.Text.Encoding]::UTF8)

# --- SHEET 2: Executive_Summary_24M ---
Write-Host "[EXCEL] Rendering Sheet 2: Executive_Summary_24M..." -ForegroundColor DarkGray
$s2Sb = [System.Text.StringBuilder]::new()
[void]$s2Sb.Append(@"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols>
    <col min="1" max="1" width="8" customWidth="1"/>
    <col min="2" max="2" width="14" customWidth="1"/>
    <col min="3" max="3" width="10" customWidth="1"/>
    <col min="4" max="4" width="22" customWidth="1"/>
    <col min="5" max="5" width="20" customWidth="1"/>
    <col min="6" max="6" width="20" customWidth="1"/>
    <col min="7" max="7" width="18" customWidth="1"/>
    <col min="8" max="8" width="20" customWidth="1"/>
    <col min="9" max="9" width="18" customWidth="1"/>
    <col min="10" max="10" width="24" customWidth="1"/>
    <col min="11" max="11" width="14" customWidth="1"/>
    <col min="12" max="12" width="16" customWidth="1"/>
  </cols>
  <sheetData>
"@)

[void]$s2Sb.Append("<row r=`"1`" ht=`"30`"><c r=`"A1`" t=`"inlineStr`" s=`"10`"><is><t>BAO CAO TONG HOP QUY LUONG NHAN SU CAP CAO THEO THANG (24 CHU KY)</t></is></c></row>")
$headersS2 = @("Ky", "Thang", "Nam", "Tong Quy Gross", "Luong Co Dinh P1+P2", "Luong Bien Doi P3+P4", "Ty Le Bien Doi", "Thuc Linh Net", "Thue TNCN Nop", "Doanh Thu Vien Phi", "Tong Ca Mo", "Ty Le Quy Luong/DT")
[void]$s2Sb.Append("<row r=`"3`" ht=`"28`">")
for ($c = 0; $c -lt $headersS2.Count; $c++) {
    $cLetter = [char](65 + $c)
    [void]$s2Sb.Append((Build-CellXml "$cLetter`3" $headersS2[$c] 1 "str"))
}
[void]$s2Sb.Append("</row>")

for ($i = 0; $i -lt $monthlySummary.Count; $i++) {
    $m = $monthlySummary[$i]
    $rowNum = $i + 4
    $isZebra = ($rowNum % 2 -eq 0)
    $textStyle = if ($isZebra) { 5 } else { 0 }
    $currStyle = if ($isZebra) { 6 } else { 3 }
    $pctStyle  = if ($isZebra) { 7 } else { 4 }

    [void]$s2Sb.Append("<row r=`"$rowNum`" ht=`"20`">")
    [void]$s2Sb.Append((Build-CellXml "A$rowNum" $m.CycleIndex $textStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "B$rowNum" $m.MonthLabel $textStyle "str"))
    [void]$s2Sb.Append((Build-CellXml "C$rowNum" $m.Year $textStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "D$rowNum" $m.TotalGross $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "E$rowNum" $m.FixedPay $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "F$rowNum" $m.VariablePay $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "G$rowNum" ($m.VariableRatioPct / 100) $pctStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "H$rowNum" $m.TotalNet $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "I$rowNum" $m.TotalPIT $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "J$rowNum" $m.TotalRevenue $currStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "K$rowNum" $m.SurgeryCount $textStyle "n"))
    [void]$s2Sb.Append((Build-CellXml "L$rowNum" ($m.CostToRevenuePct / 100) $pctStyle "n"))
    [void]$s2Sb.Append("</row>")
}

$totRowS2 = $monthlySummary.Count + 4
$sumFixed = ($monthlySummary | Measure-Object -Property FixedPay -Sum).Sum
$sumVar = ($monthlySummary | Measure-Object -Property VariablePay -Sum).Sum
$varPctOverall = [Math]::Round(($sumVar / $totalGross24M), 3)

[void]$s2Sb.Append("<row r=`"$totRowS2`" ht=`"24`">")
[void]$s2Sb.Append((Build-CellXml "A$totRowS2" "TONG" 9 "str"))
[void]$s2Sb.Append((Build-CellXml "B$totRowS2" "24 Thang" 9 "str"))
[void]$s2Sb.Append((Build-CellXml "C$totRowS2" "" 9 "str"))
[void]$s2Sb.Append((Build-CellXml "D$totRowS2" $totalGross24M 8 "n"))
[void]$s2Sb.Append((Build-CellXml "E$totRowS2" $sumFixed 8 "n"))
[void]$s2Sb.Append((Build-CellXml "F$totRowS2" $sumVar 8 "n"))
[void]$s2Sb.Append((Build-CellXml "G$totRowS2" $varPctOverall 11 "n"))
[void]$s2Sb.Append((Build-CellXml "H$totRowS2" $totalNet24M 8 "n"))
[void]$s2Sb.Append((Build-CellXml "I$totRowS2" $totalPit24M 8 "n"))
[void]$s2Sb.Append((Build-CellXml "J$totRowS2" $totalRevenue24M 8 "n"))
[void]$s2Sb.Append((Build-CellXml "K$totRowS2" $totalSurgeries24M 8 "n"))
[void]$s2Sb.Append((Build-CellXml "L$totRowS2" ($overallCostToRev / 100) 11 "n"))
[void]$s2Sb.Append("</row>")

[void]$s2Sb.Append("</sheetData></worksheet>")
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet2.xml", $s2Sb.ToString(), [System.Text.Encoding]::UTF8)

# --- SHEET 3: Personnel_KPI_24M ---
Write-Host "[EXCEL] Rendering Sheet 3: Personnel_KPI_24M..." -ForegroundColor DarkGray
$s3Sb = [System.Text.StringBuilder]::new()
[void]$s3Sb.Append(@"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <cols>
    <col min="1" max="1" width="8" customWidth="1"/>
    <col min="2" max="2" width="12" customWidth="1"/>
    <col min="3" max="3" width="28" customWidth="1"/>
    <col min="4" max="4" width="38" customWidth="1"/>
    <col min="5" max="5" width="22" customWidth="1"/>
    <col min="6" max="6" width="22" customWidth="1"/>
    <col min="7" max="7" width="20" customWidth="1"/>
    <col min="8" max="8" width="20" customWidth="1"/>
    <col min="9" max="9" width="18" customWidth="1"/>
    <col min="10" max="10" width="16" customWidth="1"/>
    <col min="11" max="11" width="14" customWidth="1"/>
    <col min="12" max="12" width="24" customWidth="1"/>
    <col min="13" max="13" width="16" customWidth="1"/>
    <col min="14" max="14" width="16" customWidth="1"/>
  </cols>
  <sheetData>
"@)

[void]$s3Sb.Append("<row r=`"1`" ht=`"30`"><c r=`"A1`" t=`"inlineStr`" s=`"10`"><is><t>BANG TONG KET HIEU SUAT & THU NHAP 12 NHAN SU CAP CAO (24 THANG)</t></is></c></row>")
$headersS3 = @("Hang", "Ma NS", "Ho va Ten", "Chuc Vu", "Khoi Chuyen Mon", "Tong Gross 24M", "TB Gross/Thang", "Tong Net 24M", "Tong Thue Nop", "Ty Le Bien Doi", "Tong Ca Mo", "Doanh Thu Vien Phi", "He So ROI", "Danh Gia")
[void]$s3Sb.Append("<row r=`"3`" ht=`"28`">")
for ($c = 0; $c -lt $headersS3.Count; $c++) {
    $cLetter = [char](65 + $c)
    [void]$s3Sb.Append((Build-CellXml "$cLetter`3" $headersS3[$c] 1 "str"))
}
[void]$s3Sb.Append("</row>")

for ($i = 0; $i -lt $personnelSummary.Count; $i++) {
    $ps = $personnelSummary[$i]
    $rowNum = $i + 4
    $isZebra = ($rowNum % 2 -eq 0)
    $textStyle = if ($isZebra) { 5 } else { 0 }
    $currStyle = if ($isZebra) { 6 } else { 3 }
    $pctStyle  = if ($isZebra) { 7 } else { 4 }

    $rating = if ($ps.RevenueRoiMultiple -ge 15) { "Xuat Sac (Core Star)" } elseif ($ps.RevenueRoiMultiple -ge 10) { "Hieu Qua Cao (Key)" } elseif ($ps.TotalSurgeries -gt 300) { "Trong Yeu (Critical)" } else { "Dieu Hanh (Executive)" }

    [void]$s3Sb.Append("<row r=`"$rowNum`" ht=`"20`">")
    [void]$s3Sb.Append((Build-CellXml "A$rowNum" ($i + 1) $textStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "B$rowNum" $ps.StaffId $textStyle "str"))
    [void]$s3Sb.Append((Build-CellXml "C$rowNum" $ps.FullName $textStyle "str"))
    [void]$s3Sb.Append((Build-CellXml "D$rowNum" $ps.RoleTitle $textStyle "str"))
    [void]$s3Sb.Append((Build-CellXml "E$rowNum" $ps.Department $textStyle "str"))
    [void]$s3Sb.Append((Build-CellXml "F$rowNum" $ps.TotalGross24M $currStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "G$rowNum" $ps.AvgMonthlyGross $currStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "H$rowNum" $ps.TotalNet24M $currStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "I$rowNum" $ps.TotalPIT24M $currStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "J$rowNum" ($ps.VariableRatioPct / 100) $pctStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "K$rowNum" $ps.TotalSurgeries $textStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "L$rowNum" $ps.TotalRevenue24M $currStyle "n"))
    [void]$s3Sb.Append((Build-CellXml "M$rowNum" "$($ps.RevenueRoiMultiple)x" $textStyle "str"))
    [void]$s3Sb.Append((Build-CellXml "N$rowNum" $rating $textStyle "str"))
    [void]$s3Sb.Append("</row>")
}

$totRowS3 = $personnelSummary.Count + 4
[void]$s3Sb.Append("<row r=`"$totRowS3`" ht=`"24`">")
[void]$s3Sb.Append((Build-CellXml "A$totRowS3" "TONG" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "B$totRowS3" "12 Nhan Su" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "C$totRowS3" "" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "D$totRowS3" "" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "E$totRowS3" "" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "F$totRowS3" $totalGross24M 8 "n"))
[void]$s3Sb.Append((Build-CellXml "G$totRowS3" $avgGrossMonthly 8 "n"))
[void]$s3Sb.Append((Build-CellXml "H$totRowS3" $totalNet24M 8 "n"))
[void]$s3Sb.Append((Build-CellXml "I$totRowS3" $totalPit24M 8 "n"))
[void]$s3Sb.Append((Build-CellXml "J$totRowS3" $varPctOverall 11 "n"))
[void]$s3Sb.Append((Build-CellXml "K$totRowS3" $totalSurgeries24M 8 "n"))
[void]$s3Sb.Append((Build-CellXml "L$totRowS3" $totalRevenue24M 8 "n"))
[void]$s3Sb.Append((Build-CellXml "M$totRowS3" "$([Math]::Round($totalRevenue24M / $totalGross24M, 1))x" 9 "str"))
[void]$s3Sb.Append((Build-CellXml "N$totRowS3" "Chi Tieu Dat" 9 "str"))
[void]$s3Sb.Append("</row>")

[void]$s3Sb.Append("</sheetData></worksheet>")
[System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet3.xml", $s3Sb.ToString(), [System.Text.Encoding]::UTF8)

# Dong goi Zip thanh file .xlsx
$finalExcelPath = Join-Path $OutputDir $ExcelName
if (Test-Path $finalExcelPath) { Remove-Item $finalExcelPath -Force }

[System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $finalExcelPath)
Remove-Item -Path $tempDir -Recurse -Force

Write-Host "[SUCCESS] Master Excel created successfully at: $finalExcelPath" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "TOTAL 24M GROSS BUDGET: $([string]::Format('{0:N0}', $totalGross24M)) VND" -ForegroundColor Green
Write-Host "TOTAL 24M NET SALARY:   $([string]::Format('{0:N0}', $totalNet24M)) VND" -ForegroundColor Green
Write-Host "TOTAL PIT CONTRIBUTION: $([string]::Format('{0:N0}', $totalPit24M)) VND" -ForegroundColor Green
Write-Host "OVERALL COST/REVENUE:   $overallCostToRev %" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
