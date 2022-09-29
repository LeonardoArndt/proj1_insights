####################################
#biblioteas
import streamlit as st
import pandas as pd
import geopandas
import folium
import numpy as np
from datetime import datetime, time
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from streamlit_option_menu import option_menu
import plotly.express as px
####################################
st.set_page_config( layout='wide' )
st.title('House Rocket Company')

####################################
#Functions
@st.cache( allow_output_mutation=True )
def get_data(path):
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    geofile = geopandas.read_file( url )
    return geofile
####################################


####################################
#Extract
# Sidebar
with st.sidebar:
    selected = option_menu("Menu", ['Introduction', 'Insights', 'Analytics', 'Conclusion'], icons=['house','lightbulb', 'list-task', 'bookmark-check'], menu_icon="cast", default_index=0)

####################################
#Transformation
def price_m(df):
    df['price_m2'] = df['price'] / df['sqft_lot']
    return df
####################################


####################################
#Load
#filters

def Introduction(df):
    if selected == 'Introduction':
        st.header('Bem vindo ao banco de análise de compra e venda de imóveis desta compania')
        st.write("A empresa House Rocket visa seu lucro a partir das melhores aquisições. Ao longo do tempo a base de dados dos imóveis disponíveis para a venda da empresa vem crescendo e a análise acaba levando mais tempo. Com base nisso, esse projeto visa facilitar a tomada de decisão da empresa. Utilizando a base de imóveis formada pela empresa, buscou-se preparar os dados e apresentá-los de uma forma que facilite a consulta. Somado a isso, um modelo de recomendação de compra foi gerado e como resultado também é apresentado o potencial de lucro.")
        st.title("> Premissas")
        st.write("1 - A empresa somente aplica mantêm aplicações em aberto de até 100 milhões de dolares.")
        st.write("2 - A empresa somente irá aplicar dinheiro em imóveis em bom estato para que não necessite aplicar mais dinheiro em reformas.")
        st.write("3 - Imóveis sem informação de data de renovação vai ser considerado sem reforma")
        st.title("> Planejamento da solução")
        st.write("1 - Analisar as métricas")
        st.write("2 - Manipular e organizar os dados para gerar visualizações para facilitar a tomada de decisão do time House Rocket.")
        st.write("3 - Gerar Insights para melhor planejar as recomendações de compra.")
        st.write("4 - Montar uma visualização das recomendações de compras e vendas, juntamente com o lucro potencial das negociações.")
        st.write(" >> Para isso:")
        st.write(" > - Um mapa com a média por região do imóveis sugeridos é apresentado. Mapas baseados em bibliotecas folium e dados vindos da biblioteda geopandas")
        st.write(" > - Um mapa com informações de cada imóvel e sua localização é apresentado. Mapas baseados em bibliotecas folium e dados vindos da biblioteda geopandas")


        f_zipcode = st.sidebar.multiselect('Selecione Zipcode', df['zipcode'].unique())
        #criando condições para meu filtro acima funcionar
        st.title( 'Visão geral dos dados' )
        if ( f_zipcode != [] ):
            df = df.loc[df['zipcode'].isin( f_zipcode ), :]
        else:
            df = df.copy()
        st.write( df.head() )
        #criando bloco duplo de paineis no app (avg metrics e statistic descriptive)
        c1, c2 = st.columns((1, 1) )
        # Average metrics
        df1 = df[['id', 'zipcode']].groupby( 'zipcode' ).count().reset_index()
        df2 = df[['price', 'zipcode']].groupby( 'zipcode').mean().reset_index()
        df3 = df[['sqft_living', 'zipcode']].groupby( 'zipcode').mean().reset_index()
        df4 = df[['price_m2', 'zipcode']].groupby( 'zipcode').mean().reset_index()
        m1 = pd.merge( df1, df2, on='zipcode', how='inner' )
        m2 = pd.merge( m1, df3, on='zipcode', how='inner' )
        df5 =pd.merge( m2, df4, on='zipcode', how='inner' )
        df5.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICE', 'SQRT LIVING', 'PRICe/M2']
        c1.header( 'Valores médios' )
        c1.dataframe( df5, height=600, width= 800 )
        # Statistic Descriptive
        num_attributes = df.select_dtypes( include=['int64', 'float64'] )
        media = pd.DataFrame( num_attributes.apply( np.mean ) )
        mediana = pd.DataFrame( num_attributes.apply( np.median ) )
        std = pd.DataFrame( num_attributes.apply( np.std ) )
        max_ = pd.DataFrame( num_attributes.apply( np.max ) )
        min_ = pd.DataFrame( num_attributes.apply( np.min ) )
        df1 = pd.concat([max_, min_, media, mediana, std], axis=1 ).reset_index()
        df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']
        c2.header( 'Descrição analítica' )
        c2.dataframe( df1, height=600, width= 800)

        #criando meu mapa
        price_slider = st.slider('Price Range', int(df['price'].min()), int(df['price'].max()), int(df['price'].mean()))
        st.write('Se quiser analisar os dados no mapa de Seattle clique na checkbox abaixo:')
        is_check = st.checkbox('Display map')
        if is_check:
            #select row
            house = df[df['price'] < price_slider][['id', 'lat', 'long', 'price']]
            fig = px.scatter_mapbox(house,
                                 lat='lat',
                                 lon='long',
                                 size='price',
                                 size_max=15,
                                 zoom=10)
            fig.update_layout(mapbox_style='open-street-map')
            fig.update_layout(height=400,width=1500 ,margin={'r':0, 'b':0, 'l':0, 't':0});
            st.plotly_chart(fig)
            return None

