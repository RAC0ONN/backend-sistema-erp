from django.urls import path
from usuarios.controller import (
    listar_usuarios_view, 
    crear_usuario_view, 
    actualizar_usuario_view, 
    eliminar_usuario_view,
    login_view
)

urlpatterns = [
    path('usuarios/', listar_usuarios_view, name='listar_usuarios'),
    path('usuarios/crear/', crear_usuario_view, name='crear_usuario'),
    path('usuarios/actualizar/<int:id_usuario>/', actualizar_usuario_view, name='actualizar_usuario'),
    path('usuarios/eliminar/<int:id_usuario>/', eliminar_usuario_view, name='eliminar_usuario'),
    path('usuarios/login/', login_view, name='login'),
]