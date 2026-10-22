from .producto_controller import (
    listar_productos_view,
    crear_producto_view,
    actualizar_producto_view,
    eliminar_producto_view,
    listar_categorias_view,
)
from .movimiento_inventario_controller import (
    listar_movimientos_view,
    crear_movimiento_view,
)

__all__ = [
    "listar_productos_view",
    "crear_producto_view",
    "actualizar_producto_view",
    "eliminar_producto_view",
    "listar_categorias_view",
    "listar_movimientos_view",
    "crear_movimiento_view",
]