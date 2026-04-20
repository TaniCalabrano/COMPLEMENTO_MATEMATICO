"""
sphere_button_component.py
Botón "Ingresar al repositorio" con esfera 3D giratoria decorativa encima.
La esfera es visual (canvas), el botón real es un st.button de Streamlit.
"""
import streamlit as st
import streamlit.components.v1 as components

SPHERE_ANIM_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    background: transparent;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 150px;
    overflow: hidden;
  }
  .scene {
    width: 280px;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  #sphereCanvas {
    position: absolute;
    top: 0; left: 0;
    width: 280px; height: 150px;
    pointer-events: none;
  }
  .sphere-deco {
    position: relative;
    z-index: 10;
    background: radial-gradient(circle at 35% 35%,
      rgba(255,255,255,0.18) 0%,
      rgba(245,166,35,0.22) 30%,
      rgba(30,20,0,0.85) 80%,
      rgba(10,8,0,0.95) 100%
    );
    border: 2px solid rgba(245,166,35,0.7);
    border-radius: 50%;
    width: 124px;
    height: 124px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    box-shadow:
      0 0 24px rgba(245,166,35,0.45),
      0 0 60px rgba(245,166,35,0.15),
      inset 0 0 20px rgba(245,166,35,0.08);
    animation: spherePulse 3s ease-in-out infinite;
    pointer-events: none;
  }
  @keyframes spherePulse {
    0%,100% {
      box-shadow: 0 0 24px rgba(245,166,35,0.45),
                  0 0 60px rgba(245,166,35,0.15),
                  inset 0 0 20px rgba(245,166,35,0.08);
    }
    50% {
      box-shadow: 0 0 40px rgba(245,166,35,0.70),
                  0 0 90px rgba(245,166,35,0.28),
                  inset 0 0 30px rgba(245,166,35,0.16);
    }
  }
  .bolt { font-size: 22px; line-height:1; }
  .btn-label {
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #f5e6a0;
    text-align: center;
    line-height: 1.3;
    text-shadow: 0 0 8px rgba(245,166,35,0.7);
    padding: 0 6px;
    font-family: Georgia, serif;
  }
  .sphere-deco::before {
    content: '';
    position: absolute;
    top: 10%; left: 18%;
    width: 38%; height: 28%;
    background: radial-gradient(ellipse, rgba(255,255,255,0.25) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
  }
</style>
</head>
<body>
<div class="scene">
  <canvas id="sphereCanvas" width="280" height="150"></canvas>
  <div class="sphere-deco">
    <span class="bolt">⚡</span>
    <span class="btn-label">Ingresar<br>al repositorio</span>
  </div>
</div>
<script>
(function(){
  var canvas = document.getElementById('sphereCanvas');
  var ctx    = canvas.getContext('2d');
  var W = 280, H = 150, cx = W/2, cy = H/2, R = 62, t = 0;

  var rings = [
    { tilt: 0.45,  speed: 0.012,  color: 'rgba(245,166,35,',  width: 1.4 },
    { tilt: -0.55, speed: -0.009, color: 'rgba(126,207,255,', width: 1.1 },
    { tilt: 1.1,   speed: 0.007,  color: 'rgba(245,166,35,',  width: 0.8 },
    { tilt: 0.0,   speed: 0.015,  color: 'rgba(200,180,80,',  width: 1.0 },
  ];

  function drawRing(ring, angle) {
    var rx = R, ry = R * Math.abs(Math.sin(ring.tilt));
    ctx.beginPath();
    for (var i = 0; i <= 120; i++) {
      var theta = (i / 120) * Math.PI * 2;
      var x3 = rx * Math.cos(theta);
      var y3 = ry * Math.sin(theta) * Math.cos(ring.tilt);
      var xR = x3 * Math.cos(angle);
      var zR = x3 * Math.sin(angle);
      var depth = (zR / (R * 1.5)) * 0.5 + 0.5;
      var alpha = 0.12 + depth * 0.38;
      if (i === 0) { ctx.moveTo(cx+xR, cy+y3); ctx.strokeStyle = ring.color + alpha + ')'; }
      else ctx.lineTo(cx+xR, cy+y3);
    }
    ctx.lineWidth = ring.width;
    ctx.stroke();
  }

  function drawDot(ring, angle, phase) {
    var theta = angle * ring.speed * 60 + phase;
    var rx = R, ry = R * Math.abs(Math.sin(ring.tilt));
    var x3 = rx * Math.cos(theta), y3 = ry * Math.sin(theta) * Math.cos(ring.tilt);
    var xR = x3 * Math.cos(angle), zR = x3 * Math.sin(angle);
    var depth = (zR / (R * 1.5)) * 0.5 + 0.5;
    ctx.beginPath();
    ctx.arc(cx+xR, cy+y3, 2.2 + depth*1.8, 0, Math.PI*2);
    ctx.fillStyle = ring.color + (0.4 + depth*0.6) + ')';
    ctx.fill();
  }

  var phases = [0, 1.5, 3.0, 4.5];
  function animate() {
    ctx.clearRect(0, 0, W, H);
    t++;
    rings.forEach(function(ring, i) {
      var angle = t * ring.speed;
      drawRing(ring, angle);
      drawDot(ring, angle, phases[i]);
    });
    requestAnimationFrame(animate);
  }
  animate();
})();
</script>
</body>
</html>
"""

def mostrar_boton_esfera():
    """
    Muestra la esfera animada decorativa y un st.button real de Streamlit debajo.
    Retorna True si el botón fue presionado.
    """
    components.html(SPHERE_ANIM_HTML, height=150, scrolling=False)

    st.markdown("""
    <style>
    .btn-esfera-wrapper > div > button {
        background: linear-gradient(135deg, #7a4a00, #c07a00) !important;
        color: #fff8e0 !important;
        border: 2px solid #f5a623 !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        box-shadow: 0 0 18px rgba(245,166,35,0.35) !important;
        margin-top: -8px !important;
    }
    .btn-esfera-wrapper > div > button:hover {
        background: linear-gradient(135deg, #c07a00, #f5a623) !important;
        color: #1a0a00 !important;
        box-shadow: 0 0 30px rgba(245,166,35,0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        st.markdown('<div class="btn-esfera-wrapper">', unsafe_allow_html=True)
        clicked = st.button("⚡ Ingresar al repositorio", key="btn_esfera_ingreso", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    return clicked
