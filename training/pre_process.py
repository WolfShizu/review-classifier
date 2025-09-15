import ast
import joblib

import pandas

import config
from utils import Utils

utils = Utils()

data_frame = pandas.read_csv(
    config.RAW_DATA_PATH,
    usecols= ["review_title", "review_text", "polarity", "topics"]
    )

# Transforma as strings em listas
data_frame["review_score"] = data_frame["polarity"].apply(ast.literal_eval)
data_frame["topics"] = data_frame["topics"].apply(ast.literal_eval)

data_frame["full_text"] = data_frame["review_title"].astype(str) + " " + data_frame["review_text"].astype(str)

# Mapeia as reviews em score (0.0, 0.5 e 1.0)
data_frame["review_score"] = data_frame["review_score"].apply(utils.map_reviews)
print("Reviews mapeadas")

data_frame = data_frame[data_frame["topics"].apply(utils.remove_invalid_data)]
print(f"{utils.invalid_data_count} dados invalidos removidos")

# Remove colunas desnecessárias 
data_frame = data_frame.drop(columns= ["review_title", "review_text", "polarity", "topics"])

data_frame["full_text"] = data_frame["full_text"].apply(utils.clear_text)
print("Textos limpados")

print("Iniciando correção de palavras")
data_frame = utils.correct_df_text(data_frame)
print("\nCorreção de palavras concluída")

data_frame["full_text"] = data_frame["full_text"].apply(utils.remove_accent)
print("Acentos removidos")

# Salva os dados limpos
data_frame.to_csv(config.CLEAN_REVIEWS_PATH, index= False)
print("Dados limpos salvos")

joblib.dump(utils.pt_stopwords, config.STOPWORDS_PATH)
print("Stopwords salvas")