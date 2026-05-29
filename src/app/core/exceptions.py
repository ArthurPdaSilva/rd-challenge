class BusinessException(Exception):
    """Classe base para todas as exceções de negócio."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class GridSizeInvalidException(BusinessException):
    def __init__(self):
        super().__init__("O tamanho da malha deve ser maior que zero.")


class ProbeNotFoundException(BusinessException):
    def __init__(self):
        super().__init__("Sonda não encontrada.")


class InvalidCommandException(BusinessException):
    def __init__(self):
        super().__init__("Comando inválido. Use apenas 'L', 'R' e 'M'.")


class GridNotFoundException(BusinessException):
    def __init__(self):
        super().__init__("Malha associada à sonda não encontrada.")


class InvalidMovementException(BusinessException):
    def __init__(self):
        super().__init__("Movimento inválido. A sonda não pode sair da malha.")
