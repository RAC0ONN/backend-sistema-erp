from inventario.entity import MovimientoInventario, TipoMovimiento
from django.core.exceptions import ObjectDoesNotExist


class MovimientoInventarioRepository:

    @staticmethod
    def obtener_todos(solo_productos_activos=False):
        consulta = MovimientoInventario.objects.select_related('producto', 'usuario', 'tipo_movimiento').all()
        if solo_productos_activos:
            consulta = consulta.filter(producto__estado_producto__nombre__iexact='Activo')
        return consulta.order_by('-fecha', '-id_movimiento_inventario')

    @staticmethod
    def obtener_por_id(id_movimiento: int):
        try:
            return MovimientoInventario.objects.select_related(
                'producto', 'usuario', 'tipo_movimiento'
            ).get(pk=id_movimiento)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def obtener_tipo(id_tipo_movimiento):
        return TipoMovimiento.objects.filter(pk=id_tipo_movimiento).first()

    @staticmethod
    def guardar(movimiento: MovimientoInventario):
        movimiento.save()
        return movimiento
