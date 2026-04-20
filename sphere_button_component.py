"""
sphere_button_component.py

Clic funciona via un <form method="GET" target="_parent">
que envía cm_go=1 a la URL padre — esto es lo más confiable en Streamlit
porque no requiere JS cross-origin, es una navegación nativa del navegador.
"""
import streamlit as st
import streamlit.components.v1 as components


def _build_html(base_url: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{
    background: #0f1117;
    overflow: hidden;
    width: 100%;
    height: 212px;
    display: flex;
    align-items: center;
    justify-content: center;
  }}
  form {{
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border: none;
    padding: 0;
    margin: 0;
  }}
  .scene {{
    position: relative;
    width: 212px;
    height: 212px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }}
  canvas {{
    position: absolute;
    top: 0; left: 0;
    width: 212px; height: 212px;
    pointer-events: none;
  }}
  button.sphere {{
    position: relative;
    z-index: 10;
    width: 155px;
    height: 155px;
    border-radius: 50%;
    border: 2px solid rgba(245,166,35,0.85);
    background: radial-gradient(circle at 33% 30%,
      rgba(255,255,255,0.22) 0%,
      rgba(245,166,35,0.20) 22%,
      rgba(40,25,0,0.92)   65%,
      rgba(10,6,0,0.97)   100%
    );
    box-shadow:
      0 0 30px rgba(245,166,35,0.55),
      0 0 80px rgba(245,166,35,0.20),
      inset 0 0 24px rgba(245,166,35,0.12);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 6px;
    animation: pulse 3s ease-in-out infinite;
    transition: transform 0.18s, box-shadow 0.18s;
    cursor: pointer;
    outline: none;
    overflow: hidden;
    padding: 0 12px;
  }}
  button.sphere::before {{
    content:'';
    position:absolute;
    top:11%; left:17%;
    width:35%; height:25%;
    background:radial-gradient(ellipse,rgba(255,255,255,0.30) 0%,transparent 70%);
    border-radius:50%;
    pointer-events:none;
  }}
  button.sphere:hover {{
    transform: scale(1.07);
    box-shadow:
      0 0 52px rgba(245,166,35,0.88),
      0 0 120px rgba(245,166,35,0.32),
      inset 0 0 36px rgba(245,166,35,0.24);
    animation: none;
  }}
  button.sphere:active {{ transform: scale(0.93); }}
  @keyframes pulse {{
    0%,100%{{box-shadow:0 0 30px rgba(245,166,35,0.55),0 0 80px rgba(245,166,35,0.20),inset 0 0 24px rgba(245,166,35,0.12);}}
    50%    {{box-shadow:0 0 50px rgba(245,166,35,0.82),0 0 115px rgba(245,166,35,0.30),inset 0 0 38px rgba(245,166,35,0.22);}}
  }}
  .bolt {{
    font-size:28px; line-height:1;
    filter:drop-shadow(0 0 7px rgba(245,166,35,0.95));
    pointer-events:none;
    display:block;
  }}
  .label {{
    font-size:10.5px; font-weight:900; letter-spacing:1.4px;
    text-transform:uppercase; color:#f5e6a0;
    text-align:center; line-height:1.4;
    text-shadow:0 0 10px rgba(245,166,35,0.8);
    font-family:Georgia,serif; pointer-events:none;
  }}
</style>
</head>
<body>

<!-- form con target="_parent" navega en la ventana principal, no en el iframe -->
<form method="GET" action="{base_url}" target="_parent">
  <input type="hidden" name="cm_go" value="1">
  <div class="scene">
    <canvas id="c" width="212" height="212"></canvas>
    <button type="submit" class="sphere">
      <span class="bolt">⚡</span>
      <span class="label">Ingresar<br>al repositorio</span>
    </button>
  </div>
</form>

<script>
(function(){{
  var ctx=document.getElementById('c').getContext('2d');
  var cx=106,cy=106,R=82,t=0;
  var rings=[
    {{tilt:0.50, speed:0.013, col:'rgba(245,166,35,', lw:1.5}},
    {{tilt:-0.58,speed:-0.010,col:'rgba(126,207,255,',lw:1.1}},
    {{tilt:1.15, speed:0.008, col:'rgba(245,166,35,', lw:0.8}},
    {{tilt:0.05, speed:0.016, col:'rgba(210,185,80,', lw:1.0}},
  ];
  var ph=[0,1.6,3.1,4.7];
  function ring(r,a){{
    var ry=R*Math.abs(Math.sin(r.tilt));
    ctx.beginPath();
    for(var i=0;i<=120;i++){{
      var th=(i/120)*Math.PI*2;
      var x3=R*Math.cos(th),y3=ry*Math.sin(th)*Math.cos(r.tilt);
      var xR=x3*Math.cos(a),zR=x3*Math.sin(a);
      var d=(zR/(R*1.5))*.5+.5;
      if(i===0){{ctx.moveTo(cx+xR,cy+y3);ctx.strokeStyle=r.col+(0.10+d*0.42)+')';}}
      else ctx.lineTo(cx+xR,cy+y3);
    }}
    ctx.lineWidth=r.lw;ctx.stroke();
  }}
  function dot(r,a,p){{
    var th=t*r.speed*0.9+p;
    var ry=R*Math.abs(Math.sin(r.tilt));
    var x3=R*Math.cos(th),y3=ry*Math.sin(th)*Math.cos(r.tilt);
    var xR=x3*Math.cos(a),zR=x3*Math.sin(a);
    var d=(zR/(R*1.5))*.5+.5;
    ctx.beginPath();ctx.arc(cx+xR,cy+y3,2+d*2.5,0,Math.PI*2);
    ctx.fillStyle=r.col+(0.35+d*0.65)+')';ctx.fill();
  }}
  function frame(){{
    ctx.clearRect(0,0,212,212);t++;
    rings.forEach(function(r,i){{var a=t*r.speed;ring(r,a);dot(r,a,ph[i]);}});
    requestAnimationFrame(frame);
  }}
  frame();
}})();
</script>
</body>
</html>"""


def mostrar_boton_esfera() -> bool:
    """
    Muestra la esfera giratoria. Retorna True cuando el usuario hace clic.
    El clic funciona via <form target="_parent"> — el método más confiable
    para comunicar un iframe con Streamlit sin restricciones cross-origin.
    """
    # Obtener la URL base actual (sin query params)
    try:
        # En Streamlit, la URL base se puede construir así:
        base_url = st.query_params.get("_base_url", "/")
        # Limpiar cualquier parámetro previo para tener URL limpia
        import urllib.parse
        # Usamos "/" que el form convertirá en la URL actual del padre
        base_url = ""   # form action="" = misma URL del padre
    except Exception:
        base_url = ""

    _, col, _ = st.columns([1, 1, 1])
    with col:
        components.html(_build_html(base_url), height=214, scrolling=False)

    # Detectar el query param que el form envió
    if st.query_params.get("cm_go") == "1":
        st.query_params.clear()
        return True

    return False
