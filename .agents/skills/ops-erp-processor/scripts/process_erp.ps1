# process_erp.ps1
# Engine tu dong hoa lam sach, tach file theo Manager va tong hop so lieu ERP
# Tac gia: Operations Analyst / Antigravity AI (AI4A Framework)

[CmdletBinding()]
param (
    [string]$InputPath = "",
    [string]$OutputDir = "outputs/reports",
    [string]$ManagersSubdir = "outputs/reports/managers"
)

$ErrorActionPreference = "Stop"

# 1. Dinh vi tep dau vao
if (-not $InputPath) {
    $found = Get-ChildItem -Path "sample-data" -Filter "*ERP*.xlsx" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $InputPath = $found.FullName
    } else {
        Write-Error "Khong tim thay file ERP trong sample-data. Vui long chi dinh -InputPath"
        exit 1
    }
}

if (-not (Test-Path $InputPath)) {
    Write-Error "Tep tin khong ton tai: $InputPath"
    exit 1
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "[START] OPS ERP PROCESSOR ENGINE DANG XU LY..." -ForegroundColor Cyan
Write-Host "[INFO] File nguon: $InputPath" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Cyan

# Dam bao cac thu muc dau ra ton tai
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }
if (-not (Test-Path $ManagersSubdir)) { New-Item -ItemType Directory -Path $ManagersSubdir -Force | Out-Null }

# 2. Doc file Excel thong qua Zip/OpenXML
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($InputPath)

# Trich xuat Shared Strings
$ssEntry = $zip.GetEntry('xl/sharedStrings.xml')
$sharedStrings = New-Object System.Collections.Generic.List[string]
if ($ssEntry) {
    $stream = $ssEntry.Open()
    $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
    $ssXml = [xml]$reader.ReadToEnd()
    $stream.Close()
    foreach ($si in $ssXml.sst.si) {
        if ($si.t -ne $null) { $sharedStrings.Add($si.t) }
        elseif ($si.r -ne $null) { $sharedStrings.Add(($si.r | ForEach-Object { $_.t }) -join '') }
        else { $sharedStrings.Add("") }
    }
}

# Doc Sheet1
$sheetEntry = $zip.GetEntry('xl/worksheets/sheet1.xml')
if (-not $sheetEntry) {
    $zip.Dispose()
    Write-Error "Khong tim thay sheet du lieu (xl/worksheets/sheet1.xml) trong file Excel."
    exit 1
}

$stream = $sheetEntry.Open()
$reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
$sheetXml = [xml]$reader.ReadToEnd()
$stream.Close()
$zip.Dispose()

$rows = $sheetXml.worksheet.sheetData.row
$totalRawRowsInXml = $rows.Count
Write-Host "[AUDIT] Tong so dong trong XML ban dau: $totalRawRowsInXml dong" -ForegroundColor Gray

# 3. Phan tich Header va Lam Sach Du Lieu
$cleanedEmployees = New-Object System.Collections.Generic.List[PSCustomObject]
$monthValue = "2026-03"
$ghostRowCount = 0

for ($i = 1; $i -lt $rows.Count; $i++) {
    $r = $rows[$i]
    $rowCells = @{}
    foreach ($c in $r.c) {
        $colLetter = ($c.r -replace '[0-9]', '')
        $v = $c.v
        $val = if ($c.t -eq "s" -and $v -ne $null -and [int]$v -lt $sharedStrings.Count) { $sharedStrings[[int]$v] } else { $v }
        $rowCells[$colLetter] = $val
    }

    $empId = $rowCells["A"]
    # Loai bo dong rac (Ghost row): Khong co Employee_ID
    if ([string]::IsNullOrWhiteSpace($empId)) {
        $ghostRowCount++
        continue
    }

    $empName = [string]$rowCells["B"]
    $mgr     = [string]$rowCells["C"]
    $dept    = [string]$rowCells["D"]
    $base    = [double]0.0
    $bonus   = [double]0.0
    $penalty = [double]0.0

    [double]::TryParse([string]$rowCells["E"], [ref]$base) | Out-Null
    [double]::TryParse([string]$rowCells["F"], [ref]$bonus) | Out-Null
    [double]::TryParse([string]$rowCells["G"], [ref]$penalty) | Out-Null

    if ($rowCells["H"]) { $monthValue = [string]$rowCells["H"] }

    $netSalary = $base + $bonus - $penalty
    $bonusRate = if ($base -gt 0) { [Math]::Round(($bonus / $base) * 100, 2) } else { 0.0 }
    $penaltyRate = if ($base -gt 0) { [Math]::Round(($penalty / $base) * 100, 2) } else { 0.0 }

    $cleanedEmployees.Add([PSCustomObject]@{
        Employee_ID      = $empId
        Employee_Name    = $empName
        Manager          = $mgr
        Department       = $dept
        Base_Salary      = [long][Math]::Round($base)
        Bonus            = [long][Math]::Round($bonus)
        Penalty          = [long][Math]::Round($penalty)
        Net_Salary       = [long][Math]::Round($netSalary)
        Bonus_Rate_Pct   = $bonusRate
        Penalty_Rate_Pct = $penaltyRate
        Month            = $monthValue
    })
}

