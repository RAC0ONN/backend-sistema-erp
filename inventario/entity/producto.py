from django.db import models
from .categoria import Categoria
from .estado_producto import EstadoProducto


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_identificacion = models.CharField(max_length=50, unique=True)
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        db_column="id_categoria",
        related_name="productos"
    )

    estado_producto = models.ForeignKey(
        EstadoProducto,
        on_delete=models.PROTECT,
        db_column="id_estado_producto",
        related_name="productos"
    )

    nombre = models.CharField(max_length=150)
    unidad_medida = models.CharField(max_length=20)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2)
    stock_actual = models.IntegerField()
    stock_minimo = models.IntegerField()

    class Meta:
        managed = False
        db_table = "producto"

    def __str__(self):
        return f"{self.codigo_identificacion} - {self.nombre}"