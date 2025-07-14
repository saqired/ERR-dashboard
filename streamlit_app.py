import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="Sales Dashboard", layout="centered")

# --- Title ---
st.title("📊 Product Sales Dashboard")

# --- Sample Data ---
data = {
    'Product': ['Apples', 'Bananas', 'Cherries', 'Dates'],
    'Sales': [120, 90, 60, 150]
}
df = pd.DataFrame(data)

# --- Show Data Table ---
st.subheader("🧾 Sales Table")
st.dataframe(df, use_container_width=True)

# --- Plotly Bar Chart ---
st.subheader("📈 Sales Bar Chart")
fig = px.bar(
    df,
    x='Product',
    y='Sales',
    text='Sales',
    color='Product',
    title="Product Sales Overview",
    labels={'Sales': 'Units Sold'},
    template='plotly_white'
)
fig.update_traces(textposition='outside')
fig.update_layout(yaxis=dict(title='Units Sold'), xaxis=dict(title='Product'))

# --- Display Chart ---
st.plotly_chart(fig, use_container_width=True)
