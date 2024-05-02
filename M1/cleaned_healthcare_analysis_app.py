
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title='Healthcare Data Analysis', layout='wide')

# Chargement des données
@st.cache
def load_data():
    return pd.read_json(r"C:\Users\hp\Desktop\M1\healthcare.json")

df = load_data()

# Nettoyage des données
df['bmi'].replace('N/A', pd.NA, inplace=True)
df['bmi'] = pd.to_numeric(df['bmi'], errors='coerce')
df.dropna(subset=['bmi'], inplace=True)

# Interface utilisateur
st.title('Analyse des Données de Santé')

# Sélection des variables pour l'analyse
option = st.sidebar.selectbox(
    'Choisissez une variable pour visualiser',
    ['age', 'bmi', 'avg_glucose_level', 'work_type', 'smoking_status', 'ever_married', 'Residence_type']
)

# Visualisation
if option in ['age', 'bmi', 'avg_glucose_level']:
    # Histogramme
    st.subheader(f'Histogramme de {option}')
    fig, ax = plt.subplots()
    sns.histplot(df[option], kde=True, ax=ax)
    st.pyplot(fig)

    # Boxplot
    st.subheader(f'Boxplot de {option}')
    fig, ax = plt.subplots()
    sns.boxplot(x=df[option], ax=ax)
    st.pyplot(fig)
else:
    # Bar plot pour les données catégoriques
    st.subheader(f'Répartition de {option}')
    fig, ax = plt.subplots()
    sns.countplot(x=option, data=df, palette='viridis', ax=ax)
    st.pyplot(fig)

# Corrélation entre les données numériques
if st.checkbox('Afficher la matrice de corrélation'):
    st.subheader('Matrice de Corrélation')
    fig, ax = plt.subplots()
    sns.heatmap(df[['age', 'bmi', 'avg_glucose_level']].corr(), annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)
