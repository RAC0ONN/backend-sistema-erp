from django.http import JsonResponse

from sistema_erp.respuestas import vista_api, leer_json
from sistema_erp.sesion import usuario_actual
from inventario.service import MovimientoInventarioService
from inventario.dto import MovimientoInventarioCrearDTO


@vista_api('GET')
def listar_movimientos_view(request):
    responsable = usuario_actual(request)
    movimientos = MovimientoInventarioService.listar_movimientos(responsable)
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
    return JsonResponse({"status": "success", "data": resultado})


@vista_api('POST')
def crear_movimiento_view(request):
    responsable = usuario_actual(request)
    data = leer_json(request)
    dto = MovimientoInventarioCrearDTO(
        id_producto=data.get('id_producto'),
        id_tipo_movimiento=data.get('id_tipo_movimiento'),
        cantidad=data.get('cantidad'),
        costo_unitario=data.get('costo_unitario'),
    )
    nuevo_id, stock = MovimientoInventarioService.registrar_movimiento(dto, responsable)
    return JsonResponse({
        "status": "success",
        "message": "Movimiento registrado",
        "id_movimiento_inventario": nuevo_id,
        "stock_actual": stock
    }, status=201)
