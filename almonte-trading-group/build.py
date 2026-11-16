#!/usr/bin/env python3
"""
Almonte Trading Group – static site generator.
Writes a FLAT website (no sub-folders) into ./website : every page, stylesheet, script and image side by side.
Run:  python3 build.py
Edit company details in SITE below and page content in the page functions.
"""
import json, os, shutil, datetime, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'assets-src')
OUT = os.path.join(ROOT, 'website')

SITE = {
    'name': 'ALMONTE TRADING GROUP L.L.C.',
    'short': 'Almonte Trading Group',
    'tagline': 'Food Importing · Wholesale Distribution · Government Supply',
    'url': 'https://www.almontetradinggroup.com',  # placeholder domain – CONFIRM
    'phone': '(787) 383-2424',
    'phoneIntl': '+17873832424',
    'phoneHref': 'tel:+17873832424',
    'whatsapp': '17873832424',
    'city': 'Caguas, Puerto Rico',
    'address': '305 Calle Emajagua, Hacienda Borinquen, Caguas, PR 00725',
    'mailing': 'P.O. Box 5901, Caguas, PR 00726',
    'president': 'Awilda López',
    'founded': '2022-07-18',
    'uei': 'TBF2WJMVM4G5',
    'cage': '9YA47',
    'naics': '424490',
}

# ---------------------------------------------------------------- icons (inline SVG, stroke-based)
P = {
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    'pin': '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    'check': '<path d="M5 12.5 10 17l9-10"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'truck': '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
    'ship': '<path d="M3 17c2 1.5 4 1.5 6 0 2 1.5 4 1.5 6 0 2 1.5 4 1.5 6 0"/><path d="M5 14 4 9h16l-1 5M8 9V5h8v4"/>',
    'building': '<path d="M4 21V5l8-3 8 3v16M9 21v-4h6v4M8 8h.01M12 8h.01M16 8h.01M8 12h.01M12 12h.01M16 12h.01"/>',
    'cart': '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h11l2-8H6.2"/>',
    'store': '<path d="M3 9 5 4h14l2 5M4 9v11h16V9M3 9h18M9 20v-6h6v6"/>',
    'flag': '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-4-6"/>',
    'box': '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9z"/><path d="m4 7.5 8 4.5 8-4.5M12 12v9"/>',
    'handshake': '<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11l-1.5 1.5a2 2 0 0 1-3-3L13 7l-2-1-6 6 3 3"/><path d="m21 12-3-3-3 1"/><path d="m3 12 3-3"/>',
    'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'doc': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/>',
    'chart': '<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'tag': '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
}
def ic(n, cls=''):
    return f'<svg{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[n]}</svg>'
ARR = ic('arrow', 'arr')

LOGO = '''<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#0b1f3a"/><path d="M12 35 24 11l12 24" fill="none" stroke="#f2a900" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/><path d="M16.5 27h15" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/><circle cx="24" cy="35" r="2.6" fill="#fff"/></svg>'''

NAV = [('index.html', 'Home', 'home'), ('about.html', 'About Us', 'about'), ('products.html', 'Products', 'products'),
       ('services.html', 'Services', 'services'), ('gallery.html', 'Gallery', 'gallery'), ('contact.html', 'Contact Us', 'contact')]

PRODUCTS = [
    ('cookies', 'Cookies & Biscuits', 'cookies', 'Packaged cookies and biscuits for retail shelves, snack programmes and institutional buyers.',
     ['Packaged cookies', 'Biscuits & crackers', 'Snack packs', 'Retail & bulk packs']),
    ('chocolates', 'Chocolates & Confectionery', 'chocolate-almonds', 'Chocolate, chocolate almonds and confectionery that sell through year-round and at peak seasons.',
     ['Chocolates', 'Chocolate almonds', 'Confectionery', 'Seasonal assortments']),
    ('canned-seafood', 'Canned Goods & Seafood', 'shrimp', 'Shelf-stable canned products and seafood, including tuna and frozen shrimp.',
     ['Canned tuna', 'Frozen shrimp', 'Canned & packaged foods', 'Seafood']),
    ('water', 'Mineral Water', 'water-bottle', 'Still and carbonated mineral water for retail, offices, institutions and events.',
     ['Still mineral water', 'Carbonated mineral water', 'Single bottles & cases']),
    ('beverages', 'Sports, Isotonic & Soft Drinks', 'drinks', 'Isotonic and sports beverages and sodas for retail, institutional and government programmes.',
     ['Isotonic drinks', 'Sports beverages', 'Sodas & soft drinks']),
    ('grocery', 'Grocery Products', 'grocery-aisle', 'Packaged and general grocery supplies to keep shelves and pantries stocked.',
     ['Packaged groceries', 'Pantry staples', 'Condiments & oils', 'Coffee, tea & cocoa']),
]
SERVICES = [
    ('wholesale', 'Wholesale Food Distribution', 'hero-warehouse', 'truck',
     'Supply of packaged food, confectionery, beverages and grocery products to supermarkets and commercial buyers across Puerto Rico.',
     ['Supermarkets and retail chains', 'Packaged food, confectionery and beverages', 'Consistent product availability', 'Responsive account support']),
    ('importing', 'Food Importing & Sourcing', 'port-containers', 'ship',
     'Importing, product sourcing and brand representation for food and beverage categories in the Puerto Rico market.',
     ['Product sourcing for your requirements', 'Import and representation of food brands', 'Category expansion for retailers', 'Supplier coordination']),
    ('government', 'Government & Institutional Supply', 'documents', 'flag',
     'Food supply for federal, public-sector and institutional purchasing requirements, backed by an active SAM registration.',
     ['SAM-registered federal supplier', 'Canned, packaged and fresh foods', 'Bases, facilities and institutions', 'Compliant documentation and delivery']),
    ('partnerships', 'Commercial Supply Partnerships', 'handshake', 'handshake',
     'Long-term wholesale supply relationships with supermarkets, retailers and other commercial buyers.',
     ['Recurring supply agreements', 'Volume and seasonal planning', 'Dedicated point of contact', 'Built on dependable service']),
]

