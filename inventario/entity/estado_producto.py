from django.db import models


class EstadoProducto(models.Model):
    id_estado_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = False
        db_table = "estado_producto"

    def __str__(self):
        return self.nombre