from django.http import JsonResponse

from sistema_erp.respuestas import vista_api
from sistema_erp.sesion import usuario_actual, exigir_rol, ADMINISTRADOR, AUXILIAR
from usuarios.service import BitacoraService


@vista_api('GET')
def listar_bitacora_view(request):
    responsable = usuario_actual(request)
    exigir_rol(responsable, ADMINISTRADOR, AUXILIAR)
    registros = BitacoraService.listar_historial()
    resultado = [
        {
            "id_registro_bitacora": r.id_registro_bitacora,
            "id_usuario_afectado": r.id_usuario_afectado,
            "usuario_afectado": r.usuario_afectado,
            "id_usuario_responsable": r.id_usuario_responsable,
            "usuario_responsable": r.usuario_responsable,
            "accion": r.accion,
            "cambio_realizado": r.cambio_realizado,
            "fecha": r.fecha
        }
        for r in registros
    ]
    return JsonResponse({"status": "success", "data": resultado}, status=200)