def Insights(df):
    if selected == 'Insights':
        #H1 e 2
        c1, c2 = st.columns((1, 1))
        #H1
        c1.title('Hipótese 1: Imóveis com vista para água são em média 30% mais caros.')
        c1.header('Verdadeiro')
        df1 = df[['price', 'waterfront']].groupby('waterfront').mean().reset_index()
        df1['waterfront'] = df1['waterfront'].apply(lambda x: str('yes') if x == 1 else str('no'))
        df1.columns = ['Is_waterfront?', 'Price']
        fig = px.bar(df1, x='Is_waterfront?', y='Price', color='Is_waterfront?')
        c1.plotly_chart(fig, use_container_width=True)
        #H2
        c2.title('Hipótese 2: Imóveis com data de construção menor que 1955 são em média 50% mais baratos.')
        c2.header('Falso')
        df2 = pd.DataFrame({"BuiltBefor_1955": ['yes', 'no'], "Price": [df[df['yr_built'] < 1955]['price'].mean(), df[df['yr_built'] > 1955]['price'].mean()]})
        fig2 = px.bar( df2, x='BuiltBefor_1955', y='Price', color='BuiltBefor_1955' )
        c2.plotly_chart(fig2, use_container_width=True)
        #H3 e 4
        c3, c4 = st.columns((1, 1))
        #H3
        c3.title('Hipótese 3: Imóveis sem porão possuem área total maior, sendo em média 40% maior.')
        c3.header('Falso')
        df3 = pd.DataFrame({"Basement": ['yes', 'no'], "Lot_area": [df[df['sqft_basement'] > 0]['sqft_lot'].mean(), df[df['sqft_basement'] == 0]['sqft_lot'].mean()]})
        fig3 = px.bar( df3, x='Basement', y='Lot_area', color='Basement' )
        c3.plotly_chart(fig3, use_container_width=True)
        #H4
        c4.title('Hipótese 4: Crescimento do preço dos imóveis YoY é de 10% na média.')
        c4.header('Falso')
        df_t = df.copy()
        df_t['yr_built'] = df_t['yr_built'].astype(int)
        df4 = df_t[(df_t['yr_built'] == 1950) | (df_t['yr_built'] == 1960) | (df_t['yr_built'] == 1970) | (df_t['yr_built'] == 1980) | (df_t['yr_built'] == 1990) | (df_t['yr_built'] == 2000) | (df_t['yr_built'] == 2010)]
        df4 = df4[['yr_built', 'price']].groupby('yr_built').mean().sort_values('yr_built', ascending=True).reset_index()
        valor = 0
        for i, row in df4.iterrows():
            df4.loc[i, 'percentage'] = str(((row['price'] / valor) - 1) * 100) + '%'
            valor = row['price']
            i += 1
        df4.columns = ['Year_Built', 'Price', 'Percentage']
        fig4 = px.line( df4, x= 'Year_Built', y='Price')
        c4.plotly_chart(fig4, use_container_width=True)
        #H5 e 6
        c5, c6 = st.columns((1, 1))
        c5.title('Hipótese 5: Imóveis com renovação após 2010 são em média 40% mais caros que os renovadas antes.')
        c5.header('Falso')
        #H5
        df5 = pd.DataFrame({"Renovated_Year": ['>2010', '<2010'], "Price": [df[df['yr_renovated']>2010]['price'].mean(), df[df['yr_renovated']<2010]['price'].mean()]})
        fig5 = px.bar( df5, x='Renovated_Year', y='Price', color='Renovated_Year' )
        c5.plotly_chart(fig5, use_container_width=True)
        #H6
        c6.title('Hipótese 6: Casas com menos de 2 quartos são mais baratas.')
        c6.header('Verdadeiro')
        df6 = pd.DataFrame({"Bedrooms": ['>2', '<=2'], "Price": [df[df['bedrooms']< 2]['price'].mean(), df[df['bedrooms']>= 2]['price'].mean()]})
        fig6 = px.bar( df6, x='Bedrooms', y='Price', color='Bedrooms' )
        c6.plotly_chart(fig6, use_container_width=True)
        #H7 e 8
        c7, c8 = st.columns((1, 1))
        #H7
        c7.title('Hipótese 7: Casas não renovadas são em média 30% mais baratas que as renovadas.')
        c7.header('Verdadeiro')
        df7 = pd.DataFrame({"IsRenovated?": ['Yes', 'No'], "Price": [df[df['yr_renovated']>0]['price'].mean(), df[df['yr_renovated']==0]['price'].mean()]})
        fig7 = px.bar(df7, x='IsRenovated?', y='Price', color='IsRenovated?')
        c7.plotly_chart(fig7, use_container_width=True)
        #H8
        c8.title('Hipótese 8: O preço no inverno é 20% mais barato que no verão.')
        c8.header('Falso')
        df_tt = df.copy()
        df_tt['date'] = pd.to_datetime(df_tt['date']).dt.strftime('%m')
        df_tt['date'] = df_tt['date'].astype(int)
        df_tt['Season'] = df_tt['date'].apply(lambda x: 'summer' if (x >= 6) & (x <= 8) else 'fall' if (x >= 9) & (x <= 11) else 'winter' if (x == 12) or (x <= 2) else 'spring')
        df8 = df_tt[['Season', 'price']].groupby('Season').mean().reset_index()
        df8.columns = ['Season' , 'Price']
        fig8 = px.bar( df8, x='Season', y='Price', color='Season' )
        c8.plotly_chart(fig8, use_container_width=True)

