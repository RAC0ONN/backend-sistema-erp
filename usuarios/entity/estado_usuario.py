
from django.db import models

class EstadoUsuario(models.Model):
    id_estado_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)

    class Meta:
        managed = False
        db_table = "estado_usuario"

    def __str__(self):
        return self.nombre