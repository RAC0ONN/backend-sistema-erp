from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = "categoria"

    def __str__(self):
        return self.nombre