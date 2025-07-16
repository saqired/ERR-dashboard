import streamlit as st
import pandas as pd
import altair as alt
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard (Google Sheets)")

# --- Google Sheet URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?output=csv"

# --- Refresh interval ---
refresh_interval = 10  # seconds

while True:
    try:
        # --- Load full sheet ---
        full_df = pd.read_csv(sheet_url)

        # --- Table 1: Defect Summary for Bar Chart ---
        df_chart = full_df[['Defects', 'Total Number']].dropna()
        df_chart_clean = df_chart.set_index('Defects')

        # --- Table 2: Defect by Alloy-Temper (starts around row 20) ---
        raw_table = full_df.iloc[20:].dropna(how='all')  # Adjust row if needed
        raw_table = raw_table.reset_index(drop=True)
        raw_table.columns = raw_table.iloc[0]  # Use first row as header
        df_table1 = raw_table[1:].copy()
        df_table1 = df_table1.apply(pd.to_numeric, errors='ignore')
        df_table1 = df_table1.dropna(axis=1, how='all')

        # --- Section 1: Bar Chart with Value Labels ---
        st.subheader("📊 Total Number vs. Defects (with labels)")

        chart_data = df_chart_clean.reset_index()
        chart_data['Total Number'] = pd.to_numeric(chart_data['Total Number'], errors='coerce')

        bar = alt.Chart(chart_data).mark_bar(color='#1f77b4').encode(
            x=alt.X('Defects:N', title='Defects'),
            y=alt.Y('Total Number:Q', title='Total Count')
        ).properties(
            width=600,
            height=400
        )

        labels = alt.Chart(chart_data).mark_text(
            align='center',
            baseline='bottom',
            dy=-5,
            fontSize=12
        ).encode(
            x='Defects:N',
            y='Total Number:Q',
            text=alt.Text('Total Number:Q')
        )

        st.altair_chart(bar + labels, use_container_width=True)

        # --- Section 2: Defect Summary Table ---
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
