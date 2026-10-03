"""
=============================================================================
STREAMLIT CLOUD ENTRYPOINT
Master Customs Pre-Clearance & Compliance Orchestrator v2.0 Pro
Phát triển bởi: Phạm Minh Hoàng (AI4A - Antigravity)
=============================================================================
"""
import runpy
import os

# Tự động nạp và thực thi ứng dụng chính app_customs_preclearance.py
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_app = os.path.join(current_dir, "app_customs_preclearance.py")
    if os.path.exists(target_app):
        runpy.run_path(target_app, run_name="__main__")
    else:
        import streamlit as st
        st.error(f"Không tìm thấy file {target_app}!")
