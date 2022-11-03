

from xmlrpc import client
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user, login_required

from models.usuariosdb import usuariosNew,acciones

from utils.db import db


usuarioss = Blueprint("usuarios", __name__)

@usuarioss.route("/nuw_usua/<string:accion>")
@login_required
def new_usua(accion):
    accion_re=db.session.query(acciones).filter_by(accion=accion).first()
  
    if current_user.Rol== "Funcional":
        flash("El funcional no puede registrar usuarios, solo testing.")
        accion ="eliminar"
        accion_re=db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html",accion_re=accion_re)
    
    busque = db.session.query(usuariosNew).all()
    return render_template("crearusuarios.html", busque=busque,accion_re=accion_re)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404



@usuarioss.route("/updateUs2/<string:accion>", methods=["GET", "POST"])
@login_required
def updateUs2(accion):
    accion_re=db.session.query(acciones).filter_by(accion=accion).first()
    if current_user.Rol== "Funcional":
        flash("no puedes realizar esa acción.")
        accion ="eliminar"
        accion_re=db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html",accion_re=accion_re)
    

    id = current_user.id
    resul = db.session.query(usuariosNew).filter_by(id=id).first()

    if request.method == "POST":

        contra1 = request.form["contrasena"]
        contra2 = request.form["contrasena2"]

        if contra1 == contra2:

            resul.nombre = request.form["nombre"]
            resul.contrasena = request.form["contrasena"]
            db.session.commit()
            flash("contraseña o usuario actualizados")
            accion ="guardar"
            return redirect("/seguimiento/"+accion)
        else:
            flash("las contraseñas no son iguales")
            accion="eliminar"
            return redirect("/updateUs2/"+accion)
    return render_template("actualizarContra.html",accion_re=accion_re)




@usuarioss.route("/creatUsu", methods=["POST"])
@login_required
def creatUsu():
    if current_user.Rol== "Funcional":
        flash("no puedes realizar esa acción.")
        accion ="eliminar"
        accion_re=db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html",accion_re=accion_re)
    Rol = request.form["tipo_usu"]
    nombre = request.form["nombre"]
    num_doc = request.form["numeDoc"]
    contrasena = request.form["contrasena"]

    busque = db.session.query(usuariosNew).filter_by(num_doc=num_doc).first()
    db.session.commit()
    if busque is None:

        guar = usuariosNew(nombre, num_doc, contrasena,Rol)

        db.session.add(guar)
        print(current_user)
        db.session.commit()

        flash("usuario creado")
        accion="guardar"
        return redirect("/nuw_usua/"+accion)
    flash("el usuario ya existe")
    accion="eliminar"
    return redirect("/nuw_usua/"+accion)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@usuarioss.route("/deleteUs2/<id>")
@login_required
def deleteU2(id):
    if current_user.Rol== "Funcional":
        flash("no puedes realizar esa acción.")
        accion ="eliminar"
        accion_re=db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html",accion_re=accion_re)
    usu = usuariosNew.query.get(id)
    db.session.delete(usu)
    db.session.commit()

    id2 = current_user.id

    idi = db.session.query(usuariosNew).filter_by(id=id2).first()

    if idi:

        flash("eliminado")
        accion="eliminar"
        return redirect("/nuw_usua/"+accion)
    return redirect("/salida")


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@usuarioss.route("/deleteUs/<id>")
def deleteUs(id):
    
    if current_user.Rol== "Funcional":
        flash("no puedes realizar esa acción.")
        accion ="eliminar"
        accion_re=db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html",accion_re=accion_re)

    resu = db.session.query(usuariosNew).filter_by(id=id).first()

    pagi = "/nuw_usua"
    pagi2 = "/deleteUs2"

    return render_template("eliminar2.html", resu=resu, pagi=pagi, pagi2=pagi2)


@usuarioss.route("/updateUs/<id>", methods=["GET", "POST"])
@login_required
def updateUs(id):
    
    if current_user.Rol== "Funcional":
        flash("no puedes realizar esa acción.")
        return render_template("inicio2.html")
    resul = db.session.query(usuariosNew).filter_by(id=id).first()

    if request.method == "POST":
        resul.nombre = request.form["nombre"]
        resul.Rol = request.form["tipo_usu"]
        resul.num_doc = request.form["numeDoc"]

        db.session.commit()
        flash("usuario actualizado")
        accion="guardar"
        return redirect("/nuw_usua/"+accion)

    return render_template("actuali_usu.html", resul=resul)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404