def page(key, title, desc, body, canonical, hero_img=None):
    nav = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if k == key else ""}>{l}</a></li>' for h, l, k in NAV)
    ld = {
        '@context': 'https://schema.org', '@type': 'WholesaleStore', 'name': SITE['name'], 'alternateName': SITE['short'],
        'description': 'Puerto Rico food importing, wholesale distribution and government supply company.',
        'url': SITE['url'], 'telephone': SITE['phoneIntl'], 'foundingDate': SITE['founded'],
        'founder': {'@type': 'Person', 'name': SITE['president'], 'jobTitle': 'President'},
        'address': {'@type': 'PostalAddress', 'streetAddress': '305 Calle Emajagua, Hacienda Borinquen', 'addressLocality': 'Caguas', 'addressRegion': 'PR', 'postalCode': '00725', 'addressCountry': 'US'},
        'areaServed': 'Puerto Rico', 'naics': SITE['naics'],
        'identifier': [{'@type': 'PropertyValue', 'propertyID': 'UEI', 'value': SITE['uei']}, {'@type': 'PropertyValue', 'propertyID': 'CAGE', 'value': SITE['cage']}],
        'image': SITE['url'] + '/og-image.jpg',
    }
    url = SITE['url'] + '/' + ('' if canonical == 'index.html' else canonical)
    preload = f'<link rel="preload" as="image" href="{hero_img}">' if hero_img else ''
    return f'''<!doctype html>
<html lang="en-US" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b1f3a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['short']}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE['url']}/og-image.jpg">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="logo-mark.svg" type="image/svg+xml">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
{preload}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script>window.SITE_BASE = "";</script>
<script defer src="site-config.js"></script>
<script defer src="main.js"></script>
<script defer src="chatbot.js"></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap">
  <span>{ic('pin')} {SITE['city']}</span>
  <span>{ic('shield')} Federal supplier · <b>UEI</b> {SITE['uei']} · <b>CAGE</b> {SITE['cage']}</span>
  <span>{ic('phone')} <a href="{SITE['phoneHref']}">{SITE['phone']}</a></span>
</div></div>
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="logo" href="index.html" aria-label="{SITE['short']} home">{LOGO}<span><b>ALMONTE</b><small>Trading Group L.L.C.</small></span></a>
    <nav class="nav" id="nav" aria-label="Main"><ul>{nav}<li class="nav-cta"><a class="btn btn-gold btn-block" href="contact.html#quote">Request a Quote {ARR}</a></li></ul></nav>
    <div class="hdr-cta">
      <a class="hdr-phone" href="{SITE['phoneHref']}"><i>{ic('phone')}</i><span><small>Call us</small>{SITE['phone']}</span></a>
      <a class="btn btn-gold" href="contact.html#quote">Request a Quote {ARR}</a>
      <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <a class="logo" href="index.html">{LOGO}<span><b>ALMONTE</b><small>Trading Group L.L.C.</small></span></a>
      <p>Food importing, wholesale distribution and government supply from {SITE['city']}. Dependable sourcing for supermarkets, commercial buyers and public-sector customers.</p>
      <div class="ids"><span>UEI {SITE['uei']}</span><span>CAGE {SITE['cage']}</span><span>NAICS {SITE['naics']}</span><span>WOSB</span><span>HUBZone</span></div>
    </div>
    <div><h4>Company</h4><ul>{''.join(f'<li><a href="{h}">{l}</a></li>' for h, l, k in NAV)}</ul></div>
    <div><h4>Products</h4><ul>{''.join(f'<li><a href="products.html#{p[0]}">{p[1]}</a></li>' for p in PRODUCTS)}</ul></div>
    <div><h4>Contact</h4><ul>
      <li><a href="{SITE['phoneHref']}">{SITE['phone']}</a></li>
      <li><a href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener">WhatsApp</a></li>
      <li>{SITE['address']}</li>
      <li>Mailing: {SITE['mailing']}</li>
    </ul></div>
  </div>
  <div class="wrap foot-bottom"><span>© <span data-year>{datetime.date.today().year}</span> {SITE['name']} All rights reserved.</span><span><a href="contact.html#quote">Request a Quote</a> · <a href="#main">Back to top</a></span></div>
</footer>
<a class="fab-call" href="{SITE['phoneHref']}" aria-label="Call {SITE['phone']}">{ic('phone')}</a>
</body>
</html>
'''

def phero(crumb, title, lead, img):
    return f'''<section class="phero"><img src="{img}" alt="" width="1500" height="1000">
  <div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span aria-current="page">{crumb}</span></nav>
  <h1 class="rv">{title}</h1><p class="rv d1">{lead}</p></div></section>'''

def cta():
    return f'''<section class="sec" style="padding-top:0"><div class="wrap"><div class="cta rv">
  <div><h2>Need a reliable food supplier?</h2><p>Tell us what you need – products, volumes and delivery location – and we’ll prepare a quote.</p></div>
  <div class="btn-row"><a class="btn" href="contact.html#quote">Request a Quote {ARR}</a><a class="btn btn-line" href="{SITE['phoneHref']}">{ic('phone')} {SITE['phone']}</a></div>
</div></div></section>'''

