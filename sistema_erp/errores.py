# errores propios del sistema, los controladores los convierten en la respuesta http que toca


class ErrorValidacion(Exception):
    """datos mal enviados, trae un diccionario campo -> mensaje para mostrar en el formulario"""

    def __init__(self, errores):
        if isinstance(errores, str):
            errores = {"general": errores}
        self.errores = errores
        super().__init__(next(iter(errores.values())))


class NoEncontrado(Exception):
    pass


class NoAutenticado(Exception):
    pass


class SinPermiso(Exception):
    pass
