# Importacion de modulos
from FactoryPatron import EventFactory
from chain_of_responsability import EventValidatorChain, NotNullValidator, EventTypeValidator, ProductDetailsValidator
from generador_datos_sinteticos import generar_eventos_prueba

if __name__ == "__main__":
    # SIMULCACION DE PROCESAMIENTO
    eventos_prueba = generar_eventos_prueba(15)

    # CADENA DE VALIDADORES
    validator_chain = EventValidatorChain()
    # Anadir validadores a la cadena
    validator_chain.add_validator(NotNullValidator(["tipo_evento","fecha_accion","user_id","sesion_id"]))
    validator_chain.add_validator(EventTypeValidator(["ProductViewed", "AddTocart", "LogEvent"]))
    validator_chain.add_validator(ProductDetailsValidator())

    validator_chain.build_chain()
    resultados = []

    for i, evento_bruto in enumerate(eventos_prueba):
        evento = EventFactory.crear_evento(evento_bruto)
        es_valido = validator_chain.validate(evento)

        #Guardar resultados
        resultados.append({
            "id": i + 1,
            "tipo": evento_bruto["tipo_evento"],
            "valido": es_valido,
            "errores": validator_chain.errors.copy(),
            "evento": evento.to_dict() if hasattr(evento, 'to_dict') else str(evento)
        })
        # Mostrar resumen
        print(
            f"Evento {i + 1}: {evento_bruto['tipo_evento']} - {'Válido' if es_valido else f'Inválido: {validator_chain.errors}'}")

    # Análisis de resultados
    total_eventos = len(resultados)
    eventos_validos = sum(1 for r in resultados if r["valido"])
    porcentaje_valido = (eventos_validos / total_eventos) * 100

    print(f"\nResumen de validación:")
    print(f"Total eventos: {total_eventos}")
    print(f"Eventos válidos: {eventos_validos} ({porcentaje_valido:.2f}%)")
    print(f"Eventos inválidos: {total_eventos - eventos_validos}")

    # Mostrar detalles de eventos inválidos
    print("\nDetalles de eventos inválidos:")
    for res in resultados:
        if not res["valido"]:
            print(f"Evento {res['id']} ({res['tipo']}):")
            for error in res["errores"]:
                print(f"  - {error['field']}: {error['message']}")
            print("  Datos completos:", res["evento"])
            print()




