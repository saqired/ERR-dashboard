import streamlit as st
import pandas as pd
import numpy as np

#Sample data
data = pd.DataFrame({
  'x': range(10),
  'y': np.random.randint(1,100,10)
})

#Line chart
st.bar_chart(data.set_index('x'))