# ---------------------------------------------------------------- HOME
def home():
    tiles = []
    layout = ['wide', '', 'tall', '', '', '']
    for i, (pid, title, img, intro, _) in enumerate(PRODUCTS):
        tiles.append(f'''<a class="tile {layout[i]} rv d{(i % 4) + 1}" href="products.html#{pid}"><img src="{img}.webp" alt="" loading="lazy"><span class="num">0{i + 1}</span><span class="go">{ic('arrow')}</span><h3>{title}</h3><p>{intro}</p></a>''')
    tab_btns, panels = [], []
    for i, (sid, title, img, icon, intro, pts) in enumerate(SERVICES):
        sel = 'true' if i == 0 else 'false'
        tab_btns.append(f'<button class="tab-btn" role="tab" id="t-{sid}" aria-selected="{sel}" aria-controls="p-{sid}" tabindex="{0 if i == 0 else -1}"><i>{ic(icon)}</i>{title}</button>')
        panels.append(f'''<div class="tab-panel{' show' if i == 0 else ''}" role="tabpanel" id="p-{sid}" aria-labelledby="t-{sid}"{'' if i == 0 else ' hidden'}>
      <div class="tp-img"><img src="{img}.webp" alt="" loading="lazy"></div>
      <div class="tp-body"><span class="kicker">Service 0{i + 1}</span><h3 style="font-size:1.6rem">{title}</h3><p style="color:var(--muted)">{intro}</p>
        <ul class="ticks">{''.join(f'<li><i>{ic("check")}</i><span>{p}</span></li>' for p in pts)}</ul>
        <a class="link-arrow" href="services.html#{sid}">Learn more {ic('arrow')}</a></div></div>''')
    body = f'''
<section class="hero">
  <div class="wrap hero-in">
    <div>
      <span class="tag rv"><i>{ic('shield')}</i>Food Importing · Wholesale Distribution · Government Supply</span>
      <h1 class="rv d1">Your Trusted Partner in <em>Food Distribution</em> &amp; Supply</h1>
      <p class="lead rv d2">Almonte Trading Group delivers dependable food sourcing, wholesale distribution and supply solutions for supermarkets, commercial buyers and government customers across Puerto Rico.</p>
      <div class="btn-row rv d3"><a class="btn btn-gold" href="contact.html#quote">Request a Quote {ARR}</a><a class="btn btn-ghost" href="products.html">Explore Our Products</a></div>
      <div class="creds rv d4"><span>{ic('check')} SAM-registered federal supplier</span><span>{ic('check')} SBA WOSB</span><span>{ic('check')} SBA HUBZone</span></div>
    </div>
    <div class="mosaic rv d2">
      <figure><img src="hero-warehouse.webp" alt="Warehouse stocked with food products ready for distribution" width="1500" height="1000" fetchpriority="high"></figure>
      <figure><img src="port-containers.webp" alt="Cargo ship with containers at port" width="1500" height="1000" loading="lazy"></figure>
      <figure><img src="truck-road.webp" alt="Delivery truck on the road" width="1500" height="1000" loading="lazy"></figure>
      <div class="float-card fc-1"><i>{ic('chart')}</i><div><strong>$2.5M+</strong><small>in federal contracts by June 2025</small></div></div>
      <div class="float-card fc-2"><i>{ic('award')}</i><div><strong>WOSB</strong><small>Women-owned small business</small></div></div>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">{''.join(f'<span>{w}</span>' for w in ['Cookies & Biscuits','Chocolates','Chocolate Almonds','Canned Tuna','Frozen Shrimp','Mineral Water','Isotonic Drinks','Sodas','Grocery Products','Government Supply']*2)}</div></div>

<section class="sec">
  <div class="wrap split">
    <div class="rv rv-l">
      <span class="kicker">Who we are</span>
      <h2>Reliable food distribution &amp; wholesale supply from Puerto Rico</h2>
      <p style="font-size:1.1rem">Almonte Trading Group L.L.C. is a Caguas-based food importing, representation and distribution company. We supply quality food products, groceries, confectionery, beverages and packaged goods.</p>
      <p style="color:var(--muted)">We serve supermarkets, commercial buyers, institutional customers and government agencies with a focus on reliable sourcing, product availability and professional distribution.</p>
      <ul class="ticks">
        <li><i>{ic('check')}</i><span><strong>Local roots:</strong> founded in Caguas in 2022 and supplying local supermarkets.</span></li>
        <li><i>{ic('check')}</i><span><strong>Federal supplier:</strong> four federal contracts reported, worth over $2.5 million.</span></li>
        <li><i>{ic('check')}</i><span><strong>Long-term focus:</strong> dependable supply and responsive service.</span></li>
      </ul>
      <a class="btn btn-line" href="about.html">About Almonte {ARR}</a>
    </div>
    <div class="split-img rv rv-r"><img src="warehouse-racks.webp" alt="Warehouse racks stocked with boxed goods" width="1500" height="998" loading="lazy">
      <div class="stamp"><strong>Since 2022</strong><span>Caguas, Puerto Rico</span></div></div>
  </div>
</section>

<section class="sec sec-soft">
  <div class="wrap">
    <div class="head-row"><div class="sec-head rv"><span class="kicker">Product categories</span><h2>Food, beverages &amp; grocery supply</h2><p>Core categories we import and distribute. Product lists and brands are available on request.</p></div>
    <a class="link-arrow rv" href="products.html">View all products {ic('arrow')}</a></div>
    <div class="bento">{''.join(tiles)}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center rv"><span class="kicker">What we do</span><h2>Wholesale, sourcing &amp; supply services</h2><p>Four ways we help buyers keep products moving.</p></div>
    <div class="tabs rv d1"><div class="tab-list" role="tablist" aria-label="Services">{''.join(tab_btns)}<span class="tab-ink"></span></div>{''.join(panels)}</div>
  </div>
</section>

<section class="sec sec-navy" id="government">
  <div class="wrap gov">
    <div class="rv rv-l">
      <span class="kicker">Government &amp; institutional supply</span>
      <h2>A registered federal food supplier</h2>
      <p>Almonte Trading Group grew from local distribution into federal contracting, supplying canned, packaged and fresh foods, including meats and seafood, to federal customers in Puerto Rico.</p>
      <ul class="ticks">
        <li><i>{ic('check')}</i><span><strong>Active SAM registration</strong> with a Dynamic Small Business Search profile.</span></li>
        <li><i>{ic('check')}</i><span><strong>Four federal contracts</strong> worth over $2.5 million, reported June 2025.</span></li>
        <li><i>{ic('check')}</i><span><strong>Certified</strong> SBA Women-Owned Small Business and HUBZone.</span></li>
      </ul>
      <p style="margin:18px 0 0;font-size:.9rem;color:#9fb2cb">Federal customers reported by the Puerto Rico Federal Contracting Center:</p>
      <div class="served"><span>MDC</span><span>Fort Allen</span><span>Camp Santiago</span><span>U.S. Navy</span><span>National Guard</span></div>
    </div>
    <div class="id-cards">
      <div class="id-card rv d1"><small>Unique Entity ID</small><strong>{SITE['uei']}</strong><span>SAM.gov</span></div>
      <div class="id-card rv d2"><small>CAGE Code</small><strong>{SITE['cage']}</strong><span>Commercial & Government Entity</span></div>
      <div class="id-card gold rv d3"><small>Primary NAICS</small><strong>{SITE['naics']}</strong><span>Other grocery & related products merchant wholesalers</span></div>
      <div class="id-card rv d4"><small>SBA certifications</small><strong>WOSB · HUBZone</strong><span>Women-owned · Historically underutilized business zone</span></div>
    </div>
  </div>
</section>
<section style="background:var(--bg);padding-bottom:20px"><div class="wrap">
  <div class="stats rv">
    <div class="stat"><strong data-count="2.5" data-prefix="$" data-suffix="M<sup>+</sup>">$2.5M<sup>+</sup></strong><span>Federal contracts</span><small>Reported by June 2025</small></div>
    <div class="stat"><strong data-count="4">4</strong><span>Federal contracts</span><small>Won in under a year</small></div>
    <div class="stat"><strong data-count="2022">2022</strong><span>Established</span><small>July 18, 2022</small></div>
    <div class="stat"><strong data-count="3" data-suffix="×">3×</strong><span>Workforce growth</span><small>Since entering federal supply</small></div>
  </div>
</div></section>

<section class="sec sec-soft" style="padding-top:70px">
  <div class="wrap">
    <div class="sec-head center rv"><span class="kicker">Who we serve</span><h2>Built for professional buyers</h2></div>
    <div class="cards4">
      <div class="card rv d1"><span class="ic">{ic('cart')}</span><h3>Supermarkets</h3><p>Reliable wholesale food supply that keeps shelves stocked.</p></div>
      <div class="card rv d2"><span class="ic">{ic('store')}</span><h3>Retail stores</h3><p>Packaged groceries, confectionery and beverages.</p></div>
      <div class="card rv d3"><span class="ic">{ic('flag')}</span><h3>Government agencies</h3><p>Food procurement and supply from a SAM-registered supplier.</p></div>
      <div class="card rv d4"><span class="ic">{ic('building')}</span><h3>Institutional buyers</h3><p>Bulk food supply for institutions and facilities.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head rv"><span class="kicker">Why Almonte</span><h2>Why buyers choose Almonte Trading Group</h2></div>
    <div class="why">
      <div class="why-item rv d1"><b>01</b><div><h3>Dependable supply</h3><p>Consistent product availability so you can plan with confidence.</p></div></div>
      <div class="why-item rv d2"><b>02</b><div><h3>Federal-ready</h3><p>SAM-registered with UEI, CAGE and SBA certifications in place.</p></div></div>
      <div class="why-item rv d3"><b>03</b><div><h3>Broad food range</h3><p>Confectionery, canned goods, seafood, beverages and groceries.</p></div></div>
      <div class="why-item rv d1"><b>04</b><div><h3>Local in Puerto Rico</h3><p>Based in Caguas, close to our customers across the island.</p></div></div>
      <div class="why-item rv d2"><b>05</b><div><h3>Responsive service</h3><p>Direct contact with a team that answers and follows up.</p></div></div>
      <div class="why-item rv d3"><b>06</b><div><h3>Long-term partners</h3><p>We build lasting supply relationships, not one-off orders.</p></div></div>
    </div>
  </div>
</section>
{cta()}'''
    return page('home', 'Almonte Trading Group L.L.C. | Food Distribution & Wholesale Supply, Puerto Rico',
                'Almonte Trading Group L.L.C. is a Caguas, Puerto Rico food importing, wholesale distribution and government supply company. SAM-registered, WOSB and HUBZone. Call (787) 383-2424.',
                body, 'index.html', 'hero-warehouse.webp')

