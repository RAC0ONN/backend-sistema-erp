from dataclasses import dataclass
from typing import Any
from decimal import Decimal


# el codigo ya no se recibe: lo genera el sistema segun la categoria (CAL-001, BOL-002...)

@dataclass
class ProductoCrearDTO:
    nombre: Any
    unidad_medida: Any
    precio_venta: Any
    stock_actual: Any
    stock_minimo: Any
    id_categoria: Any


@dataclass
class ProductoActualizarDTO:
    # el stock no se edita aqui, solo cambia con entradas y salidas
    nombre: Any
    unidad_medida: Any
    precio_venta: Any
    stock_minimo: Any
    id_categoria: Any
    id_estado_producto: Any


@dataclass
class ProductoRespuestaDTO:
    id_producto: int
    codigo_identificacion: str
    nombre: str
    unidad_medida: str
    precio_venta: Decimal
    stock_actual: int
    stock_minimo: int
    id_categoria: int
    nombre_categoria: str
    id_estado_producto: int
    nombre_estado_producto: str
