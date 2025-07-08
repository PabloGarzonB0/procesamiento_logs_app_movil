from detalles_log import LogEvent, Info_dispositivo, Location, ProductViewEvent, AddTocartEvent
from typing import Optional

class EventFactory:  #Patron de diseno factory
    @staticmethod
    def crear_evento(raw_data : dict) -> LogEvent:
        # Creacion de objeto en base a los datos subministrados de sistema
        # argumetos: diccionario de datos en formato bruto
        # retorna: Instancia de LogEvent asignada a su subclase
        info_dispositivo = EventFactory._crear_info_dispositivo(raw_data.get('info_dispositivo',{}))
        locacion = EventFactory._crear_locacion(raw_data.get('locacion'))

        # Propiedades comunes
        args_comunes = {
            'fecha_accion' : raw_data.get('fecha_accion'),
            'user_id' : raw_data.get('user_id'),
            'sesion_id' : raw_data.get('sesion_id'),
            'info_dispositivo': info_dispositivo,
            'locacion' : locacion,
            'estado_evento' : True
        }
        # Tipos de eventos
        tipo_evento = raw_data.get('tipo_evento','')
        propiedades_evento = raw_data.get('propiedades_evento',{})
        if tipo_evento == "ProductViewed":
            return EventFactory._create_product_view(propiedades_evento, args_comunes)
        elif tipo_evento == "AddTocart": return EventFactory._create_add_to_cart(propiedades_evento, args_comunes)
        else:
            return LogEvent(
                tipo_evento=tipo_evento,
                **args_comunes
            )
# --------------  METODOS GENERALES PARAT ODO LOS EVENTOS ----------------
    @staticmethod
    def _crear_info_dispositivo(datos_dispositivo:dict) -> Info_dispositivo:
        """Creacion de objetos de tipo dispositivo desde diccionario"""
        return Info_dispositivo(
            os=datos_dispositivo.get('os',''),
            model=datos_dispositivo.get('model',''),
            app_version=datos_dispositivo.get('app_version','')
        )
    @staticmethod
    def _crear_locacion(datos_locacion:Optional[dict]) -> Optional[Location]:
        """Creacion objeto location desde diccionario (opcional)"""
        if datos_locacion:
            return Location(
                lat=datos_locacion.get('lat',0.0),
                lon=datos_locacion.get('lon',0.0)
            )
        return None

# -------------- Metodo para el log de tipo ver producto -----------------
    @staticmethod
    def _create_product_view(event_props: dict, args_comunes:dict) -> ProductViewEvent:
        """Creacion de evento ProductViewEvent con propiedades especificas"""
        return ProductViewEvent(
            product_id=event_props.get('product_id',''),
            product_name=event_props.get('product_name',''),
            category=event_props.get('category',''),
            price=event_props.get('price',0.0), **args_comunes
        )
# -------------- Metodo para el log de tipo agregar a corrito -----------------
    @staticmethod
    def _create_add_to_cart(event_props: dict, args_comunes:dict) -> AddTocartEvent:
        """Creacion evento AddToCartEvent con propiedades especificas"""
        return AddTocartEvent(
            product_id=event_props.get('product_id',''),
            product_name=event_props.get('product_name', ''),
            price=event_props.get('cantidad', 0.0),
            cart_id=event_props.get('cart_id',''),
            **args_comunes)