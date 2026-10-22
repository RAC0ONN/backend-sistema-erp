from django.urls import path
from inventario.controller import (
    listar_productos_view,
    crear_producto_view,
    actualizar_producto_view,
    eliminar_producto_view,
    listar_categorias_view,
    listar_movimientos_view,
    crear_movimiento_view,
)

urlpatterns = [
    
    path('productos/', listar_productos_view, name='listar_productos'),
    path('productos/crear/', crear_producto_view, name='crear_producto'),
    path('productos/actualizar/<int:id_producto>/', actualizar_producto_view, name='actualizar_producto'),
    path('productos/eliminar/<int:id_producto>/', eliminar_producto_view, name='eliminar_producto'),

    path('categorias/', listar_categorias_view, name='listar_categorias'),

    path('movimientos/', listar_movimientos_view, name='listar_movimientos'),
    path('movimientos/crear/', crear_movimiento_view, name='crear_movimiento'),
]