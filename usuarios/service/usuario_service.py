from django.contrib.auth.hashers import make_password, check_password, identify_hasher
from django.core import signing

from usuarios.repository import UsuarioRepository
from usuarios.entity import Usuario, Rol, TipoDocumento, EstadoUsuario
from usuarios.dto import UsuarioRespuestaDTO

# estados que no pueden entrar al sistema
ESTADOS_SIN_ACCESO = ('Suspendido', 'Retirado')


def limpiar(texto):
    # quita espacios y tabulaciones de más al inicio y al final
    return texto.strip() if isinstance(texto, str) else texto


class UsuarioService:

    @staticmethod
    def listar_usuarios():
        usuarios = UsuarioRepository.obtener_todos()
        resultado = []
        for u in usuarios:
            dto = UsuarioRespuestaDTO(
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
                nombre_estado_usuario=u.estado_usuario.nombre
            )
            resultado.append(dto)
        return resultado

    @staticmethod
    def crear_usuario(dto_crear):
        
        usuario = Usuario(
            nombre_usuario=limpiar(dto_crear.nombre_usuario),
            primer_nombre=limpiar(dto_crear.primer_nombre),
            segundo_nombre=limpiar(dto_crear.segundo_nombre),
            primer_apellido=limpiar(dto_crear.primer_apellido),
            segundo_apellido=limpiar(dto_crear.segundo_apellido),
            correo=limpiar(dto_crear.correo),
            numero_documento=limpiar(dto_crear.numero_documento),
            contrasenia=make_password(dto_crear.contrasenia),  # la contraseña se guarda cifrada, no en texto plano
            rol_id=dto_crear.id_rol,
            tipo_documento_id=dto_crear.id_tipo_documento,
            estado_usuario_id=dto_crear.id_estado_usuario
        )
        usuario_guardado = UsuarioRepository.guardar(usuario)
        return usuario_guardado.id_usuario
    
    @staticmethod
    def actualizar_usuario(id_usuario: int, dto_actualizar):
        usuario = UsuarioRepository.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe")
        usuario.nombre_usuario = limpiar(dto_actualizar.nombre_usuario)
        usuario.primer_nombre = limpiar(dto_actualizar.primer_nombre)
        usuario.segundo_nombre = limpiar(dto_actualizar.segundo_nombre)
        usuario.primer_apellido = limpiar(dto_actualizar.primer_apellido)
        usuario.segundo_apellido = limpiar(dto_actualizar.segundo_apellido)
        usuario.correo = limpiar(dto_actualizar.correo)
        usuario.numero_documento = limpiar(dto_actualizar.numero_documento)
        usuario.rol_id = dto_actualizar.id_rol
        usuario.tipo_documento_id = dto_actualizar.id_tipo_documento
        usuario.estado_usuario_id = dto_actualizar.id_estado_usuario
        usuario_actualizado = UsuarioRepository.actualizar(usuario)
        return usuario_actualizado.id_usuario

    @staticmethod
    def eliminar_usuario(id_usuario: int):
        usuario = UsuarioRepository.obtener_por_id(id_usuario)
        if not usuario:
            raise ValueError("El usuario no existe")
        return UsuarioRepository.eliminar(usuario)

    @staticmethod
    def iniciar_sesion(dto_login):
        # se puede entrar con el correo o con el nombre de usuario
        dato = limpiar(dto_login.usuario) or ''
        usuario = UsuarioRepository.obtener_por_correo(dato) or UsuarioRepository.obtener_por_nombre_usuario(dato)
        if not usuario or not dto_login.contrasenia:
            return None

        try:
            identify_hasher(usuario.contrasenia)
            es_valida = check_password(dto_login.contrasenia, usuario.contrasenia)
        except ValueError:
            # usuarios creados antes del cifrado: se compara normal y se cifra de una vez
            es_valida = usuario.contrasenia == dto_login.contrasenia
            if es_valida:
                usuario.contrasenia = make_password(dto_login.contrasenia)
                UsuarioRepository.actualizar(usuario)

        if not es_valida:
            return None
        if usuario.estado_usuario.nombre in ESTADOS_SIN_ACCESO:
            raise PermissionError("El usuario está " + usuario.estado_usuario.nombre.lower() + " y no puede entrar al sistema")

        token = signing.dumps({"id_usuario": usuario.id_usuario}, salt="login")
        return {
            "token": token,
            "id_usuario": usuario.id_usuario,
            "nombre_usuario": usuario.nombre_usuario,
            "primer_nombre": usuario.primer_nombre,
            "primer_apellido": usuario.primer_apellido,
            "correo": usuario.correo,
            "id_rol": usuario.rol.id_rol,
            "rol": usuario.rol.nombre,
            "estado": usuario.estado_usuario.nombre
        }
