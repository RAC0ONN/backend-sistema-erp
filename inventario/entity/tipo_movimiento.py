from django.db import models


class TipoMovimiento(models.Model):
    id_tipo_movimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = False
        db_table = "tipo_movimiento"

    def __str__(self):
        return self.nombre