import streamlit as st
import altair as alt
import pandas as pd

# Load the generated JSON chart
chart_data = 'adoption_rates_by_breed.json'

st.title("Pet Adoption Center Dashboard")

st.header("Adoption Rates Across Different Breeds")

# Display the chart
st.altair_chart(alt.Chart.from_json(chart_data), use_container_width=True)

st.write("This chart displays the adoption success rate for each breed at the pet adoption center.")
