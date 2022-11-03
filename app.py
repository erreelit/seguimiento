from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from routes.inicio import inicios
from  models.usuariosdb import usuariosNew
from routes.seguimiento import seguimientoss,status_404,status_401 
from routes.usuarios import usuarioss
from routes.Empresas import empresas
from routes.funcionales import funcional
from routes.archivos import archivoss








app = Flask(__name__)
csrf=CSRFProtect()
app.secret_key="secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/seguimiento'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE']=300
app.config['SQLALCHEMY_POOL_TIMEOUT']=20
app.secret_key="secret_key"
app.config['UPLOAD_FOLDER'] = "static/archivos"
login_manager=LoginManager(app)
csrf.init_app(app)
SQLAlchemy(app)

@login_manager.user_loader
def Load_user(id):
   return usuariosNew.query.get(id)


app.register_blueprint(inicios)
app.register_blueprint(seguimientoss)
app.register_blueprint(usuarioss)
app.register_blueprint(empresas)
app.register_blueprint(funcional)
app.register_blueprint(archivoss)

app.register_error_handler(404,status_404)
app.register_error_handler(401,status_401)