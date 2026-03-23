# ══════════════════════════════════════════════════════════════════════
#  MÓDULO: Actividades Interactivas
#  Integración en app.py:
#    1. from actividades_modal import mostrar_boton_actividades, mostrar_modal_actividades
#    2. En sidebar_timer(): llamar mostrar_boton_actividades()
#    3. En main(), justo después de mostrar_header(): llamar mostrar_modal_actividades()
# ══════════════════════════════════════════════════════════════════════

import streamlit as st
import streamlit.components.v1 as components
import json
from pathlib import Path

DORADO = "#FFD600"

EJES_COLORES = {
    "Álgebra":     {"bg": "rgba(74,158,255,0.12)",  "border": "#4a9eff", "text": "#4a9eff"},
    "Geometría":   {"bg": "rgba(62,207,142,0.12)",  "border": "#3ecf8e", "text": "#3ecf8e"},
    "Números":     {"bg": "rgba(245,166,35,0.12)",  "border": "#f5a623", "text": "#f5a623"},
    "Estadística": {"bg": "rgba(181,122,255,0.12)", "border": "#b57aff", "text": "#b57aff"},
    "Física":      {"bg": "rgba(239,83,80,0.12)",   "border": "#ef5350", "text": "#ef5350"},
}
EJES_DEFAULT = {"bg": "rgba(200,200,200,0.1)", "border": "#888", "text": "#aaa"}


@st.cache_data
def _cargar_actividades():
    ruta = Path("actividades.json")
    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def mostrar_boton_actividades():
    """Botón en el sidebar que abre el modal."""
    st.sidebar.markdown("")
    st.sidebar.markdown(
        f'<div style="font-size:0.75rem;font-weight:700;letter-spacing:2px;'
        f'text-transform:uppercase;color:{DORADO};margin:1rem 0 0.4rem;'
        f'border-left:3px solid {DORADO};padding-left:8px;">🧩 ACTIVIDADES</div>',
        unsafe_allow_html=True
    )
    if st.sidebar.button(
        "🧩  Actividades interactivas",
        key="btn_abrir_actividades",
        use_container_width=True,
    ):
        st.session_state["modal_actividades"] = True
        st.rerun()


