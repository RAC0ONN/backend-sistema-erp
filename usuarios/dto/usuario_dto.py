from dataclasses import dataclass
from typing import Any, Optional


# los dto reciben los datos tal cual llegan del front, el servicio es el que los valida

@dataclass
class UsuarioCrearDTO:
    # al crear no se recibe estado ni contraseña: el estado siempre es Contratado
    # y la contraseña la genera el sistema y se envia al correo
    nombre_usuario: Any
    primer_nombre: Any
    primer_apellido: Any
    correo: Any
    numero_documento: Any
    id_rol: Any
    id_tipo_documento: Any
    segundo_nombre: Any = None
    segundo_apellido: Any = None


@dataclass
class UsuarioActualizarDTO:
    nombre_usuario: Any
    primer_nombre: Any
    primer_apellido: Any
    correo: Any
    numero_documento: Any
    id_rol: Any
    id_tipo_documento: Any
    id_estado_usuario: Any
    segundo_nombre: Any = None
    segundo_apellido: Any = None


@dataclass
class CambioContraseniaDTO:
    contrasenia_actual: Any
    contrasenia_nueva: Any
    confirmacion: Any


@dataclass
class UsuarioRespuestaDTO:
    id_usuario: int
    nombre_usuario: str
    primer_nombre: str
    segundo_nombre: Optional[str]
    primer_apellido: str
    segundo_apellido: Optional[str]
    correo: str
    numero_documento: str
    id_rol: int
    nombre_rol: str
    id_tipo_documento: int
    nombre_tipo_documento: str
    id_estado_usuario: int
    nombre_estado_usuario: str


@dataclass
class LoginDTO:
    usuario: Any
    contrasenia: Any
