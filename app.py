import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el dataset desde un archivo local
data = pd.read_csv("vehicles.csv")

# Normalizar los nombres de las columnas a minúsculas
data.columns = data.columns.str.lower()

# Título del Dashboard
st.title("Análisis de Economía de Combustible de Vehículos (EPA 1984–2017)")

# Descripción del dataset
st.write("Este conjunto de datos contiene información sobre vehículos, incluyendo consumo de combustible, emisiones de CO₂ y más.")

# Filtros interactivos en la barra lateral
st.sidebar.header("Filtros de Datos")

# Filtro por fabricante (make)
make = st.sidebar.selectbox('Selecciona un fabricante', data['make'].dropna().unique())

# Filtro por año de fabricación
year = st.sidebar.slider('Selecciona el año de fabricación', int(data['year'].min()), int(data['year'].max()), int(data['year'].mean()))

# Filtrar los datos según las selecciones
filtered_data = data[(data['make'] == make) & (data['year'] == year)]

# Mostrar los datos filtrados
st.write(f"Mostrando vehículos de la marca: {make} del año: {year}")
st.write(filtered_data)

# Visualización de la relación entre peso y consumo de combustible en ciudad
if not filtered_data.empty:
    if 'curb-weight' in data.columns and 'city-mpg' in data.columns:
        fig = px.scatter(filtered_data, x="curb-weight", y="city-mpg", color="make", title="Relación entre peso del vehículo y consumo de combustible en ciudad")
        st.plotly_chart(fig)

    # Visualización de emisiones promedio de CO₂ por fabricante
    if 'co2-emissions' in data.columns:
        emissions_by_make = filtered_data.groupby("make")["co2-emissions"].mean().reset_index()
        fig2 = px.bar(emissions_by_make, x="make", y="co2-emissions", title="Emisiones promedio de CO₂ por fabricante")
        st.plotly_chart(fig2)

    # Filtro adicional por eficiencia de combustible en ciudad
    if 'city-mpg' in filtered_data.columns:
        mpg_filter = st.sidebar.slider("Filtrar por 'city-mpg' (millas por galón en ciudad)", 
                                       int(filtered_data['city-mpg'].min()), 
                                       int(filtered_data['city-mpg'].max()), 
                                       int(filtered_data['city-mpg'].mean()))
        filtered_data_mpg = filtered_data[filtered_data['city-mpg'] >= mpg_filter]

        # Mostrar los nuevos datos filtrados
        st.write(f"Mostrando vehículos con más de {mpg_filter} millas por galón en ciudad.")
        fig3 = px.scatter(filtered_data_mpg, x="curb-weight", y="city-mpg", color="make", title="Vehículos filtrados por eficiencia de combustible")
        st.plotly_chart(fig3)
else:
    st.write("No se encontraron vehículos que coincidan con los filtros seleccionados.")
