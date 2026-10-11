from usuarios.entity import Usuario
from django.core.exceptions import ObjectDoesNotExist

class UsuarioRepository:
    
    @staticmethod
    def obtener_todos():
        return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').all()

    @staticmethod
    def obtener_por_id(id_usuario: int):
        try:
            return Usuario.objects.select_related('rol', 'tipo_documento', 'estado_usuario').get(pk=id_usuario)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def guardar(usuario: Usuario):
        usuario.save()
        return usuario

    @staticmethod
    def eliminar(usuario: Usuario):
        usuario.delete()
        return True

    @staticmethod
    def actualizar(usuario: Usuario):
        usuario.save()
        return usuario