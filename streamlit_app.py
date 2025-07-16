import streamlit as st
import pandas as pd
import altair as alt
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard")

# --- Google Sheet CSV Export URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?output=csv"

# --- Auto Refresh Interval ---
refresh_interval = 10  # seconds

while True:
    try:
        # --- Load Sheet ---
        full_df = pd.read_csv(sheet_url)

        # --- Section A: Bar Chart Data (Defect Summary) ---
        df_chart = full_df[['Defects', 'Total Number']].dropna()
        df_chart['Defects'] = df_chart['Defects'].astype(str).str.strip()
        df_chart['Total Number'] = pd.to_numeric(df_chart['Total Number'], errors='coerce')
        df_chart = df_chart.dropna()
        chart_data = df_chart.reset_index(drop=True)

        # --- Section B: Second Table (Defect by Alloy-Temper) ---
        raw_table = full_df.iloc[20:].dropna(how='all')  # Adjust row if needed
        raw_table = raw_table.reset_index(drop=True)
        raw_table.columns = raw_table.iloc[0]  # Use first row as headers
        df_table2 = raw_table[1:].copy()
        df_table2 = df_table2.apply(pd.to_numeric, errors='ignore')
        df_table2 = df_table2.dropna(axis=1, how='all')

        # --- Section 1: Bar Chart with Color & Labels ---
        st.subheader("📊 Total Number vs. Defects")

        bar = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Defects:N', title='Defects'),
            y=alt.Y('Total Number:Q', title='Total Count'),
            color=alt.Color('Defects:N', title="Defect Type")  # Different color per bar
        ).properties(
            width=600,
            height=400
        )

        labels = alt.Chart(chart_data).mark_text(
            align='center',
            baseline='bottom',
            dy=-10,
            fontSize=12,
            fontWeight='bold',
            color='black'
        ).encode(
            x='Defects:N',
            y='Total Number:Q',
            text='Total Number:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)

        # --- Section 2: Table - Defect Summary ---
        st.subheader("📋 Defect Summary Table")
        st.dataframe(df_chart, use_container_width=True)

        # --- Section 3: Table - Defect Count by Alloy-Temper ---
        st.subheader("📋 Table: Defect Count by Alloy-Temper")
        st.dataframe(df_table2, use_container_width=True)

        # --- Footer & Auto-Refresh ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
        break
