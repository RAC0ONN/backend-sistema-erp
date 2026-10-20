from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

from inventario.service import MovimientoInventarioService
from inventario.dto import MovimientoInventarioCrearDTO


@csrf_exempt
def listar_movimientos_view(request):
    if request.method == 'GET':
        try:
            movimientos = MovimientoInventarioService.listar_movimientos()
            resultado = [
                {
                    "id_movimiento_inventario": m.id_movimiento_inventario,
                    "id_producto": m.id_producto,
                    "producto": m.nombre_producto,
                    "id_usuario": m.id_usuario,
                    "usuario": m.nombre_usuario,
                    "id_tipo_movimiento": m.id_tipo_movimiento,
                    "tipo_movimiento": m.nombre_tipo_movimiento,
                    "cantidad": m.cantidad,
                    "costo_unitario": str(m.costo_unitario),
                    "fecha": m.fecha
                }
                for m in movimientos
            ]
            return JsonResponse({"status": "success", "data": resultado}, safe=False)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def crear_movimiento_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dto = MovimientoInventarioCrearDTO(
                id_producto=int(data.get('id_producto')),
                id_usuario=int(data.get('id_usuario')),
                id_tipo_movimiento=int(data.get('id_tipo_movimiento')),
                cantidad=int(data.get('cantidad')),
                costo_unitario=Decimal(str(data.get('costo_unitario', 0)))
            )
            nuevo_id = MovimientoInventarioService.registrar_movimiento(dto)
            
            return JsonResponse({
                "status": "success", 
                "message": "Exito", 
                "id_movimiento_inventario": nuevo_id
            }, status=201)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)