"""
sphere_button_component.py

Esfera circular giratoria como botón de ingreso.
Solución sin rectángulo visible:
  - Los anillos animados se dibujan en un components.html() con fondo transparente
  - El botón real de Streamlit se posiciona encima con CSS (border-radius:50%)
  - Se usa margin-top negativo para superponerlos visualmente
  - NO hay botón de texto debajo
"""
import streamlit as st
import streamlit.components.v1 as components


RINGS_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    background: transparent !important;
    overflow: hidden;
    width: 100%;
    height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  canvas { display: block; }
</style>
</head>
<body>
<canvas id="c" width="160" height="160"></canvas>
<script>
(function(){
  var c = document.getElementById('c');
  var ctx = c.getContext('2d');
  var cx=80, cy=80, R=64, t=0;
  var rings = [
    {tilt:0.50, speed:0.013, col:'rgba(245,166,35,',  lw:1.4},
    {tilt:-0.58,speed:-0.010,col:'rgba(126,207,255,', lw:1.1},
    {tilt:1.15, speed:0.008, col:'rgba(245,166,35,',  lw:0.8},
    {tilt:0.05, speed:0.016, col:'rgba(210,185,80,',  lw:0.9},
  ];
  var phases=[0,1.6,3.1,4.7];

  function drawRing(r,angle){
    var ry=R*Math.abs(Math.sin(r.tilt));
    ctx.beginPath();
    for(var i=0;i<=120;i++){
      var th=(i/120)*Math.PI*2;
      var x3=R*Math.cos(th), y3=ry*Math.sin(th)*Math.cos(r.tilt);
      var xR=x3*Math.cos(angle), zR=x3*Math.sin(angle);
      var d=(zR/(R*1.5))*0.5+0.5;
      if(i===0){ctx.moveTo(cx+xR,cy+y3);ctx.strokeStyle=r.col+(0.10+d*0.42)+')';}
      else ctx.lineTo(cx+xR,cy+y3);
    }
    ctx.lineWidth=r.lw; ctx.stroke();
  }

  function drawDot(r,angle,ph){
    var th=t*r.speed*0.9+ph;
    var ry=R*Math.abs(Math.sin(r.tilt));
    var x3=R*Math.cos(th), y3=ry*Math.sin(th)*Math.cos(r.tilt);
    var xR=x3*Math.cos(angle), zR=x3*Math.sin(angle);
    var d=(zR/(R*1.5))*0.5+0.5;
    ctx.beginPath();
    ctx.arc(cx+xR,cy+y3,1.8+d*2.2,0,Math.PI*2);
    ctx.fillStyle=r.col+(0.35+d*0.65)+')'; ctx.fill();
  }

  function frame(){
    ctx.clearRect(0,0,160,160);
    t++;
    rings.forEach(function(r,i){
      var a=t*r.speed;
      drawRing(r,a); drawDot(r,a,phases[i]);
    });
    requestAnimationFrame(frame);
  }
  frame();
})();
</script>
</body>
</html>
"""


def mostrar_boton_esfera():
    """
    Muestra anillos animados + botón circular superpuesto.
    Retorna True si el botón fue presionado.
    """

    st.markdown("""
    <style>
    /* ─── Forzar fondo transparente en el iframe de anillos ─── */
    div[data-testid="stCustomComponentV1"] > iframe,
    div.element-container iframe {
        background: transparent !important;
        background-color: transparent !important;
    }

    /* ─── Wrapper que sube el botón sobre los anillos ─── */
    .sphere-overlap-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 0;
    }
    .sphere-rings-row {
        display: flex;
        justify-content: center;
        margin-bottom: -150px;   /* overlaps the button on top */
        position: relative;
        z-index: 0;
        pointer-events: none;    /* rings don't steal clicks */
        width: 100%;
    }
    .sphere-btn-row {
        position: relative;
        z-index: 10;
        display: flex;
        justify-content: center;
        margin-bottom: 16px;
    }

    /* ─── El botón esfera circular perfecta ─── */
    .sphere-btn-row button,
    .sphere-btn-row > div > button,
    .sphere-btn-row > div > div > button {
        width:  130px !important;
        height: 130px !important;
        min-height: 130px !important;
        border-radius: 50% !important;
        padding: 0 12px !important;
        font-size: 9.5px !important;
        font-weight: 900 !important;
        letter-spacing: 1.3px !important;
        text-transform: uppercase !important;
        line-height: 1.4 !important;
        font-family: Georgia, serif !important;
        color: #f5e6a0 !important;
        text-align: center !important;
        white-space: pre-line !important;
        background: radial-gradient(circle at 33% 30%,
            rgba(255,255,255,0.20) 0%,
            rgba(245,166,35,0.18) 25%,
            rgba(40,25,0,0.92) 65%,
            rgba(10,6,0,0.97) 100%
        ) !important;
        border: 2px solid rgba(245,166,35,0.85) !important;
        box-shadow:
            0 0 28px rgba(245,166,35,0.55),
            0 0 70px rgba(245,166,35,0.20),
            inset 0 0 22px rgba(245,166,35,0.12) !important;
        cursor: pointer !important;
        animation: spherePulseBtn 3s ease-in-out infinite !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease !important;
        overflow: hidden !important;
    }

    .sphere-btn-row button:hover,
    .sphere-btn-row > div > button:hover,
    .sphere-btn-row > div > div > button:hover {
        transform: scale(1.08) !important;
        box-shadow:
            0 0 50px rgba(245,166,35,0.90),
            0 0 110px rgba(245,166,35,0.35),
            inset 0 0 36px rgba(245,166,35,0.25) !important;
        animation: none !important;
        color: #ffffff !important;
        background: radial-gradient(circle at 33% 30%,
            rgba(255,255,255,0.28) 0%,
            rgba(245,166,35,0.30) 25%,
            rgba(60,38,0,0.92) 65%,
            rgba(20,12,0,0.97) 100%
        ) !important;
    }

    .sphere-btn-row button:active,
    .sphere-btn-row > div > button:active,
    .sphere-btn-row > div > div > button:active {
        transform: scale(0.93) !important;
    }

    @keyframes spherePulseBtn {
        0%,100% {
            box-shadow:
                0 0 28px rgba(245,166,35,0.55),
                0 0 70px rgba(245,166,35,0.20),
                inset 0 0 22px rgba(245,166,35,0.12);
        }
        50% {
            box-shadow:
                0 0 46px rgba(245,166,35,0.80),
                0 0 105px rgba(245,166,35,0.32),
                inset 0 0 34px rgba(245,166,35,0.22);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Anillos (decorativos, z-index bajo) ──────────────────────────────────
    st.markdown('<div class="sphere-overlap-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="sphere-rings-row">', unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1, 1])
    with mid:
        components.html(RINGS_HTML, height=160, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)  # close rings-row

    # ── Botón circular (z-index alto, visualmente sobre los anillos) ──────────
    st.markdown('<div class="sphere-btn-row">', unsafe_allow_html=True)
    clicked = st.button("⚡\nIngresar\nal repositorio", key="btn_esfera_ingreso")
    st.markdown('</div>', unsafe_allow_html=True)  # close btn-row
    st.markdown('</div>', unsafe_allow_html=True)  # close wrapper

    return clicked
