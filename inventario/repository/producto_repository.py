from inventario.entity import Producto
from django.core.exceptions import ObjectDoesNotExist

class ProductoRepository:
    
    @staticmethod
    def obtener_todos():
        return Producto.objects.select_related('categoria', 'estado_producto').all()

    @staticmethod
    def obtener_por_id(id_producto: int):
        try:
            return Producto.objects.select_related('categoria', 'estado_producto').get(pk=id_producto)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def obtener_por_codigo(codigo_identificacion: str):
        try:
            return Producto.objects.select_related('categoria', 'estado_producto').get(codigo_identificacion__iexact=codigo_identificacion)
        except ObjectDoesNotExist:
            return None

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