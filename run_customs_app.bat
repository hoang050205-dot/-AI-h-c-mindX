@echo off
title Customs Pre-Clearance Copilot (Minh Hoang Private Suite)
color 0b
echo ===============================================================================
echo     CUSTOMS PRE-CLEARANCE COPILOT - PRIVATE STREAMLIT SUITE
echo     Chu so huu: Pham Minh Hoang (AI4A - Antigravity)
echo     Che do: Private Localhost (127.0.0.1 - Khong chia se mang LAN)
echo ===============================================================================
echo.
echo [1/2] Dang kiem tra moi truong Python va thu vien...
python -c "import streamlit, openpyxl, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Thieu thu vien! Dang cai dat tu dong: streamlit openpyxl pandas...
    pip install streamlit openpyxl pandas
)

echo [2/2] Dang khoi dong Web App tren cong 8501 (Local Only)...
echo Ung dung se tu dong mo tren trinh duyet tai: http://localhost:8501
echo Ma PIN bao mat mac dinh: 0502 (hoac bam 'Chay ngay')
echo.
streamlit run app_customs_preclearance.py --server.port 8501 --server.address 127.0.0.1 --server.headless false

pause
