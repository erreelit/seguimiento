
from msilib.schema import Patch
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, flash, send_from_directory
from flask_login import current_user, login_required
from datetime import datetime

from sqlalchemy import false
from models.usuariosdb import usuariosNew, t_seguimiento, estados, t_empresas, Funcionales, t_archivo, acciones
import os
from os import path, remove
from werkzeug.utils import secure_filename

from utils.db import db


seguimientoss = Blueprint("seguimiento", __name__)


@seguimientoss.route("/seguimiento/<string:accion>")
@login_required
def seguimiento(accion):

    if current_user.Rol == "Funcional":
        accion = "guardar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)

    usuariio = db.session.query(usuariosNew).all()
    R_empresa = db.session.query(t_empresas).all()

    accion_re = db.session.query(acciones).filter_by(accion=accion).first()

    Funcionaless = db.session.query(Funcionales).all()

    return render_template("inicio.html", usuariio=usuariio, Funcionaless=Funcionaless, R_empresa=R_empresa, accion_re=accion_re)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@seguimientoss.route("/save", methods=["POST"])
def save():
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)
    Codigo = request.form["codigo"]
    Empresa = request.form["Empresa"]
    issue = request.form["issue"]
    Nombre_Iniciativa = request.form["fullname"]
    responsables = request.form["responsables"]
    PETICION = request.form["peticion"]
    VoBo_Oferta_EX = request.form["VoBo_oferta"]
    VoBo_FunctionalDesign_EX = request.form["VoBo_Df"]
    VoBo_E380_EX = request.form["VoBo_E380"]
    VoBo_E380_UAT_EX = request.form["VoBo_UAT"]
    Oferta_Economica = request.form["oferta_eco"]
    Oferta_Tecnica = request.form["oferta_tec"]
    Estimador = request.form["estimador"]
    Plan_Interno = request.form["Plan_interno"]
    Nivel_de_Riesgo_de_Producto = request.form["riesgos_prod"]
    FD_Functional_Design = request.form["Dis_funcional"]
    CL_Functional_Design = request.form["C_dis_fun"]
    SP_Set_Pruebas = request.form["Set_prueba"]
    E420_Diseño_Tecnico = request.form["Dis_tec"]
    CL_E420_Diseno_Tecnico = request.form["C_dis_tec"]
    E380_Plan_Pruebas = request.form["E380"]
    CL_E380_Plan_Pruebas = request.form["C_E380"]
    Plan_Pruebas_Unitarias = request.form["Prue_Uni"]
    Guia_Integracion = request.form["Guia_integracion"]
    Observacion = request.form["observaciones"]

    if (responsables == "seleccionar" or Empresa == "seleccionar" or PETICION == "seleccionar" or VoBo_Oferta_EX == "seleccionar"
       or VoBo_FunctionalDesign_EX == "seleccionar" or
        VoBo_E380_EX == "seleccionar" or VoBo_E380_UAT_EX == "seleccionar" or Oferta_Economica == "seleccionar" or Oferta_Tecnica == "seleccionar" or Estimador == "seleccionar" or Plan_Interno == "seleccionar" or
        Nivel_de_Riesgo_de_Producto == "seleccionar" or FD_Functional_Design == "seleccionar" or CL_Functional_Design == "seleccionar" or SP_Set_Pruebas == "seleccionar" or
            E420_Diseño_Tecnico == "seleccionar" or CL_E420_Diseno_Tecnico == "seleccionar" or E380_Plan_Pruebas == "seleccionar" or CL_E380_Plan_Pruebas == "seleccionar" or Plan_Pruebas_Unitarias == "seleccionar" or Guia_Integracion == "seleccionar"):

        flash("Debe llenar todos los campos desplegables")
        accion = "eliminar"
        return redirect("/seguimiento/"+accion)

    now = datetime.now()
    format = now.strftime('%Y/%m/%d %H:%M')
    fecha_actual = str(format)
    fecha_modificacion = fecha_actual

    usuario = current_user.nombre

    result = db.session.query(t_seguimiento).filter_by(Codigo=Codigo).first()
    db.session.commit()

    if result is None:
        new_iniciativa = t_seguimiento(Codigo, Empresa, issue, Nombre_Iniciativa, responsables, PETICION, VoBo_Oferta_EX, VoBo_FunctionalDesign_EX,
                                       VoBo_E380_EX, VoBo_E380_UAT_EX, Oferta_Economica, Oferta_Tecnica, Estimador, Plan_Interno,
                                       Nivel_de_Riesgo_de_Producto, FD_Functional_Design, CL_Functional_Design, SP_Set_Pruebas,
                                       E420_Diseño_Tecnico, CL_E420_Diseno_Tecnico, E380_Plan_Pruebas, CL_E380_Plan_Pruebas, Plan_Pruebas_Unitarias, Guia_Integracion, Observacion, fecha_actual=fecha_actual, fecha_modificacion=fecha_modificacion, usuario=usuario)  # type: ignore

        db.session.add(new_iniciativa)
        db.session.commit()

        flash("iniciativa guarada")
        accion = "guardar"
        return redirect("/seguimiento/"+accion)

    flash("Ya existe la iniciativa")
    accion = "eliminar"
    return redirect("/seguimiento/"+accion)


