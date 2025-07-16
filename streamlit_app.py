import streamlit as st
import pandas as pd
import altair as alt
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard")

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
        df_chart['Defects'] = df_chart['Defects'].astype(str).str.strip()  # ensure clean text
        df_chart['Total Number'] = pd.to_numeric(df_chart['Total Number'], errors='coerce')
        df_chart_clean = df_chart.set_index('Defects')

        # --- Table 2: Defect by Alloy-Temper (starts around row 20) ---
        raw_table = full_df.iloc[20:].dropna(how='all')
        raw_table = raw_table.reset_index(drop=True)
        raw_table.columns = raw_table.iloc[0]
        df_table1 = raw_table[1:].copy()
        df_table1 = df_table1.apply(pd.to_numeric, errors='ignore')
        df_table1 = df_table1.dropna(axis=1, how='all')

        # --- Section 1: Bar Chart with Colored Bars and Labels ---
        st.subheader("📊 Total Number vs. Defects")

        chart_data = df_chart_clean.reset_index()

        # Bar chart with one color per Defect
        bar = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Defects:N', title='Defects'),
            y=alt.Y('Total Number:Q', title='Total Count'),
            color=alt.Color('Defects:N', title="Defect Type")  # 👈 this makes each bar a different color
        ).properties(
            width=600,
            height=400
        )

        # Add number labels on bars
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

        # Display chart with labels
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
