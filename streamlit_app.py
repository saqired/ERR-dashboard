import streamlit as st
import pandas as pd
import altair as alt
import time

# --- Page Setup ---
st.set_page_config(page_title="Live Extrusion Rejection Record Dashboard", layout="centered")
st.title("🛠️ Live Extrusion Rejection Record Dashboard")

# --- Google Sheet CSV Export URL ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRuotFDwz3Gs5cVnYjcMhPovYHUpMsVe6LdHHUIDSJcYVVfII1pVWBXZUriMqEbim6Bs8diKBn9glc7/pub?output=csv"

# --- Auto Refresh Interval ---
refresh_interval = 10  # seconds

while True:
    try:
        # --- Load raw sheet ---
        full_df = pd.read_csv(sheet_url)

        # --- Clean Table 1: Defect Summary (assume starts at row 0 and ends before row 20) ---
        df_chart = full_df.loc[0:19, ['Defects', 'Total Number']].dropna()
        df_chart['Defects'] = df_chart['Defects'].astype(str).str.strip()
        df_chart['Total Number'] = pd.to_numeric(df_chart['Total Number'], errors='coerce')
        df_chart = df_chart.dropna()

        # --- Clean Table 2: Alloy-Temper table (assume starts at row 21 onward) ---
        raw_table2 = full_df.iloc[21:].dropna(how='all').reset_index(drop=True)

        if not raw_table2.empty:
            raw_table2.columns = raw_table2.iloc[0]
            df_table2 = raw_table2[1:].copy()
            df_table2 = df_table2.apply(pd.to_numeric, errors='ignore')
            df_table2 = df_table2.dropna(axis=1, how='all')
        else:
            df_table2 = pd.DataFrame()  # empty fallback

        # --- Bar Chart with Labels & Color ---
        st.subheader("📊 Total Number vs. Defects")

        chart_data = df_chart.reset_index(drop=True)

        bar = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Defects:N', title='Defects'),
            y=alt.Y('Total Number:Q', title='Total Count'),
            color=alt.Color('Defects:N', title="Defect Type")
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
            color='grey'
        ).encode(
            x='Defects:N',
            y='Total Number:Q',
            text='Total Number:Q'
        )

        st.altair_chart(bar + labels, use_container_width=True)

        # --- Defect Summary Table ---
        st.subheader("📋 Defect Summary Table")
        st.dataframe(df_chart, use_container_width=True)

        # --- Alloy-Temper Table ---
        if not df_table2.empty:
            st.subheader("📋 Table: Defect Count by Alloy-Temper")
            st.dataframe(df_table2, use_container_width=True)

        # --- Footer ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
        break