@seguimientoss.route("/buscarINI", methods=["POST"])
@login_required
def buscarINI():

    accion = "guardar"
    accion_re = db.session.query(acciones).filter_by(accion=accion).first()

    Codigo = request.form["BuscarI"]
    buscar = db.session.query(
        t_seguimiento).filter_by(Codigo=Codigo).first()

    buscar2 = db.session.query(
        t_archivo).filter_by(Codigo=Codigo).first()

    if buscar is None:
        accion = "eliminar"
        flash("Iniciativa no registrada")
        return redirect("/seguimiento/"+accion)

    coloP = buscar.PETICION
    ColVof = buscar.VoBo_Oferta_EX
    Col_V_f = buscar.VoBo_FunctionalDesign_EX
    Col_E380 = buscar.VoBo_E380_EX
    Col_V_U_a_T = buscar.VoBo_E380_UAT_EX
    Col_O_E = buscar.Oferta_Economica
    Col_O_t = buscar.Oferta_Tecnica
    Col_E = buscar.Estimador
    Col_P_i = buscar.Plan_Interno
    Col_N_R = buscar.Nivel_de_Riesgo_de_Producto
    Col_F_D_F_D = buscar.FD_Functional_Design
    Col_CL_F_D = buscar.CL_Functional_Design
    Col_SP_S_P = buscar.SP_Set_Pruebas
    Col_E420_D_T = buscar.E420_Diseño_Tecnico
    Col_E420_CL = buscar.CL_E420_Diseno_Tecnico
    Col_E380_PL_P = buscar.E380_Plan_Pruebas
    Col_Cl_E380_PL_P = buscar.CL_E380_Plan_Pruebas
    Col_P_U = buscar.Plan_Pruebas_Unitarias
    Col_G_I = buscar.Guia_Integracion
    Col_Ob = buscar.Observacion

    """aqui van las consultas"""
    colorPeticion = db.session.query(
        estados).filter_by(estado=coloP).first()
    colorVOF = db.session.query(
        estados).filter_by(estado=ColVof).first()
    ColVf = db.session.query(
        estados).filter_by(estado=Col_V_f).first()
    ColE380 = db.session.query(
        estados).filter_by(estado=Col_E380).first()
    ColVUaT = db.session.query(
        estados).filter_by(estado=Col_V_U_a_T).first()
    ColOE = db.session.query(
        estados).filter_by(estado=Col_O_E).first()
    ColOt = db.session.query(
        estados).filter_by(estado=Col_O_t).first()
    ColE = db.session.query(
        estados).filter_by(estado=Col_E).first()
    ColPi = db.session.query(
        estados).filter_by(estado=Col_P_i).first()
    ColNR = db.session.query(
        estados).filter_by(estado=Col_N_R).first()
    ColFDFD = db.session.query(
        estados).filter_by(estado=Col_F_D_F_D).first()
    ColCLFD = db.session.query(
        estados).filter_by(estado=Col_CL_F_D).first()
    ColSPSP = db.session.query(
        estados).filter_by(estado=Col_SP_S_P).first()
    ColE420DT = db.session.query(
        estados).filter_by(estado=Col_E420_D_T).first()
    ColE420CL = db.session.query(
        estados).filter_by(estado=Col_E420_CL).first()
    ColE380PLP = db.session.query(
        estados).filter_by(estado=Col_E380_PL_P).first()
    ColClE380PLP = db.session.query(
        estados).filter_by(estado=Col_Cl_E380_PL_P).first()
    ColPU = db.session.query(
        estados).filter_by(estado=Col_P_U).first()
    ColGI = db.session.query(
        estados).filter_by(estado=Col_G_I).first()
    ColOb = db.session.query(
        estados).filter_by(estado=Col_Ob).first()

    R_empresa = db.session.query(t_empresas).all()

    Funcionaless = db.session.query(Funcionales).all()

    fecha_actual = buscar.fecha_actual
    fecha_modificacion = buscar.fecha_modificacion

    if current_user.Rol == "Funcional":
        return render_template("/busquedaINiFun.html", color=colorPeticion, colorVOF=colorVOF, buscar=buscar, ColVf=ColVf, ColE380=ColE380, ColVUaT=ColVUaT, ColOE=ColOE, ColOt=ColOt, ColE=ColE, ColPi=ColPi, ColNR=ColNR, ColFDFD=ColFDFD,
                               ColCLFD=ColCLFD, ColSPSP=ColSPSP, ColE420DT=ColE420DT, ColE420CL=ColE420CL, ColE380PLP=ColE380PLP,
                               ColClE380PLP=ColClE380PLP, ColPU=ColPU, ColGI=ColGI, ColOb=ColOb, fecha_modificacion=fecha_modificacion, buscar2=buscar2, accion_re=accion_re)

    return render_template("/ActualizaElimina.html", R_empresa=R_empresa, Funcionaless=Funcionaless, buscar=buscar, color=colorPeticion, colorVOF=colorVOF, ColVf=ColVf, ColE380=ColE380, ColVUaT=ColVUaT, ColOE=ColOE, ColOt=ColOt, ColE=ColE, ColPi=ColPi, ColNR=ColNR, ColFDFD=ColFDFD,
                           ColCLFD=ColCLFD, ColSPSP=ColSPSP, ColE420DT=ColE420DT, ColE420CL=ColE420CL, ColE380PLP=ColE380PLP,
                           ColClE380PLP=ColClE380PLP, ColPU=ColPU, ColGI=ColGI, ColOb=ColOb, fecha_actual=fecha_actual, fecha_modificacion=fecha_modificacion, buscar2=buscar2, accion_re=accion_re)


