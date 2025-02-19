import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
def BarChart():
    selected_column = st.selectbox("Choose a column to visualize:", st.session_state.dataframe.select_dtypes(include=['object']).columns)
    st.html(f"<h2>Bar Chart of Categorical Column - {selected_column}</h2>")
    fig, ax = plt.subplots()
    st.session_state.dataframe[selected_column].value_counts().plot(kind="bar", ax=ax)
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Count")
    ax.set_title(f"Bar Chart of {selected_column}")
    plt.xticks(rotation=90)
    st.pyplot(fig)

def Histogram():
    selected_column = st.selectbox("Choose a column to visualize:", st.session_state.dataframe.select_dtypes(include=['number']).columns)
    st.html(f"<h2>Histogram of Numerical Column - {selected_column}</h2>")
    fig, ax = plt.subplots()
    st.session_state.dataframe[selected_column].plot(kind="hist", bins=20, alpha=0.7, edgecolor="black", ax=ax)
    ax.set_xlabel(selected_column)
    ax.set_ylabel("Frequency")
    ax.set_title(f"Histogram of {selected_column}")
    st.pyplot(fig)

def BoxPlot():
    st.html("<h2>Box Plot</h2>")
    numeric_columns = st.session_state.dataframe.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 0:
        selected_column = st.selectbox("Choose a numerical column for Box Plot:", numeric_columns)
        # Create Box Plot
        fig, ax = plt.subplots()
        ax.boxplot(st.session_state.dataframe[selected_column], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
        ax.set_xlabel(selected_column)
        ax.set_title(f"Box Plot of {selected_column}")
        st.pyplot(fig)
    else:
        st.warning("No numerical columns found in the dataset.")


def PieChart():
    st.html("<h2>Pie Chart</h2>")
    categorical_columns = st.session_state.dataframe.select_dtypes(include=['object']).columns
                
    if len(categorical_columns) > 0:
        selected_column = st.selectbox("Choose a categorical column for Pie Chart:", categorical_columns)

        value_counts = st.session_state.dataframe[selected_column].value_counts()
                    
        # Create Pie Chart
        fig, ax = plt.subplots()
        ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title(f"Pie Chart of {selected_column}")

        st.pyplot(fig)
    else:
        st.warning("No categorical columns found in the dataset.")
        

def ScatterPlot():
    st.html("<h2>Scatter Plot for Numerical Columns</h2>")
    numeric_columns = st.session_state.dataframe.select_dtypes(include=['number']).columns
    if len(numeric_columns) > 1:
        col1, col2 = st.selectbox("Choose X-axis column:", numeric_columns), st.selectbox("Choose Y-axis column:", numeric_columns, index=1)
        if col1 != col2:
            fig, ax = plt.subplots()
            ax.scatter(st.session_state.dataframe[col1], st.session_state.dataframe[col2], alpha=0.7, color="blue", edgecolors="black")
            ax.set_xlabel(col1)
            ax.set_ylabel(col2)
            ax.set_title(f"Scatter Plot of {col1} vs {col2}")
            st.pyplot(fig)
        else:
            st.warning("Please select different columns for X and Y axes.")
    else:
        st.warning("Not enough numerical columns for a scatter plot.")
    
    
def CorrelationHeatMap():
    st.html("<h2>Correlation Heatmap</h2>")
    numeric_columns = st.session_state.dataframe.select_dtypes(include=['number'])
    if not numeric_columns.empty:
        correlation_matrix = numeric_columns.corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        cax = ax.matshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar(cax)
        ticks = np.arange(len(correlation_matrix.columns))
        ax.set_xticks(ticks)
        ax.set_yticks(ticks)
        ax.set_xticklabels(correlation_matrix.columns, rotation=90)
        ax.set_yticklabels(correlation_matrix.columns)
        ax.set_title("Correlation Heatmap", pad=20)
        st.pyplot(fig)
    else:
        st.warning("No numerical columns found in the dataset.")               