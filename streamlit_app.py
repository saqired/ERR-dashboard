import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Prepare your data ---
data = {
    'Product': ['Apples', 'Bananas', 'Cherries', 'Dates'],
    'Sales': [120, 90, 60, 150]
}
df = pd.DataFrame(data)

# --- Step 2: Show the table ---
st.subheader("📋 Sales Table")
st.dataframe(df)

# --- Step 3: Create and show the bar chart ---
st.subheader("📊 Sales Bar Chart")

# Plot using Matplotlib
fig, ax = plt.subplots()
ax.bar(df['Product'], df['Sales'], color='skyblue')
ax.set_xlabel('Product')
ax.set_ylabel('Units Sold')
ax.set_title('Fruit Sales Bar Chart')

# Show chart in Streamlit
st.pyplot(fig)
