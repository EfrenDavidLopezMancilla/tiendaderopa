from tiendaderopa import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from tiendaderopa.models import db
        db.create_all()  # Crear tablas si no existen
    app.run(debug=True)