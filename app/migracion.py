from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.models import db, Cliente, Producto, Pedido, DetallePedido


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://jhonatan_admin:Mynameisjhonax@mysql-jhonatan.alwaysdata.net/jhonatan_coffe'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
