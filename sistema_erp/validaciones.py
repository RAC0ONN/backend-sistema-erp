import re
from decimal import Decimal, InvalidOperation

# funciones de validacion que usan los servicios. cada una recibe el diccionario de errores,
# si el dato esta mal agrega el mensaje con el nombre del campo y devuelve el valor ya limpio

LETRAS = r"A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
PATRON_NOMBRE = re.compile(rf"^[{LETRAS}]+( [{LETRAS}]+)*$")
PATRON_USUARIO = re.compile(r"^[A-Za-z0-9._]+$")
PATRON_CORREO = re.compile(r"^[a-z0-9]+([._%+-][a-z0-9]+)*@[a-z0-9]+(-[a-z0-9]+)*(\.[a-z0-9]+(-[a-z0-9]+)*)*\.(?P<dominio>[a-z]{2,})$")

# terminaciones de correo aceptadas, asi un .coml o .con no pasa como valido
DOMINIOS_VALIDOS = {
    "com", "co", "net", "org", "edu", "gov", "mil", "int", "info", "biz", "io", "app", "dev",
    "online", "store", "shop", "tech", "site", "me", "us", "es", "mx", "ar", "cl", "pe", "ec",
    "ve", "br", "uy", "py", "bo", "pa", "cr", "gt", "do", "uk", "de", "fr", "it", "pt", "ca",
}


def limpiar(texto):
    """quita espacios de los lados y deja un solo espacio entre palabras"""
    if not isinstance(texto, str):
        return texto
    return " ".join(texto.split())


def texto(errores, campo, valor, etiqueta, requerido=True, minimo=1, maximo=50):
    valor = limpiar(valor) if isinstance(valor, str) else valor
    if valor in (None, ""):
        if requerido:
            errores[campo] = f"{etiqueta} es obligatorio"
        return None
    if not isinstance(valor, str):
        errores[campo] = f"{etiqueta} debe ser texto"
        return None
    if len(valor) < minimo:
        errores[campo] = f"{etiqueta} debe tener mínimo {minimo} caracteres"
    elif len(valor) > maximo:
        errores[campo] = f"{etiqueta} debe tener máximo {maximo} caracteres"
    return valor


def nombre_persona(errores, campo, valor, etiqueta, requerido=True):
    valor = texto(errores, campo, valor, etiqueta, requerido, minimo=2, maximo=50)
    if valor and campo not in errores and not PATRON_NOMBRE.match(valor):
        errores[campo] = f"{etiqueta} solo puede tener letras y espacios"
    return valor


def nombre_usuario(errores, campo, valor):
    valor = texto(errores, campo, valor, "El nombre de usuario", minimo=4, maximo=50)
    if valor and campo not in errores:
        if " " in valor:
            errores[campo] = "El nombre de usuario no puede tener espacios"
        elif not PATRON_USUARIO.match(valor):
            errores[campo] = "El nombre de usuario solo puede tener letras, números, punto y guion bajo"
        elif valor.isdigit():
            errores[campo] = "El nombre de usuario no puede ser solo números"
    return valor


def correo(errores, campo, valor):
    valor = texto(errores, campo, valor, "El correo", minimo=6, maximo=50)
    if not valor or campo in errores:
        return valor
    valor = valor.lower()
    if " " in valor:
        errores[campo] = "El correo no puede tener espacios"
        return valor
    coincide = PATRON_CORREO.match(valor)
    if not coincide:
        errores[campo] = "El correo no tiene un formato válido (ej. usuario@empresa.com)"
    elif coincide.group("dominio") not in DOMINIOS_VALIDOS:
        terminacion = coincide.group("dominio")
        errores[campo] = f"La terminación '.{terminacion}' del correo no es válida, revisa que esté bien escrito"
    return valor


def numero_documento(errores, campo, valor, id_tipo_documento):
    if isinstance(valor, int) and not isinstance(valor, bool):
        valor = str(valor)
    valor = texto(errores, campo, valor, "El número de documento", minimo=1, maximo=30)
    if not valor or campo in errores:
        return valor
    valor = valor.replace(" ", "")
    if not valor.isdigit():
        errores[campo] = "El número de documento solo puede tener números (sin puntos ni guiones)"
    elif valor.startswith("0"):
        errores[campo] = "El número de documento no puede empezar en 0"
    elif id_tipo_documento == 1 and not 6 <= len(valor) <= 10:
        errores[campo] = "La cédula de ciudadanía debe tener entre 6 y 10 dígitos"
    elif id_tipo_documento == 2 and not 6 <= len(valor) <= 12:
        errores[campo] = "La cédula de extranjería debe tener entre 6 y 12 dígitos"
    return valor


def entero(errores, campo, valor, etiqueta, requerido=True, minimo=None, maximo=None):
    if valor in (None, ""):
        if requerido:
            errores[campo] = f"{etiqueta} es obligatorio"
        return None
    if isinstance(valor, bool):
        errores[campo] = f"{etiqueta} debe ser un número entero"
        return None
    try:
        if isinstance(valor, float) and not valor.is_integer():
            raise ValueError
        if isinstance(valor, str) and not re.fullmatch(r"-?\d+", valor.strip()):
            raise ValueError
        numero = int(valor)
    except (TypeError, ValueError):
        errores[campo] = f"{etiqueta} debe ser un número entero"
        return None
    if minimo is not None and numero < minimo:
        errores[campo] = f"{etiqueta} debe ser mínimo {minimo}"
    elif maximo is not None and numero > maximo:
        errores[campo] = f"{etiqueta} debe ser máximo {maximo:,}".replace(",", ".")
    return numero


def decimal(errores, campo, valor, etiqueta, minimo=None, maximo=None, mayor_que_cero=False):
    if valor in (None, ""):
        errores[campo] = f"{etiqueta} es obligatorio"
        return None
    if isinstance(valor, bool):
        errores[campo] = f"{etiqueta} debe ser un número"
        return None
    try:
        numero = Decimal(str(valor).strip())
    except (InvalidOperation, ValueError):
        errores[campo] = f"{etiqueta} debe ser un número"
        return None
    if not numero.is_finite():
        errores[campo] = f"{etiqueta} debe ser un número"
        return None
    if numero.as_tuple().exponent < -2:
        errores[campo] = f"{etiqueta} puede tener máximo 2 decimales"
    elif mayor_que_cero and numero <= 0:
        errores[campo] = f"{etiqueta} debe ser mayor que cero"
    elif minimo is not None and numero < minimo:
        errores[campo] = f"{etiqueta} no puede ser menor que {minimo}"
    elif maximo is not None and numero > maximo:
        errores[campo] = f"{etiqueta} no puede ser mayor que {maximo:,}".replace(",", ".")
    return numero


def contrasenia_segura(errores, campo, valor, etiqueta="La contraseña"):
    if not valor or not isinstance(valor, str):
        errores[campo] = f"{etiqueta} es obligatoria"
        return None
    if len(valor) < 8:
        errores[campo] = f"{etiqueta} debe tener mínimo 8 caracteres"
    elif len(valor) > 64:
        errores[campo] = f"{etiqueta} debe tener máximo 64 caracteres"
    elif " " in valor:
        errores[campo] = f"{etiqueta} no puede tener espacios"
    elif not re.search(r"[A-Z]", valor) or not re.search(r"[a-z]", valor) or not re.search(r"\d", valor):
        errores[campo] = f"{etiqueta} debe tener al menos una mayúscula, una minúscula y un número"
    return valor
