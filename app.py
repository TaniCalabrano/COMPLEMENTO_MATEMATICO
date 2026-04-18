import streamlit as st
import streamlit.components.v1 as components
import json
import time
import random
import base64
from pathlib import Path
from PIL import Image
from actividades_modal import mostrar_boton_actividades, mostrar_modal_actividades

logo_favicon = Image.open("LogoCM.png")

# ── Habilidades por PRUEBA ───────────────────────────────────────────────────
HABILIDADES_POR_PRUEBA = {
    "M1": [
        "Resolver problemas",
        "Modelar",
        "Representar",
        "Argumentar y comunicar",
    ],
    "M2": [
        "Resolver problemas",
        "Modelar",
        "Representar",
        "Argumentar y comunicar",
    ],
    "FISICA": [
        "Observar y preguntar",
        "Planificar y conducir investigaciones",
        "Analizar e interpretar datos",
        "Construir explicaciones",
        "Argumentar",
        "Procesar y analizar la evidencia",
    ],
}

# ── Ejes por PRUEBA ──────────────────────────────────────────────────────────
EJES_POR_PRUEBA = {
    "M1":    ["Números", "Álgebra", "Geometría", "Estadística"],
    "M2":    ["Números", "Álgebra", "Geometría", "Estadística"],
    "FISICA": ["Ondas", "Mecánica", "Energía y Tierra", "Electricidad"],
}

# ── Contenidos por EJE ───────────────────────────────────────────────────────
CONTENIDOS_POR_EJE = {
    # M1 / M2
    "Números": [
        "Números naturales",
        "Números enteros",
        "Números racionales",
        "Fracciones",
        "Decimales",
        "Porcentajes",
        "Proporcionalidad",
        "Proporcionalidad directa",
        "Proporcionalidad inversa",
        "Potencias",
        "Raíces",
        "Números reales",
    ],
    "Álgebra": [
        "Expresiones algebraicas",
        "Ecuaciones de primer grado",
        "Ecuaciones cuadráticas",
        "Inecuaciones de primer grado",
        "Inecuaciones cuadráticas",
        "Sistemas de ecuaciones",
        "Funciones",
        "Función lineal",
        "Función cuadrática",
        "Función exponencial",
    ],
    "Geometría": [
        "Figuras y cuerpos geométricos",
        "Perímetro",
        "Área",
        "Volumen",
        "Teorema de Pitágoras",
        "Semejanza y congruencia",
        "Transformaciones isométricas",
        "Geometría analítica",
        "Trigonometría",
    ],
    "Estadística": [
        "Tablas y gráficos estadísticos",
        "Medidas de tendencia central",
        "Medidas de dispersión",
        "Probabilidad",
        "Distribuciones",
    ],
    # FISICA
    "Ondas": [
        "Características de las ondas",
        "Sonido",
        "Luz y óptica geométrica",
        "Espectro electromagnético",
        "Ondas electromagnéticas",
    ],
    "Mecánica": [
        "Cinemática",
        "Dinámica y Leyes de Newton",
        "Trabajo y energía",
        "Cantidad de movimiento",
    ],
    "Energía y Tierra": [
        "Ondas sísmicas",
        "Capas de la tierra",
        "Núcleo de la tierra",
    ],
    "Electricidad": [
        "Carga eléctrica y campo eléctrico",
        "Circuitos eléctricos",
        "Magnetismo",
        "Inducción electromagnética",
    ],
}


def _habilidades_para_filtro(prueba_activa):
    """Devuelve lista de habilidades según prueba activa."""
    if prueba_activa == "Todas":
        visto = set()
        result = []
        for lst in HABILIDADES_POR_PRUEBA.values():
            for h in lst:
                if h not in visto:
                    visto.add(h)
                    result.append(h)
        return sorted(result)
    return HABILIDADES_POR_PRUEBA.get(prueba_activa, [])


