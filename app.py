from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

def get_news():
    # Ejemplo: Noticias de NewsAPI
    url = "https://newsapi.org/v2/everything?q=China&apiKey=e715ff500ac0437db588e82f282c1998"
    response = requests.get(url)
    return response.json().get("articles", [])

@app.route("/")
def index():
    news = get_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto de Render o 5000 por defecto
    app.run(host="0.0.0.0", port=port)
