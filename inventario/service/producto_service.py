import re
import unicodedata
from decimal import Decimal

from django.db import transaction, IntegrityError

from sistema_erp import validaciones as v
from sistema_erp.errores import ErrorValidacion, NoEncontrado, SinPermiso
from sistema_erp.sesion import exigir_rol, ADMINISTRADOR, AUXILIAR
from inventario.repository import ProductoRepository
from inventario.entity import Producto
from inventario.dto import ProductoRespuestaDTO


UNIDADES_MEDIDA = ("Unidad", "Par", "Caja", "Paquete", "Metro", "Kilogramo")
PRECIO_MAXIMO = Decimal("100000000")  # 100 millones
STOCK_MAXIMO = 1000000

# solo el administrador ve los inactivos, activa/inactiva y elimina productos
ROLES_GESTIONAN_PRODUCTOS = (ADMINISTRADOR, AUXILIAR)
ROLES_VEN_INACTIVOS = (ADMINISTRADOR,)
ROLES_CAMBIAN_ESTADO = (ADMINISTRADOR,)
ROLES_ELIMINAN = (ADMINISTRADOR,)


def prefijo_categoria(nombre_categoria):
    """primeras 3 letras de la categoria sin tildes: Calzado -> CAL, Bisutería -> BIS"""
    sin_tildes = unicodedata.normalize("NFKD", nombre_categoria).encode("ascii", "ignore").decode()
    letras = re.sub(r"[^A-Za-z]", "", sin_tildes).upper()
    return (letras + "XXX")[:3]


def siguiente_codigo(categoria):
    prefijo = prefijo_categoria(categoria.nombre)
    numeros = [0]
    for codigo in ProductoRepository.codigos_con_prefijo(prefijo):
        sufijo = codigo.split("-", 1)[1]
        if sufijo.isdigit():
            numeros.append(int(sufijo))
    return f"{prefijo}-{max(numeros) + 1:03d}"


def a_dto(p):
    return ProductoRespuestaDTO(
        id_producto=p.id_producto,
        codigo_identificacion=p.codigo_identificacion,
        nombre=p.nombre,
        unidad_medida=p.unidad_medida,
        precio_venta=p.precio_venta,
        stock_actual=p.stock_actual,
        stock_minimo=p.stock_minimo,
        id_categoria=p.categoria.id_categoria,
        nombre_categoria=p.categoria.nombre,
        id_estado_producto=p.estado_producto.id_estado_producto,
        nombre_estado_producto=p.estado_producto.nombre,
    )


def validar_comunes(dto, errores, excluir_id=None):
    datos = {
        "nombre": v.texto(errores, "nombre", dto.nombre, "El nombre del producto", minimo=3, maximo=150),
        "unidad_medida": v.texto(errores, "unidad_medida", dto.unidad_medida, "La unidad de medida", maximo=20),
        "precio_venta": v.decimal(errores, "precio_venta", dto.precio_venta, "El precio", maximo=PRECIO_MAXIMO, mayor_que_cero=True),
        "stock_minimo": v.entero(errores, "stock_minimo", dto.stock_minimo, "El stock mínimo", minimo=0, maximo=STOCK_MAXIMO),
        "id_categoria": v.entero(errores, "id_categoria", dto.id_categoria, "La categoría", minimo=1),
    }
    nombre = datos["nombre"]
    if nombre and "nombre" not in errores:
        if not re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", nombre):
            errores["nombre"] = "El nombre del producto debe tener letras"
        elif ProductoRepository.existe_nombre(nombre, excluir_id):
            errores["nombre"] = "Ya existe un producto con ese nombre"
    if datos["unidad_medida"] and "unidad_medida" not in errores and datos["unidad_medida"] not in UNIDADES_MEDIDA:
        errores["unidad_medida"] = "La unidad de medida debe ser una de: " + ", ".join(UNIDADES_MEDIDA)
    datos["categoria"] = None
    if datos["id_categoria"] and "id_categoria" not in errores:
        datos["categoria"] = ProductoRepository.obtener_categoria(datos["id_categoria"])
        if not datos["categoria"]:
            errores["id_categoria"] = "La categoría seleccionada no existe"
    return datos


