import streamlit as st
import json
import time
import random
from pathlib import Path

# ─── Configuración de página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="PAES Repositorio",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS personalizado ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #0f1117; }

    /* Título principal */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        padding: 1rem 0 0.2rem 0;
        letter-spacing: 1px;
    }
    .main-subtitle {
        text-align: center;
        color: #888;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Tarjeta de pregunta */
    .question-card {
        background: #1a1d2e;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #2a2d3e;
        margin-bottom: 1rem;
    }

    /* Badge prueba/eje */
    .badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 10px;
    }
    .badge-m1  { background: #1e3a5f; color: #90CAF9; }
    .badge-m2  { background: #1e3a2a; color: #A5D6A7; }
    .badge-fis { background: #3a1e2a; color: #F48FB1; }
    .badge-eje { background: #2a2a1e; color: #FFD54F; }

    /* Timer */
    .timer-box {
        background: #1a1d2e;
        border: 2px solid #2a2d3e;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .timer-digits {
        font-size: 2.8rem;
        font-weight: 800;
        font-family: monospace;
        color: #90CAF9;
        line-height: 1;
    }
    .timer-digits.warning { color: #FFD54F; }
    .timer-digits.danger  { color: #EF5350; }
    .timer-label {
        font-size: 0.75rem;
        color: #888;
        margin-top: 4px;
    }

    /* Botones alternativas */
    div[data-testid="stRadio"] > label {
        font-size: 1rem;
        color: #ddd;
    }

    /* Resultado correcto/incorrecto */
    .result-correct {
        background: #1b3a2a;
        border: 1.5px solid #4CAF50;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #A5D6A7;
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }
    .result-incorrect {
        background: #3a1a1a;
        border: 1.5px solid #EF5350;
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        color: #EF9A9A;
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #13151f;
    }
    .sidebar-section {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 1rem 0 0.4rem 0;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ─── Cargar problemas ──────────────────────────────────────────────────────────
@st.cache_data
def load_problems():
    with open("problems.json", "r", encoding="utf-8") as f:
        return json.load(f)

problems = load_problems()

# ─── Estado de sesión ──────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "problema_actual": None,
        "respondido": False,
        "seleccion": None,
        "timer_start": None,
        "timer_duracion": 90,
        "tiempo_agotado": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📐 PAES Repositorio")
    st.markdown("---")

    st.markdown('<div class="sidebar-section">⏱ Tiempo por pregunta</div>', unsafe_allow_html=True)
    timer_choice = st.radio(
        "Selecciona duración",
        [90, 120],
        format_func=lambda x: f"{x} segundos",
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.timer_duracion = timer_choice

    st.markdown("---")
    st.markdown('<div class="sidebar-section">🔍 Buscar por nombre</div>', unsafe_allow_html=True)
    nombres = [p["nombre"] for p in problems]
    busqueda = st.selectbox("Buscar problema", ["— Selecciona —"] + nombres, label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="sidebar-section">🎯 Filtrar por prueba</div>', unsafe_allow_html=True)
    pruebas_disp = sorted(set(p["prueba"] for p in problems))
    filtro_prueba = st.multiselect("Prueba", pruebas_disp, default=pruebas_disp, label_visibility="collapsed")

    st.markdown('<div class="sidebar-section">📚 Filtrar por eje</div>', unsafe_allow_html=True)
    ejes_disp = sorted(set(p["eje"] for p in problems))
    filtro_eje = st.multiselect("Eje", ejes_disp, default=ejes_disp, label_visibility="collapsed")

    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        btn_aleatorio = st.button("🎲 Aleatorio", use_container_width=True)
    with col_s2:
        btn_buscar = st.button("🔎 Buscar", use_container_width=True)

# ─── Lógica de selección de problema ──────────────────────────────────────────
pool = [p for p in problems if p["prueba"] in filtro_prueba and p["eje"] in filtro_eje]

if btn_aleatorio and pool:
    st.session_state.problema_actual = random.choice(pool)
    st.session_state.respondido     = False
    st.session_state.seleccion      = None
    st.session_state.timer_start    = time.time()
    st.session_state.tiempo_agotado = False

if btn_buscar and busqueda != "— Selecciona —":
    encontrado = next((p for p in problems if p["nombre"] == busqueda), None)
    if encontrado:
        st.session_state.problema_actual = encontrado
        st.session_state.respondido     = False
        st.session_state.seleccion      = None
        st.session_state.timer_start    = time.time()
        st.session_state.tiempo_agotado = False

# ─── ÁREA PRINCIPAL ────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📐 Repositorio PAES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Practica problemas de M1 · M2 · Física</div>', unsafe_allow_html=True)

prob = st.session_state.problema_actual

if prob is None:
    st.info("👈 Usa el panel izquierdo para seleccionar un problema aleatorio o buscarlo por nombre.")
    st.stop()

# ─── Layout: pregunta (izq) + timer (der) ─────────────────────────────────────
col_q, col_t = st.columns([3, 1])

# ── Timer ──────────────────────────────────────────────────────────────────────
with col_t:
    duracion = st.session_state.timer_duracion
    elapsed  = time.time() - (st.session_state.timer_start or time.time())
    restante = max(0, duracion - int(elapsed))

    mins = restante // 60
    segs = restante % 60

    # Color según tiempo restante
    pct = restante / duracion
    if pct > 0.4:
        cls = ""
    elif pct > 0.2:
        cls = "warning"
    else:
        cls = "danger"

    # Emoji reloj de arena animado
    hourglass = "⏳" if segs % 2 == 0 else "⌛"

    st.markdown(f"""
    <div class="timer-box">
        <div style="font-size:2rem;">{hourglass}</div>
        <div class="timer-digits {cls}">{mins:01d}:{segs:02d}</div>
        <div class="timer-label">{'⏱ '+str(duracion)+'s disponibles'}</div>
    </div>
    """, unsafe_allow_html=True)

    if restante == 0 and not st.session_state.respondido:
        st.session_state.tiempo_agotado = True
        st.session_state.respondido     = True

    if not st.session_state.respondido:
        time.sleep(1)
        st.rerun()

# ── Pregunta ───────────────────────────────────────────────────────────────────
with col_q:
    # Badges
    badge_cls = {"M1": "badge-m1", "M2": "badge-m2", "Física": "badge-fis"}.get(prob["prueba"], "badge-m1")
    st.markdown(f"""
    <span class="badge {badge_cls}">{prob['prueba']}</span>
    <span class="badge badge-eje">{prob['eje']}</span>
    <span style="color:#666; font-size:0.8rem;">{prob['nombre']}</span>
    """, unsafe_allow_html=True)

    # Imagen del problema
    img_path = Path(prob["imagen"])
    if img_path.exists():
        st.image(str(img_path), use_container_width=True)
    else:
        st.warning(f"⚠️ Imagen no encontrada: `{prob['imagen']}`")

    st.markdown("---")

    # Alternativas
    alt = prob["alternativas"]
    opciones = [f"**{k})** {v}" for k, v in alt.items()]
    letras   = list(alt.keys())

    if not st.session_state.respondido:
        seleccion_idx = st.radio(
            "Selecciona tu respuesta:",
            range(len(opciones)),
            format_func=lambda i: opciones[i],
            index=None,
            key="radio_resp"
        )

        col_b1, col_b2 = st.columns([1, 3])
        with col_b1:
            confirmar = st.button("✅ Confirmar", use_container_width=True, type="primary")

        if confirmar:
            if seleccion_idx is None:
                st.warning("Selecciona una alternativa antes de confirmar.")
            else:
                st.session_state.seleccion  = letras[seleccion_idx]
                st.session_state.respondido = True
                st.rerun()
    else:
        # Mostrar alternativas sin interacción
        for k, v in alt.items():
            st.markdown(f"**{k})** {v}")

    # ── Resultado ──────────────────────────────────────────────────────────────
    if st.session_state.respondido:
        correcta = prob["respuesta_correcta"]

        if st.session_state.tiempo_agotado:
            st.markdown(f"""
            <div class="result-incorrect">
                ⏰ ¡Tiempo agotado! La respuesta correcta era <strong>{correcta}</strong>.
            </div>
            """, unsafe_allow_html=True)

        elif st.session_state.seleccion == correcta:
            st.markdown(f"""
            <div class="result-correct">
                ✅ ¡Correcto! La alternativa <strong>{correcta}</strong> es la respuesta correcta.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-incorrect">
                ❌ Incorrecto. Seleccionaste <strong>{st.session_state.seleccion}</strong>,
                pero la respuesta correcta es <strong>{correcta}</strong>.
            </div>
            """, unsafe_allow_html=True)

        # Botón YouTube
        if prob.get("video_youtube"):
            st.markdown("---")
            st.link_button(
                "▶️ Ver explicación en YouTube",
                prob["video_youtube"],
                use_container_width=False,
                type="secondary"
            )

        # Botón siguiente problema
        st.markdown("")
        if st.button("➡️ Otro problema aleatorio", use_container_width=False):
            if pool:
                st.session_state.problema_actual = random.choice(pool)
                st.session_state.respondido     = False
                st.session_state.seleccion      = None
                st.session_state.timer_start    = time.time()
                st.session_state.tiempo_agotado = False
                st.rerun()
