import secrets
import string

from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password, identify_hasher
from django.core.mail import send_mail
from django.db import transaction

from sistema_erp import validaciones as v
from sistema_erp.errores import ErrorValidacion, NoEncontrado, SinPermiso
from sistema_erp.sesion import (
    crear_token, exigir_rol, ESTADOS_SIN_ACCESO, ADMINISTRADOR, AUXILIAR,
)
from usuarios.repository import UsuarioRepository
from usuarios.entity import Usuario
from usuarios.dto import UsuarioRespuestaDTO
from usuarios.service.registro_bitacora_service import BitacoraService


# el que crea y modifica usuarios es el auxiliar administrativo, el administrador (gerente) solo consulta
ROLES_GESTIONAN_USUARIOS = (AUXILIAR,)
ROLES_CONSULTAN_USUARIOS = (ADMINISTRADOR, AUXILIAR)

ESTADO_INICIAL = "Contratado"


def generar_contrasenia(largo=10):
    """contraseña aleatoria con mayuscula, minuscula, numero y simbolo, sin letras que se confunden (O/0, l/1)"""
    mayus = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    minus = "abcdefghijkmnpqrstuvwxyz"
    numeros = "23456789"
    simbolos = "@#$%*!?"
    obligatorios = [secrets.choice(mayus), secrets.choice(minus), secrets.choice(numeros), secrets.choice(simbolos)]
    resto = [secrets.choice(mayus + minus + numeros) for _ in range(largo - len(obligatorios))]
    caracteres = obligatorios + resto
    secrets.SystemRandom().shuffle(caracteres)
    return "".join(caracteres)


def enviar_correo_bienvenida(usuario, contrasenia):
    asunto = "Tu acceso al sistema Kinetix IT"
    mensaje = (
        f"Hola {usuario.primer_nombre},\n\n"
        f"Se creó tu usuario en el sistema Kinetix IT.\n\n"
        f"Usuario: {usuario.nombre_usuario}\n"
        f"Correo: {usuario.correo}\n"
        f"Contraseña temporal: {contrasenia}\n\n"
        f"Puedes entrar con tu correo o tu usuario. Te recomendamos cambiar la contraseña "
        f"desde 'Mi perfil' apenas ingreses.\n\n"
        f"Este es un mensaje automático, no lo respondas."
    )
    send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [usuario.correo], fail_silently=False)
    if settings.EMAIL_BACKEND.endswith("console.EmailBackend"):
        # sin correo configurado: se deja la contraseña legible en la consola para poder probar
        print(f"\n[correo de prueba] usuario: {usuario.nombre_usuario} | contraseña: {contrasenia}\n", flush=True)


def a_dto(u):
    return UsuarioRespuestaDTO(
        id_usuario=u.id_usuario,
        nombre_usuario=u.nombre_usuario,
        primer_nombre=u.primer_nombre,
        segundo_nombre=u.segundo_nombre,
        primer_apellido=u.primer_apellido,
        segundo_apellido=u.segundo_apellido,
        correo=u.correo,
        numero_documento=u.numero_documento,
        id_rol=u.rol.id_rol,
        nombre_rol=u.rol.nombre,
        id_tipo_documento=u.tipo_documento.id_tipo_documento,
        nombre_tipo_documento=u.tipo_documento.nombre,
        id_estado_usuario=u.estado_usuario.id_estado_usuario,
        nombre_estado_usuario=u.estado_usuario.nombre,
    )


