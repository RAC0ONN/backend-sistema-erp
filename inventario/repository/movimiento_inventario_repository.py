from inventario.entity import MovimientoInventario
from django.core.exceptions import ObjectDoesNotExist


class MovimientoInventarioRepository:
    
    @staticmethod
    def obtener_todos():
        return MovimientoInventario.objects.select_related(
            'producto', 'usuario', 'tipo_movimiento'
        ).all()

    @staticmethod
    def obtener_por_id(id_movimiento: int):
        try:
            return MovimientoInventario.objects.select_related(
                'producto', 'usuario', 'tipo_movimiento'
            ).get(pk=id_movimiento)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def guardar(movimiento: MovimientoInventario):
        movimiento.save()
        return movimiento