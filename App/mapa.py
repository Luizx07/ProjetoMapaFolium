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

# mapa com filtro por região
mapa_regioes = folium.Map(
    location=[-15.2738, -55.4459],
    zoom_start=5
)

# aqui faremos uma camada para cada região
for regiao in df["regiao"].unique():

    # usamos o FeatureGroup para conseguir criar um grupo de marcadores
    grupo_regiao = folium.FeatureGroup(name=regiao)

    # filtramos as capitais daquela região
    dados_regiao = df[df["regiao"] == regiao]

    # colocamos as capitais de suas respectivas regiões no grupo indicado a elas
    for linha in dados_regiao.itertuples():

        texto_popup = f"""
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
            popup=folium.Popup(texto_popup, max_width=300),
            tooltip=linha.capital
        ).add_to(grupo_regiao)

    # adicionamos o grupo no mapa
    grupo_regiao.add_to(mapa_regioes)

# aqui temos o controle para mostrar ou nao determinada região no mapa
folium.LayerControl(collapsed=False).add_to(mapa_regioes)

mapa_regioes.save("mapa_capitais_brasil_regioes.html")

mapa_regioes

# docker run --rm -v "${PWD}\App:/app" pc-python (para rodar o mapa no docker)