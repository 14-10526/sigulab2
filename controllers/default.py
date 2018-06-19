# -------------------------------------------------------------------------
# Controladores Basicos
# - index sera la accion basica de la aplicacion donde se muestran los modulos de SMyDP, Personal y servicios
#
# - download y call son ejemplos de aplicaciones basicas de web2py.
# -------------------------------------------------------------------------

# Pagina principal 
@auth.requires_login(otherwise=URL('modulos', 'login'))
def index():
    val = contar_notificaciones();
    session.validaciones_pendientes = val
    return dict()

def register():
    return redirect(URL('modulos','register'))

def recoverpassword():
    return dict(form=auth.reset_password())

# Inicio de Sesion
def login():
    return redirect(URL('modulos', 'login', vars=dict(error='invalid_data')))

def contar_notificaciones():
    usuario =db(db.t_Personal.f_email == auth.user.email).select(db.t_Personal.ALL)
    if(len(usuario)>1): usuario = usuario[1]
    else: usuario = usuario.first()
    print("---------------------------------------")
    print("Nombre: "+usuario.f_nombre+" /// Correo: "+str(usuario.f_email)+" ///Dependencia: "+str(usuario.f_dependencia))
    es_supervisor = usuario.f_es_supervisor
    dependencia = None
    if es_supervisor:
        if(auth.user.email == "sigulabusb@gmail.com") or (auth.user.email == "asis-ulab@usb.ve"):
            notif = db(db.t_Personal.f_por_validar == True).count()
        else:
            dependencia = usuario.f_dependencia
            notif = db((db.t_Personal.f_dependencia == dependencia)&(db.t_Personal.f_es_supervisor == False)&(db.t_Personal.f_por_validar == True)).count()
    return notif

#--------------------------------------
# Otras Funcionalidades Basicas
#--------------------------------------

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
