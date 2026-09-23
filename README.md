# 🌱 EcoTrack

MVP web que estima la **huella de carbono diaria** a partir de una frase en lenguaje natural, por ejemplo: *"Hoy comí carne y viajé 20km en bus"*. Fue construido con la metodología **Vibe Coding**: el código se generó y se iteró con agentes de IA (Cursor y Replit), y mi trabajo fue definir la visión, las reglas y verificar el resultado.

- **App desplegada:** https://erayt5kwopqjyqmdzdw9wk.streamlit.app/
- **Repositorio:** https://github.com/Jacobo2025/EcoTrack-

---

## 1. ¿Qué hace la app?

1. El usuario escribe qué hizo durante el día.
2. La app identifica actividades (transporte y alimentación) y estima sus emisiones en **kg CO₂e**.
3. Muestra el total acumulado, una tabla de actividades y un gráfico de barras por categoría.
4. Ofrece consejos personalizados según la categoría que más contamina (sección "Un empujón para mañana", añadida con el Composer de Cursor).
5. Permite reiniciar el día.

**Ejemplo:** *"Hoy comí carne y viajé 20km en bus"* → 6.00 kg (comida con carne) + 1.78 kg (20 km × 0.089) = **7.78 kg CO₂e**.

### Dos motores de estimación

| Motor | Cuándo se usa | Cómo funciona |
|---|---|---|
| **IA (Claude)** | Si existe la variable `ANTHROPIC_API_KEY` | El modelo (por defecto `claude-sonnet-5`, configurable con `ANTHROPIC_MODEL`) devuelve un JSON con actividades, categoría y kg CO₂e. |
| **Reglas de respaldo** | Sin API key o si Claude falla | Expresiones regulares y palabras clave con factores de emisión fijos. |

La app **nunca se rompe** si el modelo falla: cae al parser de reglas. Un mensaje en pantalla indica qué motor hizo la estimación.

### Factores de emisión del modo de reglas (aproximados)

| Transporte | kg CO₂e por km | Alimentación | kg CO₂e por comida |
|---|---|---|---|
| Bus / autobús | 0.089 | Carne / res | 6.0 |
| Auto / carro / coche | 0.17 | Cerdo | 2.5 |
| Moto | 0.10 | Pollo | 1.6 |
| Metro | 0.04 | Pescado | 1.5 |
| Avión | 0.15 | Huevo / vegetariano | 0.8 |
| Bici / bicicleta | 0.0 | Ensalada | 0.4 |

> Son promedios orientativos, no mediciones exactas. La interfaz lo advierte.

---

## 2. Estructura del proyecto

```
EcoTrack-/
├── app.py                 # Aplicación Streamlit (parser, cálculo y UI)
├── requirements.txt       # streamlit, anthropic
├── .cursorrules           # Reglas del agente de IA (Cursor)
├── .replit                # Configuración de ejecución en Replit
├── .streamlit/config.toml # Tema verde/tierra (creado por el agente de Cursor)
├── .gitignore             # Excluye .venv, __pycache__, .env
├── VIBE_REPORT.md         # Reflexión sobre el proceso (máx. 500 palabras)
└── README.md              # Este documento
```

**Diseño de `app.py`:** funciones pequeñas y separadas: `normalize` (limpia texto y tildes), `parse_with_rules` (respaldo), `parse_with_llm` (Claude), `estimate` (elige motor con respaldo automático) y la interfaz Streamlit.

---

## 3. Cómo ejecutarlo en local

