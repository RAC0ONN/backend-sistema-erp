from usuarios.repository import UsuarioRepository
from usuarios.entity import Usuario, Rol, TipoDocumento, EstadoUsuario
from usuarios.dto import UsuarioRespuestaDTO

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
            nombre_usuario=dto_crear.nombre_usuario,
            primer_nombre=dto_crear.primer_nombre,
            segundo_nombre=dto_crear.segundo_nombre,
            primer_apellido=dto_crear.primer_apellido,
            segundo_apellido=dto_crear.segundo_apellido,
            correo=dto_crear.correo,
            numero_documento=dto_crear.numero_documento,
            contrasenia=dto_crear.contrasenia,  
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
        usuario.nombre_usuario = dto_actualizar.nombre_usuario
        usuario.primer_nombre = dto_actualizar.primer_nombre
        usuario.segundo_nombre = dto_actualizar.segundo_nombre
        usuario.primer_apellido = dto_actualizar.primer_apellido
        usuario.segundo_apellido = dto_actualizar.segundo_apellido
        usuario.correo = dto_actualizar.correo
        usuario.numero_documento = dto_actualizar.numero_documento
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