@seguimientoss.route("/actualizar", methods=["POST"])
@login_required
def actualizar():
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)

    Codigo = request.form["codigo"]
    actualizar = db.session.query(
        t_seguimiento).filter_by(Codigo=Codigo).first()

    print(Codigo)

    actualizar.Codigo = request.form["codigo"]
    actualizar.Empresa = request.form["Empresa"]
    actualizar.issue = request.form["issue"]
    actualizar.Nombre_Iniciativa = request.form["fullname"]
    actualizar.RESPONSABLE = request.form["responsable"]
    actualizar.PETICION = request.form["peticion"]
    actualizar.VoBo_Oferta_EX = request.form["VoBo_oferta"]
    actualizar.VoBo_FunctionalDesign_EX = request.form["VoBo_Df"]
    actualizar.VoBo_E380_EX = request.form["VoBo_E380"]
    actualizar.VoBo_E380_UAT_EX = request.form["VoBo_UAT"]
    actualizar.Oferta_Economica = request.form["oferta_eco"]
    actualizar.Oferta_Tecnica = request.form["oferta_tec"]
    actualizar.Estimador = request.form["estimador"]
    actualizar.Plan_Interno = request.form["Plan_interno"]
    actualizar.Nivel_de_Riesgo_de_Producto = request.form["riesgos_prod"]
    actualizar.FD_Functional_Design = request.form["Dis_funcional"]
    actualizar.CL_Functional_Design = request.form["C_dis_fun"]
    actualizar.SP_Set_Pruebas = request.form["Set_prueba"]
    actualizar.E420_Diseño_Tecnico = request.form["Dis_tec"]
    actualizar.CL_E420_Diseno_Tecnico = request.form["C_dis_tec"]
    actualizar.E380_Plan_Pruebas = request.form["E380"]
    actualizar.CL_E380_Plan_Pruebas = request.form["C_E380"]
    actualizar.Plan_Pruebas_Unitarias = request.form["Prue_Uni"]
    actualizar.Guia_Integracion = request.form["Guia_integracion"]
    actualizar.Observacion = request.form["observaciones"]
    actualizar.fecha_actual = str(request.form["fecha_c"])
    actualizar.usuario = current_user.nombre

    Codigo = request.form["codigo"]
    Empresa = request.form["Empresa"]
    responsables = request.form["responsable"]
    PETICION = request.form["peticion"]
    VoBo_Oferta_EX = request.form["VoBo_oferta"]
    VoBo_FunctionalDesign_EX = request.form["VoBo_Df"]
    VoBo_E380_EX = request.form["VoBo_E380"]
    VoBo_E380_UAT_EX = request.form["VoBo_UAT"]
    Oferta_Economica = request.form["oferta_eco"]
    Oferta_Tecnica = request.form["oferta_tec"]
    Estimador = request.form["estimador"]
    Plan_Interno = request.form["Plan_interno"]
    Nivel_de_Riesgo_de_Producto = request.form["riesgos_prod"]
    FD_Functional_Design = request.form["Dis_funcional"]
    CL_Functional_Design = request.form["C_dis_fun"]
    SP_Set_Pruebas = request.form["Set_prueba"]
    E420_Diseño_Tecnico = request.form["Dis_tec"]
    CL_E420_Diseno_Tecnico = request.form["C_dis_tec"]
    E380_Plan_Pruebas = request.form["E380"]
    CL_E380_Plan_Pruebas = request.form["C_E380"]
    Plan_Pruebas_Unitarias = request.form["Prue_Uni"]
    Guia_Integracion = request.form["Guia_integracion"]

    if (responsables == "seleccionar" or Empresa == "seleccionar" or PETICION == "seleccionar" or VoBo_Oferta_EX == "seleccionar"
        or VoBo_FunctionalDesign_EX == "seleccionar" or
        VoBo_E380_EX == "seleccionar" or VoBo_E380_UAT_EX == "seleccionar" or Oferta_Economica == "seleccionar" or Oferta_Tecnica == "seleccionar" or Estimador == "seleccionar" or Plan_Interno == "seleccionar" or
        Nivel_de_Riesgo_de_Producto == "seleccionar" or FD_Functional_Design == "seleccionar" or CL_Functional_Design == "seleccionar" or SP_Set_Pruebas == "seleccionar" or
            E420_Diseño_Tecnico == "seleccionar" or CL_E420_Diseno_Tecnico == "seleccionar" or E380_Plan_Pruebas == "seleccionar" or CL_E380_Plan_Pruebas == "seleccionar" or Plan_Pruebas_Unitarias == "seleccionar" or Guia_Integracion == "seleccionar"):

        flash("Debe llenar todos los campos desplegables")
        accion = "eliminar"
        return redirect("/seguimiento/"+accion)

    now = datetime.now()
    format = now.strftime('%Y/%m/%d %H:%M')
    actualizar.fecha_modificacion = str(format)
    db.session.commit()

    flash("iniciativa actualizada")
    accion = "guardar"

    return redirect("/seguimiento/"+accion)


