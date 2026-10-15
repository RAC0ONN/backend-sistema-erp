from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from usuarios.service import UsuarioService
from usuarios.dto import UsuarioCrearDTO, UsuarioActualizarDTO, LoginDTO


@csrf_exempt
def listar_usuarios_view(request):
    if request.method == 'GET':
        try:
            usuarios = UsuarioService.listar_usuarios()
            resultado = [
                {
                    "id_usuario": u.id_usuario,
                    "nombre_usuario": u.nombre_usuario,
                    "primer_nombre": u.primer_nombre,
                    "segundo_nombre": u.segundo_nombre,
                    "primer_apellido": u.primer_apellido,
                    "segundo_apellido": u.segundo_apellido,
                    "correo": u.correo,
                    "numero_documento": u.numero_documento,
                    "id_rol": u.id_rol,
                    "rol": u.nombre_rol,
                    "id_tipo_documento": u.id_tipo_documento,
                    "tipo_documento": u.nombre_tipo_documento,
                    "id_estado_usuario": u.id_estado_usuario,
                    "estado": u.nombre_estado_usuario
                }
                for u in usuarios
            ]
            return JsonResponse({"status": "success", "data": resultado}, safe=False)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def crear_usuario_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dto = UsuarioCrearDTO(
                nombre_usuario=data.get('nombre_usuario'),
                primer_nombre=data.get('primer_nombre'),
                segundo_nombre=data.get('segundo_nombre'),
                primer_apellido=data.get('primer_apellido'),
                segundo_apellido=data.get('segundo_apellido'),
                correo=data.get('correo'),
                numero_documento=data.get('numero_documento'),
                contrasenia=data.get('contrasenia'),
                id_rol=int(data.get('id_rol')),
                id_tipo_documento=int(data.get('id_tipo_documento')),
                id_estado_usuario=int(data.get('id_estado_usuario'))
            )
            nuevo_id = UsuarioService.crear_usuario(dto)
            
            return JsonResponse({
                "status": "success", 
                "message": "Exito", 
                "id_usuario": nuevo_id
            }, status=201)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)

@csrf_exempt
def actualizar_usuario_view(request, id_usuario):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            dto = UsuarioActualizarDTO(
                nombre_usuario=data.get('nombre_usuario'),
                primer_nombre=data.get('primer_nombre'),
                segundo_nombre=data.get('segundo_nombre'),
                primer_apellido=data.get('primer_apellido'),
                segundo_apellido=data.get('segundo_apellido'),
                correo=data.get('correo'),
                numero_documento=data.get('numero_documento'),
                id_rol=int(data.get('id_rol')),
                id_tipo_documento=int(data.get('id_tipo_documento')),
                id_estado_usuario=int(data.get('id_estado_usuario'))
            )
            UsuarioService.actualizar_usuario(id_usuario, dto)
            
            return JsonResponse({
                "status": "success", 
                "message": "Exito"
            }, status=200)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def eliminar_usuario_view(request, id_usuario):
    if request.method == 'DELETE':
        try:
            UsuarioService.eliminar_usuario(id_usuario)
            return JsonResponse({
                "status": "success", 
                "message": "Exito"
            }, status=200)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
            
    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dto = LoginDTO(
                usuario=data.get('correo') or data.get('nombre_usuario'),
                contrasenia=data.get('contrasenia')
            )
            sesion = UsuarioService.iniciar_sesion(dto)
            if sesion is None:
                return JsonResponse({"status": "error", "message": "Correo o contraseña incorrectos"}, status=401)

            return JsonResponse({
                "status": "success",
                "message": "Bienvenido",
                "data": sesion
            }, status=200)

        except PermissionError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=403)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "No permitido"}, status=405)