```bash
git clone https://github.com/Jacobo2025/EcoTrack-.git
cd EcoTrack-
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Se abre en http://localhost:8501.

**Opcional (IA real):**

```bash
export ANTHROPIC_API_KEY="tu_clave"
export ANTHROPIC_MODEL="claude-sonnet-5"   # opcional
```

Nunca escribas la clave dentro del código. En Replit se guarda en *Secrets*, y en Streamlit Cloud en *Advanced settings → Secrets*.

**Pruebas sugeridas:**
1. `Hoy comí carne y viajé 20km en bus` → 7.78 kg CO₂e.
2. `viajé 80 km en auto` → el transporte pasa a ser la categoría dominante y cambian los consejos.
3. `hola` → aviso amarillo, sin errores.
4. Botón **Reiniciar día** → vacía el registro.

---

## 4. Qué hicimos, paso a paso

### Fase 1: Preparación del entorno
1. **Cursor:** instalé el IDE, creé la carpeta del proyecto y añadí `.cursorrules` y `app.py`.
2. **Replit:** creé la cuenta e importé el repositorio desde GitHub.
3. **Modelos:** usé los agentes integrados de Cursor y Replit; la app opcionalmente llama a Claude con la API de Anthropic.

### Fase 2: El "vibe" inicial
1. Ejecuté la app en local (`localhost:8501`) y verifiqué el cálculo.
2. En el Composer de Cursor usé este prompt:
   > *"Lee .cursorrules. Revisa app.py y mejora la interfaz con un tono verde minimalista. Añade una sección de consejos personalizados según la categoría que más contamina. Explícame cómo probarlo."*
   
   El agente aplicó una paleta verde/tierra, creó `.streamlit/config.toml`, añadió la sección de consejos y respetó la regla de no tocar el parser.
3. Detecté que los archivos de configuración quedaron sin punto inicial (`cursorrules`, `replit`) y los renombré a `.cursorrules` y `.replit`.
4. Creé un `.gitignore` para no subir el entorno virtual `.venv`.
5. Subí todo a GitHub.

### Fase 3: Despliegue
1. **Replit:** el agente configuró el workflow de Streamlit y la app corrió correctamente en la vista previa.
2. Se agotaron los **créditos diarios** del agente, y la **publicación en Replit Cloud falló**. Además, el plan gratuito hace expirar las apps publicadas a los 30 días.
3. **Solución:** desplegué el mismo repositorio en **Streamlit Community Cloud** (gratuito), que redespliega automáticamente con cada `git push`.

### Fase 4: Documentación
Redacté el `VIBE_REPORT.md` y este README, y tomé una captura con Cursor y Replit operando en conjunto.

---

## 5. Contenido de `.cursorrules`

Define la "personalidad" y las reglas del agente. Está organizado en cinco bloques:

```
# Rol
Eres el copiloto senior de EcoTrack, un MVP web que estima la huella de carbono
diaria a partir de texto en lenguaje natural. Yo defino la visión; tú escribes
y ejecutas el código.

# Stack
- Python 3.11 + Streamlit. Sin frameworks extra salvo que los pida.
- LLM: API de Anthropic (modelo en variable de entorno ANTHROPIC_MODEL).
- Secretos solo en variables de entorno (Replit Secrets). Nunca en el código.

# Estilo de código
- Limpio y modular: separa parsing, cálculo y UI en funciones pequeñas (<30 líneas).
- Type hints y docstrings de una línea.
- Nombres en inglés, textos de interfaz en español.
- Sin código muerto ni comentarios obvios.

# Comportamiento
- Antes de programar algo grande, resume tu plan en 3-5 viñetas.
- Si hay un error, diagnostica la causa raíz y corrígela; no me pidas arreglar sintaxis.
- Cambios mínimos: no reescribas archivos completos si basta un parche.
- Toda estimación de CO2 debe indicar unidad (kg CO2e) y ser transparente sobre
  que es aproximada.
- Si el LLM falla, usa el parser de respaldo por reglas; la app nunca debe romperse.
- Tras cada cambio, dime en una línea cómo probarlo.

