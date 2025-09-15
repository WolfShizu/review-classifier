import json
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
