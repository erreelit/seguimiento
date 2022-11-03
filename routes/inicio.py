
from flask import render_template, redirect, flash, Blueprint, request, logging
from sqlalchemy import null
from models.usuariosdb import usuariosNew
from utils.db import db

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField

from flask_login import (
    login_user,
    LoginManager,
    logout_user,
    current_user,
)


from flask import Blueprint, render_template, request, redirect, flash
inicios = Blueprint("inicio", __name__)


@inicios.route("/")
def inicio():

    if current_user.is_authenticated:  # type: ignore
        
        accion="guardar"

        return redirect("/seguimiento/"+accion)

    usuEX = db.session.query(usuariosNew).all()
    db.session.commit()

    if usuEX:
        usuEXx = 0
    else:
        nombre = "admin"
        num_doc = "1"
        contrasena = "admin"
        Rol = "Tester"
        new_usu = usuariosNew(nombre, num_doc, contrasena, Rol)
        db.session.add(new_usu)
        db.session.commit()
        

    return render_template("login.html")


@inicios.route("/logeo", methods=["POST"])
def logeo():
    usuario = request.form["usuario"]
    contrasena = request.form["contrasena"]

    resultados = db.session.query(
        usuariosNew).filter_by(num_doc=usuario).first()

    if resultados is None:

        flash("Usuario no registrado")
        return redirect("/")

    if resultados.contrasena == contrasena:

        login_user(resultados, remember=True)

        flash("Bienvenido " + current_user.nombre)  # type: ignore
        
        accion="guardar"

        return redirect("/seguimiento/"+accion)
    else:
        flash("contraseña incorrecta")
        return redirect("/")


@inicios.route("/salida")
def salida():
    logout_user()
    return redirect("/")
