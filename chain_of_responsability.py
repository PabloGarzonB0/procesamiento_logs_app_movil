from typing import List, Optional, Dict
from abc import ABC, abstractmethod


class ValidationError(Exception):
    """Excepción para errores de validación específicos"""

    def __init__(self, message: str, field: str):
        super().__init__(message)  # Corregido: super() debe ser llamado como función
        self.field = field
        self.message = message


# Handler Interface
class BaseValidador(ABC):
    """Clase base abstracta para validadores"""

    def __init__(self):
        self.next_validador: Optional['BaseValidador'] = None

    def set_next(self, validador: 'BaseValidador') -> 'BaseValidador':
        """Establece el siguiente validador en la cadena"""
        self.next_validador = validador
        return validador

    @abstractmethod
    def validate(self, event: 'LogEvent') -> bool:
        """Método abstracto que debe implementar cada validador concreto"""
        pass


# Clases handler concretas
class NotNullValidator(BaseValidador):
    """Valida que campos críticos no sean nulos o vacíos"""

    def __init__(self, fields: List[str]):
        super().__init__()
        self.fields = fields

    def validate(self, event: 'LogEvent') -> bool:
        """Implementación concreta del método validate"""
        for field in self.fields:
            value = getattr(event, field, None)

            # Verificar diferentes casos de "vacío"
            if value is None:
                raise ValidationError(f"Campo {field} no puede ser nulo", field)
            if isinstance(value, str) and value.strip() == "":
                raise ValidationError(f"Campo {field} no puede estar vacío", field)
            if isinstance(value, (list, dict)) and len(value) == 0:
                raise ValidationError(f"Campo {field} no puede estar vacío", field)

        # Pasar al siguiente validador en la cadena si existe
        if self.next_validador:
            return self.next_validador.validate(event)

        return True


class EventTypeValidator(BaseValidador):
    """Valida que el tipo de evento sea válido y obligatorio"""

    def __init__(self, allowed_types: Optional[List[str]] = None):
        super().__init__()
        self.allowed_types = allowed_types

    def validate(self, event: 'LogEvent') -> bool:
        """Implementación concreta del método validate"""
        if not event.tipo_evento:
            raise ValidationError("El tipo de evento es obligatorio", "tipo_evento")

        if self.allowed_types and event.tipo_evento not in self.allowed_types:
            allowed = ", ".join(self.allowed_types)
            raise ValidationError(
                f"Tipo de evento '{event.tipo_evento}' no permitido. Tipos válidos: {allowed}",
                "tipo_evento"
            )

        # Pasar al siguiente validador en la cadena si existe
        if self.next_validador:
            return self.next_validador.validate(event)

        return True


class ProductDetailsValidator(BaseValidador):
    """Valida detalles específicos de eventos de producto"""

    def validate(self, event: 'LogEvent') -> bool:
        """Implementación concreta del método validate"""
        # Solo aplica a eventos relacionados con productos
        if event.tipo_evento not in ["ProductViewed", "AddTocart"]:
            # Si no es evento de producto, pasar al siguiente validador
            if self.next_validador:
                return self.next_validador.validate(event)
            return True

        # Verificar que exista product_id en las propiedades
        if not hasattr(event, 'propiedades_evento') or 'product_id' not in event.event_properties:
            raise ValidationError("product_id es obligatorio para eventos de producto", "product_id")

        product_id = event.event_properties['product_id']
        if not product_id or not isinstance(product_id, str) or product_id.strip() == "":
            raise ValidationError("product_id debe ser un string no vacío", "product_id")

        # Validación adicional para eventos de carrito
        if event.tipo_evento == "AddTocart":
            if 'cantidad' not in event.event_properties:
                raise ValidationError("cantidad es obligatorio para eventos AddToCart", "cantidad")

            cantidad = event.event_properties['cantidad']
            if not isinstance(cantidad, int) or cantidad <= 0:
                raise ValidationError("cantidad debe ser un entero positivo", "cantidad")

        # Pasar al siguiente validador en la cadena si existe
        if self.next_validador:
            return self.next_validador.validate(event)

        return True


class EventValidatorChain:
    """Cadena de validadores que ejecuta validaciones secuenciales"""

    def __init__(self):
        self.validators: List[BaseValidador] = []
        self.errors: List[Dict[str, str]] = []

    def add_validator(self, validator: BaseValidador) -> None:
        """Añade un validador a la cadena"""
        self.validators.append(validator)

    def build_chain(self) -> Optional[BaseValidador]:
        """Construye la cadena de validadores"""
        if not self.validators:
            return None

        # Conecta todos los validadores en secuencia
        for i in range(len(self.validators) - 1):
            self.validators[i].set_next(self.validators[i + 1])

        return self.validators[0]

    def validate(self, event: 'LogEvent') -> bool:
        """Ejecuta toda la cadena de validación"""
        self.errors = []  # Reinicia los errores

        if not self.validators:
            return True

        head = self.build_chain()

        try:
            return head.validate(event)
        except ValidationError as e:
            # Captura el primer error encontrado
            self.errors.append({
                "field": e.field,
                "message": e.message
            })
            return False