def Analytics(df):
    if selected == 'Analytics':
        #dados comerciais
        st.sidebar.title( 'Opções comerciais' )
        st.title( 'Atributos comerciais' )
        # ---------- Average Price per year built
        # setup filters
        min_year_built = int( df['yr_built'].min() )
        max_year_built = int( df['yr_built'].max() )
        st.sidebar.subheader( 'Selecione o ano máximo de construção' )
        f_year_built = st.sidebar.slider( 'Year Built', min_year_built, max_year_built, min_year_built )
        st.header( 'Média de preço por ano de construção' )
        # get data
        df['date'] = pd.to_datetime( df['date'] ).dt.strftime( '%Y-%m-%d' )
        df1 = df.loc[df['yr_built'] < f_year_built]
        df1 = df1[['yr_built', 'price']].groupby( 'yr_built' ).mean().reset_index()
        fig = px.line( df1, x='yr_built', y='price' )
        st.plotly_chart( fig, use_container_width=True )
        # ---------- Average Price per day
        st.header( 'Média de preço por dia' )
        st.sidebar.subheader( 'Selecione a data máxima' )
        # setup filters
        min_date = datetime.strptime( df['date'].min(), '%Y-%m-%d' )
        max_date = datetime.strptime( df['date'].max(), '%Y-%m-%d' )
        f_date = st.sidebar.slider( 'Date', min_date, max_date, min_date )
        # get data
        df['date'] = pd.to_datetime( df['date'] )
        df1 = df[df['date'] < f_date]
        df1 = df1[['date', 'price']].groupby( 'date' ).mean().reset_index()
        fig = px.line( df1, x='date', y='price' )
        st.plotly_chart( fig, use_container_width=True )
        # ---------- Histogram -----------
        st.header( 'Distribuição de preço' )
        st.sidebar.subheader( 'Selecione preço máximo' )
        # filters
        min_price = int( df['price'].min() )
        max_price = int( df['price'].max() )
        avg_price = int( df['price'].mean() )
        f_price = st.sidebar.slider( 'Price', min_price, max_price, avg_price )
        df1 = df[df['price'] < f_price]
        fig = px.histogram( df1, x='price', nbins=50 )
        st.plotly_chart( fig, use_container_width=True )

        #dados físicos dos imóveis
        st.sidebar.title( 'Opções de atributos' )
        st.title( 'Atributos dos imóveis' )
        # filters
        f_bedrooms = st.sidebar.selectbox( 'Número máx de quartos', sorted( set( df['bedrooms'].unique() ) ) )
        f_bathrooms = st.sidebar.selectbox( 'Número máx de banheiros', sorted( set( df['bathrooms'].unique() ) ) )
        f_floors = st.sidebar.selectbox('Número máx de andares', sorted( set( df['floors'].unique() ) ) )
        f_waterview = st.sidebar.checkbox('Somente casas com vista para água' )
        #criando bloco duplo gráficos(casas por quartos e por banheiros)
        c1, c2 = st.columns( 2 )
        # Houses per bedrooms
        c1.header( 'Quartos' )
        df1 = df[df['bedrooms'] < f_bedrooms]
        fig = px.histogram( df1, x='bedrooms', nbins=19 )
        c1.plotly_chart( fig, use_containder_width=True )
        # Houses per bathrooms
        c2.header( 'Banheiros' )
        df1 = df[df['bathrooms'] < f_bathrooms]
        fig = px.histogram( df1, x='bathrooms', nbins=10 )
        c2.plotly_chart( fig, use_containder_width=True )
        #criando bloco duplo gráficos(casas andares e por vista pra água)
        c1, c2 = st.columns( 2 )
        # Houses per floors
        c1.header( 'Imóveis por andares' )
        df1 = df[df['floors'] < f_floors]
        fig = px.histogram( df1, x='floors', nbins=19)
        c1.plotly_chart( fig, use_containder_width=True )
        # Houses per water view
        if f_waterview:
            df1 = df[df['waterfront'] == 1]
        else:
            df1 = df.copy()
        fig = px.histogram( df1, x='waterfront', nbins=10 )
        c2.header( 'Imóveis com vista para água' )
        c2.plotly_chart( fig, use_containder_width=True )
        return None

