import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
# Set the full path to your image
background_image_path = 'img.jpg'  # Update the path if necessary

def set_background_image(path):
    css = f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpg;base64,{path});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        opacity: 0.5;  # Adjust the transparency as needed
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Encode the image to base64
import base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return encoded

# Set the background
image_base64 = get_image_base64(background_image_path)
set_background_image(image_base64)
# Function to load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_json('healthcare.json')
    df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['avg_glucose_level'] = pd.to_numeric(df['avg_glucose_level'], errors='coerce')
    df['bmi'] = df['bmi'].fillna(df['bmi'].median())
    df['age'] = df['age'].fillna(df['age'].median())
    df['avg_glucose_level'] = df['avg_glucose_level'].fillna(df['avg_glucose_level'].median())
    return df

df = load_data()

# App title and description
st.title('Identification des individus à haut risque d’AVC')

st.markdown("Ce projet utilise Streamlit pour visualiser et analyser des données de santé afin d'identifier les individus à haut risque d'AVC en fonction de multiples facteurs de santé.")

# Checkbox to show raw data
if st.checkbox('Show raw data'):
    st.dataframe(df.style.highlight_max(axis=0))
# En-tête de configuration dans la sidebar
st.sidebar.header('Configuration')
analysis_options = ['age', 'bmi', 'avg_glucose_level', 'hypertension', 'heart_disease', 'stroke', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']
option = st.sidebar.selectbox('Vous voulez analyser quelle variable?', analysis_options)

# Slider to filter data by age in the sidebar
age_filter = st.sidebar.slider('Filtration de data par age', int(df['age'].min()), int(df['age'].max()), (int(df['age'].min()), int(df['age'].max())))
df_filtered = df[(df['age'] >= age_filter[0]) & (df['age'] <= age_filter[1])]

# Visualizations for numerical data
if option in ['age', 'bmi', 'avg_glucose_level']:
    st.subheader(f'Histogramme {option}')
    fig = px.histogram(df_filtered[option].dropna(), nbins=20, color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig)

    st.subheader(f'Boxplot {option}')
    fig = px.box(df_filtered, y=option, color_discrete_sequence=["#EF553B"])
    st.plotly_chart(fig)

# Checkbox and plot for 3D Scatter Plot
if st.checkbox('Montrer 3D Scatter Plot'):
    st.subheader('3D Scatter Plot de Age, BMI, and Avg Glucose Level')
    fig = px.scatter_3d(df_filtered, x='age', y='bmi', z='avg_glucose_level', color='avg_glucose_level',
                        symbol='stroke', opacity=0.7, color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

# Visualizations for categorical data
if option in ['hypertension', 'heart_disease', 'stroke', 'ever_married', 'work_type', 'Residence_type', 'smoking_status']:
    st.subheader(f'Bar plot pour {option}')
    fig, ax = plt.subplots()
    sns.countplot(x=option, data=df_filtered, ax=ax, palette="viridis")
    st.pyplot(fig)

# Checkbox and heatmap for numerical data correlations
if st.checkbox('Montrer correlation heatmap pour les données numériques'):
    st.subheader('Correlation Heatmap')
    numeric_cols = ['age', 'avg_glucose_level', 'bmi']
    fig, ax = plt.subplots()
    sns.heatmap(df_filtered[numeric_cols].corr(), annot=True, cmap='viridis', ax=ax)
    st.pyplot(fig)
# Footer
st.markdown('---\n Ce projet de visualisation des données de santé avec Streamlit facilite l’identification préventive des individus à haut risque d’AVC, améliorant ainsi les interventions de santé publique et clinique.')