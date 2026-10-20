from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from usuarios.service import BitacoraService

@csrf_exempt
def listar_bitacora_view(request):
    if request.method == 'GET':
        try:
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
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)