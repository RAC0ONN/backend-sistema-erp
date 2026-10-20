from inventario.repository import MovimientoInventarioRepository, ProductoRepository
from inventario.entity import MovimientoInventario
from inventario.dto import MovimientoInventarioRespuestaDTO
from django.db import transaction


class MovimientoInventarioService:

    @staticmethod
    def listar_movimientos():
        movimientos = MovimientoInventarioRepository.obtener_todos()
        resultado = []
        for m in movimientos:
            dto = MovimientoInventarioRespuestaDTO(
                id_movimiento_inventario=m.id_movimiento_inventario,
                id_producto=m.producto.id_producto,
                nombre_producto=m.producto.nombre,
                id_usuario=m.usuario.id_usuario,
                nombre_usuario=m.usuario.nombre_usuario,
                id_tipo_movimiento=m.tipo_movimiento.id_tipo_movimiento,
                nombre_tipo_movimiento=m.tipo_movimiento.nombre,
                cantidad=m.cantidad,
                costo_unitario=m.costo_unitario,
                fecha=str(m.fecha)
            )
            resultado.append(dto)
        return resultado

    @staticmethod
    @transaction.atomic
    def registrar_movimiento(dto_crear):
        if dto_crear.cantidad <= 0:
            raise ValueError("La cantidad del movimiento debe ser mayor a cero")
        if dto_crear.costo_unitario < 0:
            raise ValueError("El costo unitario no puede ser negativo")

        producto = ProductoRepository.obtener_por_id(dto_crear.id_producto)
        if not producto:
            raise ValueError("El producto especificado no existe.")

        if dto_crear.id_tipo_movimiento == 2 and producto.stock_actual < dto_crear.cantidad:
            raise ValueError(f"No hay existencias suficientes. Stock actual: {producto.stock_actual}")

        movimiento = MovimientoInventario(
            producto_id=dto_crear.id_producto,
            usuario_id=dto_crear.id_usuario,
            tipo_movimiento_id=dto_crear.id_tipo_movimiento,
            cantidad=dto_crear.cantidad,
            costo_unitario=dto_crear.costo_unitario
        )
        movimiento_guardado = MovimientoInventarioRepository.guardar(movimiento)

        if dto_crear.id_tipo_movimiento == 1:  
            producto.stock_actual += dto_crear.cantidad
        elif dto_crear.id_tipo_movimiento == 2:  
            producto.stock_actual -= dto_crear.cantidad

        ProductoRepository.guardar(producto)

        return movimiento_guardado.id_movimiento_inventario