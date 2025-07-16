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
        df_chart['Defects'] = df_chart['Defects'].astype(str).str.strip()
        df_chart['Total Number'] = pd.to_numeric(df_chart['Total Number'], errors='coerce')
        df_chart = df_chart.dropna()

        # Show debug to confirm defects are valid and unique
        st.subheader("🧪 Debug: Defect Values")
        st.write("Unique Defects:", df_chart['Defects'].unique())

        chart_data = df_chart.reset_index(drop=True)

        # --- Bar Chart with Different Colors per Defect ---
        st.subheader("📊 Total Number vs. Defects (Multi-colored with labels)")

        bar = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Defects:N', title='Defects'),
            y=alt.Y('Total Number:Q', title='Total Count'),
            color=alt.Color('Defects:N', title="Defect Type")  # force unique color per defect
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

        # --- Optional: Show raw table
        st.subheader("📋 Defect Summary Table")
        st.dataframe(df_chart, use_container_width=True)

        # --- Footer ---
        st.caption(f"🔄 Auto-refreshing every {refresh_interval} seconds...")
        time.sleep(refresh_interval)
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")
        break
