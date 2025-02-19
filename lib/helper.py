import streamlit as st
import pandas as pd
import io
def handleFileUploader():
    st.session_state.dataframe = None
    st.session_state.old_dataframe = None
    st.session_state.duplicates_removed = False
    st.session_state.nulls_removed = False
    st.session_state.nulls_filled = False
    st.session_state.cleaning_done = False
    st.success("File Upload Successfully")
    
def readDatasetFile(dataset_path):
    if dataset_path.name.endswith('.csv'):
        df = pd.read_csv(dataset_path)
    elif dataset_path.name.endswith('.xlsx'):
        df = pd.read_excel(dataset_path)
    else:
        st.error("Unsupported file format.")
        return None
    df.index = range(1, len(df) + 1)
    return df

def get_download_link(df, file_format):
    output = io.BytesIO()
    if file_format == "csv":
        df.to_csv(output, index=False)
        mime = "text/csv"
        file_name = "processed_dataset.csv"
    elif file_format == "xlsx":
        df.to_excel(output, index=False, engine='openpyxl')
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        file_name = "processed_dataset.xlsx"
    else:
        st.error("Unsupported file format.")
        return None

    output.seek(0)
    return st.download_button(
        label="Download Dataset",
        data=output,
        file_name=file_name,
        mime=mime
    )
    
    
    
def showCleanedData(dataframe):
    # Print number of rows and columns
    st.markdown(f"<h4>Number of Rows: {dataframe.shape[0]}</h4><h4>Number of Columns: {dataframe.shape[1]}</h4>",unsafe_allow_html=True)

    # print top 5 rows
    st.markdown("<h3>Preview of top 5 rows of uploaded dataset:</h3>", unsafe_allow_html=True)
    st.dataframe(dataframe.head(5))  
        
    # print bottom 5 rows
    st.markdown("<h3>Preview of bottom 5 rows of uploaded dataset:</h3>", unsafe_allow_html=True)
    st.dataframe(dataframe.tail(5))  

    # print null values count
    st.markdown("<h2>Null Values Count Per Column</h2>", unsafe_allow_html=True)
    null_value_df = pd.DataFrame(
        {
            "**Columns**": dataframe.columns,
            "**Null Count**": dataframe.isnull().sum().values
        }
    )
    null_value_df.index = range(1, len(null_value_df) + 1)
    st.table(null_value_df)

st.set_page_config(page_title="Data Manipulator Web App")
st.title("Upload Dataset File")