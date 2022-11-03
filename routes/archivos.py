from msilib.schema import File
from flask import Blueprint, render_template, request, redirect, flash, send_from_directory
from flask_login import current_user, login_required
import os
from os import path, remove
from models.usuariosdb import t_archivo, t_seguimiento, estados, t_empresas, Funcionales, acciones
from werkzeug.utils import secure_filename
from utils.db import db


archivoss = Blueprint("archivo", __name__)

ALLOWED_EXTENSIONS = set(['xlsx', 'doc', 'docx', 'pdf', 'msg', ' '])


def alowoed_file(file):
    file = file.split('.')
    print(file)
    if file[1] in ALLOWED_EXTENSIONS or file[2] in ALLOWED_EXTENSIONS or file[3] in ALLOWED_EXTENSIONS or file[4] in ALLOWED_EXTENSIONS:
        return True
    return False


@archivoss.route('/InterArchivo/<string:Codigo>/<string:accion>', methods=["GET"])
@login_required
def InterArchivo(Codigo, accion):

    resultado = db.session.query(t_archivo).filter_by(Codigo=Codigo).all()

    accion_re = db.session.query(acciones).filter_by(accion=accion).first()

    return render_template('Archivos.html', resultado=resultado, Codigo=Codigo, accion_re=accion_re)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@archivoss.route("/SaveDoc", methods=["POST"])
@login_required
def SaveDoc():

    upload_files = request.files.getlist("archivo")
    Codigo = request.form["Codigo"]

    for file in upload_files:

        filename = secure_filename(file.filename)

        if file and alowoed_file(filename):

            os.makedirs('static/archivos/'+Codigo, exist_ok=True)

            file.save(os.path.join("static/archivos/"+Codigo, filename))
            A_nombre = str(filename)

            resultado_eliminar2 = db.session.query(
                t_archivo).filter_by(A_nombre=A_nombre).first()

            if resultado_eliminar2 is None:
                arc_nuevo = t_archivo(Codigo, A_nombre)
                db.session.add(arc_nuevo)
                db.session.commit()
        else:

            flash("Archivo no permitido")
            accion = "eliminar"
            return redirect("/InterArchivo/"+Codigo+"/"+accion)
    flash("Se guardo correctamente")

    accion = "/guardar"
    return redirect("/InterArchivo/"+Codigo+"/"+accion)


@archivoss.route('/eliminarArchivos2/<string:Codigo>/<string:filename>', methods=["GET"])
@login_required
def eliminarArchi(Codigo, filename):

    pagi1 = "/InterArchivo/"+Codigo+"/Save"
    pagi2 = "/eliminarArchivos/"+Codigo+"/"+filename

    return render_template("Eliminararchivos.html", pagi1=pagi1, pagi2=pagi2)


@archivoss.route('/eliminarArchivos/<string:Codigo>/<string:filename>', methods=["GET"])
@login_required
def eliminarArchivos(Codigo, filename):

    file_name = filename

    print(file_name)
    if path.isfile("static/archivos/"+Codigo+"/"+file_name) == False:

        flash("No existe el archivo")
        accion = "eliminar"
        return redirect("/InterArchivo/"+Codigo+"/"+accion)

    else:
        try:

            remove("static/archivos/"+Codigo+"/"+file_name)
            flash("Se elimino " + file_name)

            resultado_eliminar2 = db.session.query(
                t_archivo).filter_by(A_nombre=file_name).first()
            db.session.delete(resultado_eliminar2)
            db.session.commit()

            accion = "eliminar"

            return redirect("/InterArchivo/"+Codigo+"/"+accion)
        except OSError:
            flash("no se pudo borrar", file_name)
            accion = "eliminar"
            return redirect("/InterArchivo/"+Codigo+"/"+accion)


@archivoss.route("/descargarArchivos/<string:Codigo>/<string:filename>", methods=['GET'])
@login_required
def descargarArchivos(Codigo, filename):

    return send_from_directory(directory="static/archivos/"+Codigo, path=filename, as_attachment=True)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404


@archivoss.route("/Volver/<string:Codigo>", methods=['GET'])
@login_required
def Volver(Codigo):
    buscar = db.session.query(
        t_seguimiento).filter_by(Codigo=Codigo).first()

    buscar2 = db.session.query(
        t_archivo).filter_by(Codigo=Codigo).first()

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
                               ColClE380PLP=ColClE380PLP, ColPU=ColPU, ColGI=ColGI, ColOb=ColOb, fecha_modificacion=fecha_modificacion, buscar2=buscar2)

    return render_template("/ActualizaElimina.html", R_empresa=R_empresa, Funcionaless=Funcionaless, buscar=buscar, color=colorPeticion, colorVOF=colorVOF, ColVf=ColVf, ColE380=ColE380, ColVUaT=ColVUaT, ColOE=ColOE, ColOt=ColOt, ColE=ColE, ColPi=ColPi, ColNR=ColNR, ColFDFD=ColFDFD,
                           ColCLFD=ColCLFD, ColSPSP=ColSPSP, ColE420DT=ColE420DT, ColE420CL=ColE420CL, ColE380PLP=ColE380PLP,
                           ColClE380PLP=ColClE380PLP, ColPU=ColPU, ColGI=ColGI, ColOb=ColOb, fecha_actual=fecha_actual, fecha_modificacion=fecha_modificacion, buscar2=buscar2)


def status_401(error):
    return redirect("/")


def status_404(error):
    return "<h1>pagina no encontrada</h1>", 404
