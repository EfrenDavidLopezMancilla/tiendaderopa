from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Crear la aplicación Flask
    app = Flask(__name__)
    
    # Configuración
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tiendaderopa_1i9t_user:JZh0A8ZrLKg2B71hwMo8gEbWim0qfrnb@db:5432/tiendaderopa_1i9t'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'clave_secreta_para_mensajes_flash'
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints (rutas)
    from . import models, routes
    app.register_blueprint(routes.bp)
    
    # Crear tablas automáticamente al iniciar (solo en desarrollo)
    with app.app_context():
        db.create_all()
    
    return app