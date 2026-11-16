/* Almonte Trading Group – scripted chat assistant (no AI service, no dependencies).
   Answers common buyer questions and collects quote requests, which are handed to WhatsApp / text. */
(function () {
  'use strict';
  const S = window.SITE;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const css = `
  .ac-btn{position:fixed;right:18px;bottom:18px;z-index:70;display:flex;align-items:center;gap:10px;padding:10px 18px 10px 10px;border:0;border-radius:999px;background:#0b1f3a;color:#fff;font:700 .95rem Manrope,system-ui,sans-serif;cursor:pointer;box-shadow:0 18px 40px -14px rgba(11,31,58,.6);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
  .ac-btn:hover{transform:translateY(-3px)}
  .ac-btn i{width:38px;height:38px;border-radius:50%;background:#f2a900;color:#0b1f3a;display:grid;place-items:center}
  .ac-btn svg{width:20px;height:20px}
  .ac-panel{position:fixed;right:18px;bottom:86px;z-index:71;width:min(380px,calc(100vw - 36px));height:min(560px,calc(100vh - 120px));background:#fff;border-radius:22px;box-shadow:0 30px 70px -20px rgba(11,31,58,.45);display:flex;flex-direction:column;overflow:hidden;transform:translateY(16px) scale(.97);opacity:0;pointer-events:none;transition:all .35s cubic-bezier(.2,.7,.2,1);border:1px solid #e2e8f0}
  .ac-panel.open{transform:none;opacity:1;pointer-events:auto}
  .ac-head{background:#0b1f3a;color:#fff;padding:16px 18px;display:flex;align-items:center;gap:12px}
  .ac-head b{display:block;font:800 1rem Manrope,system-ui,sans-serif;letter-spacing:.04em}
  .ac-head small{color:#9fb2cb;font-size:.78rem}
  .ac-head .x{margin-left:auto;background:rgba(255,255,255,.1);border:0;color:#fff;width:34px;height:34px;border-radius:50%;cursor:pointer;font-size:1.1rem}
  .ac-body{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:#f5f7fb}
  .ac-m{max-width:86%;padding:10px 14px;border-radius:16px;font-size:.93rem;line-height:1.5;white-space:pre-line;animation:acIn .35s ease both}
  .ac-m a{color:#18375f;font-weight:700;text-decoration:underline}
  .ac-bot{background:#fff;border:1px solid #e2e8f0;border-bottom-left-radius:4px;color:#2b3a4f}
  .ac-me{align-self:flex-end;background:#0b1f3a;color:#fff;border-bottom-right-radius:4px}
  .ac-chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 16px 10px;background:#f5f7fb}
  .ac-chips button{border:1.5px solid #0b1f3a;background:#fff;color:#0b1f3a;border-radius:999px;padding:6px 12px;font:600 .82rem Inter,system-ui,sans-serif;cursor:pointer;transition:all .25s}
  .ac-chips button:hover{background:#0b1f3a;color:#fff}
  .ac-form{display:flex;gap:8px;padding:12px;border-top:1px solid #e2e8f0;background:#fff}
  .ac-form input{flex:1;min-width:0;border:1.5px solid #e2e8f0;border-radius:999px;padding:10px 14px;font:inherit;font-size:.93rem}
  .ac-form input:focus{outline:none;border-color:#18375f}
  .ac-form button{width:42px;height:42px;border-radius:50%;border:0;background:#f2a900;color:#0b1f3a;cursor:pointer;display:grid;place-items:center}
  .ac-form svg{width:18px;height:18px}
  .ac-typing{display:inline-flex;gap:4px}.ac-typing span{width:6px;height:6px;border-radius:50%;background:#9fb2cb;animation:acDot 1s infinite}.ac-typing span:nth-child(2){animation-delay:.15s}.ac-typing span:nth-child(3){animation-delay:.3s}
  @keyframes acIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
  @keyframes acDot{0%,80%,100%{opacity:.3}40%{opacity:1}}
  @media (max-width:640px){.ac-btn span{display:none}.ac-btn{padding:8px}}
  @media (prefers-reduced-motion:reduce){.ac-m,.ac-panel{animation:none;transition:none}}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const chatIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';
  const sendIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4z"/></svg>';
  const root = document.createElement('div');
  root.innerHTML = `
  <button class="ac-btn" aria-expanded="false" aria-controls="ac-panel"><i>${chatIcon}</i><span>Ask about supply</span></button>
  <section class="ac-panel" id="ac-panel" role="dialog" aria-label="Chat with Almonte Trading Group">
    <div class="ac-head"><div><b>ALMONTE TRADING</b><small>Automated assistant · set answers</small></div><button class="x" aria-label="Close chat">✕</button></div>
    <div class="ac-body" aria-live="polite"></div>
    <div class="ac-chips"></div>
    <form class="ac-form"><label class="sr-only" for="ac-in">Type your message</label><input id="ac-in" autocomplete="off" placeholder="Type your question…" maxlength="400"><button aria-label="Send">${sendIcon}</button></form>
  </section>`;
  document.body.appendChild(root);
  const btn = root.querySelector('.ac-btn'), panel = root.querySelector('.ac-panel'), body = root.querySelector('.ac-body'),
    chipBox = root.querySelector('.ac-chips'), form = root.querySelector('.ac-form'), input = root.querySelector('#ac-in');
  const BASE = window.SITE_BASE || '';
  let started = false, busy = false, lead = null;

  const add = (html, who = 'bot') => { const m = document.createElement('div'); m.className = 'ac-m ac-' + who; m.innerHTML = html; body.appendChild(m); body.scrollTop = body.scrollHeight; return m; };
  const say = (html, wait = 450) => new Promise((res) => {
    const t = add('<span class="ac-typing"><span></span><span></span><span></span></span>');
    setTimeout(() => { t.innerHTML = html; body.scrollTop = body.scrollHeight; res(); }, wait);
  });
  const chips = (list) => { chipBox.innerHTML = ''; list.forEach((c) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = c; b.onclick = () => handle(c); chipBox.appendChild(b); }); };
  const MAIN = ['Products', 'Government supply', 'Request a quote', 'Contact'];
  const contact = () => `📞 <a href="${S.phoneHref}">${S.phone}</a>\n💬 <a href="https://wa.me/${S.whatsapp}" target="_blank" rel="noopener">WhatsApp</a>\n📍 ${esc(S.city)}`;

  const intents = [
    { re: /quote|price|pricing|cost|how much|order|buy|purchase|bid|rfq|rfp/i, run: startLead },
    { re: /cookie|biscuit/i, run: () => cat('cookies', 'We supply packaged cookies and biscuits for retail shelves and institutional buyers.') },
    { re: /chocolate|candy|sweet|confection|almond/i, run: () => cat('chocolates', 'We supply chocolates, chocolate almonds and other confectionery.') },
    { re: /\btuna\b|\bcanned\b|\bcans?\b(?! you)|seafood|shrimp|\bfish\b|frozen|\bmeats?\b/i, run: () => cat('canned-seafood', 'We supply canned tuna, frozen shrimp and other canned and seafood products.') },
    { re: /water|mineral|sparkling|carbonated/i, run: () => cat('water', 'We supply still and carbonated mineral water.') },
    { re: /isotonic|sport|energy|soda|soft drink|beverage|drink/i, run: () => cat('beverages', 'We supply isotonic and sports drinks, sodas and other beverages.') },
    { re: /grocer|packaged|pantry|dry goods|condiment|oil|coffee|cereal/i, run: () => cat('grocery', 'We supply a wide range of packaged and general grocery products.') },
    { re: /federal|government|\bgov\b|military|navy|national guard|agenc|\bsam\b|\buei\b|\bcage\b|naics|contract/i, run: () => say(`We’re an active federal supplier (SAM-registered).\n• UEI: <strong>${S.uei}</strong>\n• CAGE: <strong>${S.cage}</strong>\n• Primary NAICS: <strong>424490</strong>\nWe reported four federal contracts worth over $2.5 million by June 2025. <a href="${BASE}services.html#government">Government supply</a>`).then(() => chips(['Certifications', 'Request a quote', 'Contact'])) },
    { re: /certif|wosb|women|hubzone|minority|hispanic|small business/i, run: () => say('SBA records list Almonte Trading Group as a certified <strong>Women-Owned Small Business (WOSB)</strong> and <strong>HUBZone</strong> business. Ask us for our capability statement.').then(() => chips(['Government supply', 'Request a quote'])) },
    { re: /supermarket|retail|store|wholesale|distribut|bulk|commercial/i, run: () => say(`We supply supermarkets, retail stores and commercial buyers with packaged food, confectionery and beverages. <a href="${BASE}services.html#wholesale">Wholesale distribution</a>`).then(() => chips(['Products', 'Request a quote'])) },
    { re: /import|sourc|represent|brand|supplier|manufactur/i, run: () => say(`We import and represent food and beverage products for the Puerto Rico market. <a href="${BASE}services.html#importing">Importing &amp; sourcing</a>`).then(() => chips(['Request a quote', 'Contact'])) },
    { re: /deliver|ship|area|island|where do you|coverage|puerto rico/i, run: () => say(`We’re based in ${esc(S.city)} and supply customers in Puerto Rico. For delivery details on your order, call <a href="${S.phoneHref}">${S.phone}</a>.`).then(() => chips(MAIN)) },
    { re: /\b(products?|catalog|catalogue|what do you (sell|supply|carry))\b/i, run: () => say(`Our main categories:\n• Cookies &amp; biscuits\n• Chocolates &amp; confectionery\n• Canned &amp; seafood\n• Mineral water\n• Sports &amp; isotonic drinks\n• Grocery products\n<a href="${BASE}products.html">See all products</a>`).then(() => chips(['Request a quote', 'Government supply'])) },
    { re: /hour|open|time|when/i, run: () => say(`Please call <a href="${S.phoneHref}">${S.phone}</a> to arrange a meeting or delivery time.`).then(() => chips(MAIN)) },
    { re: /address|located|location|caguas|office|warehouse|visit/i, run: () => say(`We’re located in <strong>${esc(S.city)}</strong>.\nPhysical: ${esc(S.address)}\nMailing: ${esc(S.mailing)}`).then(() => chips(MAIN)) },
    { re: /contact|phone|call|whatsapp|email|reach|talk|human|person|president|awilda/i, run: () => say(`You can reach us here:\n${contact()}`).then(() => chips(MAIN)) },
    { re: /^(hi|hello|hey|hola|buenas|good (morning|afternoon|evening))\b/i, run: () => say('Hello! How can we help with your food supply needs?').then(() => chips(MAIN)) },
    { re: /thank|gracias/i, run: () => say('You’re welcome. Anything else we can help with?').then(() => chips(MAIN)) },
  ];
  function cat(id, text) {
    return say(`${text}\n<a href="${BASE}products.html#${id}">View this category</a>`).then(() => chips(['Request a quote', 'Products']));
  }
  function startLead() {
    lead = { step: 'name' }; chips([]);
    return say('Happy to help with a quote. First, what’s your <strong>name</strong>?');
  }
  async function leadStep(v) {
    v = v.trim();
    if (/^(cancel|stop|exit)$/i.test(v)) { lead = null; await say('No problem, cancelled. Anything else?'); return chips(MAIN); }
    if (lead.step === 'name') { if (v.length < 2) return say('Could you tell me your name?'); lead.name = v.slice(0, 80); lead.step = 'company'; return say(`Thanks, ${esc(lead.name.split(' ')[0])}. Which <strong>company or organisation</strong> are you buying for?`); }
    if (lead.step === 'company') { lead.company = v.slice(0, 120); lead.step = 'contact'; return say('What’s the best <strong>phone number or email</strong> to reach you?'); }
    if (lead.step === 'contact') {
      const isMail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v), isPhone = v.replace(/\D/g, '').length >= 10;
      if (!isMail && !isPhone) return say('That doesn’t look like a valid phone number or email. Could you check it?');
      lead.contact = v; lead.step = 'needs'; chips(['Supermarket supply', 'Government order', 'Beverages', 'Confectionery']);
      return say('Lastly, what do you need? Products, approximate quantities and delivery location help us quote faster.');
    }
    if (lead.step === 'needs') {
      if (v.length < 3) return say('Could you add a few more details?');
      chips([]);
      const text = encodeURIComponent(['Quote request – website chat', `Name: ${lead.name}`, `Company: ${lead.company}`, `Contact: ${lead.contact}`, '', v.slice(0, 1200)].join('\n'));
      const wa = `https://wa.me/${S.whatsapp}?text=${text}`, sms = `sms:${S.phoneIntl}?&body=${text}`;
      lead = null;
      await say(`Thank you! I’ve prepared your request. Tap below to send it to our team:\n<a href="${wa}" target="_blank" rel="noopener">➜ Send on WhatsApp</a>\nNo WhatsApp? <a href="${sms}">Send as a text</a> or call <a href="${S.phoneHref}">${S.phone}</a>.`);
      return chips(MAIN);
    }
  }
  async function handle(text) {
    if (busy || !text.trim()) return;
    busy = true; add(esc(text), 'me');
    try {
      if (lead) { await leadStep(text); return; }
      const map = { 'Products': 'products', 'Government supply': 'federal', 'Request a quote': 'quote', 'Contact': 'contact', 'Certifications': 'certifications' };
      const q = map[text] || text;
      const hit = intents.find((i) => i.re.test(q));
      if (hit) { await hit.run(); return; }
      await say(`I don’t have a set answer for that one, but our team can help:\n${contact()}\n\nOr I can take your details for a quote.`);
      chips(MAIN);
    } finally { busy = false; }
  }
  const open = async (state) => {
    panel.classList.toggle('open', state); btn.setAttribute('aria-expanded', String(state));
    if (state) {
      input.focus();
      if (!started) { started = true; await say('Welcome to <strong>Almonte Trading Group</strong>. I can answer questions about our products, wholesale and government supply, or take a quote request.', 300); add('<small>This is an automated assistant with set answers. For anything else, call ' + `<a href="${S.phoneHref}">${S.phone}</a>.</small>`); chips(MAIN); }
    }
  };
  btn.addEventListener('click', () => open(!panel.classList.contains('open')));
  root.querySelector('.x').addEventListener('click', () => open(false));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && panel.classList.contains('open')) open(false); });
  form.addEventListener('submit', (e) => { e.preventDefault(); const v = input.value; input.value = ''; handle(v); });
})();
