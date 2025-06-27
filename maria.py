import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the Streamlit app
st.title("Distribuição de Pets por Espécie")

# Load the dataset
# Make sure 'pet_adoption_center.csv' is in the same directory as your Streamlit app
df = pd.read_csv('pet_adoption_center.csv')

# Calculate the count of each species
species_counts = df['species'].value_counts().reset_index()
species_counts.columns = ['Species', 'Count']

# Create a bar chart using Plotly Express
fig = px.bar(species_counts,
             x='Species',
             y='Count',
             title='Número de Pets por Espécie',
             labels={'Species': 'Espécie', 'Count': 'Número de Pets'},
             color='Species') # Optional: color bars by species

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

st.write("Este gráfico mostra a quantidade de cada tipo de animal (espécie) presente no centro de adoção.")

