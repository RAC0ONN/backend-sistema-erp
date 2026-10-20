from django.db import models

class RegistroBitacora(models.Model):
    id_registro_bitacora = models.AutoField(primary_key=True)
    
    id_usuario_afectado = models.ForeignKey(
        'Usuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='id_usuario_afectado',  
        related_name='bitacoras_afectadas'
    )
    
    id_usuario_responsable = models.ForeignKey(
        'Usuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='id_usuario_responsable',  
        related_name='bitacoras_responsables'
    )
    
    accion = models.CharField(max_length=50)  
    cambio_realizado = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registro_bitacora'
        verbose_name = 'Registro de Bitácora'
        verbose_name_plural = 'Registros de Bitácora'