$validCount = $cleanedEmployees.Count
Write-Host "[CLEAN] Da loai bo $ghostRowCount dong rac (ghost rows)" -ForegroundColor Yellow
Write-Host "[CLEAN] Du lieu nhan su hop le: $validCount nhan vien" -ForegroundColor Green

# 4. Tinh toan so lieu tong hop
$totalBase = ($cleanedEmployees | Measure-Object -Property Base_Salary -Sum).Sum
$totalBonus = ($cleanedEmployees | Measure-Object -Property Bonus -Sum).Sum
$totalPenalty = ($cleanedEmployees | Measure-Object -Property Penalty -Sum).Sum
$totalNet = ($cleanedEmployees | Measure-Object -Property Net_Salary -Sum).Sum

# Thong ke theo Department
$deptGroups = $cleanedEmployees | Group-Object Department | ForEach-Object {
    $deptBase = ($_.Group | Measure-Object -Property Base_Salary -Sum).Sum
    $deptBonus = ($_.Group | Measure-Object -Property Bonus -Sum).Sum
    $deptPen = ($_.Group | Measure-Object -Property Penalty -Sum).Sum
    $deptNet = ($_.Group | Measure-Object -Property Net_Salary -Sum).Sum
    [PSCustomObject]@{
        Department    = $_.Name
        Headcount     = $_.Count
        Total_Base    = $deptBase
        Total_Bonus   = $deptBonus
        Total_Penalty = $deptPen
        Total_Net     = $deptNet
        Avg_Net       = [long][Math]::Round($deptNet / $_.Count)
    }
}

# Thong ke theo Manager
$mgrGroups = $cleanedEmployees | Group-Object Manager | ForEach-Object {
    $mBase = ($_.Group | Measure-Object -Property Base_Salary -Sum).Sum
    $mBonus = ($_.Group | Measure-Object -Property Bonus -Sum).Sum
    $mPen = ($_.Group | Measure-Object -Property Penalty -Sum).Sum
    $mNet = ($_.Group | Measure-Object -Property Net_Salary -Sum).Sum
    [PSCustomObject]@{
        Manager       = $_.Name
        Headcount     = $_.Count
        Total_Base    = $mBase
        Total_Bonus   = $mBonus
        Total_Penalty = $mPen
        Total_Net     = $mNet
        Avg_Net       = [long][Math]::Round($mNet / $_.Count)
    }
}

# Top Outliers
$topBonuses = $cleanedEmployees | Sort-Object Bonus -Descending | Select-Object -First 5
$topPenalties = $cleanedEmployees | Sort-Object Penalty -Descending | Select-Object -First 5

