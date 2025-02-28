# Weather Report - Análise Climática de Municípios Brasileiros

Este projeto visa a coleta, transformação, armazenamento e visualização de dados relacionados aos municípios brasileiros e seus respectivos indicadores climáticos. A partir da integração com as APIs do IBGE e OpenWeather, os dados são carregados no BigQuery e visualizados por meio de um dashboard interativo no Power BI.

## APIs Utilizadas

- **IBGE API**: Para obter os dados dos municípios brasileiros.
- **OpenWeather API**: Para coletar os indicadores de temperatura.

## Etapas do Projeto

### 1. Extração de Dados
Os dados do IBGE foram consumidos por meio de sua API, criando uma lista com todos os municípios do Brasil.

### 2. Transformação
Os dados JSON obtidos foram transformados em um DataFrame, onde selecionamos apenas os campos necessários para o processo de análise.

### 3. Carga no BigQuery
A tabela de municípios foi carregada no BigQuery, criando uma tabela de dimensão com as informações essenciais.

### 4. Coleta de Indicadores Climáticos
A API do OpenWeather foi utilizada para consultar os dados de temperatura para cada município. Um looping foi implementado para percorrer a lista de municípios e realizar múltiplas requisições simultâneas.

### 5. Armazenamento dos Dados
Os dados climáticos foram armazenados em uma tabela fato no BigQuery.

### 6. Visualização no Power BI
Um painel interativo foi desenvolvido no Power BI para permitir uma análise visual e intuitiva dos dados.

## Destaques e Aprendizados

1. **Modelagem Simples e Eficiente**: A escolha de uma modelagem de dados simples garantiu um processo de análise ágil e eficiente.
2. **Uso do módulo `concurrent.futures`**: A implementação do módulo `concurrent.futures` melhorou significativamente a performance das requisições simultâneas para a coleta dos dados climáticos.

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/leonardo-antunes-fonseca/weather-report.git
