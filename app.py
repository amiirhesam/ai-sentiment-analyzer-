from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load the sentiment analysis model from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        if text.strip():
            prediction = sentiment_pipeline(text)[0]
            label = prediction["label"]
            score = prediction["score"]
            if label == "POSITIVE":
                sentiment = "Positive 😊"
                color = "green"
            elif label == "NEGATIVE":
                sentiment = "Negative 😞"
                color = "red"
            else:
                sentiment = "Neutral 😐"
                color = "gray"
            result = {
                "text": text,
                "sentiment": sentiment,
                "score": round(score * 100, 2),
                "color": color
            }
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
