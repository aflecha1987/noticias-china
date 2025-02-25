from flask import Flask, render_template
import requests

app = Flask(__name__)

def get_news():
    # Ejemplo: Noticias de NewsAPI
    url = "https://newsapi.org/v2/everything?q=China&apiKey=TU_API_KEY"
    response = requests.get(url)
    return response.json().get("articles", [])

@app.route("/")
def index():
    news = get_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(debug=True)
