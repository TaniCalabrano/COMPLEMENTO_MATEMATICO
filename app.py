import streamlit as st
import streamlit.components.v1 as components
import json
import time
import random
import base64
from pathlib import Path
from PIL import Image

logo_favicon = Image.open("LogoCM.png")

st.set_page_config(
    page_title="Complemento Matemático - PAES",
    page_icon=logo_favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Cargar logo dinámicamente desde archivo ──────────────────────────────────
def _cargar_logo_b64() -> str:
    ruta = Path("LogoCM.png")
    if ruta.exists():
        with open(ruta, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

LOGO_B64 = _cargar_logo_b64()


st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    .header-bar {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 1.8rem 2rem 1rem 2rem;
        text-align: center;
        border-bottom: 1px solid #2d3748;
        margin-bottom: 0.8rem;
    }
    .header-top {
        display: flex; align-items: center; justify-content: center; gap: 1rem;
        margin-bottom: 0.5rem;
    }
    .header-logo img {
        height: 80px; width: 80px;
        border-radius: 50%;
        object-fit: cover; object-position: center;
        clip-path: circle(47% at 50% 50%);
        flex-shrink: 0;
    }
    .header-title {
        font-size: 2.2rem; font-weight: 900;
        letter-spacing: 3px; line-height: 1; white-space: nowrap;
        background: linear-gradient(135deg, #f5a623 0%, #f0c040 50%, #e8890a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        filter: drop-shadow(0px 1px 2px rgba(0,0,0,0.5));
    }
    .header-title span {
        background: linear-gradient(135deg, #ffffff 0%, #f5e6c8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .header-subtitle {
        font-size: 0.88rem; color: #f5a623; font-weight: 600;
        margin-top: 4px; letter-spacing: 0.5px;
    }
    .header-subtitle2 {
        font-size: 0.78rem; color: #c8a96e; font-weight: 400; margin-top: 3px;
    }
    .header-subtitle3 {
        font-size: 0.72rem; color: #8a7355; font-weight: 400; margin-top: 2px; font-style: italic;
    }
    .sidebar-brand {
        display: flex; flex-direction: column; align-items: center;
        padding: 1.2rem 0.5rem 0.8rem 0.5rem; text-align: center;
        border-bottom: 1px solid #7a5a1a; margin-bottom: 0.5rem;
    }
    .sidebar-brand img {
        height: 90px; width: 90px;
        border-radius: 50%;
        object-fit: cover;
        object-position: center;
        clip-path: circle(47% at 50% 50%);
        margin-bottom: 0.6rem;
        box-shadow: 0 0 14px rgba(245,166,35,0.4);
    }
    .sidebar-brand-title {
        font-size: 0.95rem; font-weight: 900; letter-spacing: 1.5px; line-height: 1.2;
        background: linear-gradient(135deg, #f5a623, #f0c040);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-brand-prof {
        font-size: 0.72rem; color: #c8a96e; font-weight: 600;
        margin-top: 4px; letter-spacing: 0.3px;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"] {
        background-color: #1a1200 !important;
        background: #1a1200 !important;
    }
    div[data-testid="stSidebarContent"] { padding: 1.5rem 1rem; }
    .sidebar-section {
        color: #f5a623; font-size: 0.75rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase; margin: 1.2rem 0 0.4rem;
        border-left: 3px solid #f5a623; padding-left: 8px;
    }
    .stRadio label { color: #e8d5a0 !important; font-size: 0.9rem; }
    .stSelectbox label { color: #f5a623 !important; font-weight: 700;
        font-size: 0.75rem; letter-spacing: 1.5px; text-transform: uppercase; }
    .stButton > button {
        width: 100%; border-radius: 8px; font-weight: 700;
        transition: all 0.2s; border: none; cursor: pointer;
    }
    .btn-aleatorio > button {
        background: linear-gradient(135deg, #7a4a00, #c07a00);
        color: #fff8e0; border: 1px solid #f5a623;
    }
    .btn-aleatorio > button:hover { background: linear-gradient(135deg, #c07a00, #f5a623); color: #1a1200; }
    .btn-random-timer > button {
        background: linear-gradient(135deg, #7a4a00, #c07a00) !important;
        color: #fff8e0 !important; border: 1px solid #f5a623 !important;
        margin-top: 0.3rem;
    }
    .btn-random-timer > button:hover { background: linear-gradient(135deg, #c07a00, #f5a623) !important; color: #1a1200 !important; }
    .btn-reiniciar > button {
        background: linear-gradient(135deg, #374151, #4b5563) !important;
        color: #f9fafb !important;
        border: 1px solid #6b7280 !important;
        margin-top: 0.2rem;
    }
    .btn-reiniciar > button:hover {
        background: linear-gradient(135deg, #4b5563, #6b7280) !important;
    }
    .stSelectbox > div > div {
        background-color: #2a1f00 !important;
        color: #e8d5a0 !important;
        border-color: #7a5a1a !important;
    }
    .stTextInput > div > div > input {
        background-color: #2a1f00 !important;
        color: #e8d5a0 !important;
        border-color: #7a5a1a !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #7a5a1a !important;
    }
    .question-card {
        background: #ffffff; border-radius: 16px; padding: 2rem 2.5rem;
        box-shadow: 0 4px 32px rgba(0,0,0,0.4); color: #1a1a2e;
        margin: 0 auto; max-width: 820px;
    }
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
    .block-container { padding-top: 1.5rem !important; }
    .header-versiculo {
        font-size: 0.78rem; color: #d4af6e; font-style: italic;
        margin-top: 6px; letter-spacing: 0.3px;
        font-family: Georgia, 'Times New Roman', serif;
    }
    .footer-biblica {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: linear-gradient(90deg, #1a0f00, #2a1800, #1a0f00);
        border-top: 1px solid #7a5a1a;
        padding: 0.55rem 2rem;
        text-align: center;
        z-index: 9999;
    }
    .footer-biblica p {
        margin: 0;
        font-family: Georgia, 'Times New Roman', serif;
        font-size: 0.82rem;
        font-style: italic;
        color: #f0d090;
        letter-spacing: 0.6px;
    }
    .footer-biblica span.ref {
        font-style: normal;
        font-weight: 700;
        color: #f5a623;
        font-size: 0.78rem;
        margin-left: 6px;
        letter-spacing: 1px;
    }
    /* Espacio para que el footer no tape contenido */
    .block-container { padding-bottom: 3.5rem !important; }

    /* ── Animaciones de entrada ────────────────────────────────── */
    @keyframes fadeSlideDown {
        from { opacity: 0; transform: translateY(-18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    /* Header entra desde arriba */
    .header-bar {
        animation: fadeSlideDown 0.6s ease both;
    }
    /* Card de pregunta entra desde abajo */
    .question-card {
        animation: fadeSlideUp 0.55s ease both;
    }
    /* Badges entran con fade suave */
    .badge-prueba, .badge-eje, .badge-nombre {
        animation: fadeIn 0.5s ease both;
    }
    /* Mensajes de resultado aparecen con fade */
    .result-msg-correct, .result-msg-incorrect {
        animation: fadeIn 0.4s ease both;
    }
    /* Footer entra desde abajo */
    .footer-biblica {
        animation: fadeSlideUp 0.7s ease both;
    }
    /* Sidebar brand entra con fade */
    .sidebar-brand {
        animation: fadeIn 0.8s ease both;
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
        <div class="header-top">
            <div class="header-logo">
                <img src="data:image/png;base64,{LOGO_B64}" alt="Logo">
            </div>
            <div class="header-title">COMPLEMENTO <span>MATEMÁTICO</span></div>
        </div>
        <div class="header-subtitle">Prof. Bastiani Calabrano Inostroza</div>
        <div class="header-subtitle2">Entrenamiento PAES · M1 · M2 · Física</div>
        <div class="header-subtitle3">(Los problemas son de autoría del DEMRE)</div>
        <div class="header-versiculo">“Todo lo puedo en Cristo que me fortalece” &mdash; Filipenses 4:13</div>
    </div>
    """, unsafe_allow_html=True)


def mostrar_footer():
    st.markdown("""
    <div class="footer-biblica">
        <p>
            “Porque Jehová da la sabiduría, y de su boca viene el conocimiento y la inteligencia.”
            <span class="ref">Proverbios 2:6</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def mostrar_pregunta_card(pregunta, preguntas):
    import base64 as _b64

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

    # Imagen embebida en base64
    img_path = Path(imagen)
    if img_path.exists():
        with open(img_path, "rb") as _f:
            _img_b64 = _b64.b64encode(_f.read()).decode()
        _img_ext = img_path.suffix.lower().replace(".", "")
        if _img_ext == "jpg":
            _img_ext = "jpeg"
        img_html = (
            f'<div style="margin-bottom:1rem;">'
            f'<img src="data:image/{_img_ext};base64,{_img_b64}" '
            f'style="width:100%;border-radius:8px;" alt="pregunta"/>'
            f'</div>'
        )
    else:
        img_html = f'<div style="color:#e74c3c;padding:1rem;">⚠ Imagen no encontrada: {imagen}</div>'

    st.markdown(f'<div class="question-card">{img_html}', unsafe_allow_html=True)
    st.markdown("**Selecciona una alternativa:**")

    sel_key = f"sel_{nombre}"
    if sel_key not in st.session_state:
        st.session_state[sel_key] = None

    for letra, texto in alts.items():
        if st.button(
            f"{letra})  {texto}",
            key=f"alt_{nombre}_{letra}",
            use_container_width=True,
            disabled=(st.session_state[sel_key] is not None)
        ):
            st.session_state[sel_key] = letra
            st.rerun()

    # ── Resultado ──────────────────────────────────────────────────────────
    if st.session_state[sel_key] is not None:
        import time as _time
        tiempo_str = ""
        t_start = st.session_state.get("timer_start_ts")
        if t_start is not None:
            elapsed  = int(_time.time() - t_start)
            duracion = st.session_state.get("timer_duracion_ts", 90)
            usados   = min(elapsed, duracion)
            m_u = usados // 60
            s_u = usados % 60
            tiempo_str = f" · ⏱ {m_u}m {s_u}s" if m_u > 0 else f" · ⏱ {s_u} segundos"

        if st.session_state[sel_key] == resp:
            st.markdown(
                f'<div class="result-msg-correct">✅ ¡Correcto! Muy bien.{tiempo_str}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="result-msg-incorrect">❌ Incorrecto. La respuesta correcta es <strong>{resp}</strong>.{tiempo_str}</div>',
                unsafe_allow_html=True
            )

        # Video YouTube
        if video:
            import re
            match = re.search(
                r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/))([A-Za-z0-9_-]{11})",
                video
            )
            if match:
                video_id = match.group(1)
                st.markdown("""
                <p style="text-align:center; color:#6b7280; font-size:0.85rem;
                margin-top:1rem; margin-bottom:0.4rem; font-style:italic;">
                    Compara tu desarrollo y respuesta con el siguiente video explicativo.
                </p>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="margin-top:0rem;border-radius:10px;overflow:hidden;">
                    <iframe
                        width="100%"
                        height="220"
                        src="https://www.youtube.com/embed/{video_id}"
                        frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowfullscreen
                        style="border-radius:10px;">
                    </iframe>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div style="margin-top:0.6rem;">
                    <a href="{video}" target="_blank"
                       style="display:block;background:linear-gradient(135deg,#c0392b,#e74c3c);
                              color:white;text-align:center;padding:0.7rem;border-radius:10px;
                              text-decoration:none;font-weight:700;">
                        ▶ Ver solución en YouTube
                    </a>
                </div>
                ''', unsafe_allow_html=True)

        # ── BOTÓN DE REINICIO ──────────────────────────────────────────────
        st.markdown(
            "<hr style='border-color:#e2e8f0;margin:1.2rem 0 0.8rem'>",
            unsafe_allow_html=True
        )
        st.markdown('<div class="btn-reiniciar">', unsafe_allow_html=True)
        if st.button("🔄 Reiniciar pregunta", key=f"reset_{nombre}", use_container_width=True):
            del st.session_state[sel_key]
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def sidebar_timer():
    st.sidebar.markdown(f"""
    <div class="sidebar-brand">
        <img src="data:image/png;base64,{LOGO_B64}" alt="Logo CM">
        <div class="sidebar-brand-title">COMPLEMENTO<br>MATEMÁTICO</div>
        <div class="sidebar-brand-prof">Prof. Bastiani Calabrano Inostroza</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="sidebar-section">⏱ TIEMPO POR PREGUNTA</div>', unsafe_allow_html=True)
    tiempo_seg = st.sidebar.radio(
        "",
        options=[90, 120],
        format_func=lambda x: f"{x} segundos",
        key="tiempo_radio"
    )
    return tiempo_seg


def main():
    mostrar_header()
    mostrar_footer()
    preguntas = cargar_preguntas()

    if not preguntas:
        st.error("No se encontraron preguntas. Verifica el archivo problems.json.")
        return

    nombres = [p.get("nombre", p.get("id", "")) for p in preguntas]

    # ── Estado inicial ──────────────────────────────────────────────────────
    if "pregunta_idx" not in st.session_state:
        st.session_state.pregunta_idx = 0
    if "selectbox_nombre" not in st.session_state:
        st.session_state.selectbox_nombre = nombres[0]

    # ── Sidebar ─────────────────────────────────────────────────────────────
    tiempo_seg = sidebar_timer()

    # ── Filtro por prueba ────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">📋 FILTRAR POR PRUEBA</div>', unsafe_allow_html=True)

    pruebas_disponibles = ["Todas"] + sorted(list(set(
        p.get("prueba", "Sin prueba") for p in preguntas if p.get("prueba")
    )))

    if "filtro_prueba" not in st.session_state:
        st.session_state.filtro_prueba = "Todas"

    def on_prueba_change():
        prueba_sel = st.session_state["filtro_prueba"]
        st.session_state.filtro_eje = "Todos"
        st.session_state.texto_busqueda = ""
        if prueba_sel == "Todas":
            filtradas = preguntas
        else:
            filtradas = [p for p in preguntas if p.get("prueba") == prueba_sel]
        if filtradas:
            primer_nombre = filtradas[0].get("nombre", filtradas[0].get("id", ""))
            idx_global = nombres.index(primer_nombre)
            st.session_state.pregunta_idx   = idx_global
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False

    st.sidebar.selectbox(
        "",
        options=pruebas_disponibles,
        key="filtro_prueba",
        on_change=on_prueba_change,
    )

    # ── Filtro por eje ───────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">📚 FILTRAR POR EJE</div>', unsafe_allow_html=True)

    prueba_activa = st.session_state.filtro_prueba
    if prueba_activa == "Todas":
        preguntas_por_prueba = preguntas
    else:
        preguntas_por_prueba = [p for p in preguntas if p.get("prueba") == prueba_activa]

    ejes_disponibles = ["Todos"] + sorted(list(set(
        p.get("eje", "Sin eje") for p in preguntas_por_prueba if p.get("eje")
    )))

    if "filtro_eje" not in st.session_state:
        st.session_state.filtro_eje = "Todos"

    def on_eje_change():
        eje_sel    = st.session_state["filtro_eje"]
        prueba_sel = st.session_state["filtro_prueba"]
        st.session_state.texto_busqueda = ""
        if prueba_sel == "Todas":
            base = preguntas
        else:
            base = [p for p in preguntas if p.get("prueba") == prueba_sel]
        if eje_sel == "Todos":
            filtradas = base
        else:
            filtradas = [p for p in base if p.get("eje") == eje_sel]
        if filtradas:
            primer_nombre = filtradas[0].get("nombre", filtradas[0].get("id", ""))
            idx_global = nombres.index(primer_nombre)
            st.session_state.pregunta_idx   = idx_global
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False

    if st.session_state.filtro_eje not in ejes_disponibles:
        st.session_state.filtro_eje = "Todos"

    st.sidebar.selectbox(
        "",
        options=ejes_disponibles,
        key="filtro_eje",
        on_change=on_eje_change,
    )

    # ── Construir lista filtrada (prueba + eje) ──────────────────────────────
    prueba_activa = st.session_state.filtro_prueba
    eje_activo    = st.session_state.filtro_eje

    if prueba_activa == "Todas":
        preguntas_filtradas = preguntas
    else:
        preguntas_filtradas = [p for p in preguntas if p.get("prueba") == prueba_activa]

    if eje_activo != "Todos":
        preguntas_filtradas = [p for p in preguntas_filtradas if p.get("eje") == eje_activo]

    if not preguntas_filtradas:
        st.sidebar.warning("No hay preguntas para este filtro.")
        preguntas_filtradas = preguntas

    nombres_filtrados = [p.get("nombre", p.get("id", "")) for p in preguntas_filtradas]

    nombre_actual_global = nombres[st.session_state.pregunta_idx]
    if nombre_actual_global in nombres_filtrados:
        idx_en_filtro = nombres_filtrados.index(nombre_actual_global)
    else:
        idx_en_filtro = 0
        st.session_state.pregunta_idx = nombres.index(nombres_filtrados[0])

    # ── Buscador de texto + selectbox mejorado ───────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">🔍 BUSCAR POR NOMBRE</div>', unsafe_allow_html=True)

    if "texto_busqueda" not in st.session_state:
        st.session_state.texto_busqueda = ""

    texto_busqueda = st.sidebar.text_input(
        "",
        placeholder="Escribe parte del nombre...",
        key="texto_busqueda",
    )

    # Filtrar nombres según el texto escrito
    if texto_busqueda:
        nombres_buscados = [
            n for n in nombres_filtrados
            if texto_busqueda.lower() in n.lower()
        ]
    else:
        nombres_buscados = nombres_filtrados

    if not nombres_buscados:
        st.sidebar.caption("⚠️ Sin coincidencias. Mostrando todas.")
        nombres_buscados = nombres_filtrados

    # Determinar índice en la lista buscada
    nombre_actual_global = nombres[st.session_state.pregunta_idx]
    if nombre_actual_global in nombres_buscados:
        idx_buscado = nombres_buscados.index(nombre_actual_global)
    else:
        idx_buscado = 0
        st.session_state.pregunta_idx = nombres.index(nombres_buscados[0])

    def on_select_change():
        nombre_sel = st.session_state["buscar_select"]
        if nombre_sel in nombres:
            st.session_state.pregunta_idx   = nombres.index(nombre_sel)
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False

    st.sidebar.selectbox(
        "",
        options=nombres_buscados,
        index=idx_buscado,
        key="buscar_select",
        on_change=on_select_change,
    )

    # Contador informativo
    st.sidebar.caption(
        f"Mostrando **{len(nombres_buscados)}** de **{len(nombres_filtrados)}** preguntas"
    )

    # ── Botón Aleatorio ──────────────────────────────────────────────────────
    st.sidebar.markdown("")
    st.markdown('<div class="btn-aleatorio">', unsafe_allow_html=True)
    if st.sidebar.button("🎲 Pregunta aleatoria", key="btn_aleatorio", use_container_width=True):
        p_random      = random.choice(preguntas_filtradas)
        nombre_random = p_random.get("nombre", p_random.get("id", ""))
        st.session_state.pregunta_idx     = nombres.index(nombre_random)
        st.session_state.selectbox_nombre = nombre_random
        st.session_state.timer_start_ts   = None
        st.session_state.timer_stopped    = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Mostrar pregunta actual ──────────────────────────────────────────────
    idx      = st.session_state.pregunta_idx
    pregunta = preguntas[idx]

    col_pregunta, col_timer = st.columns([3, 1])

    with col_pregunta:
        mostrar_pregunta_card(pregunta, preguntas)

    with col_timer:
        import time as _time

        if "timer_start_ts" not in st.session_state:
            st.session_state.timer_start_ts    = None
            st.session_state.timer_duracion_ts = tiempo_seg
            st.session_state.timer_stopped     = False

        nombre_actual  = preguntas[st.session_state.pregunta_idx].get(
                            "nombre", preguntas[st.session_state.pregunta_idx].get("id", ""))
        sel_key_actual = f"sel_{nombre_actual}"
        ya_respondio   = st.session_state.get(sel_key_actual) is not None

        if ya_respondio and not st.session_state.timer_stopped and st.session_state.timer_start_ts:
            st.session_state.timer_stopped = True

        detenido  = st.session_state.timer_stopped
        start_ts  = st.session_state.timer_start_ts or 0
        duracion  = st.session_state.timer_duracion_ts if st.session_state.timer_start_ts else tiempo_seg
        corriendo = (st.session_state.timer_start_ts is not None) and (not detenido)

        start_ms  = int(start_ts * 1000)
        cor_js    = "true" if corriendo else "false"
        det_js    = "true" if detenido  else "false"

        timer_html = (
            "<!DOCTYPE html><html><head><style>"
            "* {box-sizing:border-box;margin:0;padding:0;}"
            "body {background:transparent;font-family:sans-serif;}"
            ".wrap {background:#161b27;border-radius:16px;padding:1rem 0.6rem;"
            "text-align:center;border:1px solid #2d3748;}"
            ".icon {font-size:1.5rem;margin-bottom:2px;}"
            "#disp {font-size:2.6rem;font-weight:900;color:#7ecfff;"
            "font-family:'Courier New',monospace;letter-spacing:3px;"
            "display:block;min-height:3.2rem;}"
            "#smsg {font-size:0.8rem;font-weight:700;margin-top:5px;min-height:1.1rem;}"
            "</style></head><body>"
            "<div class='wrap'>"
            "<div class='icon' id='icon'>⏳</div>"
            "<span id='disp'>--:--</span>"
            "<div id='smsg'></div>"
            "</div>"
            "<script>"
            f"var START_MS={start_ms};"
            f"var DURACION={duracion};"
            f"var CORRIENDO={cor_js};"
            f"var DETENIDO={det_js};"
            "var iv=null;"
            "var disp=document.getElementById('disp');"
            "var smsg=document.getElementById('smsg');"
            "var icon=document.getElementById('icon');"
            "function fmt(s){var m=Math.floor(s/60),r=s%60;return m+':'+(r<10?'0':'')+r;}"
            "function tick(){"
            "  var elapsed=Math.floor((Date.now()-START_MS)/1000);"
            "  var rest=Math.max(0,DURACION-elapsed);"
            "  disp.textContent=fmt(rest);"
            "  disp.style.color=rest<=10?'#e74c3c':'#7ecfff';"
            "  if(rest<=0){clearInterval(iv);smsg.style.color='#e74c3c';"
            "    smsg.textContent='⏰ Tiempo agotado!';icon.textContent='⏰';}"
            "}"
            "if(DETENIDO){"
            "  var el=Math.floor((Date.now()-START_MS)/1000);"
            "  var re=Math.max(0,DURACION-el);"
            "  var us=DURACION-re;"
            "  var mu=Math.floor(us/60),su=us%60;"
            "  disp.textContent=fmt(re);"
            "  disp.style.color=re<=10?'#e74c3c':'#7ecfff';"
            "  smsg.style.color='#059669';"
            "  icon.textContent='🛑';"
            "  smsg.textContent='✅ Tiempo: '+(mu>0?mu+'m ':'')+su+'s';"
            "}else if(CORRIENDO){"
            "  tick();iv=setInterval(tick,500);"
            "}else{"
            "  disp.textContent=fmt(DURACION);disp.style.color='#7ecfff';"
            "}"
            "</script></body></html>"
        )
        components.html(timer_html, height=155)

        st.markdown("")
        if not detenido:
            if st.button("▶ Iniciar cronómetro", key="btn_timer_main", use_container_width=True):
                st.session_state.timer_start_ts    = _time.time()
                st.session_state.timer_duracion_ts = tiempo_seg
                st.session_state.timer_stopped     = False
                st.rerun()
        else:
            if st.button("🔄 Nuevo cronómetro", key="btn_timer_reset", use_container_width=True):
                st.session_state.timer_start_ts  = None
                st.session_state.timer_stopped   = False
                st.rerun()

        st.markdown("")
        st.markdown('<div class="btn-random-timer">', unsafe_allow_html=True)
        if st.button("🎲 Pregunta aleatoria", key="btn_random_timer", use_container_width=True):
            p_random = random.choice(preguntas_filtradas)
            nombre_random = p_random.get("nombre", p_random.get("id", ""))
            st.session_state.pregunta_idx     = nombres.index(nombre_random)
            st.session_state.selectbox_nombre = nombre_random
            st.session_state.timer_start_ts   = None
            st.session_state.timer_stopped    = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
