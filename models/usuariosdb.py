from utils.db import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin


def get_user(id):
    user = db.session.query(usuariosNew).filter_by(id=id).first()

    return user


class usuariosNew(db.Model, UserMixin):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    num_doc = db.Column(db.String(100))
    contrasena = db.Column(db.String(100))
    Rol = db.Column(db.String(100))

    def __init__(self,  nombre, num_doc, contrasena, Rol):

        self.nombre = nombre
        self.num_doc = num_doc
        self.contrasena = contrasena
        self.Rol = Rol


class estados(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(100))
    claseEstado = db.Column(db.String(100))

    def __init__(self,  estado, claseEstado):

        self.estado = estado
        self.claseEstado = claseEstado


class t_empresas(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    E_nombre = db.Column(db.String(100))

    def __init__(self, E_nombre):

        self.E_nombre = E_nombre


class Funcionales(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    F_nombre = db.Column(db.String(100))

    def __init__(self, F_nombre):

        self.F_nombre = F_nombre
        
class t_archivo(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    Codigo = db.Column(db.String(100))
    A_nombre = db.Column(db.String(100))

    def __init__(self, Codigo,A_nombre):
        
        self.Codigo = Codigo

        self.A_nombre = A_nombre
        
        
class acciones(db.Model):  # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(100))
    color_name = db.Column(db.String(100))

    def __init__(self, accion,color_name):
        
        self.accion = accion

        self.color_name = color_name


class t_seguimiento(db.Model):   # type: ignore

    id = db.Column(db.Integer, primary_key=True)
    Codigo = db.Column(db.String(100))
    Empresa = db.Column(db.String(100))
    issue = db.Column(db.String(100))
    Nombre_Iniciativa = db.Column(db.String(500))
    RESPONSABLE = db.Column(db.String(100))
    PETICION = db.Column(db.String(100))
    VoBo_Oferta_EX = db.Column(db.String(100))
    VoBo_FunctionalDesign_EX = db.Column(db.String(100))
    VoBo_E380_EX = db.Column(db.String(100))
    VoBo_E380_UAT_EX = db.Column(db.String(100))
    Oferta_Economica = db.Column(db.String(100))
    Oferta_Tecnica = db.Column(db.String(100))
    Estimador = db.Column(db.String(100))
    Plan_Interno = db.Column(db.String(100))
    Nivel_de_Riesgo_de_Producto = db.Column(db.String(100))
    FD_Functional_Design = db.Column(db.String(100))
    CL_Functional_Design = db.Column(db.String(100))
    SP_Set_Pruebas = db.Column(db.String(100))
    E420_Diseño_Tecnico = db.Column(db.String(100))
    CL_E420_Diseno_Tecnico = db.Column(db.String(100))
    E380_Plan_Pruebas = db.Column(db.String(100))
    CL_E380_Plan_Pruebas = db.Column(db.String(100))
    Plan_Pruebas_Unitarias = db.Column(db.String(100))
    Guia_Integracion = db.Column(db.String(100))
    Observacion = db.Column(db.Text)
    fecha_actual = db.Column(db.String(100))
    fecha_modificacion = db.Column(db.String(100))
    usuario = db.Column(db.String(100))

    def __init__(self, Codigo, Empresa, issue, Nombre_Iniciativa, RESPONSABLE, PETICION, VoBo_Oferta_EX, VoBo_FunctionalDesign_EX,
                 VoBo_E380_EX, VoBo_E380_UAT_EX, Oferta_Economica, Oferta_Tecnica, Estimador, Plan_Interno,
                 Nivel_de_Riesgo_de_Producto, FD_Functional_Design, CL_Functional_Design, SP_Set_Pruebas,
                 E420_Diseño_Tecnico, CL_E420_Diseno_Tecnico, E380_Plan_Pruebas, CL_E380_Plan_Pruebas, Plan_Pruebas_Unitarias, Guia_Integracion, Observacion, fecha_actual, fecha_modificacion, usuario):

        self.Codigo = Codigo
        self.Empresa = Empresa
        self.issue = issue
        self.Nombre_Iniciativa = Nombre_Iniciativa
        self.RESPONSABLE = RESPONSABLE
        self.PETICION = PETICION
        self.VoBo_Oferta_EX = VoBo_Oferta_EX
        self.VoBo_FunctionalDesign_EX = VoBo_FunctionalDesign_EX
        self.VoBo_E380_EX = VoBo_E380_EX
        self.VoBo_E380_UAT_EX = VoBo_E380_UAT_EX
        self.Oferta_Economica = Oferta_Economica
        self.Oferta_Tecnica = Oferta_Tecnica
        self.Estimador = Estimador
        self.Plan_Interno = Plan_Interno
        self.Nivel_de_Riesgo_de_Producto = Nivel_de_Riesgo_de_Producto
        self.FD_Functional_Design = FD_Functional_Design
        self.CL_Functional_Design = CL_Functional_Design
        self.SP_Set_Pruebas = SP_Set_Pruebas
        self.E420_Diseño_Tecnico = E420_Diseño_Tecnico
        self.CL_E420_Diseno_Tecnico = CL_E420_Diseno_Tecnico
        self.E380_Plan_Pruebas = E380_Plan_Pruebas
        self.CL_E380_Plan_Pruebas = CL_E380_Plan_Pruebas
        self.Plan_Pruebas_Unitarias = Plan_Pruebas_Unitarias
        self.Guia_Integracion = Guia_Integracion
        self.Observacion = Observacion
        self.fecha_actual = fecha_actual
        self.fecha_modificacion = fecha_modificacion
        self.usuario = usuario
