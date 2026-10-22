from inventario.entity import Producto, Categoria, EstadoProducto, MovimientoInventario
from django.core.exceptions import ObjectDoesNotExist


class ProductoRepository:

    @staticmethod
    def obtener_todos(solo_activos=False):
        consulta = Producto.objects.select_related('categoria', 'estado_producto').all()
        if solo_activos:
            consulta = consulta.filter(estado_producto__nombre__iexact='Activo')
        return consulta.order_by('codigo_identificacion')

    @staticmethod
    def obtener_por_id(id_producto, bloquear=False):
        try:
            consulta = Producto.objects.select_related('categoria', 'estado_producto')
            if bloquear:
                # bloquea la fila mientras dura la transaccion, asi dos salidas al tiempo no dejan el stock negativo
                consulta = consulta.select_for_update()
            return consulta.get(pk=id_producto)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return None

    @staticmethod
    def obtener_por_codigo(codigo_identificacion: str):
        return Producto.objects.filter(codigo_identificacion__iexact=codigo_identificacion).first()

    @staticmethod
    def existe_nombre(nombre, excluir_id=None):
        return Producto.objects.filter(nombre__iexact=nombre).exclude(pk=excluir_id).exists()

    @staticmethod
    def codigos_con_prefijo(prefijo):
        return Producto.objects.filter(codigo_identificacion__istartswith=prefijo + "-").values_list('codigo_identificacion', flat=True)

    @staticmethod
    def tiene_movimientos(id_producto):
        return MovimientoInventario.objects.filter(producto_id=id_producto).exists()

    @staticmethod
    def obtener_categoria(id_categoria):
        return Categoria.objects.filter(pk=id_categoria).first()

    @staticmethod
    def obtener_estado(id_estado_producto):
        return EstadoProducto.objects.filter(pk=id_estado_producto).first()

    @staticmethod
    def obtener_estado_por_nombre(nombre):
        return EstadoProducto.objects.filter(nombre__iexact=nombre).first()

    @staticmethod
    def listar_categorias():
        return Categoria.objects.all().order_by('id_categoria')

    @staticmethod
    def guardar(producto: Producto):
        producto.save()
        return producto

    @staticmethod
    def eliminar(producto: Producto):
        producto.delete()
        return True

    @staticmethod
    def actualizar(producto: Producto):
        producto.save()
        return producto
