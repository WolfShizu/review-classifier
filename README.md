# Classificador de Reviews
Uma API que usa Machine Learning para classificar avaliações como positivas ou negativas.
Este repositório inclui o dataset de treinamento, o código de pré-processamento desses dados e do treinamento do modelo. 

# Tecnologias Utilizadas
- Python
- Bibliotecas: pandas, pyspellchecker, Unidecode, joblib e sklearn
- Serviços AWS: API Gateway e Lambda
- Modelo de Machine Learning: Ridge Regression

# Utilização da API
A API pode ser acessada fazendo uma requisição POST para ``https://u5rqox1dik.execute-api.us-east-2.amazonaws.com/classify-review``.
A requisição deve seguir o seguinte padrão:
```json
{
    "review_title": "Título da avaliação.",
    "review_text": "Texto da avaliação.",
    "show_score": true, 
    "show_full_score": false, 
    "allow_neutral": false
}
```
- Os campos ``"review_title"``, ``"show_score"``, ``"show_full_score"`` e ``"allow_neutral"``  são opcionais.
- Valores padrão estão demonstrados no exemplo acima.
- ``"show_score"``: Exibe o score.
- ``"show_full_score"``: Exibe o score total, sem arredondar casas decimais.
- ``"allow_neutral"``: Permite avaliações do tipo neutro.

### Exemplo de Requisição e Resposta
- Requisição:
```json
{
    "review_title": "Ótimo custo benefício!",
    "review_text": "Excelente fone! Tinha lido as avaliações positivas que me motivaram a comprar e supriu as expectativas. A bateria dura bastante, isola bem o som e a qualidade do áudio é muito boa. A marca não costuma decepcionar.",
    "show_score": true, 
    "show_full_score": true, 
    "allow_neutral": false
}
```
- Resposta:
```json
{
    "classification": "positive",
    "score": 0.9499954767527364
}
```
# Estrutura do Projeto
```
📦review-classifier
 ┣ 📂data
 ┃ ┣ 📂processed
 ┃ ┃ ┗ 📜clean_reviews.csv # Dados pré-processados
 ┃ ┗ 📂raw
 ┃ ┃ ┗ 📜RePro.csv # Dataset de avaliações
 ┣ 📂lambda # Código do AWS Lambda
 ┃ ┣ 📜config.py
 ┃ ┣ 📜lambda_function.py
 ┃ ┗ 📜utils.py
 ┣ 📂models # Modelo, vetorizador e lista de stopwords usados no lambda
 ┃ ┣ 📜.gitkeep # Mantém a pasta no github
 ┃ ┣ 📜model.pkl
 ┃ ┣ 📜stopwords.pkl
 ┃ ┗ 📜vectorizer.pkl
 ┣ 📂training
 ┃ ┣ 📜config.py
 ┃ ┣ 📜pre_process.py # Código para pré-processamento dos dados
 ┃ ┣ 📜train_model.py # Código para treinar o modelo usando os dados pré-processados
 ┃ ┗ 📜utils.py
 ┣ 📜.gitignore
 ┗ 📜README.md
 ```

# Pré-processamento
O dataset usado para o treinamento pode ser encontrado [neste repositório](https://github.com/lucasnil/repro).
O pré-processamento dos dados é realizado pelo código ``training/pre_process.py``.
Suas etapas são:
- **Remapeação das classificações das reviews:** Altera os rótulos ``POSITIVO`` e ``"NEGATIVO"`` para ``0`` e ``1``.
-  **Remoção de dados inválidos:** Remove os dados com a tag ``INADEQUADA``, com base na coluna ``topics``.
- **Limpeza de texto:** Deixa os dados em minúsculo e remove pontuação, acentos e números.
- **Remoção de stopwords:** Remove palavras irrelevantes para a classificação.
- **Correção ortográfica:** Corrige as palavras usando a biblioteca ``pyspellchecker``.
- **Exportação do dataset processado:** Armazena os dados processados em ``data/processed/clean_reviews.csv``
- **Exportação das stopwords:** As stopwords são armazenadas em ``models/`` para uso no Lambda.

# Treinamento do Modelo
O **Ridge Regression** é utilizado no projeto por sua simplicidade e eficiência, e mostrou bom desempenho na classificação das reviews.
O modelo é treinado em ``training/train_model.py``.
Suas etapas são:
- **Vetorização:** Os dados pré-processados são vetorizados usando o método TF-IDF.
- **Treinamento:** O modelo é treinado usando 80% dos dados vetorizados. Após o treinamento, são utilizados os 20% restantes dos dados para aferir a eficiência do modelo.
    Os resultados são:
    ```
    MSE: 0.049805436686350325
    R²: 0.7300673262541211
    ```
    - ``Mean Squared Error``: Mede o **erro médio quadrático** entre os valores previstos pelo modelo e os valores reais. O valor ``0.049`` Indica que que o modelo faz previsões bastante próximas aos valores reais.
    - ``R²-Score``: Mede a **proporção de variância dos dados** que o modelo consegue explicar. O valor ``0.73`` indica que ele consegue explicar 73% da variação dos dados.
- **Exportação do modelo e vetorizador:** O modelo e o vetorizador são armazenados em ``models/``, para uso no Lambda.

# API (Lambda + API Gateway)
