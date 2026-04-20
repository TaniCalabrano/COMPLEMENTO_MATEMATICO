"""
sphere_button_component.py

Solución simple y confiable:
  1. Esfera animada en components.html() — solo visual, fondo #0f1117
  2. st.button estilizado debajo — funciona siempre en Streamlit
  Sin superposiciones, sin declare_component, sin query params.
"""
import streamlit as st
import streamlit.components.v1 as components


SPHERE_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body {
    background: #0f1117;
    overflow: hidden;
    width: 100%;
    height: 190px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .scene {
    position: relative;
    width: 190px; height: 190px;
    display: flex; align-items: center; justify-content: center;
  }
  canvas { position:absolute; top:0; left:0; width:190px; height:190px; pointer-events:none; }
  .sphere {
    position:relative; z-index:10;
    width:140px; height:140px; border-radius:50%;
    border:2px solid rgba(245,166,35,0.85);
    background:radial-gradient(circle at 33% 30%,
      rgba(255,255,255,.22) 0%, rgba(245,166,35,.20) 22%,
      rgba(40,25,0,.92) 65%, rgba(10,6,0,.97) 100%);
    box-shadow:0 0 30px rgba(245,166,35,.55),0 0 80px rgba(245,166,35,.20),
               inset 0 0 24px rgba(245,166,35,.12);
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; gap:5px;
    animation:pulse 3s ease-in-out infinite;
    user-select:none; pointer-events:none;
  }
  .sphere::before {
    content:''; position:absolute; top:11%; left:17%;
    width:35%; height:25%;
    background:radial-gradient(ellipse,rgba(255,255,255,.30) 0%,transparent 70%);
    border-radius:50%; pointer-events:none;
  }
  @keyframes pulse {
    0%,100%{box-shadow:0 0 30px rgba(245,166,35,.55),0 0 80px rgba(245,166,35,.20),inset 0 0 24px rgba(245,166,35,.12);}
    50%    {box-shadow:0 0 50px rgba(245,166,35,.82),0 0 115px rgba(245,166,35,.30),inset 0 0 38px rgba(245,166,35,.22);}
  }
  .bolt  { font-size:26px; line-height:1; filter:drop-shadow(0 0 6px rgba(245,166,35,.95)); display:block; }
  .label { font-size:9.5px; font-weight:900; letter-spacing:1.3px; text-transform:uppercase;
           color:#f5e6a0; text-align:center; line-height:1.4;
           text-shadow:0 0 9px rgba(245,166,35,.8); font-family:Georgia,serif; padding:0 8px; }
</style>
</head>
<body>
<div class="scene">
  <canvas id="c" width="190" height="190"></canvas>
  <div class="sphere">
    <span class="bolt">⚡</span>
    <span class="label">Ingresar<br>al repositorio</span>
  </div>
</div>
<script>
(function(){
  var ctx=document.getElementById('c').getContext('2d');
  var cx=95,cy=95,R=75,t=0;
  var rings=[
    {tilt:0.50,speed:0.013,col:'rgba(245,166,35,',lw:1.5},
    {tilt:-0.58,speed:-0.010,col:'rgba(126,207,255,',lw:1.1},
    {tilt:1.15,speed:0.008,col:'rgba(245,166,35,',lw:0.8},
    {tilt:0.05,speed:0.016,col:'rgba(210,185,80,',lw:1.0},
  ];
  var ph=[0,1.6,3.1,4.7];
  function ring(r,a){
    var ry=R*Math.abs(Math.sin(r.tilt));
    ctx.beginPath();
    for(var i=0;i<=120;i++){
      var th=(i/120)*Math.PI*2;
      var x3=R*Math.cos(th),y3=ry*Math.sin(th)*Math.cos(r.tilt);
      var xR=x3*Math.cos(a),zR=x3*Math.sin(a);
      var d=(zR/(R*1.5))*.5+.5;
      if(i===0){ctx.moveTo(cx+xR,cy+y3);ctx.strokeStyle=r.col+(0.10+d*0.42)+')';}
      else ctx.lineTo(cx+xR,cy+y3);
    }
    ctx.lineWidth=r.lw;ctx.stroke();
  }
  function dot(r,a,p){
    var th=t*r.speed*0.9+p;
    var ry=R*Math.abs(Math.sin(r.tilt));
    var x3=R*Math.cos(th),y3=ry*Math.sin(th)*Math.cos(r.tilt);
    var xR=x3*Math.cos(a),zR=x3*Math.sin(a);
    var d=(zR/(R*1.5))*.5+.5;
    ctx.beginPath();ctx.arc(cx+xR,cy+y3,2+d*2.3,0,Math.PI*2);
    ctx.fillStyle=r.col+(0.35+d*0.65)+')';ctx.fill();
  }
  function frame(){
    ctx.clearRect(0,0,190,190);t++;
    rings.forEach(function(r,i){var a=t*r.speed;ring(r,a);dot(r,a,ph[i]);});
    requestAnimationFrame(frame);
  }
  frame();
})();
</script>
</body>
</html>"""


def mostrar_boton_esfera() -> bool:
    """
    Esfera animada + botón estilizado de Streamlit.
    Simple, sin trucos, funciona siempre.
    """
    st.markdown("""
    <style>
    /* Botón de ingreso estilizado */
    div[data-testid="stButton"].btn-ingresar > button {
        background: linear-gradient(135deg, #3a1e00, #7a3d00, #c06500) !important;
        color: #fff8e0 !important;
        border: 2px solid rgba(245,166,35,0.8) !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 900 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        padding: 0.6rem 1.5rem !important;
        box-shadow: 0 0 20px rgba(245,166,35,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.2s !important;
        font-family: Georgia, serif !important;
    }
    div[data-testid="stButton"].btn-ingresar > button:hover {
        background: linear-gradient(135deg, #7a3d00, #c06500, #f5a623) !important;
        color: #1a0800 !important;
        box-shadow: 0 0 35px rgba(245,166,35,0.65), 0 4px 20px rgba(0,0,0,0.5) !important;
        transform: scale(1.03) !important;
    }
    div[data-testid="stButton"].btn-ingresar > button:active {
        transform: scale(0.97) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Esfera animada centrada
    _, col, _ = st.columns([1, 1, 1])
    with col:
        components.html(SPHERE_HTML, height=192, scrolling=False)

    # Botón real de Streamlit, centrado bajo la esfera
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="btn-ingresar">', unsafe_allow_html=True)
        clicked = st.button("⚡  Ingresar con el boton de abajo", key="btn_esfera_ingreso", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    return clicked
