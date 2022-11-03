
from xmlrpc import client
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required
from sqlalchemy import null
from models.usuariosdb import Funcionales, acciones
from utils.db import db


funcional = Blueprint("funcional", __name__)


@funcional.route("/Funcionalesform/<string:accion>")
@login_required
def Empresasform(accion):

    accion_re = db.session.query(acciones).filter_by(accion=accion).first()

    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("El funcional no puede registrar Funcionales, solo testing.")
        return render_template("inicio2.html", accion_re=accion_re)

    fun = db.session.query(Funcionales).all()
    return render_template("funcionales.html", fun=fun, accion_re=accion_re)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@funcional.route("/SaveFun", methods=["POST"])
@login_required
def SaveEm():
    if current_user.Rol == "Funcional":

        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("El funcional no puede registrar Funcionales, solo testing.",)

        return render_template("inicio2.html", accion_re=accion_re)
    F_nombre = request.form["F_nombre"]

    busque = db.session.query(Funcionales).filter_by(F_nombre=F_nombre).first()
    db.session.commit()
    if busque is None:

        guar = Funcionales(F_nombre)

        db.session.add(guar)
        db.session.commit()

        flash("Funcional registrado")
        accion = "guardar"
        return redirect("/Funcionalesform/"+accion)
    flash("El funcional ya existe")
    accion = "eliminar"
    return redirect("/Funcionalesform/"+accion)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@funcional.route("/Deletefun2/<id>")
@login_required
def DeleteEm2(id):
    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("El funcional no puede registrar Funcionales, solo testing.",)

        return render_template("inicio2.html", accion_re=accion_re)
    empre = Funcionales.query.get(id)
    db.session.delete(empre)
    db.session.commit()

    flash("Funcional Eliminado")
    accion = "eliminar"
    return redirect("/Funcionalesform/"+accion)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@funcional.route("/Deletefun/<id>")
def DeleteEm(id):
    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("El funcional no puede registrar Funcionales, solo testing.",)

        return render_template("inicio2.html", accion_re=accion_re)

    resu = db.session.query(Funcionales).filter_by(id=id).first()

    pagi = "/Funcionalesform"
    pagi2 = "/Deletefun2"

    return render_template("eliminar2.html", resu=resu, pagi=pagi, pagi2=pagi2)


def status_401(error):
    return redirect("/")


@funcional.route("/updatefun/<id>", methods=["GET", "POST"])
@login_required
def updateEmpr(id):
    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        flash("El funcional no puede registrar Funcionales, solo testing.",)

        return render_template("inicio2.html", accion_re=accion_re)
    resul = db.session.query(Funcionales).filter_by(id=id).first()

    if request.method == "POST":
        F_nombre = request.form["F_nombre"]
        resul2 = db.session.query(Funcionales).filter_by(
            F_nombre=F_nombre).first()

        if resul2 is None:

            resul.F_nombre = request.form["F_nombre"]
            db.session.commit()
            flash("Funcional actualizado")
            accion = "guardar"
            return redirect("/Funcionalesform/"+accion)
        else:
            flash("Ya hay un funcional con este nombre")
            accion = "eliminar"
            return redirect("/Funcionalesform/"+accion)

    return render_template("actualizar_funcional.html", resul=resul)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404
