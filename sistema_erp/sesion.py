from django.core import signing

from sistema_erp.errores import NoAutenticado, SinPermiso

# nombres iguales a la tabla rol
ADMINISTRADOR = "Administrador"
VENDEDOR = "Vendedor"
AUXILIAR = "Auxiliar administrativo"

ESTADOS_SIN_ACCESO = ("Suspendido", "Retirado")

SALT = "login"
DURACION_SESION = 60 * 60 * 12  # 12 horas, despues toca volver a iniciar sesion


def crear_token(id_usuario):
    return signing.dumps({"id_usuario": id_usuario}, salt=SALT)


def usuario_actual(request):
    """saca el usuario del token que manda el front en el header Authorization: Bearer <token>"""
    from usuarios.repository import UsuarioRepository

    encabezado = request.META.get("HTTP_AUTHORIZATION", "")
    if not encabezado.startswith("Bearer "):
        raise NoAutenticado("Debes iniciar sesión")

    try:
        datos = signing.loads(encabezado[7:].strip(), salt=SALT, max_age=DURACION_SESION)
    except signing.SignatureExpired:
        raise NoAutenticado("Tu sesión expiró, vuelve a iniciar sesión")
    except signing.BadSignature:
        raise NoAutenticado("Sesión no válida, vuelve a iniciar sesión")

    usuario = UsuarioRepository.obtener_por_id(datos.get("id_usuario"))
    if not usuario:
        raise NoAutenticado("Sesión no válida, vuelve a iniciar sesión")
    # si lo suspendieron o retiraron mientras tenia la sesion abierta, se le corta el acceso
    if usuario.estado_usuario.nombre in ESTADOS_SIN_ACCESO:
        raise NoAutenticado("Tu usuario está " + usuario.estado_usuario.nombre.lower() + " y no puede usar el sistema")
    return usuario


def exigir_rol(usuario, *roles):
    if usuario.rol.nombre not in roles:
        raise SinPermiso("Tu rol (" + usuario.rol.nombre + ") no tiene permiso para hacer esto")
