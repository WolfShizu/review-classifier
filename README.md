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

