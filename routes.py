from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import Producto, Categoria
from . import db

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/productos')
def listar_productos():
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('productos.html', productos=productos, categorias=categorias)

# ... (todas tus otras rutas aquí)