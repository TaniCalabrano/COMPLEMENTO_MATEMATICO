import streamlit as st
import streamlit.components.v1 as components
import json
import time
import random
from pathlib import Path
 
st.set_page_config(
    page_title="PAES Repositorio",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    .main-title {
        font-size: 2.2rem; font-weight: 800; color: #ffffff;
        text-align: center; padding: 1rem 0 0.2rem 0; letter-spacing: 1px;
    }
    .main-subtitle {
        text-align: center; color: #888; font-size: 0.95rem; margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block; padding: 3px 12px; border-radius: 20px;
        font-size: 0.78rem; font-weight: 600; margin-right: 6px; margin-bottom: 10px;
    }
    .badge-m1  { background: #1e3a5f; color: #90CAF9; }
    .badge-m2  { background: #1e3a2a; color: #A5D6A7; }
    .badge-fis { background: #3a1e2a; color: #F48FB1; }
    .badge-eje { background: #2a2a1e; color: #FFD54F; }
    .result-correct {
        background: #1b3a2a; border: 1.5px solid #4CAF50; border-radius: 10px;
        padding: 0.9rem 1.2rem; color: #A5D6A7; font-size: 1.05rem;
        font-weight: 600; margin-top: 0.8rem;
    }
    .result-incorrect {
        background: #3a1a1a; border: 1.5px solid #EF5350; border-radius: 10px;
        padding: 0.9rem 1.2rem; color: #EF9A9A; font-size: 1.05rem;
        font-weight: 600; margin-top: 0.8rem;
    }
    section[data-testid="stSidebar"] { background: #13151f; }
    .sidebar-section {
        font-size: 0.8rem; color: #888; text-transform: uppercase;
        letter-spacing: 1px; margin: 1rem 0 0.4rem 0; font-weight: 700;
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
        "respondido":      False,
        "seleccion":       None,
        "timer_start":     None,
        "timer_duracion":  90,
        "tiempo_agotado":  False,
        "timer_iniciado":  False,
        "tiempo_respuesta": None,   # segundos que tardó en responder
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
        "Duración", [90, 120],
        format_func=lambda x: f"{x} segundos",
        index=0, label_visibility="collapsed"
    )
    st.session_state.timer_duracion = timer_choice
 
    st.markdown("---")
    st.markdown('<div class="sidebar-section">🔍 Buscar por nombre</div>', unsafe_allow_html=True)
    nombres  = [p["nombre"] for p in problems]
    busqueda = st.selectbox("Buscar", ["— Selecciona —"] + nombres, label_visibility="collapsed")
 
    st.markdown("---")
    st.markdown('<div class="sidebar-section">🎯 Filtrar por prueba</div>', unsafe_allow_html=True)
    pruebas_disp  = sorted(set(p["prueba"] for p in problems))
    filtro_prueba = st.multiselect("Prueba", pruebas_disp, default=pruebas_disp, label_visibility="collapsed")
 
    st.markdown('<div class="sidebar-section">📚 Filtrar por eje</div>', unsafe_allow_html=True)
    ejes_disp  = sorted(set(p["eje"] for p in problems))
    filtro_eje = st.multiselect("Eje", ejes_disp, default=ejes_disp, label_visibility="collapsed")
 
    st.markdown("---")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        btn_aleatorio = st.button("🎲 Aleatorio", use_container_width=True)
    with col_s2:
        btn_buscar = st.button("🔎 Buscar", use_container_width=True)
 
# ─── Lógica de selección ───────────────────────────────────────────────────────
pool = [p for p in problems if p["prueba"] in filtro_prueba and p["eje"] in filtro_eje]
 
def cargar_problema(p):
    st.session_state.problema_actual  = p
    st.session_state.respondido       = False
    st.session_state.seleccion        = None
    st.session_state.timer_start      = None
    st.session_state.tiempo_agotado   = False
    st.session_state.timer_iniciado   = False
    st.session_state.tiempo_respuesta = None
 
if btn_aleatorio and pool:
    cargar_problema(random.choice(pool))
 
if btn_buscar and busqueda != "— Selecciona —":
    encontrado = next((p for p in problems if p["nombre"] == busqueda), None)
    if encontrado:
        cargar_problema(encontrado)
 
# ─── ÁREA PRINCIPAL ────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📐 Repositorio PAES</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Practica problemas de M1 · M2 · Física</div>', unsafe_allow_html=True)
 
prob = st.session_state.problema_actual
 
if prob is None:
    st.info("👈 Usa el panel izquierdo para seleccionar un problema aleatorio o buscarlo por nombre.")
    st.stop()
 
# ── Detectar timeout por query param ──────────────────────────────────────────
params = st.query_params
if params.get("timeout") == "1" and not st.session_state.respondido:
    elapsed = int(time.time() - st.session_state.timer_start) if st.session_state.timer_start else st.session_state.timer_duracion
    st.session_state.tiempo_agotado   = True
    st.session_state.respondido       = True
    st.session_state.tiempo_respuesta = st.session_state.timer_duracion
    st.query_params.clear()
    st.rerun()
 
col_q, col_t = st.columns([3, 1])
 
# ══════════════════════════════════════════════════════════════════════════════
# TIMER — usando st.components.v1.html para que el JS funcione correctamente
# ══════════════════════════════════════════════════════════════════════════════
with col_t:
    duracion = st.session_state.timer_duracion
 
    # ── Caso 1: ya respondió ──────────────────────────────────────────────────
    if st.session_state.respondido:
        components.html(f"""
        <div style="background:#1a1d2e; border:2px solid #2a2d3e; border-radius:12px;
                    padding:1.2rem; text-align:center; font-family:sans-serif;">
            <div style="font-size:2rem;">⌛</div>
            <div style="font-size:2.8rem; font-weight:800; font-family:monospace;
                        color:#EF5350; line-height:1.1;">0:00</div>
            <div style="font-size:0.75rem; color:#888; margin-top:4px;">
                ⏱ {duracion}s disponibles
            </div>
        </div>
        """, height=130)
 
    # ── Caso 2: problema cargado, timer no iniciado ───────────────────────────
    elif not st.session_state.timer_iniciado:
        components.html(f"""
        <div style="background:#1a1d2e; border:2px solid #2a2d3e; border-radius:12px;
                    padding:1.2rem; text-align:center; font-family:sans-serif;">
            <div style="font-size:2rem;">⏳</div>
            <div style="font-size:2.8rem; font-weight:800; font-family:monospace;
                        color:#444; line-height:1.1;">
                {duracion // 60}:{duracion % 60:02d}
            </div>
            <div style="font-size:0.75rem; color:#888; margin-top:4px;">
                ⏱ {duracion}s disponibles
            </div>
        </div>
        """, height=130)
 
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("▶️ Iniciar cronómetro", use_container_width=True, type="primary"):
            st.session_state.timer_iniciado = True
            st.session_state.timer_start    = time.time()
            st.rerun()
 
    # ── Caso 3: timer corriendo ───────────────────────────────────────────────
    else:
        elapsed  = int(time.time() - st.session_state.timer_start)
        restante = max(0, duracion - elapsed)
 
        # Construimos la URL de timeout para pasársela al JS
        # (sin depender de window.location que puede fallar en iframes)
        components.html(f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            * {{ margin:0; padding:0; box-sizing:border-box; }}
            body {{ background: transparent; font-family: sans-serif; }}
            #timerBox {{
                background:#1a1d2e; border:2px solid #2a2d3e; border-radius:12px;
                padding:1.2rem; text-align:center;
            }}
            #timerDigits {{
                font-size:2.8rem; font-weight:800; font-family:monospace;
                line-height:1.1; color:#90CAF9;
            }}
            #timerLabel {{ font-size:0.75rem; color:#888; margin-top:4px; }}
            #pauseBtn {{
                margin-top:10px; width:100%; padding:9px 0; border-radius:8px;
                border:1.5px solid #3a3d5e; background:#23263a; color:#90CAF9;
                font-size:1rem; font-weight:700; cursor:pointer;
            }}
        </style>
        </head>
        <body>
        <div id="timerBox">
            <div id="timerEmoji" style="font-size:2rem;">⏳</div>
            <div id="timerDigits">{restante // 60}:{restante % 60:02d}</div>
            <div id="timerLabel">⏱ {duracion}s disponibles</div>
        </div>
        <button id="pauseBtn" onclick="togglePause()">⏸ Pausar</button>
 
        <script>
            var remaining = {restante};
            var total     = {duracion};
            var paused    = false;
            var digits    = document.getElementById('timerDigits');
            var emoji     = document.getElementById('timerEmoji');
            var btn       = document.getElementById('pauseBtn');
 
            function pad(n) {{ return n < 10 ? '0' + n : '' + n; }}
 
            function setColor(r) {{
                var pct = r / total;
                if (pct > 0.4)      digits.style.color = '#90CAF9';
                else if (pct > 0.2) digits.style.color = '#FFD54F';
                else                digits.style.color = '#EF5350';
            }}
 
            function togglePause() {{
                paused = !paused;
                if (paused) {{
                    btn.innerText         = '▶️ Reanudar';
                    btn.style.color       = '#FFD54F';
                    btn.style.borderColor = '#FFD54F';
                    btn.style.background  = '#1e3a5f';
                    emoji.innerText       = '⏸';
                }} else {{
                    btn.innerText         = '⏸ Pausar';
                    btn.style.color       = '#90CAF9';
                    btn.style.borderColor = '#3a3d5e';
                    btn.style.background  = '#23263a';
                }}
            }}
 
            setColor(remaining);
 
            var iv = setInterval(function() {{
                if (paused) return;
                if (remaining <= 0) {{
                    clearInterval(iv);
                    digits.innerText   = '0:00';
                    digits.style.color = '#EF5350';
                    emoji.innerText    = '⌛';
                    btn.style.display  = 'none';
                    // Notificar a Streamlit via URL del padre
                    window.parent.location.href =
                        window.parent.location.href.split('?')[0] + '?timeout=1';
                    return;
                }}
                var m = Math.floor(remaining / 60);
                var s = remaining % 60;
                digits.innerText = m + ':' + pad(s);
                emoji.innerText  = (remaining % 2 === 0) ? '⏳' : '⌛';
                setColor(remaining);
                remaining--;
            }}, 1000);
        </script>
        </body>
        </html>
        """, height=175)
 
# ── Pregunta ───────────────────────────────────────────────────────────────────
with col_q:
    badge_cls = {"M1": "badge-m1", "M2": "badge-m2", "Física": "badge-fis"}.get(prob["prueba"], "badge-m1")
    st.markdown(f"""
    <span class="badge {badge_cls}">{prob['prueba']}</span>
    <span class="badge badge-eje">{prob['eje']}</span>
    <span style="color:#666; font-size:0.8rem;">{prob['nombre']}</span>
    """, unsafe_allow_html=True)
 
    img_src = prob["imagen"]
    if img_src.startswith("http://") or img_src.startswith("https://"):
        st.image(img_src, use_container_width=True)
    else:
        img_path = Path(img_src)
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning(f"⚠️ Imagen no encontrada: `{img_src}`")
 
    st.markdown("---")
 
    alt      = prob["alternativas"]
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
        confirmar = st.button("✅ Confirmar respuesta", type="primary")
 
        if confirmar:
            if seleccion_idx is None:
                st.warning("Selecciona una alternativa antes de confirmar.")
            else:
                # Calcular tiempo de respuesta
                if st.session_state.timer_start:
                    elapsed_resp = int(time.time() - st.session_state.timer_start)
                    st.session_state.tiempo_respuesta = min(elapsed_resp, duracion)
                else:
                    st.session_state.tiempo_respuesta = None
 
                st.session_state.seleccion  = letras[seleccion_idx]
                st.session_state.respondido = True
                st.rerun()
    else:
        for k, v in alt.items():
            st.markdown(f"**{k})** {v}")
 
    # ── Resultado ──────────────────────────────────────────────────────────────
    if st.session_state.respondido:
        correcta  = prob["respuesta_correcta"]
        t_resp    = st.session_state.tiempo_respuesta
        t_str     = f"<br><span style='font-size:0.9rem; font-weight:400; opacity:0.85;'>⏱ Tiempo de respuesta: <strong>{t_resp}s</strong></span>" if t_resp is not None else ""
 
        if st.session_state.tiempo_agotado:
            st.markdown(f"""
            <div class="result-incorrect">
                ⏰ ¡Tiempo agotado! La respuesta correcta era <strong>{correcta}</strong>.
                {t_str}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.seleccion == correcta:
            st.markdown(f"""
            <div class="result-correct">
                ✅ ¡Correcto! La alternativa <strong>{correcta}</strong> es la respuesta correcta.
                {t_str}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-incorrect">
                ❌ Incorrecto. Seleccionaste <strong>{st.session_state.seleccion}</strong>,
                pero la respuesta correcta es <strong>{correcta}</strong>.
                {t_str}
            </div>
            """, unsafe_allow_html=True)
 
        if prob.get("video_youtube"):
            st.markdown("---")
            st.link_button("▶️ Ver explicación en YouTube", prob["video_youtube"], type="secondary")
 
        st.markdown("")
        if st.button("➡️ Otro problema aleatorio"):
            if pool:
                cargar_problema(random.choice(pool))
                st.rerun()
