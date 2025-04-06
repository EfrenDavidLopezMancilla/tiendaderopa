from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_secreta_para_mensajes_flash'  # Necesario para flash messages
db = SQLAlchemy(app)

# Modelos (sin cambios)
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.String(10), nullable=True)
    color = db.Column(db.String(20), nullable=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

# Rutas para productos (sin cambios)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/productos')
def listar_productos():
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('productos.html', productos=productos, categorias=categorias)

@app.route('/producto/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = Producto(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            precio=float(request.form['precio']),
            talla=request.form.get('talla'),
            color=request.form.get('color'),
            categoria_id=int(request.form['categoria_id'])
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('listar_productos'))
    
    categorias = Categoria.query.all()
    return render_template('agregar_producto.html', categorias=categorias)

@app.route('/producto/actualizar/<int:id>', methods=['GET','POST'])
def actualizar_producto(id):
    producto = Producto.query.get(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = float(request.form['precio'])
        producto.talla = request.form.get('talla')
        producto.color = request.form.get('color')
        producto.categoria_id = request.form.get('categoria_id')
        db.session.commit()
        return redirect(url_for('listar_productos'))
    
    categorias = Categoria.query.all()
    return render_template('actualizar_producto.html', producto=producto, categorias=categorias)

@app.route('/producto/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('listar_productos'))

# Nuevas rutas para categorías
@app.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categoria/agregar', methods=['GET', 'POST'])
def agregar_categoria():
    if request.method == 'POST':
        nombre = request.form['nombre']
        if Categoria.query.filter_by(nombre=nombre).first():
            flash('Esta categoría ya existe', 'error')
        else:
            nueva_categoria = Categoria(nombre=nombre)
            db.session.add(nueva_categoria)
            db.session.commit()
            flash('Categoría agregada correctamente', 'success')
            return redirect(url_for('listar_categorias'))
    
    return render_template('agregar_categoria.html')

@app.route('/categoria/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_categoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        if Categoria.query.filter(Categoria.id != id, Categoria.nombre == nuevo_nombre).first():
            flash('Ya existe otra categoría con ese nombre', 'error')
        else:
            categoria.nombre = nuevo_nombre
            db.session.commit()
            flash('Categoría actualizada correctamente', 'success')
            return redirect(url_for('listar_categorias'))
    
    return render_template('actualizar_categoria.html', categoria=categoria)

@app.route('/categoria/eliminar/<int:id>')
def eliminar_categoria(id):
    categoria = Categoria.query.get(id)
    if categoria:
        if categoria.productos:
            flash('No se puede eliminar la categoría porque tiene productos asociados', 'error')
        else:
            db.session.delete(categoria)
            db.session.commit()
            flash('Categoría eliminada correctamente', 'success')
    return redirect(url_for('listar_categorias'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)