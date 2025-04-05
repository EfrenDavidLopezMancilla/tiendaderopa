@app.route('/')
def home():
    return render_template('home.html')  # Ruta principal de la tienda

@app.route('/productos')
def productos():
    productos = Producto.query.all()
    categorias = Categoria.query.all()
    return render_template('productos.html', productos=productos, categorias=categorias)

# Actualizar producto
@app.route('/producto/actualizar/<int:id>', methods=['GET','POST'])
def update_product(id):
    producto = Producto.query.get(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = float(request.form['precio'])
        producto.talla = request.form.get('talla')
        producto.color = request.form.get('color')
        producto.categoria_id = request.form.get('categoria_id')
        db.session.commit()
        return redirect(url_for('productos'))  # Redirige a la lista de productos actualizada
    
    categorias = Categoria.query.all()
    return render_template('update_product.html', producto=producto, categorias=categorias)

# Eliminar producto
@app.route('/producto/eliminar/<int:id>')
def delete_product(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('productos'))  # Redirige a la lista de productos actualizada
