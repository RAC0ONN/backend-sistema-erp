from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal

from inventario.service import ProductoService
from inventario.dto import ProductoCrearDTO, ProductoActualizarDTO


@csrf_exempt
def listar_productos_view(request):
    if request.method == 'GET':
        try:
            productos = ProductoService.listar_productos()
            resultado = [
                {
                    "id_producto": p.id_producto,
                    "codigo_identificacion": p.codigo_identificacion,
                    "nombre": p.nombre,
                    "unidad_medida": p.unidad_medida,
                    "precio_venta": str(p.precio_venta),
                    "stock_actual": p.stock_actual,
                    "stock_minimo": p.stock_minimo,
                    "id_categoria": p.id_categoria,
                    "categoria": p.nombre_categoria,
                    "id_estado_producto": p.id_estado_producto,
                    "estado_producto": p.nombre_estado_producto
                }
                for p in productos
            ]
            return JsonResponse({"status": "success", "data": resultado}, safe=False)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def crear_producto_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dto = ProductoCrearDTO(
                codigo_identificacion=data.get('codigo_identificacion'),
                nombre=data.get('nombre'),
                unidad_medida=data.get('unidad_medida'),
                precio_venta=Decimal(str(data.get('precio_venta', 0))),
                stock_actual=int(data.get('stock_actual', 0)),
                stock_minimo=int(data.get('stock_minimo', 0)),
                id_categoria=int(data.get('id_categoria')),
                id_estado_producto=int(data.get('id_estado_producto'))
            )
            nuevo_id = ProductoService.crear_producto(dto)
            
            return JsonResponse({
                "status": "success", 
                "message": "Exito", 
                "id_producto": nuevo_id
            }, status=201)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def actualizar_producto_view(request, id_producto):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            dto = ProductoActualizarDTO(
                codigo_identificacion=data.get('codigo_identificacion'),
                nombre=data.get('nombre'),
                unidad_medida=data.get('unidad_medida'),
                precio_venta=Decimal(str(data.get('precio_venta', 0))),
                stock_actual=int(data.get('stock_actual', 0)),
                stock_minimo=int(data.get('stock_minimo', 0)),
                id_categoria=int(data.get('id_categoria')),
                id_estado_producto=int(data.get('id_estado_producto'))
            )
            ProductoService.actualizar_producto(id_producto, dto)
            
            return JsonResponse({
                "status": "success", 
                "message": "Exito"
            }, status=200)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def eliminar_producto_view(request, id_producto):
    if request.method == 'DELETE':
        try:
            ProductoService.eliminar_producto(id_producto)
            return JsonResponse({
                "status": "success", 
                "message": "Exito"
            }, status=200)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)