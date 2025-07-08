from datetime import datetime, timedelta
import random


def generar_eventos_prueba(n: int = 10) -> list:
    """Genera una lista de eventos de prueba con datos válidos e inválidos"""
    eventos = []
    tipos_evento = ["ProductViewed", "AddTocart", "LogEvent", "EventDesconocido"]
    modelos_dispositivos = ["iPhone 15", "Samsung Galaxy S23", "Google Pixel 7", "Xiaomi Mi 11", "Huawei P50"]
    productos = [
        {"id": "prod-001", "nombre": "Laptop Gaming", "categoria": "Computación", "precio": 1299.99},
        {"id": "prod-002", "nombre": "Smartphone", "categoria": "Electrónicos", "precio": 799.99},
        {"id": "prod-003", "nombre": "Tablet", "categoria": "Electrónicos", "precio": 399.99},
        {"id": "prod-004", "nombre": "Auriculares", "categoria": "Audio", "precio": 199.99},
        {"id": "prod-012", "nombre": "Producto Inválido", "categoria": "", "precio": 39.99},
    ]

    # Generar n eventos
    for i in range(n):
        # Determinar si el evento será válido (70% de probabilidad)
        es_valido = random.random() < 0.5

        # Seleccionar tipo de evento
        tipo_evento = random.choice(tipos_evento)

        # Generar timestamp (últimos 30 días)
        fecha_base = (datetime.now() - timedelta(days=random.randint(0, 30)))
        timestamp = fecha_base

        # Generar datos básicos
        evento = {
            "tipo_evento": tipo_evento,
            "fecha_accion": timestamp,
            "user_id": f"user-{random.randint(1000, 9999)}" if es_valido else "",
            "sesion_id": f"session-{random.randint(10000, 99999)}",
            "info_dispositivo": {
                "os": random.choice(["Android", "iOS", "Windows"]),
                "model": random.choice(modelos_dispositivos),
                "app_version": f"{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
            },
        "propiedades_evento": {},
        "locacion": {
            "lat": random.uniform(-90, 90),
            "lon": random.uniform(-180, 180)
        } if random.random() < 0.8 else None  # 80% de probabilidad de tener ubicación
        }

        # Añadir propiedades específicas según el tipo de evento
        if tipo_evento == "ProductViewed":
            producto = random.choice(productos)
            evento["propiedades_evento"] = {
            "product_id": producto["id"] if es_valido else "",
            "product_name": producto["nombre"],
            "category": producto["categoria"],
            "price": producto["precio"] if es_valido else random.random() * 100
            }
        elif tipo_evento == "AddTocart":
            producto = random.choice(productos)
            evento["propiedades_evento"] = {
                "product_id": producto["id"] if es_valido else "prod-inválido",
                "product_name" : producto["nombre"],
                "price": producto["precio"],
                "cantidad": random.randint(1, 5),
                "cart_id": f"cart-{random.randint(1000, 9999)}"
            }
            
        else: pass

        # Introducir errores aleatorios
        if not es_valido:
            if  random.random() < 0.2:
                campo = random.choice(["tipo_evento", "fecha_accion", "user_id", "sesion_id"])
                evento[campo] = None if random.random() < 0.5 else ""
        # 20% de probabilidad de tipo de evento inválido
        if random.random() < 0.1:
            evento["tipo_evento"] = "EventoDesconocido"

        eventos.append(evento)
    return eventos