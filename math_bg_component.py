"""
math_bg_component.py
Animación de ecuaciones flotando de abajo hacia arriba.
Solo debe llamarse en la pantalla de bienvenida.
Usa components.html() para garantizar ejecución de JS.
"""
import streamlit.components.v1 as components

MATH_BG_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { background:transparent; overflow:hidden; width:100%; height:1px; }
</style>
</head>
<body>
<script>
(function(){
  // Inject canvas into the parent Streamlit document
  var parentDoc = window.parent ? window.parent.document : document;
  var win       = window.parent ? window.parent : window;

  // Remove existing canvas if any
  var existing = parentDoc.getElementById('cm-math-canvas');
  if (existing) existing.remove();

  var canvas = parentDoc.createElement('canvas');
  canvas.id = 'cm-math-canvas';
  canvas.style.cssText = [
    'position:fixed',
    'top:0',
    'left:0',
    'width:100vw',
    'height:100vh',
    'pointer-events:none',
    'z-index:0',
  ].join(';');
  parentDoc.body.appendChild(canvas);

  var ctx = canvas.getContext('2d');

  var EXPRS = [
    'ax² + bx + c = 0',  '∫f(x)dx',           'E = mc²',
    'sen²θ + cos²θ = 1', 'Δx = v₀t + ½at²',   'F = ma',
    'y = mx + b',         'π ≈ 3.14159',         '√(a²+b²) = c',
    'P(A∪B) = P(A)+P(B)', 'lím x→∞',            'Σi = n(n+1)/2',
    'log(ab) = loga+logb','d/dx[xⁿ] = nxⁿ⁻¹',  'V = πr²h',
    'eⁱᵖⁱ + 1 = 0',      'A = ½bh',             'v = λf',
    'p = mv',              'W = Fd·cosθ',          'tanθ = s/c',
    'x = (−b±√Δ)/2a',    'σ² = Σ(xᵢ−μ)²/N',    'PV = nRT',
    '∇²φ = 0',             'n! = n·(n−1)!',       'a²=b²+c²',
  ];

  var particles = [];

  function getSize() {
    return { w: win.innerWidth, h: win.innerHeight };
  }

  function resize() {
    var s = getSize();
    canvas.width  = s.w;
    canvas.height = s.h;
  }
  win.addEventListener('resize', resize);
  resize();

  function rand(a, b) { return a + Math.random() * (b - a); }

  function spawn() {
    var s = getSize();
    return {
      text:     EXPRS[Math.floor(Math.random() * EXPRS.length)],
      x:        rand(0, s.w),
      y:        s.h + rand(0, 60),
      vy:       rand(0.30, 0.80),
      alpha:    rand(0.06, 0.17),
      fontSize: rand(11, 19),
      rot:      rand(-0.12, 0.12),
      color:    Math.random() < 0.65 ? '#f5a623' : '#7ecfff',
    };
  }

  // Initial scatter across full screen
  var s0 = getSize();
  for (var i = 0; i < 30; i++) {
    var p = spawn();
    p.y = rand(0, s0.h);
    particles.push(p);
  }

  function animate() {
    var s = getSize();
    ctx.clearRect(0, 0, s.w, s.h);

    if (Math.random() < 0.05) particles.push(spawn());

    for (var i = particles.length - 1; i >= 0; i--) {
      var p = particles[i];
      p.y -= p.vy;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot);
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle   = p.color;
      ctx.font        = 'italic ' + p.fontSize + 'px Georgia, serif';
      ctx.fillText(p.text, 0, 0);
      ctx.restore();

      if (p.y < -40) particles.splice(i, 1);
    }

    requestAnimationFrame(animate);
  }

  animate();
})();
</script>
</body>
</html>
"""

MATH_BG_REMOVE_HTML = """
<!DOCTYPE html>
<html><head><style>*{margin:0;padding:0;}html,body{background:transparent;height:1px;overflow:hidden;}</style></head>
<body>
<script>
(function(){
  var parentDoc = window.parent ? window.parent.document : document;
  var el = parentDoc.getElementById('cm-math-canvas');
  if (el) el.remove();
})();
</script>
</body>
</html>
"""

def inject_math_background():
    """Inyecta el canvas animado en la página. Llamar solo en la pantalla de bienvenida."""
    components.html(MATH_BG_HTML, height=0, scrolling=False)

def remove_math_background():
    """Elimina el canvas animado. Llamar al entrar al repositorio."""
    components.html(MATH_BG_REMOVE_HTML, height=0, scrolling=False)
