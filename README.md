# Projeto-de-Insights
Projeto de Insights - Problema de negócio House Rocket
## Introdução

A empresa House Rocket visa seu lucro a partir das melhores aquisições. Ao longo do tempo a base de dados dos imóveis disponíveis para a venda da empresa vem crescendo e a análise acaba levando mais tempo. Com base nisso, esse projeto visa facilitar a tomada de decisão da empresa. Utilizando a base de imóveis formada pela empresa, buscou-se preparar os dados e apresentá-los de uma forma que facilite a consulta. Somado a isso, um modelo de recomendação de compra foi gerado e como resultado também é apresentado o potencial de lucro.

## Produto Final

Apresentar:

* Insights;

* Dashboard para análise livre do usuário;

* Recomendações para maximizar o lucro da empresa.

## Dados

A base de dados referente a imóveis disponíveis em King County, Seattle, entre 2014 e 2015. Informações vindas do Kaggle (https://www.kaggle.com/datasets/harlfoxem/housesalesprediction):

| Coluna        | Descrição                                                             |
|---------------|-----------------------------------------------------------------------|
| id            | Identificação do imóvel a cada venda                                  |
| date          | Data da venda                                                         |
| price         | Preço do imóvel                                                       |
| bedrooms      | Quantidade de quartos                                                 |
| bathrooms     | Quantidade de banheiros (0,5 corresponde a um banheiro sem chuveiro ) |
| sqft_living   | Área interna do imóvel                                                |
| sqft_lot      | Área do lote/terreno                                                  |
| floors        | Quantidade de andares                                                 |
| waterfront    | Indicador de vista para o lago da cidade                              |
| view          | Indicador de 0 a 4 avaliando a vista do imóvel                        |
| condition     | Indicador de 0 a 5 avaliando o estado do imóvel                       |
| grade         | Indicador de 1 a 13 avaliando o design e construção do imóvel         |
| sqft_above    | Área acima do nível do solo                                           |
| sqft_basement | Área abaixo do nível do solo                                          |
| yr_built      | Ano de construção do imóvel                                           |
| yr_renovated  | Ano da última reforma do imóvel                                       |
| zipcode       | Equivalente ao CEP                                                    |
| lat           | Latitude                                                              |
| long          | Longitude                                                             |

## Premissas

* 1 - A empresa somente aplica mantêm aplicações em aberto de até 100 milhões de dolares.

* 2 - A empresa somente irá aplicar dinheiro em imóveis em bom estato para que não necessite aplicar mais dinheiro em reformas.

* 3 - Imóveis sem informação de data de renovação vai ser considerado sem reforma

## Ferramentas

* Python 3.10

* Google Colab

* PyCharm

* Streamlit

* Heroku

* Geopandas


## Solução

A solução busca análisar todo o dataframe de atributos dos imóveis e a partir dele extrair insights para failita a escolha das melhores opções.

Para a compra, imóveis com o valor abaixo da média de preços por regiões e com uma condição acima da média foi recomendado. Na aba de insights outras informações levadas em conta podem ser conferidas.

Já para a venda os imóveis que maximizam o lucro, visando a premissa do negócio que é ter 100 milhões de dolares investidos em aberto somente, foram selecionados. Dessa forma 164 imóveis com potencial de lucro em torno de 30% foi o resultado e para apresenta isso, dois mapas contemplam o resultado com maiores informações sobre a média da região e os dados de atributos dos imóveis, assim como data que o imóveis foi disponibilizado para a negociações.


## Insights

* Hipótese 1: Imóveis com vista para água são em média 30% mais caros.

* Hipótese 2: Imóveis com data de construção menor que 1955 são em média 50% mais baratos.

* Hipótese 3: Imóveis sem porão possuem área total maior, sendo em média 40% maior.

* Hipótese 4: Crescimento do preço dos imóveis YoY é de 10% na média.

* Hipótese 5: Imóveis com renovação após 2010 são em média 40% mais caros que os renovadas antes.

* Hipótese 6: Casas com menos de 2 quartos são mais baratas.

* Hipótese 7: Casas não renovadas são em média 30% mais baratas que as renovadas.

* Hipótese 8: O preço no inverno é 20% mais barato que no verão.

## Resultados

Com os 164 imóveis selecionados a empresa conseguirá investir menos de 100 milhóes de dolares e ter um potencial de lucro de cerca de 27 milhões de dolares.

## Conclusão e Próximos Passos

Com o aplicativo gerado o time da House Rocket facilmente análisa seus dados com uma visualização e não somente a partir de tabelas. Para facilitar a tomada de decisão ainda podem seguir as recomendações que o modelo preve.

Em casos de menor investimento previsto e foco em certas regiões de compra o aplicativo também facilita fazer os filtros desejados para direcionar as escolhas. 

A partir deste trabalho feito ainda fica a opções de criação de um modelo de ML em Regressão para melhorar o modelo de recomendação a partir dos atributos que melhor representam os potenciais de lucros.

## Aplicativo

* https://analytics-rocket-app.herokuapp.com/
