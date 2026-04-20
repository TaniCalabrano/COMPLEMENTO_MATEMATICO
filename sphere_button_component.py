"""
sphere_button_component.py
Componente: botón "Ingresar al repositorio" dentro de una esfera 3D giratoria.
Devuelve True cuando el usuario hace clic.
"""
import streamlit.components.v1 as components
import streamlit as st

SPHERE_BTN_HTML = """
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
    height: 160px;
    overflow: hidden;
    font-family: Georgia, serif;
  }

  .scene {
    width: 280px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  /* ── Canvas for the WebGL / 2D sphere rings ── */
  #sphereCanvas {
    position: absolute;
    top: 0; left: 0;
    width: 280px; height: 140px;
    pointer-events: none;
  }

  /* ── The actual button ── */
  .sphere-btn {
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
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    box-shadow:
      0 0 24px rgba(245,166,35,0.45),
      0 0 60px rgba(245,166,35,0.15),
      inset 0 0 20px rgba(245,166,35,0.08);
    transition: box-shadow 0.25s, transform 0.25s, border-color 0.25s;
    animation: spherePulse 3s ease-in-out infinite;
    text-decoration: none;
  }

  .sphere-btn:hover {
    box-shadow:
      0 0 38px rgba(245,166,35,0.75),
      0 0 80px rgba(245,166,35,0.3),
      inset 0 0 28px rgba(245,166,35,0.18);
    border-color: rgba(245,166,35,1);
    transform: scale(1.06);
    animation: none;
  }

  .sphere-btn:active { transform: scale(0.97); }

  @keyframes spherePulse {
    0%,100% { box-shadow: 0 0 24px rgba(245,166,35,0.45), 0 0 60px rgba(245,166,35,0.15), inset 0 0 20px rgba(245,166,35,0.08); }
    50%      { box-shadow: 0 0 36px rgba(245,166,35,0.65), 0 0 80px rgba(245,166,35,0.25), inset 0 0 28px rgba(245,166,35,0.14); }
  }

  .bolt { font-size: 22px; line-height:1; }

  .btn-label {
    font-size: 10.5px;
    font-weight: 800;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #f5e6a0;
    text-align: center;
    line-height: 1.25;
    text-shadow: 0 0 8px rgba(245,166,35,0.7);
    padding: 0 6px;
  }

  /* Shine overlay */
  .sphere-btn::before {
    content:'';
    position:absolute;
    top:10%; left:18%;
    width:38%; height:28%;
    background: radial-gradient(ellipse, rgba(255,255,255,0.25) 0%, transparent 70%);
    border-radius:50%;
    pointer-events:none;
  }
</style>
</head>
<body>
<div class="scene">
  <canvas id="sphereCanvas" width="280" height="140"></canvas>
  <button class="sphere-btn" id="enterBtn" onclick="handleClick()">
    <span class="bolt">⚡</span>
    <span class="btn-label">Ingresar<br>al repositorio</span>
  </button>
</div>

<script>
// ── Rotating orbit rings drawn on canvas ────────────────────────────────────
(function(){
  var canvas = document.getElementById('sphereCanvas');
  var ctx    = canvas.getContext('2d');
  var W = 280, H = 140;
  var cx = W/2, cy = H/2;
  var R  = 62;   // sphere radius for ring orbits
  var t  = 0;

  var rings = [
    { tilt: 0.45,  speed: 0.012, color: 'rgba(245,166,35,',  width: 1.4 },
    { tilt: -0.55, speed: -0.009, color: 'rgba(126,207,255,', width: 1.1 },
    { tilt: 1.1,   speed: 0.007, color: 'rgba(245,166,35,',  width: 0.8 },
    { tilt: 0.0,   speed: 0.015, color: 'rgba(200,180,80,',  width: 1.0 },
  ];

  function drawRing(ring, angle) {
    // Ellipse: horizontal radius = R, vertical radius = R * |sin(tilt)|
    // Rotated by angle in XZ plane
    var rx   = R;
    var ry   = R * Math.abs(Math.sin(ring.tilt));
    var rotY = angle;    // rotation around Y axis (horizontal spin)

    // We simulate a 3D ellipse by parametric drawing
    ctx.beginPath();
    var steps = 120;
    for (var i = 0; i <= steps; i++) {
      var theta = (i / steps) * Math.PI * 2;
      // 3D point on ring
      var x3 = rx * Math.cos(theta);
      var y3 = ry * Math.sin(theta) * Math.cos(ring.tilt);
      // Rotate around Y
      var xR = x3 * Math.cos(rotY) - 0;
      var zR = x3 * Math.sin(rotY);
      // Project (simple orthographic + slight perspective)
      var depth = (zR / (R * 1.5)) * 0.5 + 0.5; // 0..1 front-to-back
      var px = cx + xR;
      var py = cy + y3;

      // Alpha modulated by depth
      var alpha = 0.12 + depth * 0.38;
      if (i === 0) {
        ctx.moveTo(px, py);
        ctx.strokeStyle = ring.color + alpha + ')';
      } else {
        ctx.lineTo(px, py);
      }
    }
    ctx.lineWidth = ring.width;
    ctx.stroke();
  }

  // Rotating dots on rings
  var dots = rings.map(function(ring, idx) {
    return { ring: ring, phase: idx * 1.5 };
  });

  function drawDot(ring, angle, phase) {
    var theta = angle * ring.speed * 60 + phase;
    var rx    = R;
    var ry    = R * Math.abs(Math.sin(ring.tilt));
    var x3    = rx * Math.cos(theta);
    var y3    = ry * Math.sin(theta) * Math.cos(ring.tilt);
    var xR    = x3 * Math.cos(angle);
    var zR    = x3 * Math.sin(angle);
    var depth = (zR / (R * 1.5)) * 0.5 + 0.5;
    var px    = cx + xR;
    var py    = cy + y3;
    var r     = 2.2 + depth * 1.8;
    var alpha = 0.4 + depth * 0.6;

    ctx.beginPath();
    ctx.arc(px, py, r, 0, Math.PI*2);
    ctx.fillStyle = ring.color + alpha + ')';
    ctx.fill();
  }

  function animate() {
    ctx.clearRect(0, 0, W, H);
    t += 1;

    rings.forEach(function(ring, i) {
      var angle = t * ring.speed;
      drawRing(ring, angle);
      drawDot(ring, angle, dots[i].phase);
    });

    requestAnimationFrame(animate);
  }
  animate();
})();

// ── Click handler: notify Streamlit via postMessage ─────────────────────────
function handleClick() {
  // Visual feedback
  var btn = document.getElementById('enterBtn');
  btn.style.transform = 'scale(0.93)';
  setTimeout(function(){ btn.style.transform = ''; }, 200);

  // Send message to parent Streamlit frame
  window.parent.postMessage({ type: 'CM_INGRESAR' }, '*');
}
</script>
</body>
</html>
"""

def mostrar_boton_esfera():
    """
    Renderiza el botón-esfera. Retorna True si fue clickeado
    usando el truco del query param de Streamlit.
    """
    # Listener JS que setea un query param cuando recibe el mensaje
    LISTENER_JS = """
    <script>
    window.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'CM_INGRESAR') {
        // Navigate parent to add ?ingresar=1
        var url = new URL(window.parent.location.href);
        url.searchParams.set('ingresar', '1');
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    import streamlit as st
    st.markdown(LISTENER_JS, unsafe_allow_html=True)
    components.html(SPHERE_BTN_HTML, height=160, scrolling=False)

    # Check query param
    params = st.query_params
    if params.get("ingresar") == "1":
        st.query_params.clear()
        return True
    return False