# ---------------------------------------------------------------- ABOUT
def about():
    body = f'''{phero('About Us', 'From local distributor to trusted federal supplier', 'A Puerto Rico food importing, representation and distribution company, founded in Caguas in 2022.', 'warehouse-aisle.webp')}
<section class="sec">
  <div class="wrap split">
    <div class="rv rv-l">
      <span class="kicker">Our story</span>
      <h2>Building dependable food supply for Puerto Rico</h2>
      <p style="font-size:1.1rem">Almonte Trading Group L.L.C. was established on July 18, 2022 in Caguas, Puerto Rico. We import, represent and distribute food and beverage products, and we supply local supermarkets with cookies, chocolates, tuna, confectionery, mineral water, isotonic drinks and sodas.</p>
      <p style="color:var(--muted)">In 2024 we set out to grow beyond local distribution. With support from the Puerto Rico Federal Contracting Center we registered in SAM.gov, created our Dynamic Small Business Search profile and pursued SBA certifications. In less than a year we won four federal contracts worth over $2.5 million, tripled our workforce and expanded our product and service lines.</p>
    </div>
    <div class="rv rv-r">
      <div class="timeline">
        <div class="tl"><b>July 2022</b><h3>Company founded</h3><p>Almonte Trading Group L.L.C. established in Caguas, Puerto Rico.</p></div>
        <div class="tl"><b>2022 – 2024</b><h3>Local distribution</h3><p>Importing and supplying food and beverages to local supermarkets.</p></div>
        <div class="tl"><b>July 2024</b><h3>Federal registration</h3><p>SAM.gov registration and a DSBS profile, with guidance from the Federal Contracting Center.</p></div>
        <div class="tl"><b>Aug – Sep 2024</b><h3>SBA certifications</h3><p>HUBZone (August 2024) and Women-Owned Small Business (September 2024).</p></div>
        <div class="tl"><b>June 2025</b><h3>Four federal contracts</h3><p>Over $2.5 million in federal contracts reported.</p></div>
      </div>
    </div>
  </div>
</section>
<section class="sec sec-soft">
  <div class="wrap">
    <figure class="quote rv">
      <blockquote>Now, we are a trusted federal supplier with long-term contracts.</blockquote>
      <figcaption><span class="avatar">AL</span><span><b>{SITE['president']}</b>President, Almonte Trading Group L.L.C.</span></figcaption>
    </figure>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec-head center rv"><span class="kicker">Mission &amp; values</span><h2>What guides our work</h2><p>Our goal is to build long-term business relationships by providing dependable supply solutions and responsive customer service.</p></div>
    <div class="cards4">
      <div class="card rv d1"><span class="ic">{ic('box')}</span><h3>Reliability</h3><p>Products available when our customers need them.</p></div>
      <div class="card rv d2"><span class="ic">{ic('award')}</span><h3>Quality</h3><p>Quality food products from trusted sources.</p></div>
      <div class="card rv d3"><span class="ic">{ic('users')}</span><h3>Service</h3><p>Responsive, personal attention for every account.</p></div>
      <div class="card rv d4"><span class="ic">{ic('handshake')}</span><h3>Partnership</h3><p>Relationships built to last, order after order.</p></div>
    </div>
  </div>
</section>
<section class="sec sec-soft" id="credentials">
  <div class="wrap split" style="align-items:start">
    <div class="rv rv-l">
      <span class="kicker">Credentials</span>
      <h2>Registration &amp; certifications</h2>
      <p style="color:var(--muted)">Our federal registration details for procurement officers and prime contractors. Capability statement available on request.</p>
      <a class="btn" href="contact.html#quote">Request our capability statement {ARR}</a>
    </div>
    <div class="rv rv-r"><table class="reg">
      <tr><th>Legal name</th><td>{SITE['name']}</td></tr>
      <tr><th>President</th><td>{SITE['president']}</td></tr>
      <tr><th>Established</th><td>July 18, 2022</td></tr>
      <tr><th>UEI</th><td>{SITE['uei']}</td></tr>
      <tr><th>CAGE code</th><td>{SITE['cage']}</td></tr>
      <tr><th>Primary NAICS</th><td>424490 – Other Grocery &amp; Related Products Merchant Wholesalers</td></tr>
      <tr><th>Other NAICS include</th><td>424450 Confectionery · 424460 Fish &amp; Seafood</td></tr>
      <tr><th>SBA certifications</th><td>Women-Owned Small Business (WOSB) · HUBZone</td></tr>
      <tr><th>Physical address</th><td>{SITE['address']}</td></tr>
      <tr><th>Mailing address</th><td>{SITE['mailing']}</td></tr>
    </table></div>
  </div>
</section>
{cta()}'''
    return page('about', 'About Us | Almonte Trading Group L.L.C., Caguas, Puerto Rico',
                'Founded in Caguas in 2022, Almonte Trading Group grew from local food distribution to a federal supplier with four contracts worth over $2.5M. Led by President Awilda López.',
                body, 'about.html')

