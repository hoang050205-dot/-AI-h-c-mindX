# -*- coding: utf-8 -*-
param(
    [switch]$Register,
    [switch]$Remove,
    [switch]$Disable,
    [switch]$Enable,
    [switch]$Status,
    [switch]$RunNow,
    [string]$Time = "10:00AM"
)

$TaskName = "Telegram_AI_News_Bot_10AM"
$WorkspaceDir = $PSScriptRoot
$PythonExe = "C:\Program Files\IBM\SPSS Statistics\Python3\python.exe"
$ScriptFile = Join-Path $PSScriptRoot "send_telegram.py"

# Neu khong truyen tham so nao, mac dinh kiem tra trang thai
if (-not ($Register -or $Remove -or $Disable -or $Enable -or $Status -or $RunNow)) {
    $Status = $true
}

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "QUAN LY LICH TRINH TELEGRAM AI NEWS BOT (10:00 AM DAILY)" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

if ($Disable) {
    Write-Host "[Tam dung] Dang tam dung tac vu '$TaskName'..." -ForegroundColor Yellow
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        Disable-ScheduledTask -TaskName $TaskName | Out-Null
        Write-Host "  [OK] DA TAM DUNG TAC VU '$TaskName' THANH CONG!" -ForegroundColor Green
        Write-Host "  Bot se khong gui tin tu dong vao 10:00 AM cho den khi ban bat lai." -ForegroundColor Yellow
        Write-Host "  De bat lai, hay yeu cau toi hoac chay: .\setup_scheduler.ps1 -Enable" -ForegroundColor Cyan
    } else {
        Write-Host "  [Loi] Khong tim thay tac vu '$TaskName'." -ForegroundColor Red
    }
    exit 0
}

if ($Enable) {
    Write-Host "[Kich hoat] Dang bat lai tac vu '$TaskName'..." -ForegroundColor Yellow
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        Enable-ScheduledTask -TaskName $TaskName | Out-Null
        Write-Host "  [OK] DA BAT LAI TAC VU '$TaskName' THANH CONG!" -ForegroundColor Green
        Write-Host "  Bot se tiep tuc gui tin tu dong vao 10:00 AM hang ngay." -ForegroundColor Green
        $info = Get-ScheduledTaskInfo -TaskName $TaskName
        Write-Host "  Lan chay tiep theo: $($info.NextRunTime)" -ForegroundColor Cyan
    } else {
        Write-Host "  [Loi] Khong tim thay tac vu '$TaskName'." -ForegroundColor Red
    }
    exit 0
}

if ($Status) {
    Write-Host "[Kiem tra] Trang thai tac vu '$TaskName':" -ForegroundColor Yellow
    $existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existing) {
        if ($existing.State -eq 'Disabled') {
            Write-Host "  [TAM DUNG] Tac vu '$TaskName' DANG BI TAM DUNG (Disabled)!" -ForegroundColor Yellow
            Write-Host "  Trang thai: $($existing.State)" -ForegroundColor Yellow
        } else {
            Write-Host "  [OK] Tac vu '$TaskName' DANG HOAT DONG!" -ForegroundColor Green
            Write-Host "  Trang thai: $($existing.State)" -ForegroundColor Green
        }
        $info = Get-ScheduledTaskInfo -TaskName $TaskName
        Write-Host "  Lan chay gan nhat: $($info.LastRunTime)"
        Write-Host "  Lan chay tiep theo: $($info.NextRunTime)"
    } else {
        Write-Host "  Tac vu '$TaskName' chua duoc dang ky." -ForegroundColor Gray
    }
    exit 0
}

if ($Remove) {
    Write-Host "[Go bo] Dang xoa tac vu '$TaskName'..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Host "  [OK] Da go bo tac vu '$TaskName' thanh cong!" -ForegroundColor Green
    exit 0
}

if ($RunNow) {
    Write-Host "[Thuc thi] Dang kich hoat tac vu '$TaskName'..." -ForegroundColor Yellow
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "  [OK] Da kich hoat tac vu thanh cong!" -ForegroundColor Green
    exit 0
}

if ($Register) {
    Write-Host "[Cau hinh] Dang dang ky tac vu vao Windows Task Scheduler luc $Time moi ngay..." -ForegroundColor Yellow

    if (-not (Test-Path $PythonExe)) {
        Write-Host "  [Loi] Khong tim thay Python tai: $PythonExe" -ForegroundColor Red
        exit 1
    }
    if (-not (Test-Path $ScriptFile)) {
        Write-Host "  [Loi] Khong tim thay script tai: $ScriptFile" -ForegroundColor Red
        exit 1
    }

    $Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "send_telegram.py" -WorkingDirectory $WorkspaceDir
    $Trigger = New-ScheduledTaskTrigger -Daily -At $Time
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Description "Telegram AI News Daily Briefing at 10 AM" -Force | Out-Null

    Write-Host "  [OK] DA DANG KY THANH CONG TAC VU: $TaskName" -ForegroundColor Green
    Write-Host "  Thoi gian kich hoat: $Time moi ngay" -ForegroundColor Cyan
    Write-Host "  Script thuc thi: $ScriptFile" -ForegroundColor Cyan
    Write-Host "  Thu muc lam viec: $WorkspaceDir" -ForegroundColor Cyan

    $info = Get-ScheduledTaskInfo -TaskName $TaskName
    Write-Host "  Lan chay tiep theo: $($info.NextRunTime)" -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Cyan
}