class ProductoService:

    @staticmethod
    def listar_productos(responsable):
        # el auxiliar y el vendedor no ven los productos inactivos
        ve_inactivos = responsable.rol.nombre in ROLES_VEN_INACTIVOS
        return [a_dto(p) for p in ProductoRepository.obtener_todos(solo_activos=not ve_inactivos)]

    @staticmethod
    def listar_categorias():
        return [{"id_categoria": c.id_categoria, "nombre": c.nombre, "prefijo": prefijo_categoria(c.nombre)}
                for c in ProductoRepository.listar_categorias()]

    @staticmethod
    def crear_producto(dto_crear, responsable):
        exigir_rol(responsable, *ROLES_GESTIONAN_PRODUCTOS)

        errores = {}
        datos = validar_comunes(dto_crear, errores)
        stock = v.entero(errores, "stock_actual", dto_crear.stock_actual, "El stock inicial", minimo=0, maximo=STOCK_MAXIMO)
        if errores:
            raise ErrorValidacion(errores)

        activo = ProductoRepository.obtener_estado_por_nombre("Activo")
        if not activo:
            raise ErrorValidacion("No existe el estado 'Activo' en la base de datos")

        # si dos personas crean al mismo tiempo y sale el mismo codigo, se vuelve a intentar con el siguiente
        for _ in range(5):
            try:
                with transaction.atomic():
                    producto = Producto(
                        codigo_identificacion=siguiente_codigo(datos["categoria"]),
                        nombre=datos["nombre"],
                        unidad_medida=datos["unidad_medida"],
                        precio_venta=datos["precio_venta"],
                        stock_actual=stock,
                        stock_minimo=datos["stock_minimo"],
                        categoria_id=datos["id_categoria"],
                        estado_producto_id=activo.id_estado_producto,
                    )
                    return ProductoRepository.guardar(producto)
            except IntegrityError:
                continue
        raise ErrorValidacion("No se pudo generar el código del producto, intenta de nuevo")

    @staticmethod
    @transaction.atomic
    def actualizar_producto(id_producto, dto_actualizar, responsable):
        exigir_rol(responsable, *ROLES_GESTIONAN_PRODUCTOS)

        producto = ProductoRepository.obtener_por_id(id_producto, bloquear=True)
        if not producto:
            raise NoEncontrado("El producto no existe")
        if producto.estado_producto.nombre.lower() == "inactivo" and responsable.rol.nombre not in ROLES_VEN_INACTIVOS:
            raise NoEncontrado("El producto no existe")

        errores = {}
        datos = validar_comunes(dto_actualizar, errores, excluir_id=producto.id_producto)
        id_estado = v.entero(errores, "id_estado_producto", dto_actualizar.id_estado_producto, "El estado", minimo=1)
        estado = None
        if id_estado and "id_estado_producto" not in errores:
            estado = ProductoRepository.obtener_estado(id_estado)
            if not estado:
                errores["id_estado_producto"] = "El estado seleccionado no existe"

        if estado and estado.id_estado_producto != producto.estado_producto_id:
            if responsable.rol.nombre not in ROLES_CAMBIAN_ESTADO:
                raise SinPermiso("Solo el administrador puede activar o inactivar productos")
            # regla del profe: solo se inactiva cuando no queda ni una unidad
            if estado.nombre.lower() == "inactivo" and producto.stock_actual > 0:
                errores["id_estado_producto"] = (
                    f"No se puede inactivar: todavía hay {producto.stock_actual} unidad(es). "
                    "Primero registra la salida de todas las existencias"
                )
        if errores:
            raise ErrorValidacion(errores)

        producto.nombre = datos["nombre"]
        producto.unidad_medida = datos["unidad_medida"]
        producto.precio_venta = datos["precio_venta"]
        producto.stock_minimo = datos["stock_minimo"]
        producto.categoria_id = datos["id_categoria"]
        producto.estado_producto_id = estado.id_estado_producto
        return ProductoRepository.actualizar(producto)

    @staticmethod
    @transaction.atomic
    def eliminar_producto(id_producto, responsable):
        exigir_rol(responsable, *ROLES_ELIMINAN)

        producto = ProductoRepository.obtener_por_id(id_producto, bloquear=True)
        if not producto:
            raise NoEncontrado("El producto no existe")
        if producto.stock_actual > 0:
            raise ErrorValidacion(f"No se puede eliminar: el producto todavía tiene {producto.stock_actual} unidad(es)")
        # si ya tuvo entradas o salidas se borra el historial, por eso en ese caso solo se puede inactivar
        if ProductoRepository.tiene_movimientos(producto.id_producto):
            raise ErrorValidacion("No se puede eliminar: el producto tiene movimientos registrados. Inactívalo en su lugar")
        return ProductoRepository.eliminar(producto)