# ---------------------------------------------------------------- PRODUCTS
def products():
    nav = ''.join(f'<a href="#{p[0]}">{p[1]}</a>' for p in PRODUCTS)
    cats = ''.join(f'''<article class="cat" id="{pid}">
      <div class="cat-img rv"><img src="{img}.webp" alt="{title}" loading="lazy"></div>
      <div class="rv d1"><span class="cnum">CATEGORY 0{i + 1}</span><h2 style="font-size:clamp(1.6rem,3vw,2.2rem)">{title}</h2><p style="color:var(--muted);font-size:1.06rem">{intro}</p>
        <div class="chips">{''.join(f'<span>{x}</span>' for x in items)}</div>
        <a class="btn" href="contact.html?service=products#quote">Request pricing {ARR}</a></div>
    </article>''' for i, (pid, title, img, intro, items) in enumerate(PRODUCTS))
    psc = ['Meat, poultry & fish', 'Dairy & eggs', 'Fruits & vegetables', 'Bakery & cereal', 'Jams & preserves', 'Soups', 'Food oils & fats', 'Condiments', 'Coffee, tea & cocoa', 'Composite food packages']
    body = f'''{phero('Products', 'Food, beverage &amp; grocery products', 'Categories we import and distribute for supermarkets, retailers, institutions and government buyers.', 'grocery-aisle.webp')}
<div class="cat-nav"><div class="wrap">{nav}</div></div>
<section class="sec" style="padding-top:20px"><div class="wrap">{cats}</div></section>
<section class="sec sec-soft">
  <div class="wrap">
    <div class="sec-head rv"><span class="kicker">Federal supply categories</span><h2>Also listed in our federal registration</h2><p>Product service categories listed in our federal registration profile. Ask us about availability for your requirement.</p></div>
    <div class="psc rv">{''.join(f'<span>{ic("tag")}{x}</span>' for x in psc)}</div>
    <p class="rv" style="margin-top:28px;color:var(--muted);font-size:.95rem">Brands, pack sizes and a full product catalogue are available on request. Photos on this website are illustrative.</p>
  </div>
</section>
{cta()}'''
    return page('products', 'Products | Food, Beverages & Grocery Wholesale – Almonte Trading Group',
                'Cookies and biscuits, chocolates and confectionery, canned tuna and frozen shrimp, mineral water, isotonic and sports drinks, sodas and grocery products, supplied wholesale in Puerto Rico.',
                body, 'products.html')