def validar_datos_basicos(dto, errores, excluir_id=None):
    """validaciones que aplican igual al crear y al editar"""
    datos = {
        "nombre_usuario": v.nombre_usuario(errores, "nombre_usuario", dto.nombre_usuario),
        "primer_nombre": v.nombre_persona(errores, "primer_nombre", dto.primer_nombre, "El primer nombre"),
        "segundo_nombre": v.nombre_persona(errores, "segundo_nombre", dto.segundo_nombre, "El segundo nombre", requerido=False),
        "primer_apellido": v.nombre_persona(errores, "primer_apellido", dto.primer_apellido, "El primer apellido"),
        "segundo_apellido": v.nombre_persona(errores, "segundo_apellido", dto.segundo_apellido, "El segundo apellido", requerido=False),
        "correo": v.correo(errores, "correo", dto.correo),
        "id_rol": v.entero(errores, "id_rol", dto.id_rol, "El rol", minimo=1),
        "id_tipo_documento": v.entero(errores, "id_tipo_documento", dto.id_tipo_documento, "El tipo de documento", minimo=1),
    }
    datos["numero_documento"] = v.numero_documento(errores, "numero_documento", dto.numero_documento, datos["id_tipo_documento"])

    # que existan en la bd
    if datos["id_rol"] and "id_rol" not in errores and not UsuarioRepository.obtener_rol(datos["id_rol"]):
        errores["id_rol"] = "El rol seleccionado no existe"
    if datos["id_tipo_documento"] and "id_tipo_documento" not in errores and not UsuarioRepository.obtener_tipo_documento(datos["id_tipo_documento"]):
        errores["id_tipo_documento"] = "El tipo de documento seleccionado no existe"

    # que no esten repetidos
    if datos["nombre_usuario"] and "nombre_usuario" not in errores and UsuarioRepository.existe_nombre_usuario(datos["nombre_usuario"], excluir_id):
        errores["nombre_usuario"] = "Ya existe un usuario con ese nombre de usuario"
    if datos["correo"] and "correo" not in errores and UsuarioRepository.existe_correo(datos["correo"], excluir_id):
        errores["correo"] = "Ya existe un usuario con ese correo"
    if datos["numero_documento"] and "numero_documento" not in errores and UsuarioRepository.existe_documento(datos["numero_documento"], excluir_id):
        errores["numero_documento"] = "Ya existe un usuario con ese número de documento"

    if (datos["primer_nombre"] and datos["segundo_nombre"] and "segundo_nombre" not in errores
            and datos["primer_nombre"].lower() == datos["segundo_nombre"].lower()):
        errores["segundo_nombre"] = "El segundo nombre no puede ser igual al primero"
    return datos


