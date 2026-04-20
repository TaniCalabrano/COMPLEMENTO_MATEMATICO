"""
math_bg_component.py
Componente separado para la animación de ecuaciones flotantes.
Llamar con: inject_math_background()
"""
import streamlit.components.v1 as components

MATH_BG_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { background: transparent; overflow: hidden; width:100%; height:100%; }
  canvas { position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; }
</style>
</head>
<body>
<canvas id="c"></canvas>
<script>
(function(){
  var canvas = document.getElementById('c');
  // Place canvas in parent window if possible (iframe scenario)
  try {
    var parentDoc = window.parent.document;
    var existing = parentDoc.getElementById('cm-math-canvas');
    if (existing) existing.remove();
    canvas = parentDoc.createElement('canvas');
    canvas.id = 'cm-math-canvas';
    canvas.style.cssText = [
      'position:fixed','top:0','left:0',
      'width:100vw','height:100vh',
      'pointer-events:none','z-index:0',
      'opacity:1'
    ].join(';');
    parentDoc.body.appendChild(canvas);
  } catch(e) {
    // fallback: use iframe canvas
    canvas.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0;';
    document.body.appendChild(canvas);
  }

  var ctx = canvas.getContext('2d');

  var EXPRS = [
    'ax² + bx + c = 0',
    '∫f(x)dx',
    'E = mc²',
    'sen²θ + cos²θ = 1',
    'Δx = v₀t + ½at²',
    'F = ma',
    'y = mx + b',
    'π ≈ 3.14159',
    '√(a²+b²) = c',
    'P(A∪B) = P(A)+P(B)−P(A∩B)',
    'lím x→∞',
    'Σᵢ₌₁ⁿ i = n(n+1)/2',
    'log(ab) = loga + logb',
    'd/dx[xⁿ] = nxⁿ⁻¹',
    'V = πr²h',
    'σ² = Σ(xᵢ−μ)²/N',
    'eⁱᵖⁱ + 1 = 0',
    'A = ½bh',
    'v = λf',
    'Q = mcΔT',
    'p = mv',
    'W = Fd·cosθ',
    'x = (−b ± √Δ) / 2a',
    'f(x) = aˣ',
    'tanθ = senθ/cosθ',
    '∇²φ = 0',
    'PV = nRT',
    'Δt = t₁ − t₀',
    'a² = b² + c²',
    'n! = n·(n-1)!',
  ];

  var particles = [];

  function resize() {
    canvas.width  = (canvas.ownerDocument.defaultView || window).innerWidth;
    canvas.height = (canvas.ownerDocument.defaultView || window).innerHeight;
  }

  try { window.parent.addEventListener('resize', resize); } catch(e) {}
  window.addEventListener('resize', resize);
  resize();

  function randomBetween(a, b) { return a + Math.random() * (b - a); }

  function spawnParticle() {
    var fontSize = randomBetween(11, 20);
    return {
      text:    EXPRS[Math.floor(Math.random() * EXPRS.length)],
      x:       randomBetween(0, canvas.width),
      y:       canvas.height + randomBetween(0, 80),
      vy:      randomBetween(0.35, 0.9),      // pixels per frame upward
      alpha:   randomBetween(0.06, 0.18),
      fontSize: fontSize,
      rotation: randomBetween(-0.15, 0.15),
      color:   Math.random() < 0.65 ? '#f5a623' : '#7ecfff',
    };
  }

  // Initial burst
  for (var i = 0; i < 28; i++) {
    var p = spawnParticle();
    p.y = randomBetween(0, canvas.height); // scatter vertically on init
    particles.push(p);
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Spawn new ones steadily
    if (Math.random() < 0.045) particles.push(spawnParticle());

    for (var i = particles.length - 1; i >= 0; i--) {
      var p = particles[i];
      p.y -= p.vy;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle   = p.color;
      ctx.font        = 'italic ' + p.fontSize + 'px Georgia, serif';
      ctx.fillText(p.text, 0, 0);
      ctx.restore();

      // Remove if off screen
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

def inject_math_background():
    """Inyecta el canvas de ecuaciones flotantes en la página de Streamlit."""
    components.html(MATH_BG_HTML, height=0, scrolling=False)
