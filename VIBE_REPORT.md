# Vibe Report: EcoTrack

**App desplegada:** https://erayt5kwopqjyqmdzdw9wk.streamlit.app/
**Repositorio:** https://github.com/Jacobo2025/EcoTrack-

## 1. Cómo configuré las reglas del agente
Creé un archivo `.cursorrules` con cinco bloques: rol, stack, estilo de código, comportamiento y diseño. Fijé el stack (Python + Streamlit) para que el agente no inventara arquitecturas innecesarias, y exigí funciones pequeñas y modulares con type hints. También le pedí resumir su plan antes de cambios grandes y explicarme cómo probar cada cambio, lo que me dio control sin escribir código a mano. Añadí una regla de resiliencia: si el modelo de lenguaje falla, la app usa un parser por reglas y nunca se rompe. Los secretos, como la API key de Anthropic, se manejan solo como variables de entorno.

## 2. Dificultades al delegar el código
- **Límites de créditos:** el agente de Replit agotó mis créditos diarios y quedé sin poder pedirle más cambios. Aprendí a agrupar instrucciones en pocos prompts claros.
- **Despliegue fallido:** la publicación automática en Replit falló y, además, el plan gratuito hace expirar la app a los 30 días. Resolví el problema desplegando el mismo repositorio en Streamlit Community Cloud, que es gratuito.
- **Fallos silenciosos:** el agente de Replit notó que, si Claude falla, la app cambia al parser de reglas sin explicar por qué. Es un ejemplo de por qué revisar lo que genera la IA sigue siendo mi responsabilidad.
- **Estimaciones aproximadas:** los factores de emisión son promedios orientativos, no mediciones exactas. Por eso la interfaz lo advierte de forma explícita.
- **Verificación manual:** probé frases variadas (por ejemplo, "Hoy comí carne y viajé 20km en bus", que da 7.78 kg CO2e) en lugar de confiar ciegamente en el código generado.

## 3. De escribir código a orquestar una visión
Pasé de preguntarme "¿cómo se escribe esto?" a "¿qué debe lograr esto y cómo sabré que funciona?". Mi trabajo dejó de ser la sintaxis y pasó a ser el criterio: definir reglas claras, detectar cuándo el agente se desvía y decidir qué es suficiente para un MVP. Al principio resulta incómodo no controlar cada línea, pero la velocidad de iteración lo compensa: tuve una app funcionando en local, en Replit y en la nube en una sola sesión. También entendí que delegar no es desentenderse: la calidad del resultado depende de qué tan bien comunico la intención y de cuánto pruebo lo que me devuelve la IA. La responsabilidad final sigue siendo mía.

## 4. Conclusión
El Vibe Coding acelera el prototipado, pero exige buenas reglas, pruebas propias y un plan B cuando las herramientas fallan, como me ocurrió con los créditos y el despliegue.
