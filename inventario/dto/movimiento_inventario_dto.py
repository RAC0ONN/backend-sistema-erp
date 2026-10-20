from dataclasses import dataclass
from decimal import Decimal


@dataclass
class MovimientoInventarioCrearDTO:
    id_producto: int
    id_usuario: int
    id_tipo_movimiento: int
    cantidad: int
    costo_unitario: Decimal


@dataclass
class MovimientoInventarioRespuestaDTO:
    id_movimiento_inventario: int
    id_producto: int
    nombre_producto: str
    id_usuario: int
    nombre_usuario: str
    id_tipo_movimiento: int
    nombre_tipo_movimiento: str
    cantidad: int
    costo_unitario: Decimal
    fecha: str