# Proyecto: Simulación y Validación de Eventos de E-commerce

Este proyecto simula la generación, procesamiento y validación de eventos típicos en un sistema de e-commerce, como vistas de producto, adición al carrito y compras. Utiliza patrones de diseño como **Factory** y **Chain of Responsibility** para la creación y validación flexible de eventos.

## Estructura del Proyecto

- **main.py**  
  Script principal que orquesta la generación, validación y reporte de eventos.

- **FactoryPatron.py**  
  Implementa el patrón Factory para crear instancias de eventos según su tipo.

- **chain_of_responsability.py**  
  Implementa la cadena de validadores para comprobar la validez de los eventos (campos nulos, tipo de evento, detalles de producto, etc.).

- **generador_datos_sinteticos.py**  
  Genera eventos de prueba con datos sintéticos para simular el comportamiento real del sistema.

## Flujo General

1. **Generación de eventos:**  
   Se crean eventos de prueba con diferentes tipos y propiedades.

2. **Validación:**  
   Los eventos pasan por una cadena de validadores que revisan la integridad y consistencia de los datos.

3. **Reporte:**  
   Se imprime un resumen de la validación y los detalles de los eventos inválidos.

## Ejecución

Ejecuta el script principal:

```bash
python main.py
```

## Ejemplo de Salida

```
Evento 1: ProductViewed - Válido
Evento 2: AddTocart - Inválido: [{'field': 'product_id', 'message': 'El campo es obligatorio'}]
...

Resumen de validación:
Total eventos: 15
Eventos válidos: 12 (80.00%)
Eventos inválidos: 3

Detalles de eventos inválidos:
Evento 2 (AddTocart):
  - product_id: El campo es obligatorio
  Datos completos: {'tipo_evento': 'AddTocart', ...}
```

## Patrones de Diseño Utilizados

- **Factory:**  
  Para la creación de objetos de evento según su tipo.

- **Chain of Responsibility:**  
  Para la validación secuencial y flexible de los eventos.

## Personalización

Puedes modificar los validadores en `chain_of_responsability.py` o agregar nuevos tipos de eventos en `FactoryPatron.py` para adaptar el sistema a tus necesidades.

---

**Autor:**  
Pablo  
2025