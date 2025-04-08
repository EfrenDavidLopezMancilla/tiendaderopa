from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
db = SQLAlchemy(app)

# Importar modelos y rutas aquí si es necesario
from . import models, routes