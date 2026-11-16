/* Almonte Trading Group – site interactions (no dependencies) */
(function () {
  'use strict';
  document.documentElement.classList.remove('no-js');
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header shadow on scroll */
  const hdr = $('.hdr');
  const onScroll = () => hdr && hdr.classList.toggle('scrolled', window.scrollY > 10);
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  /* Mobile menu */
  const burger = $('.burger'), nav = $('.nav');
  if (burger && nav) {
    const close = () => { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); };
    burger.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', String(open));
    });
    $$('a', nav).forEach((a) => a.addEventListener('click', close));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  }

  /* Reveal on scroll */
  const rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    rv.forEach((el) => io.observe(el));
    // Fallback for fast jumps (anchor links, quick flings): reveal anything already at or above the viewport
    let tick = false;
    const sweep = () => { tick = false; const h = window.innerHeight; rv.forEach((el) => { if (!el.classList.contains('in') && el.getBoundingClientRect().top < h) el.classList.add('in'); }); };
    window.addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(sweep); } }, { passive: true });
    window.addEventListener('load', sweep);
  } else rv.forEach((el) => el.classList.add('in'));
  // Safety net: whatever the browser or viewer, never leave content hidden
  setTimeout(() => rv.forEach((el) => el.classList.add('in')), 2500);

  /* Animated counters: <strong data-count="2.5" data-prefix="$" data-suffix="M+"> */
  const counters = $$('[data-count]');
  const run = (el) => {
    const end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    const pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
    if (reduce) { el.innerHTML = pre + end.toFixed(dec) + suf; return; }
    const t0 = performance.now(), dur = 1600;
    const tick = (t) => {
      const p = Math.min(1, (t - t0) / dur), v = end * (1 - Math.pow(1 - p, 3));
      el.innerHTML = pre + v.toFixed(dec) + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { run(en.target); co.unobserve(en.target); }
    }), { threshold: 0.5 });
    counters.forEach((el) => co.observe(el));
  } else counters.forEach(run);

  /* Tabs with sliding indicator */
  $$('.tabs').forEach((tabs) => {
    const btns = $$('.tab-btn', tabs), ink = $('.tab-ink', tabs);
    const select = (btn, focus) => {
      btns.forEach((b) => {
        const on = b === btn;
        b.setAttribute('aria-selected', String(on)); b.tabIndex = on ? 0 : -1;
        const p = document.getElementById(b.getAttribute('aria-controls'));
        if (p) { p.hidden = !on; p.classList.toggle('show', on); }
      });
      if (ink) { ink.style.width = btn.offsetWidth + 'px'; ink.style.transform = `translateX(${btn.offsetLeft}px)`; }
      if (focus) btn.focus();
    };
    btns.forEach((b, i) => {
      b.addEventListener('click', () => select(b));
      b.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          e.preventDefault();
          select(btns[(i + (e.key === 'ArrowRight' ? 1 : btns.length - 1)) % btns.length], true);
        }
      });
    });
    const first = btns.find((b) => b.getAttribute('aria-selected') === 'true') || btns[0];
    select(first);
    window.addEventListener('resize', () => select(btns.find((b) => b.getAttribute('aria-selected') === 'true')));
  });

  /* Product category nav: highlight the section in view */
  const catLinks = $$('.cat-nav a');
  if (catLinks.length && 'IntersectionObserver' in window) {
    const so = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) catLinks.forEach((a) => a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id));
    }), { rootMargin: '-45% 0px -50% 0px' });
    $$('.cat').forEach((s) => so.observe(s));
  }

  /* Pre-select a service from ?service= */
  const params = new URLSearchParams(location.search);
  const pre = params.get('service');
  if (pre && $('#interest')) {
    const opt = $(`#interest option[value="${pre}"]`); if (opt) opt.selected = true;
  }

  /* Quote form – validates, then hands the request to WhatsApp / text (no business email supplied yet) */
  const form = $('#quote-form');
  if (form) {
    const S = window.SITE;
    const rules = {
      name: (v) => v.trim().length >= 2 || 'Please enter your name.',
      company: (v) => v.trim().length >= 2 || 'Please enter your company or organisation.',
      phone: (v) => { const d = v.replace(/\D/g, ''); return (d.length >= 10 && d.length <= 15) || 'Please enter a valid phone number, e.g. (787) 555-0123.'; },
      email: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Please enter a valid email address.',
      message: (v) => v.trim().length >= 10 || 'Please tell us a little about what you need (10+ characters).',
    };
    const check = (el) => {
      const r = rules[el.name]; if (!r) return true;
      const res = r(el.value), box = el.closest('.f'), err = box && $('.err', box);
      const ok = res === true;
      if (box) box.classList.toggle('bad', !ok);
      if (err) err.textContent = ok ? '' : res;
      el.setAttribute('aria-invalid', String(!ok));
      return ok;
    };
    Object.keys(rules).forEach((n) => {
      const el = form.elements[n]; if (!el) return;
      el.addEventListener('blur', () => check(el));
      el.addEventListener('input', () => { if (el.closest('.f').classList.contains('bad')) check(el); });
    });
    const status = $('.status', form);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (form.elements._hp.value) return;
      const ok = Object.keys(rules).map((n) => form.elements[n] ? check(form.elements[n]) : true);
      if (ok.includes(false)) {
        status.className = 'status bad'; status.textContent = 'Please fix the highlighted fields and try again.';
        const first = $('.f.bad input, .f.bad textarea', form); if (first) first.focus();
        return;
      }
      const d = new FormData(form);
      const cats = d.getAll('categories');
      const lines = [
        'Quote request – Almonte Trading Group website',
        `Name: ${d.get('name')}`, `Company: ${d.get('company')}`, `Buyer type: ${d.get('buyer') || '-'}`,
        `Phone: ${d.get('phone')}`, `Email: ${d.get('email')}`,
        `Interested in: ${d.get('interest') || '-'}`, `Categories: ${cats.length ? cats.join(', ') : '-'}`,
        '', d.get('message'),
      ];
      const text = encodeURIComponent(lines.join('\n'));
      const wa = `https://wa.me/${S.whatsapp}?text=${text}`;
      const sms = `sms:${S.phoneIntl}?&body=${text}`;
      window.open(wa, '_blank', 'noopener');
      const first = String(d.get('name')).trim().split(' ')[0].replace(/[<>&"]/g, '');
      status.className = 'status ok';
      status.innerHTML = `<strong>Thank you, ${first}!</strong> WhatsApp has opened with your quote request filled in. Just tap <strong>Send</strong>. Didn’t open? <a href="${wa}" target="_blank" rel="noopener">Open WhatsApp</a>, <a href="${sms}">send it as a text</a> or call <a href="${S.phoneHref}">${S.phone}</a>.`;
    });
  }

  /* Gallery filters + lightbox */
  const gBtns = $$('.g-filters button'), gItems = $$('.g-item');
  gBtns.forEach((b) => b.addEventListener('click', () => {
    gBtns.forEach((x) => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', String(x === b)); });
    gItems.forEach((it) => it.classList.toggle('hide', b.dataset.f !== 'all' && it.dataset.cat !== b.dataset.f));
  }));
  const lb = $('.lightbox');
  if (lb) {
    const closeLb = () => { lb.hidden = true; };
    gItems.forEach((it) => it.addEventListener('click', () => {
      $('img', lb).src = $('img', it).src; $('img', lb).alt = it.dataset.cap; $('figcaption', lb).textContent = it.dataset.cap; lb.hidden = false; $('.lb-x', lb).focus();
    }));
    $('.lb-x', lb).addEventListener('click', closeLb);
    lb.addEventListener('click', (e) => { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLb(); });
  }

  /* Year */
  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
