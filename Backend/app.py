from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # type: ignore
import torch  # type: ignore

app = Flask(__name__)
CORS(app)

tokenizer = AutoTokenizer.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained(
    "cardiffnlp/twitter-roberta-base-sentiment-latest")

label_map = {0: "negative", 1: "neutral", 2: "positive"}


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "")

    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.softmax(outputs.logits, dim=1)
    predicted_label = torch.argmax(predictions, dim=1).item()

    sentiment = label_map.get(predicted_label, "unknown")
    return jsonify({"sentiment": predicted_label})


if __name__ == "__main__":
    app.run(debug=True)
