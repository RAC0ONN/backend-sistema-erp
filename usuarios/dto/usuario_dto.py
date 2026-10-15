from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioCrearDTO:
    nombre_usuario: str
    primer_nombre: str
    primer_apellido: str
    correo: str
    numero_documento: str
    contrasenia: str
    id_rol: int
    id_tipo_documento: int
    id_estado_usuario: int
    segundo_nombre: Optional[str] = None
    segundo_apellido: Optional[str] = None


@dataclass
class UsuarioActualizarDTO:
    nombre_usuario: str
    primer_nombre: str
    primer_apellido: str
    correo: str
    numero_documento: str
    id_rol: int
    id_tipo_documento: int
    id_estado_usuario: int
    segundo_nombre: Optional[str] = None
    segundo_apellido: Optional[str] = None


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
    usuario: str
    contrasenia: str
