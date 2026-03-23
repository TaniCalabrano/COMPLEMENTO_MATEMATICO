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
BG_APP = "#0f1117"   # mismo fondo que .stApp

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
    """Modal de actividades. Usa session_state puro — sin query_params."""

    if not st.session_state.get("modal_actividades", False):
        return

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
    conteo = f"{len(filtradas)} de {len(actividades)}"

    # ── Cabecera + botón cerrar REAL de Streamlit ──────────────────────
    col_titulo, col_cerrar = st.columns([5, 1])
    with col_titulo:
        st.markdown(
            '<div style="font-size:1.5rem;font-weight:900;letter-spacing:1px;'
            'background:linear-gradient(90deg,#f5a623,#ffd980);'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            'background-clip:text;padding:0.6rem 0 0.2rem;">🧩 Actividades Interactivas</div>',
            unsafe_allow_html=True
        )
    with col_cerrar:
        st.markdown('<div style="padding-top:0.5rem;">', unsafe_allow_html=True)
        if st.button("✕  Cerrar", key="btn_cerrar_modal", use_container_width=True):
            st.session_state["modal_actividades"] = False
            st.session_state["act_filtro_eje"] = "Todos"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Intro ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#0d1424;border:1px solid #2d4a7a;border-radius:12px;
                padding:1.2rem 1.5rem;margin-bottom:1.2rem;font-size:0.88rem;
                color:#b0c4e8;line-height:1.7;">
        <strong style="color:#f5a623;">¿Cómo usar estas actividades?</strong><br>
        Cada actividad está diseñada para que practiques de forma dinámica.
        Al ingresar encontrarás secciones de:
        <div style="display:flex;flex-wrap:wrap;gap:0.6rem;margin-top:0.8rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;background:#141928;
                        border:1px solid #2d3a50;border-radius:8px;padding:0.45rem 0.9rem;
                        font-size:0.8rem;color:#c8d8ff;">
                <span style="background:#f5a623;color:#0b0e17;font-weight:900;font-size:0.7rem;
                             width:20px;height:20px;border-radius:50%;display:inline-flex;
                             align-items:center;justify-content:center;flex-shrink:0;">1</span>
                Teoría visual y ejemplos
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;background:#141928;
                        border:1px solid #2d3a50;border-radius:8px;padding:0.45rem 0.9rem;
                        font-size:0.8rem;color:#c8d8ff;">
                <span style="background:#f5a623;color:#0b0e17;font-weight:900;font-size:0.7rem;
                             width:20px;height:20px;border-radius:50%;display:inline-flex;
                             align-items:center;justify-content:center;flex-shrink:0;">2</span>
                Análisis con gráficos interactivos
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;background:#141928;
                        border:1px solid #2d3a50;border-radius:8px;padding:0.45rem 0.9rem;
                        font-size:0.8rem;color:#c8d8ff;">
                <span style="background:#f5a623;color:#0b0e17;font-weight:900;font-size:0.7rem;
                             width:20px;height:20px;border-radius:50%;display:inline-flex;
                             align-items:center;justify-content:center;flex-shrink:0;">3</span>
                Resolución de problemas guiada
            </div>
            <div style="display:flex;align-items:center;gap:0.5rem;background:#141928;
                        border:1px solid #2d3a50;border-radius:8px;padding:0.45rem 0.9rem;
                        font-size:0.8rem;color:#c8d8ff;">
                <span style="background:#f5a623;color:#0b0e17;font-weight:900;font-size:0.7rem;
                             width:20px;height:20px;border-radius:50%;display:inline-flex;
                             align-items:center;justify-content:center;flex-shrink:0;">4</span>
                Juego dinámico para autoevaluarte
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Filtros por eje (botones Streamlit reales) ─────────────────────
    st.markdown(
        '<div style="font-size:0.72rem;font-weight:700;letter-spacing:2px;'
        'text-transform:uppercase;color:#f5a623;border-left:3px solid #f5a623;'
        'padding-left:8px;margin-bottom:0.6rem;">📚 FILTRAR POR EJE</div>',
        unsafe_allow_html=True
    )

    cols_filtro = st.columns(len(ejes_disponibles))
    for i, eje in enumerate(ejes_disponibles):
        with cols_filtro[i]:
            es_activo = (eje == eje_sel)
            # Estilo diferente para el filtro activo
            if es_activo:
                st.markdown(
                    f'<div style="text-align:center;background:rgba(245,166,35,0.15);'
                    f'border:1px solid #f5a623;color:#f5a623;border-radius:20px;'
                    f'padding:4px 8px;font-size:0.78rem;font-weight:700;cursor:default;">'
                    f'{eje}</div>',
                    unsafe_allow_html=True
                )
            else:
                if st.button(eje, key=f"filtro_eje_{eje}", use_container_width=True):
                    st.session_state["act_filtro_eje"] = eje
                    st.rerun()

    st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)

    # ── Título actividades disponibles ────────────────────────────────
    st.markdown(
        f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:2px;'
        f'text-transform:uppercase;color:#f5a623;border-left:3px solid #f5a623;'
        f'padding-left:8px;margin-bottom:0.8rem;">📋 ACTIVIDADES DISPONIBLES '
        f'<span style="color:#4a5a7a;font-size:0.68rem;text-transform:none;'
        f'letter-spacing:0;margin-left:8px;">{conteo}</span></div>',
        unsafe_allow_html=True
    )

    # ── Grid de cards ──────────────────────────────────────────────────
    if not filtradas:
        st.markdown(
            '<div style="text-align:center;padding:2rem;color:#4a5a7a;'
            'font-size:0.9rem;">No hay actividades para este filtro aún.</div>',
            unsafe_allow_html=True
        )
    else:
        # 3 cards por fila
        for fila_inicio in range(0, len(filtradas), 3):
            fila = filtradas[fila_inicio:fila_inicio + 3]
            cols = st.columns(3)
            for j, act in enumerate(fila):
                eje = act.get("eje", "")
                c = EJES_COLORES.get(eje, EJES_DEFAULT)
                url = act.get("url", "#")
                with cols[j]:
                    st.markdown(
                        f'<div style="background:#141928;border:1px solid #2a3350;'
                        f'border-radius:14px;padding:1.2rem 1.3rem;margin-bottom:0.5rem;">'

                        # Icono + nombre
                        f'<div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.7rem;">'
                        f'<div style="font-size:1.7rem;width:42px;height:42px;background:#0d1020;'
                        f'border-radius:10px;display:flex;align-items:center;justify-content:center;'
                        f'flex-shrink:0;">{act.get("icono","🔬")}</div>'
                        f'<div style="font-size:0.95rem;font-weight:700;color:#e0eaff;'
                        f'line-height:1.3;">{act.get("nombre","")}</div>'
                        f'</div>'

                        # Descripción
                        f'<div style="font-size:0.78rem;color:#7a8ab0;line-height:1.55;'
                        f'margin-bottom:0.9rem;">{act.get("descripcion","")}</div>'

                        # Footer: badge + link
                        f'<div style="display:flex;align-items:center;justify-content:space-between;">'
                        f'<span style="font-size:0.7rem;font-weight:700;padding:2px 10px;'
                        f'border-radius:20px;background:{c["bg"]};border:1px solid {c["border"]};'
                        f'color:{c["text"]};">{eje}</span>'
                        f'<a href="{url}" target="_blank" rel="noopener noreferrer" '
                        f'style="font-size:0.8rem;color:#f5a623;font-weight:700;'
                        f'text-decoration:none;background:rgba(245,166,35,0.1);'
                        f'border:1px solid rgba(245,166,35,0.3);border-radius:8px;'
                        f'padding:4px 12px;">Abrir ↗</a>'
                        f'</div>'

                        f'</div>',
                        unsafe_allow_html=True
                    )

    # ── Nota al pie ────────────────────────────────────────────────────
    st.markdown(
        '<div style="text-align:center;margin-top:1.6rem;font-size:0.75rem;'
        'color:#4a5a7a;font-style:italic;">'
        'Las actividades se abren en una pestaña nueva y no afectan el rendimiento de esta página.'
        '</div>',
        unsafe_allow_html=True
    )
