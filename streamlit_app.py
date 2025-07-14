import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="Defect Summary", layout="centered")
st.title("📊 Summarized Defect Report (Press 10A)")

# --- Sample Data (manually entered from your image) ---
data = {
    'Defect': ['Dented', 'Bubble', 'Tearing', 'Scratch', 'Stopmark', 'White Line', 'Watermark', 'Die Line', 'Others'],
    'Total': [150, 137, 134, 32, 21, 5, 2, 38, 60]
}
df_defects = pd.DataFrame(data)

# --- Show Bar Chart ---
st.subheader("📈 Total Number vs. Defects")
df_defects_chart = df_defects.set_index('Defect')
st.bar_chart(df_defects_chart)

# --- Full Breakdown Table (per Alloy-Temp) ---
st.subheader("🧾 Summarized Press10A Table")

# Manually re-created from your screenshot
table_data = {
    '#': [1,2,3,4,5,6,7,8,9,10],
    'Alloy-Temp': ['6060-T5','6060-T6','6063-T5','6063-T6','6005-T5','6005-T6','6061-T6','6061-T6','6082-T5','6082-T6'],
    'Dented': [0, 50, 12, 30, 1, 2, 0, 39, 0, 16],
    'Bubble': [11, 0, 10, 10, 16, 15, 0, 83, 0, 2],
    'Tearing': [0, 11, 0, 13, 0, 0, 0, 101, 0, 0],
    'Scratch': [0, 0, 2, 2, 0, 0, 0, 5, 0, 0],
    'Stopmark': [1, 3, 2, 0, 0, 0, 0, 17, 0, 0],
    'White Line': [2, 0, 0, 0, 0, 0, 0, 8, 0, 0],
    'Watermark': [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
    'Die Line': [0, 29, 0, 0, 0, 0, 0, 9, 0, 0],
    'Others': [3, 2, 0, 0, 1, 1, 0, 45, 0, 1]
}
df_table = pd.DataFrame(table_data)

st.dataframe(df_table, use_container_width=True)