def _contenidos_para_eje(eje_activo, prueba_activa="Todas"):
    """Devuelve lista de contenidos según eje activo y prueba activa."""
    # Determinar qué ejes son válidos para esta prueba
    if prueba_activa == "Todas":
        ejes_validos = list(CONTENIDOS_POR_EJE.keys())
    else:
        ejes_validos = EJES_POR_PRUEBA.get(prueba_activa, list(CONTENIDOS_POR_EJE.keys()))

    if eje_activo == "Todos":
        visto = set()
        result = []
        for eje in ejes_validos:          # solo itera ejes válidos para la prueba activa
            for c in CONTENIDOS_POR_EJE.get(eje, []):
                if c not in visto:
                    visto.add(c)
                    result.append(c)
        return sorted(result)

    return CONTENIDOS_POR_EJE.get(eje_activo, [])


st.set_page_config(
    page_title="Complemento Matemático - PAES",
    page_icon=logo_favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .stApp > header { background-color: transparent !important; }
    [data-testid="stAppViewContainer"] { background-color: #0f1117 !important; }
    [data-testid="stMainBlockContainer"] {
        background-color: #0f1117 !important;
        padding-top: 0 !important;
    }
    [data-testid="stHeader"] { background-color: #0f1117 !important; }
    [data-testid="stToolbar"] { background-color: #0f1117 !important; }
    [data-testid="stDecoration"] { background-color: #0f1117 !important; }
    [data-testid="stMain"] { background-color: #0f1117 !important; }
    section.main { background-color: #0f1117 !important; }
    .main .block-container {
        background-color: #0f1117 !important;
        max-width: 100% !important;
    }
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
        transition: all 0.2s; cursor: pointer;
        background-color: #1c1a0a !important;
        color: #e8d5a0 !important;
        border: 1px solid #5a4010 !important;
    }
    .stButton > button:hover {
        background-color: #2a2000 !important;
        border-color: #f5a623 !important;
        color: #f5a623 !important;
    }
    .stButton > button:active {
        background-color: #3a2e00 !important;
        transform: scale(0.98);
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
    .btn-actividades > button {
        background: linear-gradient(135deg, #1a3a6a, #2255aa) !important;
        color: #c8e0ff !important;
        border: 1px solid #3a6abf !important;
        margin-top: 0.3rem;
    }
    .btn-actividades > button:hover {
        background: linear-gradient(135deg, #2255aa, #3a7aee) !important;
        color: #ffffff !important;
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
        z-index: 9997;
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
    .block-container { padding-bottom: 3.5rem !important; }
    [data-testid="stSidebar"] details {
        background-color: #2a1f00 !important;
        border: 1px solid #5a4010 !important;
        border-radius: 8px !important;
        margin-bottom: 0.3rem !important;
    }
    [data-testid="stSidebar"] details summary {
        color: #f5a623 !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        padding: 0.55rem 0.8rem !important;
        border-radius: 8px !important;
        list-style: none !important;
    }
    [data-testid="stSidebar"] details summary::-webkit-details-marker {
        display: none !important;
    }
    [data-testid="stSidebar"] details summary::before {
        content: "▶  ";
        font-size: 0.6rem;
        margin-right: 4px;
        color: #f5a623;
    }
    [data-testid="stSidebar"] details[open] summary::before {
        content: "▼  ";
    }
    [data-testid="stSidebar"] details[open] {
        border-color: #f5a623 !important;
    }
    [data-testid="stSidebar"] details > div {
        background-color: #1a1200 !important;
        border-top: 1px solid #5a4010 !important;
        padding: 0.6rem 0.4rem 0.3rem !important;
    }
    [data-testid="stSidebar"] .stCheckbox label p {
        color: #e8d5a0 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSidebar"] .stCheckbox {
        margin-bottom: 0.1rem !important;
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
        <div class="header-versiculo">"Todo lo puedo en Cristo que me fortalece" &mdash; Filipenses 4:13</div>
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
            "Porque Jehová da la sabiduría, y de su boca viene el conocimiento y la inteligencia."
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
    mostrar_modal_actividades()

    if not st.session_state.bienvenida_vista:
        mostrar_bienvenida()
        return

    preguntas = cargar_preguntas()

    if not preguntas:
        st.error("No se encontraron preguntas. Verifica el archivo problems.json.")
        return

    nombres = [p.get("nombre", p.get("id", "")) for p in preguntas]

    if "pregunta_idx" not in st.session_state:
        st.session_state.pregunta_idx = 0
    if "selectbox_nombre" not in st.session_state:
        st.session_state.selectbox_nombre = nombres[0]

    tiempo_seg = sidebar_timer()

    # ── Filtro por PRUEBA ────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">📋 FILTRAR POR PRUEBA</div>', unsafe_allow_html=True)

    pruebas_disponibles = ["Todas"] + sorted(list(set(
        p.get("prueba", "Sin prueba") for p in preguntas if p.get("prueba")
    )))

    if "filtro_prueba" not in st.session_state:
        st.session_state.filtro_prueba = "Todas"

    def on_prueba_change():
        prueba_sel = st.session_state["filtro_prueba"]
        st.session_state.filtro_eje         = "Todos"
        st.session_state.texto_busqueda     = ""
        st.session_state.filtro_habilidades = []
        st.session_state.filtro_contenidos  = []
        filtradas = preguntas if prueba_sel == "Todas" else [
            p for p in preguntas if p.get("prueba") == prueba_sel
        ]
        if filtradas:
            primer_nombre = filtradas[0].get("nombre", filtradas[0].get("id", ""))
            st.session_state.pregunta_idx   = nombres.index(primer_nombre)
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False

    st.sidebar.selectbox(
        "",
        options=pruebas_disponibles,
        key="filtro_prueba",
        on_change=on_prueba_change,
    )

    # ── Filtro por EJE — depende de PRUEBA ───────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">📚 FILTRAR POR EJE</div>', unsafe_allow_html=True)

    prueba_activa = st.session_state.filtro_prueba
    preguntas_por_prueba = preguntas if prueba_activa == "Todas" else [
        p for p in preguntas if p.get("prueba") == prueba_activa
    ]

    if prueba_activa == "Todas":
        ejes_disponibles = ["Todos"] + sorted(list(set(
            p.get("eje", "Sin eje") for p in preguntas_por_prueba if p.get("eje")
        )))
    else:
        ejes_validos     = EJES_POR_PRUEBA.get(prueba_activa, [])
        ejes_en_datos    = set(p.get("eje", "") for p in preguntas_por_prueba)
        ejes_disponibles = ["Todos"] + [e for e in ejes_validos if e in ejes_en_datos]

    if "filtro_eje" not in st.session_state:
        st.session_state.filtro_eje = "Todos"

    def on_eje_change():
        eje_sel    = st.session_state["filtro_eje"]
        prueba_sel = st.session_state["filtro_prueba"]
        st.session_state.texto_busqueda    = ""
        st.session_state.filtro_contenidos = []
        base = preguntas if prueba_sel == "Todas" else [
            p for p in preguntas if p.get("prueba") == prueba_sel
        ]
        filtradas = base if eje_sel == "Todos" else [
            p for p in base if p.get("eje") == eje_sel
        ]
        if filtradas:
            primer_nombre = filtradas[0].get("nombre", filtradas[0].get("id", ""))
            st.session_state.pregunta_idx   = nombres.index(primer_nombre)
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

    # ── Filtro por HABILIDADES — depende de PRUEBA ───────────────────────────
    if "filtro_habilidades" not in st.session_state:
        st.session_state.filtro_habilidades = []

    habilidades_disponibles = _habilidades_para_filtro(st.session_state.filtro_prueba)
    st.session_state.filtro_habilidades = [
        h for h in st.session_state.filtro_habilidades if h in habilidades_disponibles
    ]

    n_hab     = len(st.session_state.filtro_habilidades)
    label_hab = (
        f"🧠 HABILIDADES ({n_hab} activa{'s' if n_hab != 1 else ''})"
        if n_hab > 0 else "🧠 FILTRAR POR HABILIDAD"
    )

    with st.sidebar.expander(label_hab, expanded=False):
        nuevas_habilidades = []
        for hab in habilidades_disponibles:
            marcado = hab in st.session_state.filtro_habilidades
            if st.checkbox(hab, value=marcado, key=f"chk_hab_{hab}"):
                nuevas_habilidades.append(hab)
        if nuevas_habilidades != st.session_state.filtro_habilidades:
            st.session_state.filtro_habilidades = nuevas_habilidades
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False
            st.rerun()

    # ── Filtro por CONTENIDOS — depende de EJE y PRUEBA ──────────────────────
    if "filtro_contenidos" not in st.session_state:
        st.session_state.filtro_contenidos = []

    # CAMBIO CLAVE: se pasa también la prueba activa para acotar los contenidos
    contenidos_disponibles = _contenidos_para_eje(
        st.session_state.filtro_eje,
        st.session_state.filtro_prueba
    )
    st.session_state.filtro_contenidos = [
        c for c in st.session_state.filtro_contenidos if c in contenidos_disponibles
    ]

    n_cont     = len(st.session_state.filtro_contenidos)
    label_cont = (
        f"📖 CONTENIDOS ({n_cont} activo{'s' if n_cont != 1 else ''})"
        if n_cont > 0 else "📖 FILTRAR POR CONTENIDO"
    )

    with st.sidebar.expander(label_cont, expanded=False):
        nuevos_contenidos = []
        for cont in contenidos_disponibles:
            marcado = cont in st.session_state.filtro_contenidos
            if st.checkbox(cont, value=marcado, key=f"chk_cont_{cont}"):
                nuevos_contenidos.append(cont)
        if nuevos_contenidos != st.session_state.filtro_contenidos:
            st.session_state.filtro_contenidos = nuevos_contenidos
            st.session_state.timer_start_ts = None
            st.session_state.timer_stopped  = False
            st.rerun()

    # ── Lista filtrada (todos los filtros combinados) ────────────────────────
    prueba_activa = st.session_state.filtro_prueba
    eje_activo    = st.session_state.filtro_eje

    preguntas_filtradas = preguntas if prueba_activa == "Todas" else [
        p for p in preguntas if p.get("prueba") == prueba_activa
    ]
    if eje_activo != "Todos":
        preguntas_filtradas = [p for p in preguntas_filtradas if p.get("eje") == eje_activo]

    habs_sel = st.session_state.get("filtro_habilidades", [])
    if habs_sel:
        preguntas_filtradas = [
            p for p in preguntas_filtradas
            if any(h in p.get("habilidades", []) for h in habs_sel)
        ]

    conts_sel = st.session_state.get("filtro_contenidos", [])
    if conts_sel:
        preguntas_filtradas = [
            p for p in preguntas_filtradas
            if any(c in p.get("contenidos", []) for c in conts_sel)
        ]

    if not preguntas_filtradas:
        st.sidebar.warning("No hay preguntas para este filtro.")
        preguntas_filtradas = preguntas

    nombres_filtrados    = [p.get("nombre", p.get("id", "")) for p in preguntas_filtradas]
    nombre_actual_global = nombres[st.session_state.pregunta_idx]

    if nombre_actual_global not in nombres_filtrados:
        st.session_state.pregunta_idx = nombres.index(nombres_filtrados[0])

    # ── Buscador ─────────────────────────────────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-section">🔍 BUSCAR POR NOMBRE</div>', unsafe_allow_html=True)

    if "texto_busqueda" not in st.session_state:
        st.session_state.texto_busqueda = ""

    texto_busqueda = st.sidebar.text_input(
        "",
        placeholder="Escribe parte del nombre...",
        key="texto_busqueda",
    )

    nombres_buscados = (
        [n for n in nombres_filtrados if texto_busqueda.lower() in n.lower()]
        if texto_busqueda else nombres_filtrados
    )
    if not nombres_buscados:
        st.sidebar.caption("⚠️ Sin coincidencias. Mostrando todas.")
        nombres_buscados = nombres_filtrados

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

    st.sidebar.markdown(
        f'<div style="color:#f5a623;font-size:0.75rem;font-weight:700;'
        f'letter-spacing:1px;padding:3px 0 3px 11px;border-left:3px solid #f5a623;">'
        f'Mostrando {len(nombres_buscados)} de {len(nombres_filtrados)} preguntas</div>',
        unsafe_allow_html=True
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

    # ── Si el modal está abierto, no mostrar pregunta ni timer ───────────────
    if st.session_state.get("modal_actividades", False):
        return

    # ── Pregunta actual + timer ──────────────────────────────────────────────
    idx      = st.session_state.pregunta_idx
    pregunta = preguntas[idx]

    col_pregunta, col_timer = st.columns([3, 1])

    with col_pregunta:
        mostrar_pregunta_card(pregunta, preguntas)

    with col_timer:
        import time as _time

        if "mostrar_consejos" not in st.session_state:
            st.session_state.mostrar_consejos = False

        st.markdown('<div class="btn-actividades">', unsafe_allow_html=True)
        if st.button("🧩  Actividades interactivas", key="btn_actividades_timer", use_container_width=True):
            st.session_state["modal_actividades"] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:0.3rem;'></div>", unsafe_allow_html=True)

        label_btn = "✕ Cerrar consejos" if st.session_state.mostrar_consejos else "💡 Consejos de uso"
        if st.button(label_btn, key="btn_consejos", use_container_width=True):
            st.session_state.mostrar_consejos = not st.session_state.mostrar_consejos
            st.rerun()

        if st.session_state.mostrar_consejos:
            st.markdown("""
<div class="consejos-panel">
<h4>📋 Filtros de búsqueda</h4>
<p>Usa los filtros del panel lateral para encontrar problemas por <b>Prueba</b>, <b>Eje</b>, <b>Habilidad</b> y <b>Contenido</b>. Todos los filtros se combinan automáticamente.</p>
<h4>🧠 Habilidades</h4>
<p>Se filtran según la <b>Prueba</b> seleccionada (M1/M2 comparten habilidades; Física tiene las suyas).</p>
<h4>📖 Contenidos</h4>
<p>Se filtran según el <b>Eje</b> seleccionado.</p>
<h4>🔍 Buscador por nombre</h4>
<p>Escribe parte del código del problema (por ejemplo <i>2023</i> o <i>P12</i>) en el campo de texto.</p>
<h4>🎲 Pregunta aleatoria</h4>
<p>El botón <b>Pregunta aleatoria</b> elige al azar dentro de los filtros activos.</p>
<h4>⏱ Cronómetro</h4>
<p>Selecciona <b>90 o 120 segundos</b> en el panel lateral antes de iniciar.</p>
<h4>🔄 Reiniciar pregunta</h4>
<p>Presiona <b>🔄 Reiniciar pregunta</b> para volver a intentar un problema.</p>
<h4>▶ Video explicativo</h4>
<p>Al responder aparecerá el video de solución del profesor.</p>
<h4>✉ Contacto</h4>
<p><a href="mailto:complemento.matematico.cm@gmail.com" style="color:#f5a623;font-weight:700;text-decoration:none;">complemento.matematico.cm@gmail.com</a></p>
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

        start_ms = int(start_ts * 1000)
        cor_js   = "true" if corriendo else "false"
        det_js   = "true" if detenido  else "false"

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
            p_random      = random.choice(preguntas_filtradas)
            nombre_random = p_random.get("nombre", p_random.get("id", ""))
            st.session_state.pregunta_idx     = nombres.index(nombre_random)
            st.session_state.selectbox_nombre = nombre_random
            st.session_state.timer_start_ts   = None
            st.session_state.timer_stopped    = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
