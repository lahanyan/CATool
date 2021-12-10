from math import prod
from attr import attrib, attributes
from pandas.core.frame import DataFrame
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import base64


class ACBC:
    def __init__(self) -> None:
        # self.dataf = None
        self.BYO_called = False
        self.Screaning_called = False
        self.button_Screening = False
        self.dataf = pd.read_csv("/Users/larisa/Downloads/sample_data.csv")

    def Enzyme(self):
        #st.set_page_config('Adaptive Conjoint')
        st.write(self.button_Screening)
        if not self.button_Screening:
            if self.BYO_called == False:
                self.BuildYourOwn()
            
            
        elif self.Screaning_called == False:
            st.write("unblivable")
            self.Screening()
            
        else:
            #st.write("larbu")
            self.ChoicTaskTournament()

    def BuildYourOwn(self):
        self.BYO_called = True
       
        # # Upload Dataset
        # uploaded_file = st.sidebar.file_uploader('upload your CSV file',
        #                                          type=['csv', "xls", "xlsx"]
        #                                          )
        # if uploaded_file is None:
        #     st.stop()
        # try:
        #     self.dataf = pd.read_excel(uploaded_file)
        # except Exception:
        #     try:
        #         self.dataf = pd.read_csv(uploaded_file)
        #     except Exception:
        #         raise Exception("Not Supported File Format")
        

        pivotal_cols = st.sidebar.multiselect("Choose 4 Pivotal Columns",
                                              options=self.dataf.columns)

        for i in pivotal_cols:
            for_att_i = st.multiselect(
                "Choose Levels for " + str(i),
                options=self.dataf[i].unique()
            )
            self.dataf = self.dataf[self.dataf[i].isin(for_att_i)]

        st.write(self.dataf)
        st.write(len(self.dataf))
        self.button_Screening = st.button('Screening') 
        self.Enzyme()
            
            
        

    def Screening(self):
        self.Screaning_called = True
        # for each row creaqte a small window containing, make a radio button (possible, impossible)
        self.dataf["Not Possible"] = 0
        row_cnt = len(self.dataf)
        rows = [self.dataf.iloc[i] for i in range(row_cnt)]
       
        row_window = ['row_'+str(i) for i in range(3)]
        #st.write(row_window)
        row_window = st.columns(row_cnt)
        
        for i in range(len(row_window)):
            with row_window[i%3]:
                st.header("Alternative "+str(i+1))
                #st.write(rows[i])
                radio_ = st.radio('Select'+str(i+1), ['Possible','Impossible']) == 'Possible'
                if radio_ == 'Impossible':
                    self.dataf["Not Possible"].iloc[i] = 1
        # st.write('I reached to Screening :)')
        self.Enzyme()
        
        
        
    def colum_generator():
        pass
        
    def ChoicTaskTournament(self):
        st.write('I reached to ChoicTaskTournament :)')
        


if __name__ == '__main__':
    ACBC_expl = ACBC()
    ACBC_expl.Enzyme()

  # SUBMISSION OF CHOICE:
#df = dataf[dataf[key] == product]


# df.loc[(df['Brand'].isin(product))]

# df['Product'] = product
# df['Attribute'] = pd.Series(att)
# st.write(df.iloc[:,0])

# st.write(df)
# st.write(att)

# for col in df.columns:
#     if len(col) == 0:
#         df = df.drop(col,axis=1)
#         st.write(df)

#df = df[[key, attribute]]
# df = df[df[attribute] == choose_level]

# plot_imp = st.sidebar.radio("Plot something", ["No", "Yes"]) == "Yes"
# if not plot_imp:
#     st.write(df)

#     def st_pandas_to_csv_download_link(_df: pd.DataFrame, file_name: str = "dataframe.csv"):
#         csv_exp = _df.to_csv(index=False)
#         # some strings <-> bytes conversions necessary here
#         b64 = base64.b64encode(csv_exp.encode()).decode()
#         href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}" > Download Dataframe (CSV) </a>'
#         st.markdown(href, unsafe_allow_html=True)

#     st_pandas_to_csv_download_link(df, file_name="dataframe.csv")


# else:
#     st.write(px.scatter(df.iloc[:, 1],
#                         df.iloc[:, 1]
#                         )
#              )


# you are getting a csv data
# build your own -- get a table like, with the options of:
# selecting  levels in one column, next to attribute names, on the third column should be the price, on the last row TOTAL -- Price:
# return a selected CSV,
