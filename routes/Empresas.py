

from xmlrpc import client
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from sqlalchemy import null

from models.usuariosdb import t_empresas, acciones

from utils.db import db


empresas = Blueprint("empresas", __name__)


@empresas.route("/Empresasform/<string:accion>")
@login_required
def Empresasform(accion):

    accion_re = db.session.query(acciones).filter_by(accion=accion).first()

    if current_user.Rol == "Funcional":
        flash("El funcional no puede registrar empresas, solo testing.")
        accion="eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)

    empre = db.session.query(t_empresas).all()
    return render_template("Registrar_Empresas.html", empre=empre, accion_re=accion_re)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@empresas.route("/SaveEm", methods=["POST"])
@login_required
def SaveEm():
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")

        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()

        return render_template("inicio2.html", accion_re=accion_re)
    E_nombre = request.form["E_nombre"]

    busque = db.session.query(t_empresas).filter_by(E_nombre=E_nombre).first()
    db.session.commit()
    if busque is None:

        guar = t_empresas(E_nombre)

        db.session.add(guar)
        db.session.commit()

        flash("empresa creada")
        accion = "guardar"
        return redirect("/Empresasform/"+accion)
    flash("La empresa ya existe")
    accion = "eliminar"
    return redirect("/Empresasform/"+accion)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@empresas.route("/DeleteEm2/<id>")
@login_required
def DeleteEm2(id):
    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("no puedes realizar esa acción.")
        return render_template("inicio2.html", accion_re=accion_re)
    empre = t_empresas.query.get(id)
    db.session.delete(empre)
    db.session.commit()

    flash("Empresa Eliminada")
    accion = "eliminar"
    return redirect("/Empresasform/"+accion)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@empresas.route("/DeleteEm/<id>")
def DeleteEm(id):
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)

    resu = db.session.query(t_empresas).filter_by(id=id).first()

    pagi = "/Empresasform"
    pagi2 = "/DeleteEm2"

    return render_template("eliminar2.html", resu=resu, pagi=pagi, pagi2=pagi2)


def status_401(error):
    return redirect("/")


@empresas.route("/updateEmpr/<id>", methods=["GET", "POST"])
@login_required
def updateEmpr(id):
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)
    resul = db.session.query(t_empresas).filter_by(id=id).first()

    if request.method == "POST":
        E_nombre = request.form["E_nombre"]
        resul2 = db.session.query(t_empresas).filter_by(
            E_nombre=E_nombre).first()

        if resul2 is None:

            resul.E_nombre = request.form["E_nombre"]
            db.session.commit()
            flash("Empresa actualizada")
            accion = "guardar"
            return redirect("/Empresasform/"+accion)
        else:
            flash("Ya hay una empresa con este nombre")
            accion = "eliminar"
            return redirect("/Empresasform/"+accion)

    return render_template("actualizar_empresa.html", resul=resul)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404
