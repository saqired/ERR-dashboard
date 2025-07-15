import streamlit as st
import pandas as pd
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard (Google Sheets)")

# --- Single Google Sheet URL with both tables ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?output=csv"

# --- Refresh interval ---
refresh_interval = 10  # seconds

while True:
    try:
        # --- Load full sheet ---
        full_df = pd.read_csv(sheet_url)

        # --- Table 1: Defect Summary for Chart ---
        df_chart = full_df[['Defects', 'Total Number']].dropna()
        df_chart_clean = df_chart.set_index('Defects')

        # --- Table 2: Defect by Alloy-Temper (starts at row 20+) ---
raw_table = full_df.iloc[20:].dropna(how='all')  # adjust 20 if needed
raw_table = raw_table.reset_index(drop=True)

# Reset column names using the first row of the sliced data
raw_table.columns = raw_table.iloc[0]
df_table1 = raw_table[1:].copy()

# Convert columns to appropriate types safely
df_table1 = df_table1.apply(pd.to_numeric, errors='ignore')

# Drop completely empty columns (if any)
df_table1 = df_table1.dropna(axis=1, how='all')

        # --- Section 1: Bar Chart ---
        st.subheader("📊 Total Number vs. Defects")
        st.bar_chart(df_chart_clean)

        # --- Section 2: Full Defect Summary Table ---
        st.subheader("📋 Defect Summary Table")
        st.dataframe(df_chart, use_container_width=True)

        # --- Section 3: Table1 - Defect by Alloy-Temper ---
        st.subheader("📋 Table1: Defect Count by Alloy-Temper")
        st.dataframe(df_table1, use_container_width=True)

        # --- Footer ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
        break