# Diseño ("vibe")
Minimalista, tono verde/tierra, cercano y motivador. Un campo de texto, un botón,
resultados claros.
```

**Por qué funciona:** el stack fijo evita arquitecturas innecesarias; "cambios mínimos" protege el código que ya funciona; la regla de resiliencia garantiza el respaldo; y "dime cómo probarlo" mantiene mi rol de verificador.

---

## 6. Contenido de `VIBE_REPORT.md`

> Nota: esta es la versión base. El archivo del repositorio es la versión final.

### Cómo configuré las reglas del agente
Creé un archivo `.cursorrules` con cinco bloques: rol, stack, estilo de código, comportamiento y diseño. Fijé el stack (Python + Streamlit) para que el agente no inventara arquitecturas innecesarias, y exigí funciones pequeñas y modulares con type hints. También le pedí resumir su plan antes de cambios grandes y explicarme cómo probar cada cambio, lo que me dio control sin escribir código a mano. Añadí una regla de resiliencia: si el modelo de lenguaje falla, la app usa un parser por reglas y nunca se rompe. Los secretos, como la API key de Anthropic, se manejan solo como variables de entorno.

### Dificultades al delegar el código
- **Límites de créditos:** el agente de Replit agotó mis créditos diarios y quedé sin poder pedirle más cambios. Aprendí a agrupar instrucciones en pocos prompts claros.
- **Despliegue fallido:** la publicación automática en Replit falló y, además, el plan gratuito hace expirar la app a los 30 días. Resolví el problema desplegando el mismo repositorio en Streamlit Community Cloud, que es gratuito.
- **Fallos silenciosos:** el agente de Replit notó que, si Claude falla, la app cambia al parser de reglas sin explicar por qué. Es un ejemplo de por qué revisar lo que genera la IA sigue siendo mi responsabilidad.
- **Estimaciones aproximadas:** los factores de emisión son promedios orientativos, no mediciones exactas. Por eso la interfaz lo advierte de forma explícita.
- **Verificación manual:** probé frases variadas (por ejemplo, "Hoy comí carne y viajé 20km en bus", que da 7.78 kg CO2e) en lugar de confiar ciegamente en el código generado.

### De escribir código a orquestar una visión
Pasé de preguntarme "¿cómo se escribe esto?" a "¿qué debe lograr esto y cómo sabré que funciona?". Mi trabajo dejó de ser la sintaxis y pasó a ser el criterio: definir reglas claras, detectar cuándo el agente se desvía y decidir qué es suficiente para un MVP. Al principio resulta incómodo no controlar cada línea, pero la velocidad de iteración lo compensa: tuve una app funcionando en local, en Replit y en la nube en una sola sesión. También entendí que delegar no es desentenderse: la calidad del resultado depende de qué tan bien comunico la intención y de cuánto pruebo lo que me devuelve la IA. La responsabilidad final sigue siendo mía.

### Conclusión
El Vibe Coding acelera el prototipado, pero exige buenas reglas, pruebas propias y un plan B cuando las herramientas fallan, como me ocurrió con los créditos y el despliegue.

---

## 7. Limitaciones conocidas

- Solo reconoce transporte y alimentación en el modo de reglas; energía y otras categorías dependen del modo IA.
- Los factores de emisión son aproximados y no distinguen país, tamaño de porción ni tipo de vehículo.
- Sin base de datos: el registro se guarda solo en la sesión y se pierde al recargar la página.
- Sin API key no se usa IA real (modo de reglas).
- Si el modelo falla, la app cae al respaldo sin explicar la causa (mejora pendiente).

## 8. Próximos pasos

- Mostrar el motivo cuando Claude falla y se usa el respaldo.
- Añadir energía eléctrica, vuelos y residuos.
- Guardar el historial diario con una base de datos.
- Pruebas automatizadas del parser.

## 9. Herramientas

![Cursor y Replit operando en conjunto](labswnt.png)

**Cursor** (agente y reglas) · **Replit** (importación y ejecución en la nube) · **Streamlit Community Cloud** (despliegue) · **GitHub** (control de versiones) · **Python + Streamlit** · **API de Anthropic** (opcional).
