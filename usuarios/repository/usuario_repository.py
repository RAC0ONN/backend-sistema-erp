from usuarios.entity import Usuario, Rol, TipoDocumento, EstadoUsuario
from django.core.exceptions import ObjectDoesNotExist


class UsuarioRepository:

    @staticmethod
    def obtener_todos():
        return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').all().order_by('id_usuario')

    @staticmethod
    def obtener_por_id(id_usuario):
        try:
            return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').get(pk=id_usuario)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def obtener_por_correo(correo: str):
        return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').filter(correo__iexact=correo).first()

    @staticmethod
    def obtener_por_nombre_usuario(nombre_usuario: str):
        return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').filter(nombre_usuario__iexact=nombre_usuario).first()

    # para revisar duplicados sin importar mayusculas, excluyendo al mismo usuario cuando se edita
    @staticmethod
    def existe_nombre_usuario(nombre_usuario, excluir_id=None):
        return Usuario.objects.filter(nombre_usuario__iexact=nombre_usuario).exclude(pk=excluir_id).exists()

    @staticmethod
    def existe_correo(correo, excluir_id=None):
        return Usuario.objects.filter(correo__iexact=correo).exclude(pk=excluir_id).exists()

    @staticmethod
    def existe_documento(numero_documento, excluir_id=None):
        return Usuario.objects.filter(numero_documento=numero_documento).exclude(pk=excluir_id).exists()

    @staticmethod
    def obtener_rol(id_rol):
        return Rol.objects.filter(pk=id_rol).first()

    @staticmethod
    def obtener_tipo_documento(id_tipo_documento):
        return TipoDocumento.objects.filter(pk=id_tipo_documento).first()

    @staticmethod
    def obtener_estado(id_estado_usuario):
        return EstadoUsuario.objects.filter(pk=id_estado_usuario).first()

    @staticmethod
    def obtener_estado_por_nombre(nombre):
        return EstadoUsuario.objects.filter(nombre__iexact=nombre).first()

    @staticmethod
    def guardar(usuario: Usuario):
        usuario.save()
        return usuario

    @staticmethod
    def actualizar(usuario: Usuario):
        usuario.save()
        return usuario