# ---------------------------------------------------------------- SERVICES
def services():
    blocks = ''.join(f'''<article class="svc" id="{sid}">
      <div class="big rv">0{i + 1}</div>
      <div class="rv d1"><span class="kicker">Service</span><h2 style="font-size:clamp(1.6rem,3vw,2.2rem)">{title}</h2><p style="color:var(--muted);font-size:1.06rem">{intro}</p>
        <ul class="ticks">{''.join(f'<li><i>{ic("check")}</i><span>{p}</span></li>' for p in pts)}</ul>
        <a class="btn btn-line" href="contact.html?service={sid}#quote">Discuss your needs {ARR}</a></div>
      <img class="rv d2" src="{img}.webp" alt="{title}" loading="lazy">
    </article>''' for i, (sid, title, img, icon, intro, pts) in enumerate(SERVICES))
    body = f'''{phero('Services', 'Wholesale, distribution &amp; supply services', 'From importing and sourcing to delivery for commercial and government buyers.', 'truck-road.webp')}
<section class="sec" style="padding-top:30px"><div class="wrap">{blocks}</div></section>
<section class="sec sec-navy">
  <div class="wrap">
    <div class="sec-head center rv"><span class="kicker">How we work</span><h2>From enquiry to delivery</h2><p>A clear, simple process for every buyer.</p></div>
    <div class="steps">
      <div class="step rv d1"><h3>Enquiry</h3><p>Tell us the products, volumes, specifications and delivery location you need.</p></div>
      <div class="step rv d2"><h3>Quote</h3><p>We confirm availability and prepare a clear quotation or bid response.</p></div>
      <div class="step rv d3"><h3>Sourcing</h3><p>We source and prepare your order from our network and stock.</p></div>
      <div class="step rv d4"><h3>Delivery</h3><p>Your order is delivered as agreed, with documentation where required.</p></div>
    </div>
  </div>
</section>
<section class="sec sec-soft">
  <div class="wrap">
    <div class="sec-head center rv"><span class="kicker">FAQs</span><h2>Questions from buyers</h2></div>
    <div class="faq rv">
      <details><summary>Who do you supply?<i>{ic('plus')}</i></summary><p>Supermarkets, retail stores, commercial buyers, institutions and government agencies in Puerto Rico.</p></details>
      <details><summary>Are you registered as a federal supplier?<i>{ic('plus')}</i></summary><p>Yes. We are registered in SAM.gov (UEI {SITE['uei']}, CAGE {SITE['cage']}) with primary NAICS {SITE['naics']}, and hold SBA WOSB and HUBZone certifications.</p></details>
      <details><summary>Which products do you carry?<i>{ic('plus')}</i></summary><p>Cookies and biscuits, chocolates and confectionery, canned goods and seafood, mineral water, sports and isotonic drinks, sodas and grocery products. See our <a href="products.html">Products page</a>.</p></details>
      <details><summary>Can you source products we don’t see listed?<i>{ic('plus')}</i></summary><p>Ask us. Importing and sourcing is part of what we do, so send us your requirement and we’ll check availability.</p></details>
      <details><summary>How do I request a quote?<i>{ic('plus')}</i></summary><p>Use our <a href="contact.html#quote">quote form</a>, call {SITE['phone']} or message us on WhatsApp.</p></details>
    </div>
  </div>
</section>
{cta()}'''
    return page('services', 'Services | Wholesale Food Distribution & Government Supply – Almonte Trading Group',
                'Wholesale food distribution, food importing and sourcing, government and institutional supply, and commercial supply partnerships in Puerto Rico.',
                body, 'services.html')

