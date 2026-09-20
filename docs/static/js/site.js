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

  // Moving between pages. When a finger touches a link, or a pointer rests on one, fetch that
  // page quietly in the background so it is already here when she taps. Only our own pages,
  // once each, and never when the phone is on a slow connection or saving data.
  var link = navigator.connection || {};
  var thrifty = link.saveData === true || /(^|-)2g$/.test(link.effectiveType || '');
  if (!thrifty) {
    var asked = {}, budget = 10;
    var probe = document.createElement('link');
    var hints = probe.relList && probe.relList.supports && probe.relList.supports('prefetch');
    var warm = function (event) {
      var a = event.target && event.target.closest ? event.target.closest('a[href]') : null;
      if (!a || budget < 1 || a.hasAttribute('download') || a.target === '_blank') return;
      var url;
      try { url = new URL(a.href, location.href); } catch (e) { return; }
      if (url.origin !== location.origin) return;
      if (url.pathname === location.pathname || asked[url.pathname]) return;
      asked[url.pathname] = true; budget--;
      var href = url.pathname + url.search;
      if (hints) {
        var hint = document.createElement('link');
        hint.rel = 'prefetch'; hint.as = 'document'; hint.href = href;
        document.head.appendChild(hint);
      } else if (window.fetch) {
        // Safari has no prefetch hint. Asking for the page quietly puts it in the browser's
        // own cache, which the next tap then reads instead of the network.
        try { fetch(href, { credentials: 'same-origin', priority: 'low' }); } catch (e) { }
      }
    };
    ['pointerover', 'pointerenter', 'touchstart', 'focusin'].forEach(function (name) {
      document.addEventListener(name, warm, { capture: true, passive: true });
    });
  }

  if (reduce) return;
  // Gentle parallax on tagged photographs. Only the pictures actually on screen are measured,
  // so scrolling a long page on a phone stays smooth.
  var pls = Array.prototype.slice.call(document.querySelectorAll('.ph.parallax img'));
  var onScreen = [];
  var watcher = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var img = e.target.querySelector('img');
      var at = onScreen.indexOf(img);
      if (e.isIntersecting && at < 0) onScreen.push(img);
      else if (!e.isIntersecting && at > -1) onScreen.splice(at, 1);
    });
    parallax();
  }, { rootMargin: '10% 0px' });
  pls.forEach(function (img) { watcher.observe(img.parentElement); });
  var ticking = false;
  function parallax() {
    ticking = false;
    var vh = window.innerHeight;
    onScreen.forEach(function (img) {
      var r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var t = (r.top + r.height / 2 - vh / 2) / vh; // -1 .. 1
      img.style.transform = 'scale(1.08) translateY(' + (t * -18).toFixed(2) + 'px)';
    });
  }
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(parallax);
  }, { passive: true });
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
  // The light: a slow, warm 3D orb behind hero text. The library it needs is large and comes
  // from another site, so it is fetched only on a wide screen with a mouse, only when the page
  // is already usable, and never on a phone or on a thrifty connection.
  var orbs = document.querySelectorAll('canvas.orb');
  if (orbs.length && !thrifty && window.matchMedia('(min-width:1000px) and (pointer:fine)').matches) {
    var start = function () {
      var script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js';
      script.async = true;
      script.onload = function () { if (window.THREE) lightOrbs(orbs); };
      document.head.appendChild(script);
    };
    var later = function () {
      if (window.requestIdleCallback) requestIdleCallback(start, { timeout: 2500 });
      else setTimeout(start, 1200);
    };
    if (document.readyState === 'complete') later();
    else window.addEventListener('load', later);
  }

  function lightOrbs(orbs) {
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
  }
})();
