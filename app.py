from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///noticias.db"
db = SQLAlchemy(app)

class Noticia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    url = db.Column(db.String(200), nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Noticia {self.titulo}>"

# Crear la base de datos (solo la primera vez)
with app.app_context():
    db.create_all()

def obtener_noticias():
    url = "https://newsapi.org/v2/everything?q=China&sortBy=publishedAt&pageSize=10&apiKey=TU_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print("Error al obtener noticias:", response.status_code)
        return []

def actualizar_noticias():
    articulos = obtener_noticias()
    for articulo in articulos:
        # Verificar si la noticia ya existe en la base de datos
        existe = Noticia.query.filter_by(url=articulo["url"]).first()
        if not existe:
            nueva_noticia = Noticia(
                titulo=articulo["title"],
                descripcion=articulo["description"],
                url=articulo["url"],
                fecha_publicacion=datetime.strptime(articulo["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            )
            db.session.add(nueva_noticia)
    db.session.commit()

@app.route("/")
def index():
    pagina = request.args.get("pagina", 1, type=int)
    noticias = Noticia.query.order_by(Noticia.fecha_publicacion.desc()).paginate(page=pagina, per_page=5)
    return render_template("index.html", noticias=noticias)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def get_news():
    # URL de NewsAPI con parámetros para noticias recientes y ordenadas
    url = "https://newsapi.org/v2/everything?q=China&sortBy=publishedAt&pageSize=10&apiKey=e715ff500ac0437db588e82f282c1998"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print("Error al obtener noticias:", response.status_code)
        return []

@app.route("/")
def index():
    news = get_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto de Render o 5000 por defecto
    app.run(host="0.0.0.0", port=port)
