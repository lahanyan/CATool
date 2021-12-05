# to run the demo: streamlit run strmlt.py

# To complete the task, I am going to need the following libraries:
from math import prod
from pandas.core.frame import DataFrame
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import base64



st.set_page_config('Adaptive Conjoint')

# Upload Dataset
uploaded_file = st.sidebar.file_uploader('upload your CSV file',
                                 type=['csv', "xls", "xlsx"]
                                 )

# dataf = pd.read_csv("/Users/larisa/Downloads/sample_data.csv")
if uploaded_file is None:
    st.stop()
try:
    dataf = pd.read_excel(uploaded_file)
except Exception:
    try:
        dataf = pd.read_csv(uploaded_file)
    except Exception:
        raise Exception ("Not Supported File Format")

key = st.sidebar.selectbox("Choose Product Column",
                     options=dataf.columns)



product = st.sidebar.selectbox("Choose Product Type",
                         # ["Vicacell","Beeline", "Ucom"]
                         options=dataf[key].unique()
                         )




attribute = st.sidebar.selectbox(
    label="Choose the Attribute",
    # ["Price","IntSpeed", "FixedLandline", "MobileLine"]
    options=dataf.drop(key, axis=1).columns.unique()
)



chosen_level = st.sidebar.selectbox(
    "Choose " + str(attribute) + " Levels",
    options=dataf[attribute].unique()
)
  # SUBMISSION OF CHOICE:
df = dataf[dataf[key] == product]

df = df[[key, attribute]]
df = df[df[attribute] == chosen_level]

plot_imp = st.sidebar.radio("Plot something", ["No", "Yes"]) == "Yes"
if not plot_imp:
    st.write(df)

    def st_pandas_to_csv_download_link(_df: pd.DataFrame, file_name: str = "dataframe.csv"):
        csv_exp = _df.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(csv_exp.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}" > Download Dataframe (CSV) </a>'
        st.markdown(href, unsafe_allow_html=True)

    st_pandas_to_csv_download_link(df, file_name="dataframe.csv")


else:
    st.write(px.scatter(df.iloc[:, 1],
                        df.iloc[:, 1]
                        )
             )



