"""EcoTrack: estima tu huella de carbono diaria desde texto natural."""
import json
import os
import re

import streamlit as st

# Factores aproximados (kg CO2e). Fuente orientativa: promedios de literatura pública.
TRANSPORT_PER_KM = {"bus": 0.089, "autobus": 0.089, "auto": 0.17, "carro": 0.17,
                    "coche": 0.17, "moto": 0.10, "metro": 0.04, "avion": 0.15,
                    "bici": 0.0, "bicicleta": 0.0}
FOOD_PER_MEAL = {"carne": 6.0, "res": 6.0, "cerdo": 2.5, "pollo": 1.6,
                 "pescado": 1.5, "huevo": 0.8, "vegetariano": 0.8, "ensalada": 0.4}
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-5")
SYSTEM = (
    "Eres un estimador de huella de carbono. Del texto del usuario extrae actividades y "
    "responde SOLO con JSON: una lista de objetos con llaves activity (str), category "
    "(transporte|alimentacion|energia|otro) y kg_co2e (number, estimación razonable). "
    f"Referencias: bus {TRANSPORT_PER_KM['bus']} kg/km, auto {TRANSPORT_PER_KM['auto']} kg/km, "
    f"comida con carne de res {FOOD_PER_MEAL['res']} kg, pollo {FOOD_PER_MEAL['pollo']} kg. "
    "Sin texto extra ni markdown."
)


def normalize(text: str) -> str:
    """Minúsculas y sin tildes para comparar palabras clave."""
    return text.lower().translate(str.maketrans("áéíóú", "aeiou"))


def parse_with_rules(text: str) -> list[dict]:
    """Respaldo sin LLM: detecta km por medio de transporte y comidas por palabra clave."""
    t, items = normalize(text), []
    modes = "|".join(TRANSPORT_PER_KM)
    for km, mode in re.findall(rf"(\d+(?:[.,]\d+)?)\s*km\s*(?:en|de|por|con)?\s*({modes})", t):
        km = float(km.replace(",", "."))
        items.append({"activity": f"{km:g} km en {mode}", "category": "transporte",
                      "kg_co2e": round(km * TRANSPORT_PER_KM[mode], 2)})
    for food, kg in FOOD_PER_MEAL.items():
        if re.search(rf"\b{food}\b", t):
            items.append({"activity": f"Comida con {food}", "category": "alimentacion", "kg_co2e": kg})
    return items


def parse_with_llm(text: str) -> list[dict]:
    """Estimación con Claude; devuelve lista de actividades."""
    import anthropic
    resp = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=800, system=SYSTEM,
        messages=[{"role": "user", "content": text}])
    raw = re.sub(r"```json|```", "", resp.content[0].text).strip()
    return json.loads(raw)


def estimate(text: str) -> tuple[list[dict], str]:
    """Intenta el LLM y cae al parser de reglas si algo falla."""
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return parse_with_llm(text), "IA (Claude)"
        except Exception:
            pass
    return parse_with_rules(text), "reglas de respaldo"


TIPS = {
    "transporte": (
        "Prioriza bus, metro o bici en trayectos cortos.",
        "Agrupa recados en un solo viaje.",
        "Si usas auto, comparte el trayecto cuando puedas.",
    ),
    "alimentacion": (
        "Una comida sin carne de res baja mucho la huella.",
        "Prueba más vegetales y legumbres esta semana.",
        "Aprovecha sobras para no desperdiciar comida.",
    ),
    "energia": (
        "Apaga luces y equipos que no estés usando.",
        "Usa climatización con moderación.",
        "Seca la ropa al aire cuando el clima lo permita.",
    ),
    "otro": (
        "Elige cosas que duren: menos compras, menos emisiones.",
        "Reutiliza lo que ya tienes antes de comprar.",
        "Un hábito pequeño y constante sí suma.",
    ),
}
CAT_LABEL = {
    "transporte": "transporte",
    "alimentacion": "alimentación",
    "energia": "energía",
    "otro": "otros hábitos",
}


def totals_by_category(items: list[dict]) -> dict[str, float]:
    """Suma kg CO2e por categoría."""
    by_cat: dict[str, float] = {}
    for item in items:
        by_cat[item["category"]] = by_cat.get(item["category"], 0) + item["kg_co2e"]
    return by_cat


def dominant_category(items: list[dict]) -> str | None:
    """Categoría con más kg CO2e, o None si no hay datos."""
    by_cat = totals_by_category(items)
    return max(by_cat, key=by_cat.get) if by_cat else None


def apply_theme() -> None:
    """Aplica paleta verde/tierra y un layout más limpio."""
    st.markdown(
        """
        <style>
        .stApp { background-color: #f4f1ea; color: #1b4332; }
        [data-testid="stHeader"] { background: transparent; }
        .stButton>button { background: #2d6a4f; color: #f4f1ea; border: 0; }
        .stButton>button:hover { background: #40916c; color: #fff; }
        [data-testid="stMetricValue"] { color: #2d6a4f; }
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="EcoTrack", page_icon="🌱", layout="centered")
apply_theme()
st.title("🌱 EcoTrack")
st.caption("Cuéntame tu día y estimo tu huella de carbono. Los valores son aproximados.")

if "log" not in st.session_state:
    st.session_state.log = []

text = st.text_area("¿Qué hiciste hoy?", placeholder="Hoy comí carne y viajé 20km en bus")
if st.button("Calcular huella", type="primary") and text.strip():
    items, engine = estimate(text)
    if items:
        st.session_state.log.extend(items)
        st.success(f"Estimación hecha con {engine}")
    else:
        st.warning("No pude identificar actividades. Prueba con: 'viajé 10 km en auto'.")

if st.session_state.log:
    total = sum(i["kg_co2e"] for i in st.session_state.log)
    st.metric("Total acumulado", f"{total:.2f} kg CO2e")
    st.caption("Estimación aproximada en kg CO2e.")
    st.dataframe(st.session_state.log, use_container_width=True)
    by_cat = totals_by_category(st.session_state.log)
    st.bar_chart(by_cat)
    top = dominant_category(st.session_state.log)
    if top:
        st.subheader("Un empujón para mañana")
        st.write(f"Hoy tu mayor impacto está en **{CAT_LABEL.get(top, top)}**. Prueba esto:")
        for tip in TIPS.get(top, TIPS["otro"]):
            st.markdown(f"- {tip}")
    if st.button("Reiniciar día"):
        st.session_state.log = []
        st.rerun()
