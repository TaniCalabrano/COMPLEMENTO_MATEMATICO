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
    .consejos-panel {
        background: #0d1424;
        border: 1px solid #2d4a7a;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.8rem;
        font-size: 0.82rem;
        color: #b0c4e8;
        line-height: 1.6;
    }
    .consejos-panel h4 {
        color: #f5a623;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin: 0.7rem 0 0.3rem;
        border-left: 3px solid #f5a623;
        padding-left: 7px;
    }
    .consejos-panel h4:first-child { margin-top: 0; }
    .consejos-panel p { margin: 0 0 0.3rem 0; }
    .consejos-icono { font-size: 14px; margin-right: 5px; }
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


def mostrar_bienvenida():
    items = [
        ("1", "Reflexionar sobre su nivel de interés con la rendición de la evaluación."),
        ("2", "Reflexionar e informarse sobre carreras de nivel superior que se ajusten a sus intereses y posibilidades de ingreso y sostenibilidad."),
        ("3", "Gestionar su tiempo y crear un programa de estudio personalizado para tener éxito en la rendición de la evaluación. La semana es un conjunto de 168 horas — depende de ti si aprovechas o no tu tiempo, el cual es un verdadero regalo que no se puede controlar, pero sí gestionar."),
        ("4", "Infórmate sobre los contenidos que debes dominar y las habilidades que debes desarrollar para tener éxito en la evaluación."),
        ("5", "Reflexiona sobre los problemas que abordes, preguntándote: ¿Cómo se resuelve? ¿Abordé correctamente el problema? ¿De cuántas formas se podrá resolver? ¿Qué otra pregunta se puede generar a través de este problema? ¿Cómo me podría haber equivocado?"),
        ("6", "Date mensajes de éxito. Si crees que no lo lograrás, pues el resultado ya está sentenciado. En cambio, si crees en ti y das lo mejor en el periodo de tu preparación, tu entrenamiento te aseguro que te dará frutos."),
        ("7", "Para concluir: Concéntrate en conocer sobre la prueba, entrenarte como resolutor(a) de problemas y desarrollar una autoestima académica que te permita gestionar tus emociones y rendir la evaluación con la convicción de que tendrás éxito al finalizarla."),
    ]

    logo_src = f'data:image/png;base64,{LOGO_B64}' if LOGO_B64 else ""
    logo_tag = (
        f'<img src="{logo_src}" '
        'style="height:52px;width:52px;border-radius:50%;object-fit:cover;'
        'vertical-align:middle;margin-right:12px;box-shadow:0 0 10px rgba(245,166,35,0.4);" '
        'alt="Logo CM">'
    ) if logo_src else ""

    items_parts = []
    for num, texto in items:
        items_parts.append(
            '<div style="display:flex;align-items:flex-start;gap:12px;'
            'padding:0.7rem 0;border-bottom:1px solid #1a2540;">'
            '<div style="width:22px;height:22px;min-width:22px;background:#1a2e1a;'
            'border:2px solid #3a7a3a;border-radius:5px;display:flex;align-items:center;'
            'justify-content:center;font-size:13px;margin-top:2px;color:#4eff88;">&#10004;</div>'
            f'<div style="font-size:0.72rem;font-weight:700;color:#f5a623;min-width:20px;margin-top:3px;">{num}.</div>'
            f'<div style="font-size:0.88rem;color:#b0c4e8;line-height:1.55;">{texto}</div>'
            '</div>'
        )
    items_html = "".join(items_parts)

    html_bienvenida = (
        '<div style="background:linear-gradient(160deg,#0d1424 0%,#111830 100%);'
        'border:1px solid #2d3a5a;border-radius:16px;padding:2rem 2.4rem 1.6rem;'
        'max-width:820px;margin:0 auto 1.2rem auto;">'

        '<div style="font-size:1rem;color:#c8d8ff;line-height:1.7;margin-bottom:1.4rem;">'
        + logo_tag +
        '<strong style="color:#f5a623;">Estimado(a) estudiante:</strong><br><br>'
        'El repositorio de problemas de <strong style="color:#f5a623;">Complemento Matemático</strong> '
        'es un proyecto educativo <strong style="color:#4eff88;">gratuito</strong> que tiene el propósito '
        'de potenciar su preparación para la rendición de las evaluaciones '
        '<strong style="color:#7ecfff;">PAES de Matemática</strong> y las preguntas respectivas de '
        '<strong style="color:#7ecfff;">Física</strong>.<br><br>'
        'En función de ello, le recomiendo lo siguiente:'
        '</div>'

        '<div style="background:#0a0f1e;border:1px solid #243050;border-radius:12px;'
        'padding:1.2rem 1.4rem;margin-bottom:1.4rem;">'
        '<div style="font-size:0.78rem;font-weight:700;letter-spacing:2px;color:#f5a623;'
        'text-transform:uppercase;margin-bottom:1rem;">&#128203; Recomendaciones para tu proceso de preparación</div>'
        + items_html +
        '</div>'

        '<div style="font-size:0.85rem;color:#8899bb;text-align:right;'
        'margin-top:0.8rem;font-style:italic;">'
        'Mucho éxito en tus procesos de aprendizaje.<br>'
        '<strong style="color:#f5a623;font-style:normal;">'
        'Atte. Prof. Bastiani Calabrano Inostroza</strong>'
        '</div>'
        '</div>'

        '<div style="background:#0d1624;border:1px solid #2a3a5a;border-radius:10px;'
        'padding:0.9rem 1.4rem;display:flex;align-items:center;justify-content:space-between;'
        'flex-wrap:wrap;gap:10px;max-width:820px;margin:0 auto 0.8rem;">'
        '<div style="font-size:0.85rem;color:#99aac8;">'
        'Para más información sobre la PAES buscar en: '
        '<strong style="color:#7ecfff;">DEMRE — Proceso de Admisión 2027</strong>'
        '</div>'
        '<a href="https://demre.cl" target="_blank" '
        'style="display:inline-block;background:linear-gradient(135deg,#1a3a7a,#2255aa);'
        'color:#c8e0ff;border:1px solid #3366bb;border-radius:8px;padding:7px 18px;'
        'font-size:0.82rem;font-weight:700;text-decoration:none;letter-spacing:0.3px;">'
        '&#128279; Ir al sitio del DEMRE'
        '</a>'
        '</div>'

        '<div style="background:#0d1624;border:1px solid #2a3a5a;border-radius:10px;'
        'padding:0.9rem 1.4rem;display:flex;align-items:center;justify-content:space-between;'
        'flex-wrap:wrap;gap:10px;max-width:820px;margin:0 auto 0.8rem;">'
        '<div style="font-size:0.85rem;color:#99aac8;line-height:1.6;">'
        'Para complementar tu aprendizaje con videos explicativos de teoría y ejercicios,'
        '<br>te invito a mi canal de YouTube:'
        '</div>'
        + (
            '<a href="https://youtube.com/@tanicalabrano2023?si=TbUDUsGwCmCNtn9J" target="_blank" '
            'style="display:inline-flex;align-items:center;gap:10px;'
            'background:linear-gradient(135deg,#8b0000,#cc0000);'
            'color:#fff;border:1px solid #ff4444;border-radius:8px;padding:8px 18px;'
            'font-size:0.82rem;font-weight:700;text-decoration:none;letter-spacing:0.3px;">'
            + (
                f'<img src="data:image/png;base64,{LOGO_B64}" '
                'style="height:28px;width:28px;border-radius:50%;object-fit:cover;flex-shrink:0;" alt="Logo">'
                if LOGO_B64 else
                '<svg width="22" height="22" viewBox="0 0 24 24" fill="white" style="flex-shrink:0;">'
                '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.7 15.5V8.5l6.3 3.5-6.3 3.5z"/>'
                '</svg>'
            )
            + 'Complemento Matemático — YouTube'
            '</a>'
        )
        + '</div>'
    )

    st.markdown(html_bienvenida, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅  Entendido — Ingresar al repositorio", key="btn_entrar", use_container_width=True):
            st.session_state.bienvenida_vista = True
            st.rerun()


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
    if "bienvenida_vista" not in st.session_state:
        st.session_state.bienvenida_vista = False

    mostrar_header()
    mostrar_footer()

    if not st.session_state.bienvenida_vista:
        mostrar_bienvenida()
        return

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

        # ── Botón Consejos de uso ────────────────────────────────────────
        if "mostrar_consejos" not in st.session_state:
            st.session_state.mostrar_consejos = False

        label_btn = "✕ Cerrar consejos" if st.session_state.mostrar_consejos else "💡 Consejos de uso"
        if st.button(label_btn, key="btn_consejos", use_container_width=True):
            st.session_state.mostrar_consejos = not st.session_state.mostrar_consejos
            st.rerun()

        if st.session_state.mostrar_consejos:
            st.markdown("""
<div class="consejos-panel">
<h4>📋 Filtros de búsqueda</h4>
<p>Usa los filtros del panel lateral para encontrar problemas por <b>Prueba</b> (PAES M1, M2, Física) y por <b>Eje temático</b>. Ambos filtros se combinan automáticamente.</p>

<h4>🔍 Buscador por nombre</h4>
<p>Escribe parte del código del problema (por ejemplo <i>2023</i> o <i>P12</i>) en el campo de texto. El selector se reduce mostrando solo las coincidencias. Un contador indica cuántos problemas están visibles.</p>

<h4>🎲 Pregunta aleatoria</h4>
<p>El botón <b>Pregunta aleatoria</b> elige al azar dentro de los filtros activos. Úsalo para simular condiciones de examen sin elegir el tema conscientemente.</p>

<h4>⏱ Cronómetro</h4>
<p>Selecciona <b>90 o 120 segundos</b> en el panel lateral antes de iniciar. Presiona <b>▶ Iniciar</b> justo cuando comienzas a leer el problema. El cronómetro se detiene automáticamente al responder y muestra el tiempo usado.</p>

<h4>🔄 Reiniciar pregunta</h4>
<p>Si quieres volver a intentar un problema, presiona el botón <b>🔄 Reiniciar pregunta</b> que aparece debajo de tu respuesta. Borra tu selección y el cronómetro para empezar de cero.</p>

<h4>▶ Video explicativo</h4>
<p>Al responder, si el problema tiene solución en video, aparecerá incrustado debajo del resultado. Compara tu desarrollo con el del profesor.</p>

<h4>💡 Consejo de estudio</h4>
<p>No te limites a verificar si acertaste. Pregúntate siempre: <i>¿cómo lo resolví?, ¿pude haberlo resuelto de otra forma?, ¿dónde pude equivocarme?</i> Esa reflexión es lo que construye habilidad real.</p>
</div>
            """, unsafe_allow_html=True)

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
