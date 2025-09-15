import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge
from sklearn.feature_extraction.text import TfidfVectorizer

import config

data_frame = pd.read_csv(config.CLEAN_REVIEWS_PATH)

vectorizer = TfidfVectorizer(
    ngram_range= (1, 2),
    max_features= 5000,
    min_df= 5
)

text_vectors = vectorizer.fit_transform(data_frame["full_text"])
review_scores = data_frame["review_score"]

text_vectors_train, text_vectors_test, review_scores_train, review_scores_test = train_test_split(
    text_vectors, review_scores,
    test_size= 0.2,
    random_state= 14
)

model = Ridge(alpha= 1.0)
model.fit(text_vectors_train, review_scores_train)
print("Modelo treinado")

# Teste do modelo
review_score_predicted = model.predict(text_vectors_test)
print(f"MSE: {mean_squared_error(review_scores_test, review_score_predicted)}")
print(f"R²: {r2_score(review_scores_test, review_score_predicted)}")

# Salva o modelo e o vetorizador localmente
joblib.dump(model, config.MODEL_PATH)
joblib.dump(vectorizer, config.VECTORIZER_PATH)