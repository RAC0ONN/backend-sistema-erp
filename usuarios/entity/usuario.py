
from django.db import models

from .rol import Rol
from .tipo_documento import TipoDocumento
from .estado_usuario import EstadoUsuario


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        db_column="id_rol",
        related_name="usuarios"
    )

    tipo_documento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.PROTECT,
        db_column="id_tipo_documento",
        related_name="usuarios"
    )

    estado_usuario = models.ForeignKey(
        EstadoUsuario,
        on_delete=models.PROTECT,
        db_column="id_estado_usuario",
        related_name="usuarios"
    )

    nombre_usuario = models.CharField(max_length=50, unique=True)
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, null=True, blank=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, null=True, blank=True)
    correo = models.CharField(max_length=50, unique=True)
    numero_documento = models.CharField(max_length=30, unique=True)
    contrasenia = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "usuario"

    def __str__(self):
        return self.nombre_usuario