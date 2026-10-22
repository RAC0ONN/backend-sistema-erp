from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class MovimientoInventarioCrearDTO:
    # el usuario ya no se manda desde el front, se toma del que inicio sesion
    id_producto: Any
    id_tipo_movimiento: Any
    cantidad: Any
    costo_unitario: Any = None


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
