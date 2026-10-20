from dataclasses import dataclass
from typing import Optional


@dataclass
class RegistroBitacoraRespuestaDTO:
    id_registro_bitacora: int
    id_usuario_afectado: Optional[int]
    usuario_afectado: str
    id_usuario_responsable: Optional[int]
    usuario_responsable: str
    accion: str
    cambio_realizado: str
    fecha: str

    def to_dict(self):
        return {
            "id_registro_bitacora": self.id_registro_bitacora,
            "id_usuario_afectado": self.id_usuario_afectado,
            "usuario_afectado": self.usuario_afectado,
            "id_usuario_responsable": self.id_usuario_responsable,
            "usuario_responsable": self.usuario_responsable,
            "accion": self.accion,
            "cambio_realizado": self.cambio_realizado,
            "fecha": self.fecha
        }