# ---------------------------------------------------------------- CONTACT
def contact():
    opts = ''.join(f'<option value="{s[0]}">{s[1]}</option>' for s in SERVICES) + '<option value="products">Product pricing</option>'
    cats = ''.join(f'<label><input type="checkbox" name="categories" value="{p[1]}"><span>{p[1]}</span></label>' for p in PRODUCTS)
    body = f'''{phero('Contact Us', 'Request a quote', 'Business enquiries, quote requests and government procurement. We’ll get back to you promptly.', 'boxes-stock.webp')}
<section class="sec" id="quote">
  <div class="wrap contact">
    <aside class="info rv rv-l">
      <h2>Contact details</h2>
      <ul>
        <li><i>{ic('phone')}</i><div><small>Phone</small><a href="{SITE['phoneHref']}">{SITE['phone']}</a></div></li>
        <li><i>{ic('mail')}</i><div><small>WhatsApp</small><a href="https://wa.me/{SITE['whatsapp']}" target="_blank" rel="noopener">Message us on WhatsApp</a></div></li>
        <li><i>{ic('pin')}</i><div><small>Physical address</small><strong>{SITE['address']}</strong></div></li>
        <li><i>{ic('doc')}</i><div><small>Mailing address</small><strong>{SITE['mailing']}</strong></div></li>
        <li><i>{ic('shield')}</i><div><small>Federal IDs</small><strong>UEI {SITE['uei']} · CAGE {SITE['cage']}</strong></div></li>
      </ul>
      <a class="btn btn-gold btn-block" href="{SITE['phoneHref']}">{ic('phone')} Call now</a>
    </aside>
    <div class="form-card rv rv-r">
      <h2>Request a quote</h2>
      <p style="color:var(--muted)">Fields marked <span class="req">*</span> are required. When you press send, your request opens in WhatsApp ready to go.</p>
      <form id="quote-form" novalidate>
        <div class="fgrid">
          <div class="f"><label for="name">Full name <span class="req">*</span></label><input id="name" name="name" autocomplete="name" required maxlength="80"><span class="err" role="alert"></span></div>
          <div class="f"><label for="company">Company / organisation <span class="req">*</span></label><input id="company" name="company" autocomplete="organization" required maxlength="120"><span class="err" role="alert"></span></div>
          <div class="f"><label for="phone">Phone <span class="req">*</span></label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" placeholder="(787) 555-0123"><span class="err" role="alert"></span></div>
          <div class="f"><label for="email">Email <span class="req">*</span></label><input id="email" name="email" type="email" autocomplete="email" required maxlength="120"><span class="err" role="alert"></span></div>
          <div class="f"><label for="buyer">Buyer type</label><select id="buyer" name="buyer"><option value="">Select…</option><option>Supermarket</option><option>Retail store</option><option>Government agency</option><option>Institutional buyer</option><option>Distributor / other</option></select></div>
          <div class="f"><label for="interest">Interested in</label><select id="interest" name="interest"><option value="">Select…</option>{opts}</select></div>
          <fieldset class="f full"><legend>Product categories</legend><div class="checks">{cats}</div></fieldset>
          <div class="f full"><label for="message">Your requirements <span class="req">*</span></label><textarea id="message" name="message" required maxlength="2000" placeholder="Products, quantities, delivery location and timeline. For government bids, include the solicitation number."></textarea><span class="err" role="alert"></span></div>
          <div class="hp" aria-hidden="true"><label for="_hp">Leave empty</label><input id="_hp" name="_hp" tabindex="-1" autocomplete="off"></div>
        </div>
        <div class="form-foot"><small>We only use your details to respond to your enquiry.</small><button class="btn btn-gold" type="submit">Send request {ARR}</button></div>
        <div class="status" role="status" aria-live="polite"></div>
      </form>
    </div>
  </div>
</section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="map rv"><iframe title="Map of Almonte Trading Group, Caguas, Puerto Rico" src="https://maps.google.com/maps?q=Calle%20Emajagua%2C%20Hacienda%20Borinquen%2C%20Caguas%2C%20PR%2000725&amp;z=14&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>'''
    return page('contact', 'Contact & Request a Quote | Almonte Trading Group L.L.C.',
                'Request a quote from Almonte Trading Group, Caguas, Puerto Rico. Call (787) 383-2424 or send your requirements online. UEI TBF2WJMVM4G5, CAGE 9YA47.',
                body, 'contact.html')


