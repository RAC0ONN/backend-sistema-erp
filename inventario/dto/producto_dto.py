from dataclasses import dataclass
from typing import Optional
from decimal import Decimal


@dataclass
class ProductoCrearDTO:
    codigo_identificacion: str
    nombre: str
    unidad_medida: str
    precio_venta: Decimal
    stock_actual: int
    stock_minimo: int
    id_categoria: int
    id_estado_producto: int


@dataclass
class ProductoActualizarDTO:
    codigo_identificacion: str
    nombre: str
    unidad_medida: str
    precio_venta: Decimal
    stock_actual: int
    stock_minimo: int
    id_categoria: int
    id_estado_producto: int


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