class UsuarioService:

    @staticmethod
    def listar_usuarios(responsable):
        exigir_rol(responsable, *ROLES_CONSULTAN_USUARIOS)
        return [a_dto(u) for u in UsuarioRepository.obtener_todos()]

    @staticmethod
    def obtener_usuario(id_usuario):
        usuario = UsuarioRepository.obtener_por_id(id_usuario)
        if not usuario:
            raise NoEncontrado("El usuario no existe")
        return a_dto(usuario)

    @staticmethod
    @transaction.atomic
    def crear_usuario(dto_crear, responsable):
        exigir_rol(responsable, *ROLES_GESTIONAN_USUARIOS)

        errores = {}
        datos = validar_datos_basicos(dto_crear, errores)
        if errores:
            raise ErrorValidacion(errores)

        estado = UsuarioRepository.obtener_estado_por_nombre(ESTADO_INICIAL)
        if not estado:
            raise ErrorValidacion("No existe el estado 'Contratado' en la base de datos")

        contrasenia = generar_contrasenia()
        usuario = Usuario(
            nombre_usuario=datos["nombre_usuario"],
            primer_nombre=datos["primer_nombre"],
            segundo_nombre=datos["segundo_nombre"],
            primer_apellido=datos["primer_apellido"],
            segundo_apellido=datos["segundo_apellido"],
            correo=datos["correo"],
            numero_documento=datos["numero_documento"],
            contrasenia=make_password(contrasenia),
            rol_id=datos["id_rol"],
            tipo_documento_id=datos["id_tipo_documento"],
            estado_usuario_id=estado.id_estado_usuario,
        )
        usuario_guardado = UsuarioRepository.guardar(usuario)

        # si el correo no se puede enviar se deshace todo, para no dejar un usuario que no conoce su contraseña
        try:
            enviar_correo_bienvenida(usuario_guardado, contrasenia)
        except Exception as e:
            raise ErrorValidacion({"correo": "No se pudo enviar el correo con la contraseña, el usuario no se creó (" + str(e) + ")"})

        BitacoraService.registrar_evento(
            id_usuario_afectado=usuario_guardado.id_usuario,
            id_usuario_responsable=responsable.id_usuario,
            accion="CREAR_USUARIO",
            cambio_realizado=f"Se creó el usuario '{usuario_guardado.nombre_usuario}' con correo '{usuario_guardado.correo}' en estado {ESTADO_INICIAL}. La contraseña se envió al correo.",
        )
        return usuario_guardado.id_usuario

    @staticmethod
    @transaction.atomic
    def actualizar_usuario(id_usuario, dto_actualizar, responsable):
        exigir_rol(responsable, *ROLES_GESTIONAN_USUARIOS)

        usuario = UsuarioRepository.obtener_por_id(id_usuario)
        if not usuario:
            raise NoEncontrado("El usuario no existe")

        errores = {}
        datos = validar_datos_basicos(dto_actualizar, errores, excluir_id=usuario.id_usuario)
        id_estado = v.entero(errores, "id_estado_usuario", dto_actualizar.id_estado_usuario, "El estado", minimo=1)
        if id_estado and "id_estado_usuario" not in errores and not UsuarioRepository.obtener_estado(id_estado):
            errores["id_estado_usuario"] = "El estado seleccionado no existe"

        # el documento no se puede cambiar despues de creado (la bd tambien lo bloquea con un trigger)
        if datos["id_tipo_documento"] and datos["id_tipo_documento"] != usuario.tipo_documento_id:
            errores["id_tipo_documento"] = "El tipo de documento no se puede modificar"
        if datos["numero_documento"] and datos["numero_documento"] != usuario.numero_documento:
            errores["numero_documento"] = "El número de documento no se puede modificar"

        # nadie se cambia su propio rol ni su propio estado, asi no se queda sin acceso por error
        if usuario.id_usuario == responsable.id_usuario:
            if datos["id_rol"] and datos["id_rol"] != usuario.rol_id:
                errores["id_rol"] = "No puedes cambiar tu propio rol"
            if id_estado and id_estado != usuario.estado_usuario_id:
                errores["id_estado_usuario"] = "No puedes cambiar tu propio estado"

        if errores:
            raise ErrorValidacion(errores)

        antes = {
            "nombre de usuario": usuario.nombre_usuario,
            "primer nombre": usuario.primer_nombre,
            "segundo nombre": usuario.segundo_nombre,
            "primer apellido": usuario.primer_apellido,
            "segundo apellido": usuario.segundo_apellido,
            "correo": usuario.correo,
            "rol": usuario.rol.nombre,
            "estado": usuario.estado_usuario.nombre,
        }

        usuario.nombre_usuario = datos["nombre_usuario"]
        usuario.primer_nombre = datos["primer_nombre"]
        usuario.segundo_nombre = datos["segundo_nombre"]
        usuario.primer_apellido = datos["primer_apellido"]
        usuario.segundo_apellido = datos["segundo_apellido"]
        usuario.correo = datos["correo"]
        usuario.rol_id = datos["id_rol"]
        usuario.estado_usuario_id = id_estado
        UsuarioRepository.actualizar(usuario)
        usuario = UsuarioRepository.obtener_por_id(usuario.id_usuario)

        despues = {
            "nombre de usuario": usuario.nombre_usuario,
            "primer nombre": usuario.primer_nombre,
            "segundo nombre": usuario.segundo_nombre,
            "primer apellido": usuario.primer_apellido,
            "segundo apellido": usuario.segundo_apellido,
            "correo": usuario.correo,
            "rol": usuario.rol.nombre,
            "estado": usuario.estado_usuario.nombre,
        }
        cambios = [f"{campo}: '{antes[campo] or ''}' → '{despues[campo] or ''}'" for campo in antes if antes[campo] != despues[campo]]
        if not cambios:
            return usuario.id_usuario

        solo_estado = len(cambios) == 1 and antes["estado"] != despues["estado"]
        BitacoraService.registrar_evento(
            id_usuario_afectado=usuario.id_usuario,
            id_usuario_responsable=responsable.id_usuario,
            accion="CAMBIO_ESTADO_USUARIO" if solo_estado else "ACTUALIZAR_USUARIO",
            cambio_realizado=f"Usuario '{usuario.nombre_usuario}': " + "; ".join(cambios),
        )
        return usuario.id_usuario

    @staticmethod
    def cambiar_contrasenia(dto, usuario):
        errores = {}
        if not dto.contrasenia_actual or not isinstance(dto.contrasenia_actual, str):
            errores["contrasenia_actual"] = "Escribe tu contraseña actual"
        elif not check_password(dto.contrasenia_actual, usuario.contrasenia):
            errores["contrasenia_actual"] = "La contraseña actual no es correcta"

        nueva = v.contrasenia_segura(errores, "contrasenia_nueva", dto.contrasenia_nueva, "La nueva contraseña")
        if nueva and "contrasenia_nueva" not in errores:
            if dto.contrasenia_actual and nueva == dto.contrasenia_actual:
                errores["contrasenia_nueva"] = "La nueva contraseña debe ser diferente a la actual"
            elif usuario.nombre_usuario.lower() in nueva.lower():
                errores["contrasenia_nueva"] = "La contraseña no puede contener tu nombre de usuario"
        if nueva and dto.confirmacion != nueva:
            errores["confirmacion"] = "Las contraseñas no coinciden"
        if errores:
            raise ErrorValidacion(errores)

        usuario.contrasenia = make_password(nueva)
        UsuarioRepository.actualizar(usuario)
        BitacoraService.registrar_evento(
            id_usuario_afectado=usuario.id_usuario,
            id_usuario_responsable=usuario.id_usuario,
            accion="CAMBIO_CONTRASENIA",
            cambio_realizado=f"El usuario '{usuario.nombre_usuario}' cambió su contraseña.",
        )

    @staticmethod
    def iniciar_sesion(dto_login):
        errores = {}
        dato = v.limpiar(dto_login.usuario) if isinstance(dto_login.usuario, str) else None
        if not dato:
            errores["correo"] = "Escribe tu correo o nombre de usuario"
        if not dto_login.contrasenia or not isinstance(dto_login.contrasenia, str):
            errores["contrasenia"] = "Escribe tu contraseña"
        if errores:
            raise ErrorValidacion(errores)

        usuario = UsuarioRepository.obtener_por_correo(dato) or UsuarioRepository.obtener_por_nombre_usuario(dato)
        if not usuario:
            return None

        try:
            identify_hasher(usuario.contrasenia)
            es_valida = check_password(dto_login.contrasenia, usuario.contrasenia)
        except ValueError:
            # contraseñas viejas guardadas en texto plano: si coincide se cifra de una vez
            es_valida = usuario.contrasenia == dto_login.contrasenia
            if es_valida:
                usuario.contrasenia = make_password(dto_login.contrasenia)
                UsuarioRepository.actualizar(usuario)

        if not es_valida:
            return None
        if usuario.estado_usuario.nombre in ESTADOS_SIN_ACCESO:
            raise SinPermiso("El usuario está " + usuario.estado_usuario.nombre.lower() + " y no puede entrar al sistema")

        BitacoraService.registrar_evento(
            id_usuario_afectado=usuario.id_usuario,
            id_usuario_responsable=usuario.id_usuario,
            accion="INICIO_SESION",
            cambio_realizado=f"El usuario '{usuario.nombre_usuario}' inició sesión.",
        )

        return {
            "token": crear_token(usuario.id_usuario),
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "primer_nombre": usuario.primer_nombre,
            "primer_apellido": usuario.primer_apellido,
            "correo": usuario.correo,
            "id_rol": usuario.rol.id_rol,
            "rol": usuario.rol.nombre,
            "estado": usuario.estado_usuario.nombre,
        }
