param(
    [switch]$Register,
    [switch]$Remove,
    [switch]$Disable,
    [switch]$Enable,
    [switch]$Status,
    [switch]$RunNow
)

$TaskName = "Customs_Legal_Bot_OnLogon"
$WorkspaceDir = $PSScriptRoot
$PythonExe = "C:\Program Files\IBM\SPSS Statistics\Python3\python.exe"
$PythonwExe = "C:\Program Files\IBM\SPSS Statistics\Python3\pythonw.exe"
$ScriptFile = Join-Path $PSScriptRoot "customs_telegram_bot.py"
$StartupFolder = [Environment]::GetFolderPath('Startup')
$StartupShortcut = Join-Path $StartupFolder "Customs_Legal_Bot.lnk"
$DisabledFlagFile = Join-Path $WorkspaceDir "knowledge-base\legal-assets\bot_disabled.flag"

# Neu khong truyen tham so nao, mac dinh kiem tra trang thai
if (-not ($Register -or $Remove -or $Disable -or $Enable -or $Status -or $RunNow)) {
    $Status = $true
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "QUAN LY LICH TRINH CUSTOMS LEGAL TELEGRAM BOT (ON LOGON AUTOMATION)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

if ($Disable) {
    Write-Host "[Tam dung] Dang tam dung che do tu dong kich hoat cua Bot..." -ForegroundColor Yellow
    New-Item -Path $DisabledFlagFile -ItemType File -Force | Out-Null
    Write-Host "  [OK] DA TAM DUNG BOT THANH CONG!" -ForegroundColor Green
    Write-Host "  Bot se KHONG gui tin khi ban mo may tinh cho den khi ban bat lai." -ForegroundColor Yellow
    Write-Host "  De bat lai: .\setup_customs_scheduler.ps1 -Enable" -ForegroundColor Cyan
    exit 0
}

if ($Enable) {
    Write-Host "[Kich hoat] Dang bat lai che do tu dong cua Bot..." -ForegroundColor Yellow
    if (Test-Path $DisabledFlagFile) {
        Remove-Item -Path $DisabledFlagFile -Force
    }
    Write-Host "  [OK] DA BAT LAI THANH CONG!" -ForegroundColor Green
    Write-Host "  Bot se tiep tuc tu dong quet vao moi buoi sang khi ban mo may." -ForegroundColor Green
    exit 0
}

if ($Status) {
    Write-Host "[Kiem tra] Trang thai tu dong hoa cua Bot:" -ForegroundColor Yellow
    $hasShortcut = Test-Path $StartupShortcut
    $isDisabled = Test-Path $DisabledFlagFile
    $dailyRunFile = Join-Path $WorkspaceDir "knowledge-base\legal-assets\last_daily_run.json"

    if ($hasShortcut) {
        if ($isDisabled) {
            Write-Host "  • Trang thai:    [TAM DUNG] (Disabled) - Bot khong gui tin khi mo may" -ForegroundColor Yellow
            Write-Host "    De bat lai:    .\setup_customs_scheduler.ps1 -Enable" -ForegroundColor Cyan
        } else {
            Write-Host "  • Trang thai:    [DANG HOAT DONG] (Active) - Tu dong chay moi khi mo may" -ForegroundColor Green
        }
        Write-Host "  • Co che chay:   Windows Startup (On Logon) - Chay ngam khong hien cua so den" -ForegroundColor Gray
        Write-Host "  • File khoi dong: $StartupShortcut" -ForegroundColor Gray
        
        if (Test-Path $dailyRunFile) {
            $runData = Get-Content $dailyRunFile -Raw | ConvertFrom-Json
            Write-Host "  • Lan chay cuoi:  $($runData.last_run_time)" -ForegroundColor Gray
            Write-Host "  • Ngay da chay:   $($runData.last_run_date)" -ForegroundColor Gray
        } else {
            Write-Host "  • Lan chay cuoi:  Chua chay lan nao" -ForegroundColor Gray
        }
    } else {
        Write-Host "  • Trang thai:    [CHUA DANG KY] Bot chua duoc cai dat vao che do khoi dong." -ForegroundColor Red
        Write-Host "    De cai dat:    .\setup_customs_scheduler.ps1 -Register" -ForegroundColor Cyan
    }
    Write-Host "=================================================================" -ForegroundColor Cyan
    exit 0
}

if ($RunNow) {
    Write-Host "[Chay ngay] Dang kich hoat Customs Telegram Bot (che do --force)..." -ForegroundColor Yellow
    & "$PythonExe" "$ScriptFile" --force
    exit $LASTEXITCODE
}

if ($Remove) {
    Write-Host "[Go bo] Dang go bo che do tu dong khoi dong..." -ForegroundColor Yellow
    if (Test-Path $StartupShortcut) {
        Remove-Item -Path $StartupShortcut -Force
        Write-Host "  [OK] Da xoa shortcut khoi thu muc Startup thanh cong!" -ForegroundColor Green
    } else {
        Write-Host "  [Thong bao] Khong tim thay shortcut trong Startup." -ForegroundColor Yellow
    }
    if (Test-Path $DisabledFlagFile) {
        Remove-Item -Path $DisabledFlagFile -Force
    }
    exit 0
}

if ($Register) {
    Write-Host "[Cai dat] Dang thiet lap che do tu dong kich hoat khi mo may..." -ForegroundColor Yellow

    if (-not (Test-Path $PythonwExe)) {
        $PythonwExe = $PythonExe
    }

    # Tao Shortcut trong thu muc Startup cua User (Khong can quyen Admin, 100% hoat dong)
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($StartupShortcut)
        $Shortcut.TargetPath = $PythonwExe
        $Shortcut.Arguments = "`"$ScriptFile`" --on-logon"
        $Shortcut.WorkingDirectory = $WorkspaceDir
        $Shortcut.Description = "Customs Legal Telegram Copilot - Tu dong quet buoi sang khi mo may"
        $Shortcut.Save()

        if (Test-Path $DisabledFlagFile) {
            Remove-Item -Path $DisabledFlagFile -Force
        }

        Write-Host "  [THANH CONG] DA CAI DAT CHE DO TU DONG KHI MO MAY!" -ForegroundColor Green
        Write-Host "  • Thu muc khoi dong: $StartupFolder" -ForegroundColor Gray
        Write-Host "  • File thuc thi:     $StartupShortcut" -ForegroundColor Gray
        Write-Host "  • Co che 1:          Moi khi ban mo may tinh, bot se tu dong chay ngam (pythonw)." -ForegroundColor Cyan
        Write-Host "  • Co che 2:          Kiem tra last_daily_run.json: Chi gui 1 lan duy nhat vao buoi sang trong ngay, khong bi spam neu khoi dong lai may." -ForegroundColor Cyan
        Write-Host "  • Co che 3:          Bao mat 100% qua file .env (CUSTOMS_TELEGRAM_BOT_TOKEN)." -ForegroundColor Cyan
    } catch {
        Write-Host "  [LOI] Khong the tao shortcut khoi dong: $_" -ForegroundColor Red
    }
    Write-Host "=================================================================" -ForegroundColor Cyan
}