def Conclusion(df, geofile):
    if selected == 'Conclusion':
        #criando bloco duplo de mapas (mapa básico e de densidade)
        st.title('Recomendações')
        c1, c2 = st.columns((1, 1))
        c1.header('Portfólio recomendado')
        # Base Map - Folium
        df_grouped = df[['zipcode', 'price']].groupby('zipcode').median().reset_index()
        df_grouped.columns = ['zipcode', 'price_median']
        df_compra = pd.merge(df, df_grouped, on='zipcode', how='inner')
        df_compra = df_compra[df_compra['condition'] > 3].copy()
        df_compra['status'] = df_compra[['price', 'price_median']].apply(lambda x: 'comprar' if x['price'] > x['price_median'] else 'ñ comprar', axis=1)
        df_compra = df_compra[['id', 'price', 'date', 'zipcode', 'price_median', 'condition', 'status']].copy()
        df_here = df.copy()
        df_here['date'] = pd.to_datetime(df_here['date']).dt.strftime('%m')
        df_here['date'] = df_here['date'].astype(int)
        df_here['Season'] = df_here['date'].apply(lambda x: 'summer' if (x >= 6) & (x <= 8) else 'fall' if (x >= 9) & (x <= 11) else 'winter' if (x == 12) or (x <= 2) else 'spring')
        df_grouped1 = df_here[['zipcode', 'price', 'Season']].groupby(['zipcode', 'Season']).median().reset_index()
        df_grouped1.columns = ['zipcode', 'Season', 'price_median']
        df_venda = pd.merge(df_compra, df_here, how='inner', on='id')
        df_venda = df_venda[df_venda['status'] == 'comprar'].reset_index()
        df_venda = df_venda.drop(['date_y', 'price_y', 'condition_y', 'zipcode_y'], axis=1)
        df_venda['zipcode_x'] = df_venda['zipcode_x'].astype(int)
        df_venda['selling_price'] = 0
        df_venda.columns = ['index', 'id', 'price', 'date', 'zipcode', 'price_median', 'condition', 'status', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'lat', 'long', 'sqft_living15', 'sqft_lot15', 'price_m2', 'Season', 'selling_price']
        for i in range(len(df_venda)):
            for ii in range(len(df_grouped1)):
                if df_venda.loc[i, 'Season'] == df_grouped1.loc[ii, 'Season']:
                    if df_venda.loc[i, 'zipcode'] == df_grouped1.loc[ii, 'zipcode']:
                        if df_venda.loc[i, 'price'] > df_grouped1.loc[ii, 'price_median']:
                            df_venda.loc[i, 'selling_price'] = df_venda.loc[i, 'price'] * 1.1
                        else:
                            df_venda.loc[i, 'selling_price'] = df_venda.loc[i, 'price'] * 1.3
        df_venda['lucro'] = df_venda[['price', 'selling_price']].apply(lambda x: (x['selling_price'] / x['price']), axis=1)
        df_v = df_venda[df_venda['lucro'] == 1.3]
        f_zipcode = st.sidebar.multiselect('Selecione Zipcode', df_v['zipcode'].unique())
        if ( f_zipcode != [] ):
            df_v = df_v.loc[df_v['zipcode'].isin( f_zipcode ), :]
            df_grouped1 = df_grouped1.loc[df_grouped1['zipcode'].isin(f_zipcode), :]
        else:
            df_v = df_v.copy()
            df_grouped1 = df_grouped1.copy()
        density_map = folium.Map(location=[df_here['lat'].mean(), df_here['long'].mean()], default_zoom_start=15)
        marker_cluster = MarkerCluster().add_to(density_map)
        for name, row in df_v.iterrows():
            folium.Marker([row['lat'], row['long']], popup='Sold R${0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format( row['price'], row['date'], row['sqft_living'], row['bedrooms'], row['bathrooms'], row['yr_built'])).add_to(marker_cluster)
        with c1:
            folium_static(density_map)
        # Region Price Map
        c2.header('Preço médio')
        dff = df_grouped1
        dff.columns = ['ZIP','SEASON', 'PRICE']
        geofile = geofile[geofile['ZIP'].isin(dff['ZIP'].tolist())]
        region_price_map = folium.Map(location=[df_here['lat'].mean(), df_here['long'].mean()], default_zoom_start=15)
        region_price_map.choropleth(data=dff,
                                    geo_data = geofile,
                                    columns=['ZIP', 'PRICE'],
                                    key_on='feature.properties.ZIP',
                                    fill_color='YlOrRd',
                                    fill_opacity=0.7,
                                    line_opacity=0.2,
                                    legend_name='AVG PRICE')
        with c2:
            folium_static(region_price_map)
        #conclusion sheet
        df_v['price'] = df_v['price'].astype(int)
        df_v['selling_price'] = df_v['selling_price'].astype(int)
        df_v['profit'] = df_v.apply(lambda x: x['selling_price'] - x['price'], axis=1)
        df_v1 = df_v[['id', 'price', 'zipcode', 'date', 'selling_price', 'profit']]
        c1, c2= st.columns(2)
        c1.title('Métricas do resultado')
        c1.header('De todos os imóveis, 164 unidades foram selecionadas com um potencial de lucro em torno de 30% na média. Manteve-se o investimento desejado pela empresa para aquisição de imóveis e a partir desse valor podemos máximizar o lucro, veja:')
        c1.metric(label="Price (US$)", value=df_v['price'].sum())
        c1.metric(label="Profit", value=df_v['profit'].sum())
        c2.title('Relatório')
        c2.header('Abaixo informações detalhadas das recomendações.')
        c2.dataframe(df_v1)
        return None
####################################

####################################
#ETL
if __name__ == '__main__':
    #Extract
    df_raw = get_data('kc_house_data.csv')
    df_geofile = get_geofile('https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')

    #Transform
    df_completo = price_m(df_raw)

    Introduction(df_completo)

    Insights(df_raw)

    Analytics(df_raw)

    Conclusion(df_raw, df_geofile)