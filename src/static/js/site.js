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

  // A thin line across the top while the next page is on its way. Pages with large photographs
  // can take a moment, and nothing on screen said anything was happening.
  var bar = null, barTimer = 0;
  function showBar() {
    if (bar) return;
    bar = document.createElement('div');
    bar.className = 'loadbar';
    document.body.appendChild(bar);
    requestAnimationFrame(function () { if (bar) bar.classList.add('go'); });
  }
  function hideBar() {
    clearTimeout(barTimer);
    if (!bar) return;
    var going = bar; bar = null;
    going.classList.add('done');
    setTimeout(function () { going.remove(); }, 400);
  }
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.target === '_blank' || a.hasAttribute('download')) return;
    var url;
    try { url = new URL(a.href, location.href); } catch (err) { return; }
    if (url.origin !== location.origin || url.href === location.href) return;
    if (url.pathname === location.pathname && url.hash) return;   // same page, just a jump
    barTimer = setTimeout(showBar, 180);                          // a quick page never flickers one
  }, { capture: true });
  window.addEventListener('pagehide', hideBar);
  window.addEventListener('pageshow', hideBar);                   // coming back with the back button

  // The sign-up forms: the list is ours, so the page itself says thank you and nobody is sent
  // off to another site. Used by Join SHE and by the register-your-interest pages.
  document.querySelectorAll('form[data-signup]').forEach(function (f) {
    if (!f.action || f.action.indexOf('http') !== 0) return;
    var btn = f.querySelector('button'), msg = f.querySelector('.msg'), label = btn ? btn.textContent : '';
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      btn.disabled = true; btn.textContent = f.getAttribute('data-busy') || 'One moment...';
      fetch(f.action, { method: 'POST', body: new FormData(f), mode: 'cors' })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
        .then(function (res) {
          var d = res.d;
          // Only a reply that says ok: true counts. A server that is down or answers with an error never shows "thank you".
          if (!res.ok || !d || d.ok !== true) {
            btn.disabled = false; btn.textContent = label;
            if (msg) msg.textContent = (d && d.message) || 'That did not go through. Please try again.';
            return;
          }
          var field = f.querySelector('input[name=name]');
          var first = ((field && field.value) || '').trim().split(' ')[0].replace(/[<>&]/g, '');
          var thanks = document.createElement('div');
          thanks.className = 'thanks';
          thanks.setAttribute('role', 'status');
          thanks.innerHTML = '<p class="k">' + (f.getAttribute('data-title') || 'Thank you') + '</p>' +
            '<p class="serif-lede">Thank you' + (first ? ', ' + first : '') + '.</p>' +
            '<p class="muted">' + (f.getAttribute('data-note') || '') + '</p>';
          f.replaceWith(thanks);
        })
        .catch(function () {
          btn.disabled = false; btn.textContent = label;
          if (msg) msg.textContent = 'Something went wrong just now. Please try again in a moment.';
        });
    });
  });

  // SHE + ME pop-up: opens from the card, closes with the x, the backdrop or Escape. Without scripts the
  // link's #target opens it, so the form is still reachable.
  (function () {
    var m = document.getElementById('sheme-form');
    if (!m) return;
    var opener = null;
    function open(e) { if (e) e.preventDefault(); opener = document.activeElement; m.classList.add('open'); document.body.classList.add('modal-open'); var f = m.querySelector('input,iframe,button'); if (f) setTimeout(function () { f.focus(); }, 30); }
    function close(e) { if (e) e.preventDefault(); m.classList.remove('open'); document.body.classList.remove('modal-open'); if (history.replaceState && location.hash === '#sheme-form') history.replaceState(null, '', location.pathname + location.search); if (opener && opener.focus) opener.focus(); }
    document.querySelectorAll('[data-open="sheme"]').forEach(function (a) { a.addEventListener('click', open); });
    m.querySelectorAll('[data-close]').forEach(function (a) { a.addEventListener('click', close); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && m.classList.contains('open')) close(); });
    if (location.hash === '#sheme-form') m.classList.add('open');
  })();

  // Coffee Conversations booking: location, then date, then First Visit or Returning Guest, then the one
  // matching Beacons checkout. Nothing navigates by itself: only the Book Your Place button leaves the page.
  (function () {
    var root = document.querySelector('[data-ccb]');
    if (!root) return;
    var data;
    try { data = JSON.parse(document.getElementById('ccb-data').textContent); } catch (e) { return; }
    var loc = root.querySelector('#ccb-loc'), datesBox = root.querySelector('#ccb-dates'), list = root.querySelector('#ccb-datelist'),
        empty = root.querySelector('#ccb-empty'), typesBox = root.querySelector('#ccb-types'), btn = root.querySelector('#ccb-book'),
        hint = root.querySelector('#ccb-hint');
    var state = { sid: '', type: '' };
    function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
    function typeName(k) { for (var i = 0; i < data.types.length; i++) if (data.types[i][0] === k) return data.types[i][1]; return ''; }
    function session() { for (var i = 0; i < data.sessions.length; i++) if (data.sessions[i].id === state.sid) return data.sessions[i]; return null; }
    function off(msg) { btn.classList.add('is-off'); btn.setAttribute('aria-disabled', 'true'); btn.setAttribute('tabindex', '-1'); btn.removeAttribute('href'); hint.textContent = msg; }
    function refresh() {
      var s = session();
      if (!loc.value || !s || !state.type) { off(data.hint); return; }
      var url = s[state.type];
      if (!url) { off(data.closed); return; }
      btn.href = url; btn.classList.remove('is-off'); btn.setAttribute('aria-disabled', 'false'); btn.removeAttribute('tabindex');
      hint.textContent = typeName(state.type) + ': ' + s.venue + ', ' + s.dow + ' ' + s.day + ' ' + s.mon + '. The checkout opens in a new tab.';
    }
    function pickDate(id) { state.sid = id; typesBox.hidden = false; refresh(); }
    function renderDates() {
      list.innerHTML = ''; state.sid = ''; state.type = '';
      typesBox.hidden = true;
      typesBox.querySelectorAll('input').forEach(function (i) { i.checked = false; });
      var rows = data.sessions.filter(function (s) { return s.loc === loc.value; });
      datesBox.hidden = !loc.value; empty.hidden = !loc.value || rows.length > 0;
      rows.forEach(function (s) {
        var lab = el('label', 'ccb-opt'), inp = el('input'), box = el('span');
        inp.type = 'radio'; inp.name = 'ccb-date'; inp.value = s.id;
        var dt = el('span', 'ccb-dt'); dt.appendChild(el('b', '', String(s.day))); dt.appendChild(el('small', '', s.mon.slice(0, 3)));
        var tx = el('span', 'ccb-dtx'); tx.appendChild(el('strong', '', s.dow + ' ' + s.day + ' ' + s.mon)); tx.appendChild(el('em', '', s.time)); tx.appendChild(el('em', '', s.venue));
        box.appendChild(dt); box.appendChild(tx); lab.appendChild(inp); lab.appendChild(box); list.appendChild(lab);
        inp.addEventListener('change', function () { pickDate(s.id); });
      });
      refresh();
    }
    loc.addEventListener('change', renderDates);
    typesBox.querySelectorAll('input').forEach(function (i) { i.addEventListener('change', function () { state.type = i.value; refresh(); }); });
    btn.addEventListener('click', function (e) { if (btn.getAttribute('aria-disabled') === 'true' || !btn.getAttribute('href')) e.preventDefault(); });
    btn.addEventListener('keydown', function (e) { if ((e.key === ' ' || e.key === 'Spacebar') && btn.getAttribute('href')) { e.preventDefault(); btn.click(); } });
    off(data.hint);
  })();

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
