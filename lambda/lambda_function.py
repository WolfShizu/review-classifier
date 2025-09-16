import json
import sys
import os
import zipfile
import boto3

def import_libraries():
    s3 = boto3.client("s3")
    bucket_name = os.environ["BUCKET_NAME"]
    library_key = os.environ["LIBRARY_KEY"]
    local_path = "/tmp/library.zip"
    extract_path = "/tmp/libraries"

    s3.download_file(bucket_name, library_key, local_path)

    with zipfile.ZipFile(local_path, "r") as zip_file:
        zip_file.extractall(extract_path)

    sys.path.append(extract_path)

import_libraries()

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