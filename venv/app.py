# Modelo Categoría
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

# Modelo Producto
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    talla = db.Column(db.String(10))
    color = db.Column(db.String(50))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    categoria = db.relationship('Categoria', backref=db.backref('productos', lazy=True))

# Ruta para ver todos los productos
@app.route('/')
def index():
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('index.html', productos=productos, categorias=categorias)

# Ruta para agregar producto
@app.route('/producto/nuevo', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        talla = request.form.get('talla')
        color = request.form.get('color')
        categoria_id = request.form.get('categoria_id')
        
        nuevo_producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            talla=talla,
            color=color,
            categoria_id=categoria_id
        )
        
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('index'))
    
    categorias = Categoria.query.all()
    return render_template('create_product.html', categorias=categorias)

if __name__ == '__main__':
    app.run(debug=True)