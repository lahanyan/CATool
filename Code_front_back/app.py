
from pandas.core.frame import DataFrame
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import base64
#import lightgbm as lgb
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import regex as re


class ACBC:
    def __init__(self) -> None:
        # self.dataf = None
        self.BYO_called = False
        self.Screaning_called = False
        self.button_Screening = False
        self.unacceptable = False
        self.minor_cols = None
        self.columns_ = None
        self.dataf = None

    def Enzyme(self):
        #st.set_page_config('Adaptive Conjoint')

        if not self.button_Screening:
            if self.BYO_called == False:
                self.BuildYourOwn()

        elif not self.unacceptable:
            if self.Screaning_called == False:
                self.Screening()

        elif self.dataf["Not Possible"].sum() == 0:
            self.output()

        else:
            self.ChoicTaskTournament()

    def BuildYourOwn(self):
        self.BYO_called = True

        st.title("Build Your Own")
        # Upload Dataset
        uploaded_file = st.sidebar.file_uploader('upload your CSV file',
                                                 type=['csv', "xls", "xlsx"]
                                                 )
        if uploaded_file is None:
            st.stop()
        try:
            self.dataf = pd.read_excel(uploaded_file)
        except Exception:
            try:
                self.dataf = pd.read_csv(uploaded_file)
            except Exception:
                raise Exception("Not Supported File Format")

        pivotal_cols = st.sidebar.multiselect("Choose Pivotal Columns",
                                              options=self.dataf.columns)
        self.minor_cols = self.dataf.columns.drop(pivotal_cols)
        self.columns_ = self.dataf.columns
        for i in pivotal_cols:
            for_att_i = st.multiselect(
                "Choose Levels for " + str(i),
                options=self.dataf[i].unique()
            )
            self.dataf = self.dataf[self.dataf[i].isin(for_att_i)]

        self.button_Screening = st.radio(
            ' ', ["Don't Show Screening", "Show Screening"]) == "Show Screening"
        self.Enzyme()

    def Screening(self):
        self.Screaning_called = True
        st.title("Screeners")

        self.dataf["Not Possible"] = 0
        row_cnt = len(self.dataf)
        rows = [self.dataf[self.columns_].iloc[[i], ] for i in range(row_cnt)]

        row_window = None

        for i in range(row_cnt):
            row_window = st.columns(3)
            with row_window[i % 3]:

                st.header("Alternative "+str(i+1))
                st.write(rows[i].transpose())

                radio_ = st.radio('Select '+str(i+1),
                                  ['Possible', 'Impossible']) == 'Possible'

                if not radio_:
                    self.dataf["Not Possible"].iloc[i] = 1

        self.unacceptable = st.radio(
            ' ', ["Don't Show Unacceptable", "Show Unacceptable"]) == "Show Unacceptable"
        self.Enzyme()

    def ChoicTaskTournament(self):

        crucial_attribute = self.MachinLearningTools()
        st.title("Unacceptables")
        unacceptable_0 = []
        for i in self.minor_cols:
            selected_ = self.dataf.groupby(i).sum(
                'Not Possible').reset_index().sort_values("Not Possible", ascending=False)

            for j in range(2):

                if selected_[i].iloc[j] != crucial_attribute[1]:
                    #unacceptable_0.append([i, selected_[i].iloc[j]])
                    unacceptable_0.append(
                        str(i) + " is  " + str(selected_[i].iloc[j]))
                    unacceptable_0 = unacceptable_0

        unacceptable_1 = st.multiselect(
            "Select the Unacceptable Levels for Attributes", unacceptable_0)

        for unac in unacceptable_1:

            if len(unacceptable_1) > 0:
                unac = re.split(r" is  ", unac)

                self.dataf = self.dataf[self.dataf[unac[0]] != unac[1]]
        if len(unacceptable_1) != 0:
            self.output()

    def output(self):
        st.title("Choice Tournament")
        st.write(self.dataf[self.columns_])
        self.st_pandas_to_csv_download_link(file_name="dataframe.csv")

    def MachinLearningTools(self):

        # data processing
        target = ["Not Possible"]

        selected_data_ = self.dataf.copy()
        Y_ = pd.get_dummies(data=selected_data_[target], drop_first=True)
        selected_data_ = selected_data_.drop(columns=target, axis=1)
        categorical = selected_data_.nunique(
        )[selected_data_.nunique() < 10].keys().tolist()

        categorical_X = pd.get_dummies(data=selected_data_[categorical])

        selected_data_ = selected_data_.drop(columns=categorical, axis=1)
        if len(selected_data_.columns) > 0:
            scaler = StandardScaler()
            numerical_X = scaler.fit_transform(selected_data_)
            X_ = categorical_X.merge(right=numerical_X)
        else:
            X_ = categorical_X

        logreg = LogisticRegression(
            penalty="l1", C=1, solver="liblinear")  # L2
        logreg.fit(X_, Y_)

        coefficients = pd.concat([pd.DataFrame(X_.columns),
                                  pd.DataFrame(np.transpose(logreg.coef_))],
                                 axis=1)

        coefficients.columns = ["Feature", "Coefficient"]
        coefficients['Exp_Coefficient'] = np.exp(coefficients["Coefficient"])

        if coefficients['Exp_Coefficient'].min() < 0:
            possible_from_ml = coefficients["Feature"][coefficients['Exp_Coefficient']
                                                       == coefficients['Exp_Coefficient'].min()][0]

            _list = re.split(r"_|-", possible_from_ml)
            return _list
        return "NotAttributeFound"

    def st_pandas_to_csv_download_link(self: pd.DataFrame, file_name: str = "dataframe.csv"):
        csv_exp = self.dataf.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(csv_exp.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}" > Download Dataframe (CSV) </a>'
        st.markdown(href, unsafe_allow_html=True)
