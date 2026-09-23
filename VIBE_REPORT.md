# Vibe Report: EcoTrack

## 1. Cómo configuré las reglas del agente
Creé un `.cursorrules` con cinco bloques: rol, stack, estilo de código, comportamiento y diseño. Lo más útil fue fijar el stack (Python + Streamlit) y exigir funciones pequeñas y modulares, porque evitó que el agente inventara arquitecturas complejas. También le pedí resumir su plan antes de cambios grandes y explicar cómo probar cada cambio, lo que me dio control sin tocar el código. Añadí una regla de resiliencia: si el LLM falla, se usa un parser por reglas. Los secretos van en Replit Secrets, nunca en el repositorio.

## 2. Dificultades al delegar el código
- **[Completa con tu experiencia real]** Ej.: el modelo devolvía JSON envuelto en markdown y rompía el parseo; lo resolví describiendo el error al agente.
- Los prompts vagos generaban interfaces sobrecargadas; aprendí a ser específico con la intención ("un campo, un botón, resultados claros").
- Las estimaciones de CO2 del LLM varían entre llamadas; por eso incluí factores de referencia en el prompt y un aviso de que son aproximadas.
- Verificar sigue siendo mi trabajo: no confié en el resultado sin probarlo con varias frases.

## 3. De escribir código a orquestar una visión
**[Personaliza esta sección con lo que sentiste.]** Base sugerida: pasé de preguntarme "¿cómo se escribe esto?" a "¿qué debe lograr esto y cómo sabré que funciona?". Mi valor pasó de la sintaxis al criterio: definir reglas, detectar cuando el agente se desvía y decidir qué es suficientemente bueno para un MVP. Al principio hay cierta incomodidad por no controlar cada línea, pero se compensa con la velocidad de iteración. La responsabilidad no se delega: la calidad final sigue siendo mía.

## Enlaces
- Repl/Repositorio: [pega aquí tu URL]
