import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('pet_adoption_center.csv')
    
    # Converter datas
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['adoption_date'] = pd.to_datetime(df['adoption_date'])
    
    # Calcular tempo até adoção (em dias)
    df['days_to_adopt'] = (df['adoption_date'] - df['arrival_date']).dt.days
    
    return df

df = load_data()

# Sidebar com filtros
st.sidebar.header('Filtros')
species_filter = st.sidebar.multiselect(
    'Espécie',
    options=df['species'].unique(),
    default=df['species'].unique()
)

status_filter = st.sidebar.radio(
    'Status de Adoção',
    options=['Todos', 'Adotados', 'Não Adotados']
)

# Aplicar filtros
filtered_df = df[df['species'].isin(species_filter)]

if status_filter == 'Adotados':
    filtered_df = filtered_df[filtered_df['adopted'] == True]
elif status_filter == 'Não Adotados':
    filtered_df = filtered_df[filtered_df['adopted'] == False]

# Layout principal
st.title('📊 Análise de Centro de Adoção de Pets')
st.markdown('---')

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric('Total de Pets', len(filtered_df))
col2.metric('Taxa de Adoção', 
            f"{filtered_df['adopted'].mean()*100:.1f}%" if len(filtered_df) > 0 else '0%')
col3.metric('Tempo Médio para Adoção', 
            f"{filtered_df['days_to_adopt'].mean():.1f} dias" if len(filtered_df[filtered_df['adopted']]) > 0 else 'N/A')

# Gráfico 1: Distribuição por Espécie
st.subheader('Distribuição por Espécie')
fig1 = px.pie(
    filtered_df,
    names='species',
    hole=0.3,
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: Status de Adoção por Espécie
st.subheader('Status de Adoção por Espécie')
adoption_counts = filtered_df.groupby(['species', 'adopted']).size().unstack().fillna(0)
adoption_counts = adoption_counts.rename(columns={True: 'Adotados', False: 'Não Adotados'})

fig2, ax = plt.subplots()
adoption_counts.plot(kind='bar', stacked=True, ax=ax, color=['#4CAF50', '#F44336'])
ax.set_ylabel('Quantidade')
ax.legend(title='Status')
st.pyplot(fig2)

# Gráfico 3: Distribuição de Idades
st.subheader('Distribuição de Idades')
fig3 = px.histogram(
    filtered_df,
    x='age_years',
    nbins=20,
    color='species',
    barmode='overlay',
    opacity=0.7,
    labels={'age_years': 'Idade (anos)'}
)
st.plotly_chart(fig3, use_container_width=True)

# Gráfico 4: Top 10 Raças Mais Comuns
st.subheader('Raças Mais Populares')
top_breeds = filtered_df['breed'].value_counts().head(10)
fig4 = px.bar(
    top_breeds,
    orientation='v',
    labels={'value': 'Quantidade', 'index': 'Raça'},
    color=top_breeds.values,
    color_continuous_scale='Blues'
)
st.plotly_chart(fig4, use_container_width=True)

# Tabela com dados brutos
st.subheader('Dados Completos')
st.dataframe(filtered_df)

