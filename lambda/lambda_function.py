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
    review_title = body.get("review_title", "")
    review_text = body.get("review_text", None)
    
    if review_text == None:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "The field 'review_text' is required."
            })
        }

    review_full_text = review_title + " " + review_text

    processed_review = utils.process_text(review_full_text)
    text_vector = vectorizer.transform([processed_review])

    predicted_score = model.predict(text_vector)[0]

    warnings = []

    allow_neutral = utils.get_valid_bool(body, "allow_neutral", False, warnings)
    show_score = utils.get_valid_bool(body, "show_score", True, warnings)
    show_full_score = utils.get_valid_bool(body, "show_full_score", False, warnings)

    classification = ""

    if allow_neutral:
        if predicted_score < 0.4:
            classification = "negative"
        elif predicted_score < 0.6:
            classification = "neutral"
        else:
            classification = "positive"
    else:
        classification = "negative" if predicted_score < 0.5 else "positive"

    response = {"classification": classification}
    
    if show_score:
        if show_full_score:
            response["score"] = predicted_score
        else:
            response["score"] = float(f"{predicted_score:.2f}")

    if warnings:
        response["warnings"] = warnings

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }