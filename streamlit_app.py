import streamlit as st
import pandas as pd
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard (Google Sheets)")

# --- Google Sheet URL (CSV export format) ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?output=csv"

# --- Refresh interval ---
refresh_interval = 10  # seconds

# --- Live Refresh Loop ---
while True:
    try:
        # --- Load Google Sheet data ---
        df = pd.read_csv(sheet_url)

        # --- Check required columns ---
        if 'Defect' not in df.columns or 'Total' not in df.columns:
            st.error("❗ The sheet must include 'Defect' and 'Total' columns.")
            break

        # --- Format data ---
        df_chart = df[['Defect', 'Total']].set_index('Defect')

        # --- Bar Chart ---
        st.subheader("📊 Total Number vs. Defects")
        st.bar_chart(df_chart)

        # --- Full Table ---
        st.subheader("📋 Defect Data Table")
        st.dataframe(df, use_container_width=True)

        # --- Footer ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Failed to load or process the sheet: {e}")
        break
