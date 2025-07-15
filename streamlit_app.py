import streamlit as st
import pandas as pd
import time

# --- Setup ---
st.set_page_config(page_title="Live Defect Dashboard", layout="centered")
st.title("🛠️ Live Defect Dashboard (Simulated)")

# --- Refresh Rate ---
refresh_interval = 10  # seconds
st.caption(f"⏱ Auto-refreshes every {refresh_interval} seconds")

# --- Static Defect Data (from your screenshot) ---
defect_data = {
    'Defect': ['Dented', 'Bubble', 'Tearing', 'Scratch', 'Stopmark', 'White Line', 'Watermark', 'Die Line', 'Others'],
    'Total': [150, 137, 134, 32, 21, 5, 2, 38, 60]
}
df_defect = pd.DataFrame(defect_data).set_index('Defect')

# --- Simulated Full Table ---
df_table = pd.DataFrame({
    '#': [1,2,3,4,5,6,7,8,9,10],
    'Alloy-Temper': ['6060-T5','6060-T6','6063-T5','6063-T6','6005-T5','6005-T6','6061-T6','6061-T6','6082-T5','6082-T6'],
    'Dented': [0, 50, 12, 30, 1, 2, 0, 39, 0, 16],
    'Bubble': [11, 0, 10, 10, 16, 15, 0, 83, 0, 2],
    'Tearing': [0, 11, 0, 13, 0, 0, 0, 101, 0, 0],
    'Scratch': [0, 0, 2, 2, 0, 0, 0, 5, 0, 0],
    'Stopmark': [1, 3, 2, 0, 0, 0, 0, 17, 0, 0],
    'White Line': [2, 0, 0, 0, 0, 0, 0, 8, 0, 0],
    'Watermark': [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    'Die Line': [0, 29, 0, 0, 0, 0, 0, 9, 0, 0],
    'Others': [3, 2, 0, 0, 1, 1, 0, 45, 0, 1]
})

# --- Main Display ---
st.subheader("📈 Total Number vs. Defects (Bar Chart)")
st.bar_chart(df_defect)

st.subheader("📋 Defect Breakdown Table")
st.dataframe(df_table, use_container_width=True)

# --- Simulated Refresh ---
st.toast("🔁 Refreshing data...")
time.sleep(refresh_interval)
st.rerun()
