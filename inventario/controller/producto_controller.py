from django.http import JsonResponse

from sistema_erp.respuestas import vista_api, leer_json
from sistema_erp.sesion import usuario_actual
from inventario.service import ProductoService
from inventario.dto import ProductoCrearDTO, ProductoActualizarDTO


def a_json(p):
    return {
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


@vista_api('GET')
def listar_productos_view(request):
    responsable = usuario_actual(request)
    productos = ProductoService.listar_productos(responsable)
    return JsonResponse({"status": "success", "data": [a_json(p) for p in productos]})


@vista_api('GET')
def listar_categorias_view(request):
    usuario_actual(request)
    return JsonResponse({"status": "success", "data": ProductoService.listar_categorias()})


@vista_api('POST')
def crear_producto_view(request):
    responsable = usuario_actual(request)
    data = leer_json(request)
    dto = ProductoCrearDTO(
        nombre=data.get('nombre'),
        unidad_medida=data.get('unidad_medida'),
        precio_venta=data.get('precio_venta'),
        stock_actual=data.get('stock_actual'),
        stock_minimo=data.get('stock_minimo'),
        id_categoria=data.get('id_categoria'),
    )
    producto = ProductoService.crear_producto(dto, responsable)
    return JsonResponse({
        "status": "success",
        "message": f"Producto registrado con el código {producto.codigo_identificacion}",
        "id_producto": producto.id_producto,
        "codigo_identificacion": producto.codigo_identificacion
    }, status=201)


@vista_api('PUT')
def actualizar_producto_view(request, id_producto):
    responsable = usuario_actual(request)
    data = leer_json(request)
    dto = ProductoActualizarDTO(
        nombre=data.get('nombre'),
        unidad_medida=data.get('unidad_medida'),
        precio_venta=data.get('precio_venta'),
        stock_minimo=data.get('stock_minimo'),
        id_categoria=data.get('id_categoria'),
        id_estado_producto=data.get('id_estado_producto'),
    )
    ProductoService.actualizar_producto(id_producto, dto, responsable)
    return JsonResponse({"status": "success", "message": "Producto actualizado"}, status=200)


@vista_api('DELETE')
def eliminar_producto_view(request, id_producto):
    responsable = usuario_actual(request)
    ProductoService.eliminar_producto(id_producto, responsable)
    return JsonResponse({"status": "success", "message": "Producto eliminado"}, status=200)
