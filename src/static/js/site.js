/* SHE: soft, grounding motion. Reveal on scroll, gentle parallax, a slow warm light, a 3D tilt for the journals. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Mobile menu
  var burger = document.querySelector('.burger'), mnav = document.querySelector('.mnav');
  if (burger && mnav) burger.addEventListener('click', function () { mnav.classList.toggle('open'); burger.classList.toggle('x'); });
  // Reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  document.querySelectorAll('.rv, .lines').forEach(function (el) { io.observe(el); });
  if (reduce) return;
  // Gentle parallax on tagged photographs
  var pls = Array.prototype.slice.call(document.querySelectorAll('.ph.parallax img'));
  function parallax() {
    var vh = window.innerHeight;
    pls.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var t = (r.top + r.height / 2 - vh / 2) / vh; // -1 .. 1
      img.style.transform = 'scale(1.08) translateY(' + (t * -18).toFixed(2) + 'px)';
    });
  }
  window.addEventListener('scroll', function () { window.requestAnimationFrame(parallax); }, { passive: true });
  parallax();
  // Cursor light (desktop only)
  if (window.matchMedia('(pointer: fine)').matches) {
    var glow = document.createElement('div'); glow.className = 'cursor-glow'; document.body.appendChild(glow);
    var gx = 0, gy = 0, tx = 0, ty = 0;
    window.addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; glow.style.opacity = 1; });
    (function loop() { gx += (tx - gx) * .08; gy += (ty - gy) * .08; glow.style.left = gx + 'px'; glow.style.top = gy + 'px'; requestAnimationFrame(loop); })();
  }
  // 3D tilt on journals
  document.querySelectorAll('.tilt').forEach(function (el) {
    el.addEventListener('mousemove', function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
      el.style.transform = 'perspective(1100px) rotateY(' + (x * 10).toFixed(2) + 'deg) rotateX(' + (-y * 8).toFixed(2) + 'deg)';
    });
    el.addEventListener('mouseleave', function () { el.style.transform = 'perspective(1100px) rotateY(0) rotateX(0)'; });
  });
  // The light: a slow, warm 3D orb behind hero text (Three.js, only where a .orb canvas is requested)
  var orbs = document.querySelectorAll('canvas.orb');
  if (!orbs.length || !window.THREE) return;
  orbs.forEach(function (original) {
    // Swap in a fresh canvas: anything that already asked this one for a 2D context
    // would stop WebGL from starting.
    var canvas = original.cloneNode(false);
    original.parentNode.replaceChild(canvas, original);
    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    } catch (e) {
      canvas.style.display = 'none';
      return;
    }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
    var scene = new THREE.Scene();
    var cam = new THREE.PerspectiveCamera(32, 1, .1, 100); cam.position.z = 6;
    var uniforms = { t: { value: 0 } };
    var mat = new THREE.ShaderMaterial({
      transparent: true, uniforms: uniforms,
      vertexShader: 'varying vec3 vN; varying vec3 vP; uniform float t; void main(){ vN = normal; vec3 p = position + normal * (0.06*sin(position.y*3.0 + t*0.6) + 0.04*sin(position.x*4.0 - t*0.4)); vP = p; gl_Position = projectionMatrix * modelViewMatrix * vec4(p,1.0); }',
      fragmentShader: 'varying vec3 vN; varying vec3 vP; uniform float t; void main(){ float l = dot(normalize(vN), normalize(vec3(0.6,0.8,1.0)))*0.5+0.5; vec3 warm = vec3(0.98,0.86,0.72); vec3 rose = vec3(0.90,0.72,0.66); vec3 c = mix(rose, warm, l); float edge = pow(1.0 - abs(dot(normalize(vN), vec3(0.0,0.0,1.0))), 2.2); float a = 0.55*(1.0-edge) + 0.15; gl_FragColor = vec4(c, a*0.75); }'
    });
    var mesh = new THREE.Mesh(new THREE.SphereGeometry(1.7, 96, 96), mat); scene.add(mesh);
    var ring = new THREE.Mesh(new THREE.TorusGeometry(2.5, .012, 8, 200), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .35 }));
    ring.rotation.x = 1.2; scene.add(ring);
    function size() { var r = canvas.parentElement.getBoundingClientRect(); renderer.setSize(r.width, r.height, false); cam.aspect = r.width / r.height; cam.updateProjectionMatrix(); }
    window.addEventListener('resize', size); size();
    var mx = 0, my = 0; window.addEventListener('mousemove', function (e) { mx = e.clientX / window.innerWidth - .5; my = e.clientY / window.innerHeight - .5; });
    (function frame(ts) {
      uniforms.t.value = ts / 1000; mesh.rotation.y = ts / 9000; mesh.rotation.x = Math.sin(ts / 7000) * .2;
      mesh.position.x += ((mx * .5) - mesh.position.x) * .02; mesh.position.y += ((-my * .3) - mesh.position.y) * .02;
      ring.rotation.z = ts / 20000; renderer.render(scene, cam); requestAnimationFrame(frame);
    })(0);
  });
})();
