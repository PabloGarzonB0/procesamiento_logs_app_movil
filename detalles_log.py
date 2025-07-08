# Importacion de modulos
from datetime import datetime
from typing import Dict, Optional, Union

# Clases de detalle
class Info_dispositivo:
    def __init__(self, os:str, model:str, app_version:str):
        self.os = os
        self.model = model
        self.app_version = app_version

    def to_dict(self) -> Dict[str, str]:
        return {
            "os":self.os,
            "model": self.model,
            "app_version" : self.app_version
        }
class Location:
    def __init__(self, lat:float, lon:float):
        self.lat = lat
        self.lon = lon
    def to_dict(self) -> Dict[str, float]:
        return {
            "lat": self.lat,
            "lon": self.lon
                }
# ----------------- Clase Padre -------------------------------
class LogEvent:
    def __init__(
            self,
            tipo_evento: str,
            fecha_accion: Union[str, datetime],
            user_id:str,
            sesion_id:str,
            info_dispositivo: Info_dispositivo,
            estado_evento: bool,
            locacion : Optional[Location] = None
    ):
        self.tipo_evento = tipo_evento
        self.fecha_accion = fecha_accion
        self.user_id = user_id
        self.sesion_id = sesion_id
        self.info_dispositivo = info_dispositivo
        self.estado_evento = estado_evento
        self.locacion = locacion

    def is_valid(self) -> bool:
        """Validación base que siempre retorna True"""
        return True

    def to_dict(self) -> Dict:
        """Serializa el evento a un diccionario"""
        if isinstance(self.fecha_accion, datetime):
            fecha_accion = self.fecha_accion.isoformat()
        else:
            fecha_accion = self.fecha_accion
        return{
            "tipo_evento" : self.tipo_evento,
            "fecha_accion" : self.fecha_accion,
            "user_id" : self.user_id,
            "sesion_id" : self.sesion_id,
            "info_dispositivo" : self.info_dispositivo.to_dict(),
            "estado_evento" : self.estado_evento,
            "locacion" : self.locacion.to_dict() if self.locacion else None

        }
#------------------------- Subclases ----------------------------------
class ProductViewEvent(LogEvent):
    def __init__(self, product_id: str,
                 product_name: str,
                 category: str,
                 price: float,
                **kwargs):
        super().__init__(tipo_evento="ProductViewed", **kwargs)
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.price = price

    def is_valid(self) -> bool:
        """Validacion de datos de evento"""
        return all([
            self.product_id is not None,
            self.product_name is not None,
            self.category is not None,
            self.price >= 0
        ])
    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "product_name": self.product_name,
            "category": self.category,
            "price": self.price
        })
        return base


class AddTocartEvent(LogEvent):
    def __init__(self,
                 product_id=str,
                 product_name=str,
                 price=float,
                 cantidad=float,
                 cart_id=str,
                 **kwargs):
        super().__init__(tipo_evento="AddTocart", **kwargs)
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.cantidad = cantidad
        self.cart_id = cart_id
    def is_valid(self) -> bool:
        """Validacion especifica para eventos de carrito"""
        return all([
            self.product_id is not None,
            self.price >= 0,
            self.cantidad is not None,
            self.cart_id is not None
        ])

    def to_dict(self) -> Dict:
        base = super().to_dict()
        base.update({
            "product_id": self.product_id,
            "product_name": self.product_name,
            "price": self.price,
            "cantidad": self.cantidad,
            "cart_id": self.cart_id
        })
        return base