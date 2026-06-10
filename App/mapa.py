import pandas as pd
import folium
import requests

df = pd.read_csv("capitais_brasil_ibge.csv")

# API do IBGE
url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
resposta = requests.get(url)
dados_api = resposta.json()

# API em DataFrame
lista_api = []

for item in dados_api:
    lista_api.append({
        "uf": item["sigla"],
        "codigo_ibge_estado": item["id"],
        "regiao_api": item["regiao"]["nome"]
    })

df_api = pd.DataFrame(lista_api)

# CSV + API
df = df.merge(df_api, on="uf", how="left")

mapa = folium.Map(
    location=[-14.2350, -51.9253],
    zoom_start=4
)

for linha in df.itertuples():

    texto = f"""
    <b>{linha.capital}</b><br>
    Estado: {linha.estado}<br>
    UF: {linha.uf}<br>
    Região: {linha.regiao}<br>
    Código IBGE do Estado: {linha.codigo_ibge_estado}<br>
    Região pela API: {linha.regiao_api}<br>
    Latitude: {linha.latitude}<br>
    Longitude: {linha.longitude}
    """

    folium.Marker(
        location=[linha.latitude, linha.longitude],
        popup=folium.Popup(texto, max_width=300),
        tooltip=linha.capital
    ).add_to(mapa)

mapa.save("mapa_capitais_brasil.html")

mapa
