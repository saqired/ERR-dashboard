import streamlit as st
import pandas as pd

#Read an Excel file
df = pd.read_excel('Extrusion Rejection Record (10A_Jeff_250710).xlsx')
print(df.head())
