from usuarios.repository.registro_bitacora_repository import BitacoraRepository
from usuarios.entity.registro_bitacora import RegistroBitacora
from usuarios.dto.registro_bitacora_dto import RegistroBitacoraRespuestaDTO

class BitacoraService:

    @staticmethod
    def listar_historial() -> list[RegistroBitacoraRespuestaDTO]:
        registros = BitacoraRepository.obtener_todos()
        lista_dto = []
        
        for b in registros:
            dto = RegistroBitacoraRespuestaDTO(
                id_registro_bitacora=b.id_registro_bitacora,
                id_usuario_afectado=b.id_usuario_afectado.id_usuario if b.id_usuario_afectado else None,
                usuario_afectado=b.id_usuario_afectado.nombre_usuario if b.id_usuario_afectado else 'Sistema',
                id_usuario_responsable=b.id_usuario_responsable.id_usuario if b.id_usuario_responsable else None,
                usuario_responsable=b.id_usuario_responsable.nombre_usuario if b.id_usuario_responsable else 'Sistema',
                accion=b.accion,
                cambio_realizado=b.cambio_realizado,
                fecha=b.fecha.strftime('%Y-%m-%d %H:%M:%S') if b.fecha else ''
            )
            lista_dto.append(dto)
            
        return lista_dto

    @staticmethod
    def registrar_evento(id_usuario_afectado, id_usuario_responsable, accion, cambio_realizado):

        bitacora = RegistroBitacora(
            id_usuario_afectado_id=id_usuario_afectado,   
            id_usuario_responsable_id=id_usuario_responsable, 
            accion=accion,
            cambio_realizado=cambio_realizado
        )
        return BitacoraRepository.guardar(bitacora)