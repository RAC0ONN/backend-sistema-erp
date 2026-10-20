from inventario.repository import ProductoRepository
from inventario.entity import Producto
from inventario.dto import ProductoRespuestaDTO


def limpiar(texto):
    return texto.strip() if isinstance(texto, str) else texto


class ProductoService:

    @staticmethod
    def listar_productos():
        productos = ProductoRepository.obtener_todos()
        resultado = []
        for p in productos:
            dto = ProductoRespuestaDTO(
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
                nombre_estado_producto=p.estado_producto.nombre
            )
            resultado.append(dto)
        return resultado

    @staticmethod
    def crear_producto(dto_crear):
     
        existente = ProductoRepository.obtener_por_codigo(dto_crear.codigo_identificacion)
        if existente:
            raise ValueError(f"Ya existe un producto con el código '{dto_crear.codigo_identificacion}'.")

        producto = Producto(
            codigo_identificacion=limpiar(dto_crear.codigo_identificacion),
            nombre=limpiar(dto_crear.nombre),
            unidad_medida=limpiar(dto_crear.unidad_medida),
            precio_venta=dto_crear.precio_venta,
            stock_actual=dto_crear.stock_actual,
            stock_minimo=dto_crear.stock_minimo,
            categoria_id=dto_crear.id_categoria,
            estado_producto_id=dto_crear.id_estado_producto
        )
        producto_guardado = ProductoRepository.guardar(producto)
        return producto_guardado.id_producto
    
    @staticmethod
    def actualizar_producto(id_producto: int, dto_actualizar):
        producto = ProductoRepository.obtener_por_id(id_producto)
        if not producto:
            raise ValueError("El producto no existe")

        producto.codigo_identificacion = limpiar(dto_actualizar.codigo_identificacion)
        producto.nombre = limpiar(dto_actualizar.nombre)
        producto.unidad_medida = limpiar(dto_actualizar.unidad_medida)
        producto.precio_venta = dto_actualizar.precio_venta
        producto.stock_actual = dto_actualizar.stock_actual
        producto.stock_minimo = dto_actualizar.stock_minimo
        producto.categoria_id = dto_actualizar.id_categoria
        producto.estado_producto_id = dto_actualizar.id_estado_producto
        
        producto_actualizado = ProductoRepository.actualizar(producto)
        return producto_actualizado.id_producto

    @staticmethod
    def eliminar_producto(id_producto: int):
        producto = ProductoRepository.obtener_por_id(id_producto)
        if not producto:
            raise ValueError("El producto no existe")
        
        resultado = ProductoRepository.eliminar(producto)
        return resultado