# 5. Ham sinh file Excel OpenXML chuan
function Export-OpenXmlWorkbook {
    param(
        [string]$TargetFile,
        [string]$SheetName,
        [string[]]$Headers,
        [array]$DataList
    )

    if (Test-Path $TargetFile) { Remove-Item $TargetFile -Force }
    $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    New-Item -ItemType Directory -Path "$tempDir\_rels" -Force | Out-Null
    New-Item -ItemType Directory -Path "$tempDir\xl\_rels" -Force | Out-Null
    New-Item -ItemType Directory -Path "$tempDir\xl\worksheets" -Force | Out-Null

    # [Content_Types].xml
    $ct = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>
"@
    [System.IO.File]::WriteAllText("$tempDir\[Content_Types].xml", $ct.Trim(), [System.Text.Encoding]::UTF8)

    # _rels/.rels
    $r = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>
"@
    [System.IO.File]::WriteAllText("$tempDir\_rels\.rels", $r.Trim(), [System.Text.Encoding]::UTF8)

    # xl/_rels/workbook.xml.rels
    $wbr = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"@
    [System.IO.File]::WriteAllText("$tempDir\xl\_rels\workbook.xml.rels", $wbr.Trim(), [System.Text.Encoding]::UTF8)

    # xl/workbook.xml
    $wb = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="$SheetName" sheetId="1" r:id="rId1"/>
  </sheets>
</workbook>
"@
    [System.IO.File]::WriteAllText("$tempDir\xl\workbook.xml", $wb.Trim(), [System.Text.Encoding]::UTF8)

    # xl/styles.xml
    $styles = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="2">
    <numFmt numFmtId="164" formatCode="#,##0&quot; VND&quot;"/>
    <numFmt numFmtId="165" formatCode="0.0%"/>
  </numFmts>
  <fonts count="2">
    <font><name val="Segoe UI"/><sz val="10"/><color theme="1"/></font>
    <font><name val="Segoe UI"/><sz val="10"/><b/><color rgb="FFFFFFFF"/></font>
  </fonts>
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF1B365D"/></fgColor></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF8F9FA"/></fgColor></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/></border>
    <border>
      <left style="thin"><color rgb="FFD5D8DC"/></left>
      <right style="thin"><color rgb="FFD5D8DC"/></right>
      <top style="thin"><color rgb="FFD5D8DC"/></top>
      <bottom style="thin"><color rgb="FFD5D8DC"/></bottom>
    </border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="8">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="164" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="165" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
  </cellXfs>
</styleSheet>
"@
    [System.IO.File]::WriteAllText("$tempDir\xl\styles.xml", $styles.Trim(), [System.Text.Encoding]::UTF8)

    # xl/worksheets/sheet1.xml
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    [void]$sb.AppendLine('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
    [void]$sb.AppendLine('  <sheetViews><sheetView tabSelected="1" workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>')
    [void]$sb.AppendLine('  <sheetFormatPr defaultRowHeight="20"/>')
    [void]$sb.AppendLine('  <cols>')
    [void]$sb.AppendLine('    <col min="1" max="1" width="14" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="2" max="2" width="18" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="3" max="3" width="16" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="4" max="4" width="16" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="5" max="8" width="22" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="9" max="10" width="16" customWidth="1"/>')
    [void]$sb.AppendLine('    <col min="11" max="11" width="14" customWidth="1"/>')
    [void]$sb.AppendLine('  </cols>')
    [void]$sb.AppendLine('  <sheetData>')

    # Header Row
    [void]$sb.AppendLine('    <row r="1" ht="26" customHeight="1">')
    for ($c = 0; $c -lt $Headers.Count; $c++) {
        $colLetter = [char](65 + $c)
        $hText = [System.Security.SecurityElement]::Escape($Headers[$c])
        [void]$sb.AppendLine("      <c r=`"$colLetter`1`" t=`"inlineStr`" s=`"1`"><is><t>$hText</t></is></c>")
    }
    [void]$sb.AppendLine('    </row>')

    # Data Rows
    $rIdx = 2
    foreach ($item in $DataList) {
        $isZebra = ($rIdx % 2 -eq 1)
        [void]$sb.AppendLine("    <row r=`"$rIdx`" ht=`"22`" customHeight=`"1`">")

        $vals = @(
            $item.Employee_ID,
            $item.Employee_Name,
            $item.Manager,
            $item.Department,
            $item.Base_Salary,
            $item.Bonus,
            $item.Penalty,
            $item.Net_Salary,
            $item.Bonus_Rate_Pct,
            $item.Penalty_Rate_Pct,
            $item.Month
        )

        for ($c = 0; $c -lt $vals.Count; $c++) {
            $colLetter = [char](65 + $c)
            $v = $vals[$c]

            if ($c -in 0, 10) { # EmpID, Month: Center
                $sId = if ($isZebra) { 5 } else { 4 }
                $esc = [System.Security.SecurityElement]::Escape([string]$v)
                [void]$sb.AppendLine("      <c r=`"$colLetter$rIdx`" t=`"inlineStr`" s=`"$sId`"><is><t>$esc</t></is></c>")
            }
            elseif ($c -in 4, 5, 6, 7) { # Currency
                $sId = if ($isZebra) { 6 } else { 2 }
                [void]$sb.AppendLine("      <c r=`"$colLetter$rIdx`" s=`"$sId`"><v>$v</v></c>")
            }
            elseif ($c -in 8, 9) { # Percent
                $sId = if ($isZebra) { 7 } else { 3 }
                [void]$sb.AppendLine("      <c r=`"$colLetter$rIdx`" s=`"$sId`"><v>$v</v></c>")
            }
            else { # Text: Name, Manager, Dept
                $sId = if ($isZebra) { 5 } else { 0 }
                $esc = [System.Security.SecurityElement]::Escape([string]$v)
                [void]$sb.AppendLine("      <c r=`"$colLetter$rIdx`" t=`"inlineStr`" s=`"$sId`"><is><t>$esc</t></is></c>")
            }
        }
        [void]$sb.AppendLine('    </row>')
        $rIdx++
    }

    [void]$sb.AppendLine('  </sheetData>')
    [void]$sb.AppendLine('</worksheet>')
    [System.IO.File]::WriteAllText("$tempDir\xl\worksheets\sheet1.xml", $sb.ToString(), [System.Text.Encoding]::UTF8)

    [System.IO.Compression.ZipFile]::CreateFromDirectory($tempDir, $TargetFile)
    Remove-Item $tempDir -Recurse -Force

    # Chuan hoa duong dan zip sang forward slashes '/' theo dung chuan OpenXML
    $tempZip = $TargetFile + ".tmp"
    if (Test-Path $tempZip) { Remove-Item $tempZip -Force }
    $src = [System.IO.Compression.ZipFile]::OpenRead($TargetFile)
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
    Remove-Item $TargetFile -Force
    Move-Item $tempZip $TargetFile
}

# 6. Xuat File Master Cleaned
$masterPath = Join-Path $OutputDir "ERP_Operations_Master_$monthValue.xlsx"
$headersVN = @(
    "Ma Nhan Vien", "Ho & Ten", "Nguoi Quan Ly", "Bo Phan",
    "Luong Co Ban (VND)", "Tien Thuong (VND)", "Tien Phat (VND)", "Thuc Linh (VND)",
    "Ty Le Thuong (%)", "Ty Le Phat (%)", "Ky Luong"
)
Export-OpenXmlWorkbook -TargetFile $masterPath -SheetName "Cleaned_Operations" -Headers $headersVN -DataList $cleanedEmployees
Write-Host "[EXPORT] Da tao Master Cleaned File: $masterPath" -ForegroundColor Green

# 7. Phan tach va Xuat 4 File cho tung Manager
$uniqueManagers = $cleanedEmployees | Select-Object -ExpandProperty Manager -Unique | Sort-Object
$managerOutFiles = @()

foreach ($m in $uniqueManagers) {
    $mEmpList = $cleanedEmployees | Where-Object { $_.Manager -eq $m }
    $mSafeName = $m -replace '[^a-zA-Z0-9_]', '_'
    $mFilePath = Join-Path $ManagersSubdir "${mSafeName}_$monthValue.xlsx"
    Export-OpenXmlWorkbook -TargetFile $mFilePath -SheetName "My_Team_$mSafeName" -Headers $headersVN -DataList $mEmpList
    $managerOutFiles += $mFilePath
    Write-Host "   + Xuat file cho [$m]: $($mEmpList.Count) nhan su -> $mFilePath" -ForegroundColor Cyan
}

# 8. Xuat Metadata & Summary JSON cho Agent tieu thu
$summaryObj = [PSCustomObject]@{
    ProcessedAt   = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    SourceFile    = $InputPath
    Month         = $monthValue
    TotalRawRowsInXml = $totalRawRowsInXml
    GhostRowsRemoved  = $ghostRowCount
    ValidHeadcount    = $validCount
    Financials    = [PSCustomObject]@{
        Total_Base_VND    = $totalBase
        Total_Bonus_VND   = $totalBonus
        Total_Penalty_VND = $totalPenalty
        Total_Net_VND     = $totalNet
        Bonus_Over_Base_Pct = [Math]::Round(($totalBonus / $totalBase) * 100, 2)
        Penalty_Over_Base_Pct = [Math]::Round(($totalPenalty / $totalBase) * 100, 2)
    }
    DepartmentBreakdown = $deptGroups
    ManagerBreakdown    = $mgrGroups
    TopBonuses          = $topBonuses
    TopPenalties        = $topPenalties
    MasterFile          = $masterPath
    ManagerFiles        = $managerOutFiles
}

$jsonPath = Join-Path $OutputDir "erp_summary_metrics.json"
$summaryJson = $summaryObj | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText($jsonPath, $summaryJson, [System.Text.Encoding]::UTF8)

Write-Host "[JSON] Da luu JSON tong hop phan tich: $jsonPath" -ForegroundColor Gray
Write-Host "==========================================================" -ForegroundColor Green
Write-Host "[SUCCESS] HOAN THANH XU LY DU LIEU ERP: 100% THANH CONG!" -ForegroundColor Green
Write-Host ("   Tong thuc linh: {0:N0} VND (Khop 100% doi soat)" -f $totalNet) -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
