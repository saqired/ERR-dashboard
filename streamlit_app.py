import streamlit as st
import pandas as pd
import time

# --- Page setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="wide")
st.title("📊 Live Defect Dashboard (Google Sheets Connected)")

# --- Google Sheets CSV URLs ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?gid=1029560887&single=true&output=csv"

# --- Auto-refresh loop ---
refresh_interval = 10  # seconds

while True:
    try:
        # --- Load both sheets ---
        df_summary = pd.read_csv(url_summary)
        df_press10a = pd.read_csv(url_press10a)

        # --- Section 1: Total Defects Summary ---
        st.subheader("📊 Total Number vs. Defects (Summarized)")
        if 'Defect' in df_summary.columns and 'Total' in df_summary.columns:
            st.bar_chart(df_summary.set_index('Defect'))
        st.dataframe(df_summary, use_container_width=True)

        st.markdown("---")

        # --- Section 2: Press10A Defect Breakdown ---
        st.subheader("📋 Defect Summary by Alloy (Press10A)")
        st.dataframe(df_press10a, use_container_width=True)

        # --- Footer ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
        break
