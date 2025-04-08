from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para flash messages

db = SQLAlchemy(app)

# Modelos
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.String(20))
    color = db.Column(db.String(50))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

# Rutas CRUD
@app.route('/')
def index():
    productos = Producto.query.join(Categoria).add_columns(
        Producto.id,
        Producto.nombre,
        Producto.descripcion,
        Producto.precio,
        Producto.talla,
        Producto.color,
        Categoria.nombre.label('categoria_nombre')
    ).all()
    return render_template('index.html', productos=productos)

@app.route('/productos/new', methods=['GET', 'POST'])
def create_producto():
    if request.method == 'POST':
        try:
            nuevo_producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                talla=request.form['talla'],
                color=request.form['color'],
                categoria_id=int(request.form['categoria_id'])
            )
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto creado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear producto: {str(e)}', 'danger')
    
    categorias = Categoria.query.all()
    return render_template('create_producto.html', categorias=categorias)

@app.route('/productos/<int:id>/edit', methods=['GET', 'POST'])
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        try:
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form['descripcion']
            producto.precio = float(request.form['precio'])
            producto.talla = request.form['talla']
            producto.color = request.form['color']
            producto.categoria_id = int(request.form['categoria_id'])
            db.session.commit()
            flash('Producto actualizado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {str(e)}', 'danger')
    
    categorias = Categoria.query.all()
    return render_template('update_producto.html', producto=producto, categorias=categorias)

@app.route('/productos/<int:id>/delete', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar producto: {str(e)}', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Crear categorías iniciales si no existen
        if not Categoria.query.first():
            categorias_iniciales = ['Camisetas', 'Pantalones', 'Accesorios', 'Zapatos', 'Ropa Interior']
            for nombre in categorias_iniciales:
                db.session.add(Categoria(nombre=nombre))
            db.session.commit()
    app.run(debug=True)