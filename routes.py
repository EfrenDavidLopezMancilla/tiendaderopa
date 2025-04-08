from tienda_ropa import app, db
from tienda_ropa.models import Producto

@app.route('/productos')
def listar_productos():
    productos = Producto.query.all()
    # ... resto de tu lógica