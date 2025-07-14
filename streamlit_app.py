import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="Simple Bar Chart", layout="centered")
st.title("📊 Product Sales Dashboard")

# --- Sample Data ---
data = {
    'Product': ['Apples', 'Bananas', 'Cherries', 'Dates'],
    'Sales': [120, 90, 60, 150]
}
df = pd.DataFrame(data)

# --- Show Table ---
st.subheader("🧾 Sales Table")
st.dataframe(df, use_container_width=True)

# --- Convert to Streamlit's chart format ---
df_chart = df.set_index('Product')

# --- Show Bar Chart ---
st.subheader("📈 Sales Bar Chart")
st.bar_chart(df_chart)
