import json
import traceback
from functools import wraps

from django.db import IntegrityError, DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sistema_erp.errores import ErrorValidacion, NoEncontrado, NoAutenticado, SinPermiso


def error(mensaje, status, errores=None):
    cuerpo = {"status": "error", "message": mensaje}
    if errores:
        cuerpo["errores"] = errores
    return JsonResponse(cuerpo, status=status)


def leer_json(request):
    """lee el body y si no es un json valido (o no es un objeto) responde 400 en vez de reventar"""
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ErrorValidacion("Los datos enviados no tienen un formato válido")
    if not isinstance(data, dict):
        raise ErrorValidacion("Los datos enviados no tienen un formato válido")
    return data


def vista_api(*metodos):
    """envuelve las vistas: revisa el metodo http y convierte cada excepcion en su codigo de respuesta"""

    def decorador(funcion):
        @csrf_exempt
        @wraps(funcion)
        def envoltura(request, *args, **kwargs):
            if request.method not in metodos:
                return error("Método no permitido", 405)
            try:
                return funcion(request, *args, **kwargs)
            except ErrorValidacion as e:
                return error(str(e), 400, e.errores)
            except NoAutenticado as e:
                return error(str(e) or "Debes iniciar sesión", 401)
            except SinPermiso as e:
                return error(str(e) or "No tienes permiso para hacer esto", 403)
            except NoEncontrado as e:
                return error(str(e), 404)
            except IntegrityError:
                traceback.print_exc()
                return error("Ya existe un registro con esos datos o hay datos relacionados que lo impiden", 400)
            except DatabaseError as e:
                traceback.print_exc()
                # los triggers de la bd mandan su propio mensaje, se deja solo la primera linea
                mensaje = str(e).split("\n")[0].strip() or "Error en la base de datos"
                return error(mensaje, 400)
            except Exception:
                traceback.print_exc()
                return error("Ocurrió un error inesperado en el servidor", 500)

        return envoltura

    return decorador
