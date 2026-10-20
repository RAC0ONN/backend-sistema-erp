from django.db import models
from .producto import Producto
from .tipo_movimiento import TipoMovimiento
from usuarios.entity import Usuario  


class MovimientoInventario(models.Model):
    id_movimiento_inventario = models.AutoField(primary_key=True)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        db_column="id_producto",
        related_name="movimientos"
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="id_usuario",
        related_name="movimientos_inventario"
    )

    tipo_movimiento = models.ForeignKey(
        TipoMovimiento,
        on_delete=models.PROTECT,
        db_column="id_tipo_movimiento",
        related_name="movimientos"
    )

    cantidad = models.IntegerField()
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "movimiento_inventario"

    def __str__(self):
        return f"Movimiento {self.id_movimiento_inventario} - Prod: {self.producto_id}"