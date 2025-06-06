import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

from models import db, Categoria, Producto, MovimientoInventario

db.init_app(app)
migrate = Migrate(app, db)

from routes import *



if __name__ == '__main__':
    app.run(debug=True)
