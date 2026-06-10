import pandas as pd
import folium
import requests

def ler_csv():
    return pd.read_csv("capitais_brasil_ibge.csv")

def consultar_api():
    resposta = requests.get("https://servicodados.ibge.gov.br/api/v1/localidades/estados")
    return resposta.json()

def json_para_dataframe(dados_api):
    lista = [{"uf": i["sigla"],
               "codigo_ibge_estado": i["id"], 
               "regiao_api": i["regiao"]["nome"]}
                 for i in dados_api]
    return pd.DataFrame(lista)

def merge_dados(df, df_api):
    return df.merge(df_api, on="uf", how="left")

def criar_mapa(df):
    mapa = folium.Map(
        location=[-15.2738, -55.4459],
          zoom_start=5
          )
    for regiao in df["regiao"].unique():
        grupo = folium.FeatureGroup(name=regiao)
        for linha in df[df["regiao"] == regiao].itertuples():

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
                [linha.latitude, linha.longitude],
                popup=folium.Popup(texto, max_width=300),
                tooltip=linha.capital).add_to(grupo)
        grupo.add_to(mapa)

    folium.LayerControl(collapsed=False).add_to(mapa)

    return mapa

def salvar_mapa(mapa):
    mapa.save("mapa_capitais_brasil_pipeline.html")

# Pipeline
df        = ler_csv()
dados_api = consultar_api()
df_api    = json_para_dataframe(dados_api)
df        = merge_dados(df, df_api)
mapa      = criar_mapa(df)
salvar_mapa(mapa)