@seguimientoss.route("/Delete/<Codigo>", methods=["GET"])
@login_required
def Delete(Codigo):
    if current_user.Rol == "Funcional":
        flash("no puedes realizar esa acción.")
        return render_template("inicio2.html")
    resu = db.session.query(t_seguimiento).filter_by(Codigo=Codigo).first()

    pagi = "/seguimiento"

    pagi2 = "/delete2"
    accion = "guardar"

    return render_template("eliminar.html", resu=resu, pagi=pagi, pagi2=pagi2, accion=accion)


@seguimientoss.route("/delete2/<Codigo>")
@login_required
def delete2(Codigo):
    if current_user.Rol == "Funcional":
        accion = "eliminar"
        accion_re = db.session.query(acciones).filter_by(accion=accion).first()
        return render_template("inicio2.html", accion_re=accion_re)

    resultado_eliminar = db.session.query(
        t_seguimiento).filter_by(Codigo=Codigo).first()
    resultado_eliminar2 = db.session.query(
        t_archivo).filter_by(Codigo=Codigo).all()

    if resultado_eliminar2 is None:

        db.session.delete(resultado_eliminar)
        db.session.commit()
        flash("Iniciativa eliminada")
        accion = "eliminar"
        return redirect("/seguimiento/"+accion)

    for i in resultado_eliminar2:
        filename = i.A_nombre
        eliminarArchivo(filename, Codigo)
        resultado_eliminar3 = db.session.query(
            t_archivo).filter_by(A_nombre=i.A_nombre).first()

        db.session.delete(resultado_eliminar3)
        db.session.commit()
    db.session.delete(resultado_eliminar)
    db.session.commit()

    flash("Iniciativa eliminada")
    accion = "eliminar"
    return redirect("/seguimiento/"+accion)


def eliminarArchivo(filename, Codigo):

    file_name = filename

    if path.isfile("static/archivos/"+Codigo+"/"+file_name) == False:

        flash("No existe el archivo")
        accion = "eliminar"

        return redirect("/seguimiento/"+accion)

    else:
        try:
            remove("static/archivos/"+Codigo+"/"+file_name)
            accion = "eliminar"
            return redirect("/seguimiento/"+accion)
        except OSError:
            flash("no se pudo borrar", file_name)
            accion = "eliminar"
            return redirect("/seguimiento/"+accion)
