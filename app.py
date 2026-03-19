import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import json
import time
import random
from pathlib import Path

logo_favicon = Image.open("LogoCM.png")

st.set_page_config(
    page_title="Complemento Matemático - PAES",
    page_icon=logo_favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

LOGO_B64 = "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"

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    .header-bar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 1rem 2rem 0.5rem 2rem;
    }
    .header-left {
        display: flex; flex-direction: column; justify-content: center;
    }
    .header-title {
        font-size: 2rem; font-weight: 900; color: #ffffff;
        letter-spacing: 1px; line-height: 1.1;
    }
    .header-subtitle {
        font-size: 0.95rem; color: #a0a0b0; font-weight: 400; margin-top: 2px;
    }
    .header-logo img { height: 80px; }
    [data-testid="stSidebar"] { background-color: #161b27 !important; }
    div[data-testid="stSidebarContent"] { padding: 1.5rem 1rem; }
    .sidebar-section {
        color: #7ecfff; font-size: 0.75rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase; margin: 1.2rem 0 0.4rem;
    }
    .stRadio label { color: #c8d0e0 !important; font-size: 0.9rem; }
    .stSelectbox label { color: #7ecfff !important; font-weight: 700;
        font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase; }
    .stButton > button {
        width: 100%; border-radius: 8px; font-weight: 700;
        transition: all 0.2s; border: none; cursor: pointer;
    }
    .btn-aleatorio > button {
        background: linear-gradient(135deg, #1e3a5f, #2d5986);
        color: #7ecfff; border: 1px solid #2d5986;
    }
    .btn-aleatorio > button:hover { background: linear-gradient(135deg, #2d5986, #3d78c4); }
    .btn-buscar > button {
        background: linear-gradient(135deg, #1a4a2e, #2d7a4f);
        color: #5debb0; border: 1px solid #2d7a4f;
    }
    .btn-buscar > button:hover { background: linear-gradient(135deg, #2d7a4f, #3daa6f); }
    .question-card {
        background: #ffffff; border-radius: 16px; padding: 2rem 2.5rem;
        box-shadow: 0 4px 32px rgba(0,0,0,0.4); color: #1a1a2e;
        margin: 0 auto; max-width: 820px;
    }
    .question-image { width: 100%; border-radius: 8px; margin: 1rem 0; }
    .badge-prueba {
        display: inline-block; background: #1e3a5f; color: #7ecfff;
        border-radius: 20px; padding: 3px 14px; font-size: 0.8rem;
        font-weight: 700; margin-right: 6px;
    }
    .badge-eje {
        display: inline-block; background: #1a4a2e; color: #5debb0;
        border-radius: 20px; padding: 3px 14px; font-size: 0.8rem;
        font-weight: 700; margin-right: 6px;
    }
    .badge-nombre {
        display: inline-block; background: #2d1f4e; color: #c084fc;
        border-radius: 20px; padding: 3px 14px; font-size: 0.8rem; font-weight: 700;
    }
    .alt-btn {
        display: block; width: 100%; text-align: left; padding: 0.65rem 1.1rem;
        margin-bottom: 0.45rem; border-radius: 10px; cursor: pointer;
        font-size: 0.97rem; border: 1.5px solid transparent;
        background: #f0f4ff; color: #1a1a2e; transition: all 0.18s;
        font-weight: 500;
    }
    .alt-btn:hover { background: #dbeafe; border-color: #3b82f6; }
    .alt-btn.selected { background: #dbeafe; border-color: #2563eb; font-weight: 700; }
    .alt-btn.correct { background: #d1fae5; border-color: #059669; color: #065f46; font-weight: 700; }
    .alt-btn.incorrect { background: #fee2e2; border-color: #dc2626; color: #7f1d1d; }
    .result-msg-correct {
        background: #d1fae5; border-left: 5px solid #059669;
        padding: 0.9rem 1.2rem; border-radius: 8px; color: #065f46;
        font-weight: 700; margin-top: 1rem;
    }
    .result-msg-incorrect {
        background: #fee2e2; border-left: 5px solid #dc2626;
        padding: 0.9rem 1.2rem; border-radius: 8px; color: #7f1d1d;
        font-weight: 700; margin-top: 1rem;
    }
    .timer-box {
        background: #161b27; border-radius: 16px; padding: 1.2rem;
        text-align: center; border: 1px solid #2d3748; margin-bottom: 1rem;
    }
    .timer-display {
        font-size: 3rem; font-weight: 900; color: #7ecfff;
        font-family: 'Courier New', monospace; letter-spacing: 4px;
    }
    .timer-icon { font-size: 1.8rem; margin-bottom: 4px; }
    .btn-timer > button {
        background: linear-gradient(135deg, #c0392b, #e74c3c) !important;
        color: white !important; font-size: 1rem !important; padding: 0.7rem 1rem !important;
    }
    .btn-timer > button:hover { background: linear-gradient(135deg, #e74c3c, #ff6b6b) !important; }
    .youtube-btn a {
        display: block; background: linear-gradient(135deg, #c0392b, #e74c3c);
        color: white; text-align: center; padding: 0.7rem; border-radius: 10px;
        text-decoration: none; font-weight: 700; margin-top: 0.5rem;
    }
    .youtube-btn a:hover { background: linear-gradient(135deg, #e74c3c, #ff6b6b); }
    .stSelectbox > div > div {
        background-color: #1e2535 !important;
        color: #c8d0e0 !important;
        border-color: #2d3748 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def cargar_preguntas():
    ruta = Path("problems.json")
    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def mostrar_header():
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-left">
            <div class="header-title">COMPLEMENTO<br>MATEMÁTICO</div>
            <div class="header-subtitle">Entrenamiento PAES · Matemática</div>
        </div>
        <div class="header-logo">
            <img src="data:image/jpeg;base64,{LOGO_B64}" alt="Logo">
        </div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_pregunta_card(pregunta, preguntas):
    nombre = pregunta.get("nombre", pregunta.get("id", ""))
    prueba = pregunta.get("prueba", "")
    eje    = pregunta.get("eje", "")
    imagen = pregunta.get("imagen", "")
    alts   = pregunta.get("alternativas", {})
    resp   = pregunta.get("respuesta_correcta", "")
    video  = pregunta.get("video_youtube", "")

    st.markdown(f"""
    <div style="margin-bottom:0.7rem;">
        <span class="badge-prueba">{prueba}</span>
        <span class="badge-eje">{eje}</span>
        <span class="badge-nombre">{nombre}</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="question-card">', unsafe_allow_html=True)

        img_path = Path(imagen)
        if img_path.exists():
            img = Image.open(img_path)
            st.image(img, use_container_width=True)
        else:
            st.warning(f"Imagen no encontrada: {imagen}")

        st.markdown("**Selecciona una alternativa:**")

        sel_key = f"sel_{nombre}"
        if sel_key not in st.session_state:
            st.session_state[sel_key] = None

        for letra, texto in alts.items():
            estilo = "alt-btn"
            if st.session_state[sel_key] is not None:
                if letra == resp:
                    estilo += " correct"
                elif letra == st.session_state[sel_key]:
                    estilo += " incorrect"
                else:
                    estilo += " selected" if letra == st.session_state[sel_key] else ""

            if st.button(
                f"{letra})  {texto}",
                key=f"alt_{nombre}_{letra}",
                use_container_width=True
            ):
                st.session_state[sel_key] = letra
                st.rerun()

        if st.session_state[sel_key] is not None:
            if st.session_state[sel_key] == resp:
                st.markdown('<div class="result-msg-correct">✅ ¡Correcto! Muy bien.</div>', unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="result-msg-incorrect">❌ Incorrecto. La respuesta correcta es <strong>{resp}</strong>.</div>',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    col_yt, _ = st.columns([1, 2])
    with col_yt:
        if video:
            st.markdown(f"""
            <div class="youtube-btn">
                <a href="{video}" target="_blank">▶ Ver solución en YouTube</a>
            </div>
            """, unsafe_allow_html=True)


def sidebar_timer():
    st.sidebar.markdown('<div class="sidebar-section">⏱ TIEMPO POR PREGUNTA</div>', unsafe_allow_html=True)
    tiempo_seg = st.sidebar.radio(
        "",
        options=[90, 120],
        format_func=lambda x: f"{x} segundos",
        key="tiempo_radio"
    )

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False
    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None
    if "timer_duracion" not in st.session_state:
        st.session_state.timer_duracion = tiempo_seg

    ph_timer = st.sidebar.empty()

    def render_timer(segundos_restantes):
        mins = segundos_restantes // 60
        secs = segundos_restantes % 60
        color = "#e74c3c" if segundos_restantes <= 10 else "#7ecfff"
        ph_timer.markdown(f"""
        <div class="timer-box">
            <div class="timer-icon">⏳</div>
            <div class="timer-display" style="color:{color};">{mins:01d}:{secs:02d}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.timer_running:
        elapsed  = int(time.time() - st.session_state.timer_start)
        restante = max(0, st.session_state.timer_duracion - elapsed)
        render_timer(restante)
        if restante > 0:
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.sidebar.warning("⏰ ¡Tiempo agotado!")
    else:
        render_timer(tiempo_seg)

    st.sidebar.markdown('<div class="btn-timer">', unsafe_allow_html=True)
    if st.sidebar.button("▶ Iniciar cronómetro", key="btn_iniciar_timer"):
        st.session_state.timer_running  = True
        st.session_state.timer_start    = time.time()
        st.session_state.timer_duracion = tiempo_seg
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


def main():
    mostrar_header()
    preguntas = cargar_preguntas()

    if not preguntas:
        st.error("No se encontraron preguntas. Verifica el archivo preguntas.json.")
        return

    nombres = [p.get("nombre", p.get("id", "")) for p in preguntas]

    # ── Estado inicial ──────────────────────────────────────────────────────
    if "pregunta_idx" not in st.session_state:
        st.session_state.pregunta_idx = 0
    if "selectbox_nombre" not in st.session_state:
        st.session_state.selectbox_nombre = nombres[0]

    # ── Sidebar ─────────────────────────────────────────────────────────────
    sidebar_timer()

    st.sidebar.markdown('<div class="sidebar-section">🔍 BUSCAR POR NOMBRE</div>', unsafe_allow_html=True)

    # ── CAMBIO CLAVE: on_change actualiza el índice automáticamente ──────────
    def on_select_change():
        nombre_sel = st.session_state["buscar_select"]
        if nombre_sel in nombres:
            st.session_state.pregunta_idx = nombres.index(nombre_sel)

    st.sidebar.selectbox(
        "",
        options=nombres,
        index=st.session_state.pregunta_idx,
        key="buscar_select",
        on_change=on_select_change,          # ← se dispara al cambiar selección
    )

    # ── Botón Aleatorio (se mantiene) ────────────────────────────────────────
    st.sidebar.markdown("")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        st.markdown('<div class="btn-aleatorio">', unsafe_allow_html=True)
        if st.button("🎲 Aleatorio", key="btn_aleatorio"):
            st.session_state.pregunta_idx = random.randint(0, len(preguntas) - 1)
            st.session_state.selectbox_nombre = nombres[st.session_state.pregunta_idx]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Mostrar pregunta actual ──────────────────────────────────────────────
    idx      = st.session_state.pregunta_idx
    pregunta = preguntas[idx]

    col_pregunta, col_timer = st.columns([3, 1])
    with col_pregunta:
        mostrar_pregunta_card(pregunta, preguntas)


if __name__ == "__main__":
    main()
