import pandas as pd
import folium

# Lendo o arquivo CSV
df = pd.read_csv("capitais_brasil_ibge.csv")

# Criando o mapa do Brasil
mapa = folium.Map(
    location=[-14.2350, -51.9253],
    zoom_start=4
)

# Colocando as capitais no mapa
for linha in df.itertuples():

    texto = f"""
    <b>{linha.capital}</b><br>
    Estado: {linha.estado}<br>
    UF: {linha.uf}<br>
    Região: {linha.regiao}<br>
    Latitude: {linha.latitude}<br>
    Longitude: {linha.longitude}
    """

    folium.Marker(
        location=[linha.latitude, linha.longitude],
        popup=texto,
        tooltip=linha.capital
    ).add_to(mapa)

# Salvando o mapa
mapa.save("mapa_capitais_brasil.html")

# Mostrar o mapa
mapa