# ---------------------------------------------------------------- GALLERY
def gallery():
    items = [
        ('logistics', 'hero-warehouse', 'Warehouse stock ready for distribution'), ('logistics', 'port-containers', 'Imports arriving by sea'),
        ('logistics', 'truck-road', 'Delivery on the road'), ('logistics', 'warehouse-racks', 'Racked and organised stock'),
        ('products', 'cookies', 'Cookies & biscuits'), ('products', 'chocolate-almonds', 'Chocolates & chocolate almonds'),
        ('products', 'shrimp', 'Seafood'), ('products', 'water-bottle', 'Mineral water'), ('products', 'drinks', 'Sports & soft drinks'),
        ('retail', 'grocery-aisle', 'Supplying grocery aisles'), ('logistics', 'warehouse-aisle', 'Warehouse aisle'),
        ('retail', 'boxes-stock', 'Cased goods for retail and institutions'), ('retail', 'handshake', 'Long-term supply partnerships'),
    ]
    tiles = ''.join(f'<button class="g-item rv d{(i % 4) + 1}" data-cat="{c}" data-cap="{html.escape(cap)}"><img src="{img}.webp" alt="{html.escape(cap)}" loading="lazy"><span>{html.escape(cap)}</span></button>' for i, (c, img, cap) in enumerate(items))
    body = phero('Gallery', 'Gallery', 'Warehousing, logistics and the food and beverage categories we supply.', 'warehouse-racks.webp') + f'''
<section class="sec">
  <div class="wrap">
    <div class="g-filters rv" role="group" aria-label="Filter photos">
      <button class="on" data-f="all" aria-pressed="true">All</button><button data-f="logistics" aria-pressed="false">Warehouse &amp; logistics</button><button data-f="products" aria-pressed="false">Products</button><button data-f="retail" aria-pressed="false">Retail &amp; partners</button>
    </div>
    <div class="g-grid">{tiles}</div>
    <p class="rv" style="margin-top:26px;color:var(--muted);font-size:.95rem;text-align:center">Photos are illustrative. Our own warehouse and product photos are coming soon.</p>
  </div>
</section>
<div class="lightbox" hidden><button class="lb-x" aria-label="Close">&#10005;</button><figure><img alt=""><figcaption></figcaption></figure></div>
''' + cta()
    return page('gallery', 'Gallery | Almonte Trading Group L.L.C.', 'Warehousing, logistics and the food and beverage categories Almonte Trading Group supplies across Puerto Rico.', body, 'gallery.html')

def notfound():
    body = f'''<section class="nf"><div class="wrap"><div class="big">404</div><h1 style="font-size:clamp(1.6rem,3vw,2.2rem)">Sorry, we can’t find that page.</h1><p style="color:var(--muted)">It may have moved or no longer exists.</p>
  <div class="btn-row"><a class="btn btn-gold" href="index.html">Back to home {ARR}</a><a class="btn btn-line" href="contact.html">Contact us</a></div></div></section>'''
    return page('404', 'Page not found | Almonte Trading Group', 'Sorry, this page could not be found.', body, '404.html')

# ---------------------------------------------------------------- write
if os.path.isdir(OUT):
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))
else:
    os.makedirs(OUT)
pages = {'index.html': home(), 'about.html': about(), 'products.html': products(), 'services.html': services(), 'gallery.html': gallery(), 'contact.html': contact(), '404.html': notfound()}
for name, content in pages.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as fh:
        fh.write(content)
for f in ['styles.css', 'main.js', 'chatbot.js']:
    shutil.copy(os.path.join(SRC, f), os.path.join(OUT, f))
img_dir = os.path.join(SRC, 'img')
used = ''.join(pages.values())
for f in os.listdir(img_dir):
    if f in used or f in ('og-image.jpg', 'logo-mark.svg'):
        shutil.copy(os.path.join(img_dir, f), os.path.join(OUT, f))
with open(os.path.join(OUT, 'site-config.js'), 'w') as fh:
    fh.write('window.SITE = ' + json.dumps({k: SITE[k] for k in ['name', 'short', 'phone', 'phoneIntl', 'phoneHref', 'whatsapp', 'city', 'address', 'mailing', 'uei', 'cage']}, ensure_ascii=False, indent=2) + ';\n')
today = datetime.date.today().isoformat()
with open(os.path.join(OUT, 'sitemap.xml'), 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
             ''.join(f'  <url><loc>{SITE["url"]}/{"" if p == "index.html" else p}</loc><lastmod>{today}</lastmod><priority>{"1.0" if p == "index.html" else "0.8"}</priority></url>\n' for p in pages if p != '404.html') + '</urlset>\n')
with open(os.path.join(OUT, 'robots.txt'), 'w') as fh:
    fh.write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE["url"]}/sitemap.xml\n')
with open(os.path.join(OUT, 'site.webmanifest'), 'w') as fh:
    json.dump({'name': SITE['name'], 'short_name': 'Almonte', 'start_url': './', 'display': 'standalone', 'background_color': '#ffffff', 'theme_color': '#0b1f3a', 'icons': [{'src': 'logo-mark.svg', 'sizes': 'any', 'type': 'image/svg+xml'}]}, fh)
PREFIX_ASSETS = False  # set True to prefix non-page files with "almonte-"
if PREFIX_ASSETS:
    # Give every non-page file a unique "almonte-" name, so downloading files one by one never collides with
    # same-named files from other websites (browsers rename duplicates, e.g. "styles (2).css", which breaks links).
    import re as _re
    assets = [f for f in os.listdir(OUT) if not f.endswith('.html') and f not in ('robots.txt', 'sitemap.xml')]
    for f in assets:
        os.rename(os.path.join(OUT, f), os.path.join(OUT, 'almonte-' + f))
    names = sorted(assets, key=len, reverse=True)
    pat = _re.compile(r'(?<![\w./-])(' + '|'.join(_re.escape(n) for n in names) + r')')
    for f in os.listdir(OUT):
        if f.endswith(('.html', '.js', '.css', '.webmanifest')):
            fp = os.path.join(OUT, f)
            with open(fp, encoding='utf-8') as fh: t = fh.read()
            t2 = pat.sub(lambda m: 'almonte-' + m.group(1), t)
            t2 = t2.replace(SITE['url'] + '/og-image.jpg', SITE['url'] + '/almonte-og-image.jpg')
            if t2 != t:
                with open(fp, 'w', encoding='utf-8') as fh: fh.write(t2)
print('website/ written:', len(os.listdir(OUT)), 'files')
