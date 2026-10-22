from django.http import JsonResponse

from sistema_erp.respuestas import vista_api, leer_json
from sistema_erp.sesion import usuario_actual
from usuarios.service import UsuarioService
from usuarios.dto import UsuarioCrearDTO, UsuarioActualizarDTO, CambioContraseniaDTO, LoginDTO


def a_json(u):
    return {
        "id_usuario": u.id_usuario,
        "nombre_usuario": u.nombre_usuario,
        "primer_nombre": u.primer_nombre,
        "segundo_nombre": u.segundo_nombre,
        "primer_apellido": u.primer_apellido,
        "segundo_apellido": u.segundo_apellido,
        "correo": u.correo,
        "numero_documento": u.numero_documento,
        "id_rol": u.id_rol,
        "rol": u.nombre_rol,
        "id_tipo_documento": u.id_tipo_documento,
        "tipo_documento": u.nombre_tipo_documento,
        "id_estado_usuario": u.id_estado_usuario,
        "estado": u.nombre_estado_usuario,
    }


@vista_api('GET')
def listar_usuarios_view(request):
    responsable = usuario_actual(request)
    usuarios = UsuarioService.listar_usuarios(responsable)
    return JsonResponse({"status": "success", "data": [a_json(u) for u in usuarios]})


@vista_api('GET')
def mi_perfil_view(request):
    usuario = usuario_actual(request)
    return JsonResponse({"status": "success", "data": a_json(UsuarioService.obtener_usuario(usuario.id_usuario))})


@vista_api('POST')
def crear_usuario_view(request):
    responsable = usuario_actual(request)
    data = leer_json(request)
    dto = UsuarioCrearDTO(
        nombre_usuario=data.get('nombre_usuario'),
        primer_nombre=data.get('primer_nombre'),
        segundo_nombre=data.get('segundo_nombre'),
        primer_apellido=data.get('primer_apellido'),
        segundo_apellido=data.get('segundo_apellido'),
        correo=data.get('correo'),
        numero_documento=data.get('numero_documento'),
        id_rol=data.get('id_rol'),
        id_tipo_documento=data.get('id_tipo_documento'),
    )
    nuevo_id = UsuarioService.crear_usuario(dto, responsable)
    return JsonResponse({
        "status": "success",
        "message": "Usuario creado. La contraseña se envió a su correo.",
        "id_usuario": nuevo_id
    }, status=201)


@vista_api('PUT')
def actualizar_usuario_view(request, id_usuario):
    responsable = usuario_actual(request)
    data = leer_json(request)
    dto = UsuarioActualizarDTO(
        nombre_usuario=data.get('nombre_usuario'),
        primer_nombre=data.get('primer_nombre'),
        segundo_nombre=data.get('segundo_nombre'),
        primer_apellido=data.get('primer_apellido'),
        segundo_apellido=data.get('segundo_apellido'),
        correo=data.get('correo'),
        numero_documento=data.get('numero_documento'),
        id_rol=data.get('id_rol'),
        id_tipo_documento=data.get('id_tipo_documento'),
        id_estado_usuario=data.get('id_estado_usuario'),
    )
    UsuarioService.actualizar_usuario(id_usuario, dto, responsable)
    return JsonResponse({"status": "success", "message": "Usuario actualizado"}, status=200)


@vista_api('POST')
def cambiar_contrasenia_view(request):
    usuario = usuario_actual(request)
    data = leer_json(request)
    dto = CambioContraseniaDTO(
        contrasenia_actual=data.get('contrasenia_actual'),
        contrasenia_nueva=data.get('contrasenia_nueva'),
        confirmacion=data.get('confirmacion'),
    )
    UsuarioService.cambiar_contrasenia(dto, usuario)
    return JsonResponse({"status": "success", "message": "Contraseña actualizada"}, status=200)


@vista_api('POST')
def login_view(request):
    data = leer_json(request)
    dto = LoginDTO(
        usuario=data.get('correo') or data.get('nombre_usuario'),
        contrasenia=data.get('contrasenia')
    )
    sesion = UsuarioService.iniciar_sesion(dto)
    if sesion is None:
        return JsonResponse({"status": "error", "message": "Correo o contraseña incorrectos"}, status=401)
    return JsonResponse({"status": "success", "message": "Bienvenido", "data": sesion}, status=200)
