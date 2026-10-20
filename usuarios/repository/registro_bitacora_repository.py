from usuarios.entity.registro_bitacora import RegistroBitacora
from django.core.exceptions import ObjectDoesNotExist

class BitacoraRepository:

    @staticmethod
    def obtener_todos():
        return RegistroBitacora.objects.select_related(
            'id_usuario_afectado', 
            'id_usuario_responsable'
        ).all().order_by('-fecha')

    @staticmethod
    def obtener_por_id(id_registro_bitacora: int):
        try:
            return RegistroBitacora.objects.select_related(
                'id_usuario_afectado', 
                'id_usuario_responsable'
            ).get(pk=id_registro_bitacora)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def guardar(bitacora: RegistroBitacora):
        bitacora.save()
        return bitacora