def mostrar_modal_actividades():
    """Modal de actividades con comunicación iframe→Streamlit via query_params."""
    if not st.session_state.get("modal_actividades", False):
        return

    # ── Leer acción desde query params (comunicación iframe → Streamlit) ──
    params = st.query_params
    accion = params.get("act_accion", "")
    if accion == "cerrar":
        st.session_state["modal_actividades"] = False
        st.session_state["act_filtro_eje"] = "Todos"
        st.query_params.clear()
        st.rerun()
    elif accion.startswith("filtro:"):
        nuevo_eje = accion[len("filtro:"):]
        st.session_state["act_filtro_eje"] = nuevo_eje
        st.query_params.clear()
        st.rerun()

    actividades = _cargar_actividades()

    if "act_filtro_eje" not in st.session_state:
        st.session_state["act_filtro_eje"] = "Todos"

    eje_sel = st.session_state["act_filtro_eje"]
    ejes_disponibles = ["Todos"] + sorted(
        list(set(a.get("eje", "") for a in actividades if a.get("eje")))
    )

    filtradas = actividades if eje_sel == "Todos" else [
        a for a in actividades if a.get("eje") == eje_sel
    ]

    # ── Botones de filtro ──────────────────────────────────────────────
    filtros_html = ""
    for eje in ejes_disponibles:
        activo_class = "activo" if eje_sel == eje else ""
        filtros_html += (
            f'<button class="act-filtro-btn {activo_class}" '
            f'onclick="navegarA(\'filtro:{eje}\')">{eje}</button>'
        )

    # ── Cards ──────────────────────────────────────────────────────────
    cards_html = ""
    for act in filtradas:
        eje = act.get("eje", "")
        c = EJES_COLORES.get(eje, EJES_DEFAULT)
        badge = f'background:{c["bg"]};border:1px solid {c["border"]};color:{c["text"]};'
        cards_html += f"""
        <a class="act-card" href="{act.get('url','#')}" target="_blank" rel="noopener noreferrer">
            <div class="act-card-top">
                <div class="act-icono">{act.get('icono','🔬')}</div>
                <div class="act-card-nombre">{act.get('nombre','')}</div>
            </div>
            <div class="act-card-desc">{act.get('descripcion','')}</div>
            <div class="act-card-footer">
                <span class="act-eje-badge" style="{badge}">{eje}</span>
                <span class="act-card-cta">Abrir ↗</span>
            </div>
        </a>"""

    if not cards_html:
        cards_html = '<div class="act-empty">No hay actividades para este filtro aún.</div>'

    conteo = f"{len(filtradas)} de {len(actividades)}"

    # ── URL base para navegación ───────────────────────────────────────
    # Usamos window.parent.location para cambiar la URL del padre (Streamlit)
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: transparent !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    height: 100%;
  }}

  .overlay {{
    position: fixed; inset: 0; z-index: 9998;
    background: rgba(0,0,0,0.82);
    backdrop-filter: blur(4px);
    display: flex; align-items: center; justify-content: center;
  }}

  .panel {{
    background: #111827;
    border: 1px solid #2d3a50;
    border-radius: 20px;
    padding: 2rem 2.4rem 2.4rem;
    width: min(95vw, 1080px);
    max-height: 88vh;
    overflow-y: auto;
    box-shadow: 0 24px 80px rgba(0,0,0,0.7);
  }}
  .panel::-webkit-scrollbar {{ width: 6px; }}
  .panel::-webkit-scrollbar-track {{ background: #0b0e17; }}
  .panel::-webkit-scrollbar-thumb {{ background: #2d3a50; border-radius: 3px; }}

  .panel-header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1rem;
  }}
  .panel-title {{
    font-size: 1.5rem; font-weight: 900; letter-spacing: 1px;
    background: linear-gradient(90deg, #f5a623, #ffd980);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .btn-cerrar {{
    background: #1e293b; border: 1px solid #3a4a6a;
    color: #7a8ab0; border-radius: 8px;
    padding: 6px 18px; font-size: 0.85rem;
    font-weight: 700; cursor: pointer; transition: all 0.2s;
    font-family: inherit;
  }}
  .btn-cerrar:hover {{ background: #dc2626; color: #fff; border-color: #dc2626; }}

  .intro {{
    background: #0d1424; border: 1px solid #2d4a7a;
    border-radius: 12px; padding: 1.2rem 1.5rem;
    margin-bottom: 1.4rem; font-size: 0.88rem;
    color: #b0c4e8; line-height: 1.7;
  }}
  .intro strong {{ color: #f5a623; }}
  .pasos {{ display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 0.8rem; }}
  .paso {{
    display: flex; align-items: center; gap: 0.5rem;
    background: #141928; border: 1px solid #2d3a50;
    border-radius: 8px; padding: 0.45rem 0.9rem;
    font-size: 0.8rem; color: #c8d8ff;
  }}
  .paso-num {{
    background: #f5a623; color: #0b0e17; font-weight: 900;
    font-size: 0.7rem; width: 20px; height: 20px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
  }}

  .sec-label {{
    font-size: 0.72rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: #f5a623;
    border-left: 3px solid #f5a623; padding-left: 8px;
    margin-bottom: 0.6rem;
  }}

  .filtros {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.2rem; }}
  .act-filtro-btn {{
    padding: 4px 14px; border-radius: 20px;
    border: 1px solid #3a4a6a; background: transparent;
    color: #7a8ab0; font-size: 0.78rem; font-weight: 700;
    cursor: pointer; transition: all 0.2s; font-family: inherit;
  }}
  .act-filtro-btn:hover {{ border-color: #f5a623; color: #f5a623; }}
  .act-filtro-btn.activo {{
    background: rgba(245,166,35,0.15);
    border-color: #f5a623; color: #f5a623;
  }}

  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }}
  .act-card {{
    background: #141928; border: 1px solid #2a3350;
    border-radius: 14px; padding: 1.2rem 1.3rem;
    text-decoration: none;
    display: flex; flex-direction: column; gap: 0.6rem;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  }}
  .act-card:hover {{
    transform: translateY(-3px); border-color: #f5a623;
    box-shadow: 0 8px 24px rgba(245,166,35,0.15);
  }}
  .act-card-top {{ display: flex; align-items: center; gap: 0.7rem; }}
  .act-icono {{
    font-size: 1.7rem; flex-shrink: 0; width: 42px; height: 42px;
    background: #0d1020; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
  }}
  .act-card-nombre {{ font-size: 0.95rem; font-weight: 700; color: #e0eaff; line-height: 1.3; }}
  .act-card-desc {{ font-size: 0.78rem; color: #7a8ab0; line-height: 1.55; flex: 1; }}
  .act-card-footer {{
    display: flex; align-items: center;
    justify-content: space-between; margin-top: 0.2rem;
  }}
  .act-eje-badge {{ font-size: 0.7rem; font-weight: 700; padding: 2px 10px; border-radius: 20px; }}
  .act-card-cta {{ font-size: 0.75rem; color: #f5a623; font-weight: 700; }}
  .act-empty {{
    grid-column: 1/-1; text-align: center;
    padding: 2rem; color: #4a5a7a; font-size: 0.9rem;
  }}
  .nota-pie {{
    text-align: center; margin-top: 1.6rem;
    font-size: 0.75rem; color: #4a5a7a; font-style: italic;
  }}

  @media (max-width: 520px) {{
    .panel {{ padding: 1.2rem; }}
    .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="overlay">
  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">🧩 Actividades Interactivas</div>
      <button class="btn-cerrar" onclick="navegarA('cerrar')">✕ Cerrar</button>
    </div>

    <div class="intro">
      <strong>¿Cómo usar estas actividades?</strong><br>
      Cada actividad está diseñada para que practiques de forma dinámica.
      Al ingresar encontrarás secciones de:
      <div class="pasos">
        <div class="paso"><span class="paso-num">1</span>Teoría visual y ejemplos</div>
        <div class="paso"><span class="paso-num">2</span>Análisis con gráficos interactivos</div>
        <div class="paso"><span class="paso-num">3</span>Resolución de problemas guiada</div>
        <div class="paso"><span class="paso-num">4</span>Juego dinámico para autoevaluarte</div>
      </div>
    </div>

    <div class="sec-label">📚 FILTRAR POR EJE</div>
    <div class="filtros">{filtros_html}</div>

    <div class="sec-label">
      📋 ACTIVIDADES DISPONIBLES
      <span style="color:#4a5a7a;font-size:0.68rem;text-transform:none;
                   letter-spacing:0;margin-left:8px;">{conteo}</span>
    </div>
    <div class="grid">{cards_html}</div>

    <div class="nota-pie">
      Las actividades se abren en una pestaña nueva y no afectan el rendimiento de esta página.
    </div>
  </div>
</div>

<script>
  function navegarA(accion) {{
    // Modifica la URL del padre (Streamlit) con el query param y recarga
    var url = window.parent.location.href.split('?')[0];
    window.parent.location.href = url + '?act_accion=' + encodeURIComponent(accion);
  }}
</script>
</body>
</html>"""

    # ── CSS para ocultar el iframe border y fondo negro ────────────────
    st.markdown("""
    <style>
    /* Eliminar borde y fondo del contenedor del iframe del modal */
    iframe[title="actividades_modal.mostrar_modal_actividades"] {
        border: none !important;
        background: transparent !important;
    }
    /* Cubrir toda la pantalla con el iframe */
    div[data-testid="stCustomComponentV1"]:has(
        iframe[title="actividades_modal.mostrar_modal_actividades"]
    ) {
        position: fixed !important;
        inset: 0 !important;
        z-index: 9997 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: transparent !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    components.html(html, height=800, scrolling=False)
