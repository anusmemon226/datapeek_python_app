import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from lib.helper import handleFileUploader
from lib.helper import readDatasetFile
from lib.helper import get_download_link
from lib.helper import showCleanedData
from lib.graphs import BarChart
from lib.graphs import Histogram
from lib.graphs import BoxPlot
from lib.graphs import PieChart
from lib.graphs import ScatterPlot
from lib.graphs import CorrelationHeatMap


# Initialize session state variables
if "old_dataframe" not in st.session_state:
    st.session_state.old_dataframe = None
if "dataframe" not in st.session_state:
    st.session_state.dataframe = None
if "duplicates_removed" not in st.session_state:
    st.session_state.duplicates_removed = False
if "nulls_removed" not in st.session_state:
    st.session_state.nulls_removed = False
if "nulls_filled" not in st.session_state:
    st.session_state.nulls_filled = False
if "cleaning_done" not in st.session_state:
    st.session_state.cleaning_done = False


st.title("Upload Dataset File")
dataset_file = st.file_uploader('Upload Dataset File', type=["csv", "xlsx"],label_visibility="hidden",on_change=handleFileUploader)


if dataset_file is not None:
    if st.session_state.dataframe is None:
        read_dataset = readDatasetFile(dataset_file)
        st.session_state.dataframe = read_dataset
        st.session_state.old_dataframe = read_dataset

    if st.session_state.dataframe is not None:
        showCleanedData(st.session_state.old_dataframe)
        dataframe = st.session_state.dataframe
        st.title("Data Cleaning Options")
        col1, col2, col3 = st.columns(3)
        duplicate_count = dataframe.duplicated().sum()
        with col1:
            # Remove duplicate rows option
            if duplicate_count > 0 and not st.session_state.duplicates_removed:
                if st.button("Remove Duplicate Rows"):
                    st.session_state.dataframe = dataframe.drop_duplicates()
                    st.session_state.duplicates_removed = True
                    st.success("Duplicate Rows Successfully Removed...")
            else:
                st.button("No Duplicate Rows", disabled=True)
        null_count = dataframe.isnull().sum().sum()
        with col2:
            # Remove null fields rows option
            if null_count > 0 and not st.session_state.nulls_removed and not st.session_state.nulls_filled:
                if st.button("Remove Null Fields Rows"):
                    st.session_state.dataframe = dataframe.dropna()
                    st.session_state.nulls_removed = True
                    st.success("Null Rows Successfully Removed...")
            else:
                st.button("No Null Fields", disabled=True)

        with col3:
            # Fill null fields button
            if null_count > 0 and not st.session_state.nulls_removed and not st.session_state.nulls_filled:
                if st.button("Fill Null Fields"):
                    df = dataframe.copy()
                    for col in df.columns:
                        if df[col].dtype in ['int64', 'float64']:
                            df[col].fillna(df[col].mean(),inplace=True)
                        else:
                            df[col].fillna(df[col].mode()[0],inplace=True)
                    st.session_state.dataframe = df 
                    st.session_state.nulls_filled = True
                    st.success("Null Values Successfully Filled!")
            else:
                st.button("No Null Fields Available", disabled=True)


        if duplicate_count == 0 and null_count == 0:
            st.session_state.nulls_filled = True
            st.session_state.duplicates_removed = True
            st.session_state.nulls_removed = True



        if st.session_state.duplicates_removed or st.session_state.nulls_removed or st.session_state.nulls_filled:
            selected_columns = st.multiselect("Remove Unwanted Columns", dataframe.columns, default=dataframe.columns,disabled=st.session_state.cleaning_done)
            if selected_columns:
                dataframe = dataframe[selected_columns]
            else:
                st.error("Please select at least one column.")
            if st.button("Done Cleaning"):
                st.session_state.dataframe = dataframe
                st.success("Data Cleaned")
                st.session_state.cleaning_done = True
            
            if st.session_state.cleaning_done:
                if st.button("Show Cleaned Data"):
                    st.title("Dataset After Cleaning")
                    showCleanedData(st.session_state.dataframe)
                st.title("Download Processed Dataset")
                file_format = st.radio("Select File Format:", ["csv", "xlsx"])
                get_download_link(pd.DataFrame(st.session_state.dataframe),file_format)
                    
            
                st.title("Data Visualization")
                
                hist = st.checkbox("Histogram")
                bar = st.checkbox("Bar Chart")
                box = st.checkbox("Box Plot")
                pie = st.checkbox("Pie Chart")
                scatter = st.checkbox("Scatter Plot")
                corr = st.checkbox("Correlation Heatmap")
                
                if hist:
                    Histogram()
                if bar:
                    BarChart()
                if box:
                    BoxPlot()    
                if pie: 
                    PieChart()
                if scatter:
                    ScatterPlot()
                if corr: 
                    CorrelationHeatMap()