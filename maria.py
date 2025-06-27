import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Carregar os dados
data = pd.read_csv("pet_adoption_center.csv")

# Calcular taxas de adoção por raça
breed_stats = data.groupby('breed').agg(
    total_pets=('pet_id', 'count'),
    adopted_pets=('adopted', 'sum')
).reset_index()

# Calcular taxa de adoção e filtrar raças com pelo menos 5 animais
breed_stats['adoption_rate'] = breed_stats['adopted_pets'] / breed_stats['total_pets']
filtered_breeds = breed_stats[breed_stats['total_pets'] >= 5]

# Ordenar por taxa de adoção
filtered_breeds = filtered_breeds.sort_values('adoption_rate', ascending=False)

# Configurar o Streamlit
st.title("Taxas de Adoção por Raça de Animal")
st.write("""
Esta análise mostra as taxas de adoção para diferentes raças de animais no centro de adoção.
Apenas raças com pelo menos 5 animais estão incluídas para maior precisão estatística.
""")

# Criar gráfico
plt.figure(figsize=(12, 8))
bars = plt.barh(
    filtered_breeds['breed'], 
    filtered_breeds['adoption_rate'],
    color='skyblue'
)

# Adicionar rótulos de dados
for bar in bars:
    width = bar.get_width()
    plt.text(
        width + 0.01, 
        bar.get_y() + bar.get_height()/2, 
        f'{width:.0%}',
        va='center'
    )

plt.xlabel('Taxa de Adoção')
plt.ylabel('Raça')
plt.title('Taxas de Adoção por Raça (com pelo menos 5 animais)')
plt.xlim(0, 1.1)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.gca().invert_yaxis()  # Mostrar maior taxa no topo

# Mostrar no Streamlit
st.pyplot(plt)

# Mostrar tabela com dados detalhados
st.subheader("Dados Detalhados")
st.dataframe(filtered_breeds.style.format({
    'adoption_rate': '{:.0%}',
    'total_pets': '{:.0f}',
    'adopted_pets': '{:.0f}'
}))

