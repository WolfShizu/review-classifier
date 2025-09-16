import json
import sys
import subprocess
sys.path.append("/tmp")

def install_library(library_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", library_name, "-t", "/tmp/"])

install_library("pyspellchecker")
install_library("Unidecode")
install_library("joblib")

import joblib
from utils import Utils
import config

def lambda_handler(event, context):
    utils = Utils()

    model = joblib.load(config.MODEL_PATH)
    vectorizer = joblib.load(config.VECTORIZER_PATH)

    body = json.loads(event["body"])
    review_text = body["review_text"]

    processed_review = utils.process_text(review_text)
    text_vector = vectorizer.transform([processed_review])

    predicted_score = model.predict(text_vector)[0]

    response = {
        "review_score": predicted_score
        }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }