from django.db import transaction

from sistema_erp import validaciones as v
from sistema_erp.errores import ErrorValidacion
from sistema_erp.sesion import exigir_rol, ADMINISTRADOR, AUXILIAR
from inventario.repository import MovimientoInventarioRepository, ProductoRepository
from inventario.entity import MovimientoInventario
from inventario.dto import MovimientoInventarioRespuestaDTO
from inventario.service.producto_service import STOCK_MAXIMO, PRECIO_MAXIMO, ROLES_VEN_INACTIVOS

ROLES_REGISTRAN_MOVIMIENTOS = (ADMINISTRADOR, AUXILIAR)


class MovimientoInventarioService:

    @staticmethod
    def listar_movimientos(responsable):
        solo_activos = responsable.rol.nombre not in ROLES_VEN_INACTIVOS
        resultado = []
        for m in MovimientoInventarioRepository.obtener_todos(solo_productos_activos=solo_activos):
            resultado.append(MovimientoInventarioRespuestaDTO(
                id_movimiento_inventario=m.id_movimiento_inventario,
                id_producto=m.producto.id_producto,
                nombre_producto=m.producto.nombre,
                id_usuario=m.usuario.id_usuario,
                nombre_usuario=m.usuario.nombre_usuario,
                id_tipo_movimiento=m.tipo_movimiento.id_tipo_movimiento,
                nombre_tipo_movimiento=m.tipo_movimiento.nombre,
                cantidad=m.cantidad,
                costo_unitario=m.costo_unitario,
                fecha=m.fecha.isoformat() if m.fecha else ""
            ))
        return resultado

    @staticmethod
    @transaction.atomic
    def registrar_movimiento(dto_crear, responsable):
        exigir_rol(responsable, *ROLES_REGISTRAN_MOVIMIENTOS)

        errores = {}
        id_producto = v.entero(errores, "id_producto", dto_crear.id_producto, "El producto", minimo=1)
        id_tipo = v.entero(errores, "id_tipo_movimiento", dto_crear.id_tipo_movimiento, "El tipo de movimiento", minimo=1)
        cantidad = v.entero(errores, "cantidad", dto_crear.cantidad, "La cantidad", minimo=1, maximo=STOCK_MAXIMO)
        if errores:
            raise ErrorValidacion(errores)

        tipo = MovimientoInventarioRepository.obtener_tipo(id_tipo)
        if not tipo:
            raise ErrorValidacion({"id_tipo_movimiento": "El tipo de movimiento no existe"})

        producto = ProductoRepository.obtener_por_id(id_producto, bloquear=True)
        if not producto:
            raise ErrorValidacion({"id_producto": "El producto no existe"})
        if producto.estado_producto.nombre.lower() != "activo":
            raise ErrorValidacion({"id_producto": "No se pueden registrar movimientos de un producto inactivo"})

        # si no mandan costo se usa el precio del producto
        costo = producto.precio_venta
        if dto_crear.costo_unitario not in (None, ""):
            costo = v.decimal(errores, "costo_unitario", dto_crear.costo_unitario, "El costo unitario", minimo=0, maximo=PRECIO_MAXIMO)
            if errores:
                raise ErrorValidacion(errores)

        es_entrada = tipo.nombre.lower() == "entrada"
        if es_entrada:
            if producto.stock_actual + cantidad > STOCK_MAXIMO:
                raise ErrorValidacion({"cantidad": f"Con esta entrada el stock pasaría de {STOCK_MAXIMO:,}".replace(",", ".")})
            producto.stock_actual += cantidad
        else:
            if cantidad > producto.stock_actual:
                raise ErrorValidacion({"cantidad": f"No hay existencias suficientes. Stock actual: {producto.stock_actual}"})
            producto.stock_actual -= cantidad

        movimiento = MovimientoInventarioRepository.guardar(MovimientoInventario(
            producto_id=producto.id_producto,
            usuario_id=responsable.id_usuario,
            tipo_movimiento_id=tipo.id_tipo_movimiento,
            cantidad=cantidad,
            costo_unitario=costo
        ))
        ProductoRepository.guardar(producto)
        return movimiento.id_movimiento_inventario, producto.stock_actual
