#!/usr/bin/env python3
"""Gera o site da Bratecon.

  python3 build.py            -> dist/       (deploy: cada página é um HTML completo)
  python3 build.py artifact   -> artifact/   (publicação no Claude: index sem esqueleto)

Fontes: src/pages/*.html (corpo de cada página), src/extra.css, assets/.
"""
import os, re, sys, shutil, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from products import product_cards, PRODUCTS
import seo
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MODE = sys.argv[1] if len(sys.argv) > 1 else 'deploy'
OUT = os.path.join(ROOT, 'artifact' if MODE == 'artifact' else 'dist')
SITE = 'https://www.bratecon.com/'
# Contato comercial: o único lugar onde o número aparece. Trocar aqui e rodar o build.
WA_NUM = '5571992391326'
FONE = '(71) 99239-1326'
WA = 'https://wa.me/' + WA_NUM

PAGES = [
  # arquivo, chave, rótulo no menu, título, descrição, usa 3D
  ('index.html', 'inicio', 'Início', seo.META['index.html'][0], seo.META['index.html'][1], True),
  ('empresa.html', 'empresa', 'A Bratecon', seo.META['empresa.html'][0], seo.META['empresa.html'][1], False),
  ('solucoes.html', 'solucoes', 'Soluções', seo.META['solucoes.html'][0], seo.META['solucoes.html'][1], False),
  ('metodo.html', 'metodo', 'Método', seo.META['metodo.html'][0], seo.META['metodo.html'][1], False),
  ('casos.html', 'casos', 'Casos', seo.META['casos.html'][0], seo.META['casos.html'][1], True),
  ('produtos.html', 'produtos', 'Produtos', seo.META['produtos.html'][0], seo.META['produtos.html'][1], False),
  ('contato.html', 'contato', 'Contato', seo.META['contato.html'][0], seo.META['contato.html'][1], False),
]
SUB = {'inicio': '', 'empresa': 'História e propósito', 'solucoes': 'Seis frentes', 'casos': 'Clean 24h · BahiaFix', 'produtos': 'Portfólio', 'contato': 'Começar pela escuta', 'metodo': 'Move OS · 5 movimentos'}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,300..900;1,62..125,300..900&family=Montserrat:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">')
LIBS = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
        '<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>\n'
        '<script src="https://unpkg.com/lucide@0.469.0/dist/umd/lucide.min.js"></script>\n'
        '<script src="assets/site.js"></script>')
GL = ('<script type="importmap">{"imports":{"three":"https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.module.min.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}</script>\n'
      '<script type="module" src="assets/gl.js"></script>')

# Abertura: decide antes de qualquer script se o vídeo toca (uma vez por visita, sem movimento reduzido)
HOLD = ('<script>(function(){var p=true;try{if(sessionStorage.getItem("bt-intro"))p=false}catch(e){}'
        'if(matchMedia("(prefers-reduced-motion: reduce)").matches)p=false;'
        'window.__btHold=p;if(p)document.documentElement.classList.add("intro-on")})()</script>')

def head(f, key, title, desc, path):
    canon = SITE + ('' if f == 'index.html' else f)
    meta = [f'<title>{title.replace("&", "&amp;")}</title>',
            '<meta name="claude:viewport-fit-sides" content="cover">' if MODE == 'artifact' else '',
            f'<meta name="description" content="{desc}">',
            f'<link rel="canonical" href="{canon}">',
            '<meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="Bratecon">',
            f'<meta property="og:title" content="{title.replace("&", "&amp;")}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}">',
            f'<meta property="og:image" content="{SITE}assets/og/{key}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{title.replace("&", "&amp;")}">',
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{title.replace("&", "&amp;")}"><meta name="twitter:description" content="{desc}"><meta name="twitter:image" content="{SITE}assets/og/{key}.png">',
            '<meta name="theme-color" content="#061425">',
            '<link rel="icon" href="assets/img/simbolo-cor.webp" type="image/webp">',
            FONTS, '<link rel="stylesheet" href="assets/site.css">']
    meta.append(seo.jsonld(f, PRODUCTS))
    if f == 'index.html':
        meta.append(HOLD)
    meta.append('<script>document.documentElement.lang="pt-BR";try{if(localStorage.getItem("bt-theme")==="light")document.documentElement.setAttribute("data-theme","light")}catch(e){}</script>')
    return '\n'.join(m for m in meta if m)

def nav(key):
    links = ''.join(f'<a href="{f}" data-nav="{k}">{lbl}</a>' for f, k, lbl, *_ in PAGES if k != 'inicio')
    items = ''.join(
        f'<a class="mitem" href="{f}" data-nav="{k}"><span class="n">0{i+1}</span><span class="t"><span class="roll"><span>{lbl}</span><span>{lbl}</span></span></span><span class="s">{SUB[k]}</span></a>'
        for i, (f, k, lbl, *_) in enumerate(PAGES))
    return f'''<div class="grain" aria-hidden="true"></div>
<div class="rail" aria-hidden="true">Bratecon · Tecnologia &amp; Consultoria · Salvador</div>
<a class="vh" href="#conteudo">Pular para o conteúdo</a>
<header class="nav" id="nav">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Bratecon, página inicial"><img class="night" src="assets/img/logo-h-branco.webp" alt="Bratecon" width="120" height="24"><img class="paper" src="assets/img/logo-h-cor.webp" alt="Bratecon" width="120" height="24"></a>
    <nav class="pill" aria-label="Páginas do site">{links}</nav>
    <div class="navr">
      <div class="tgl" role="group" aria-label="Tema"><button type="button" data-theme-set="dark" aria-pressed="true">Noite</button><button type="button" data-theme-set="light" aria-pressed="false">Papel</button></div>
      <a class="btn btn-nav" href="contato.html">Começar ↗</a>
      <button type="button" class="ibtn mbtn" id="menuBtn" aria-label="Abrir menu" aria-controls="menu" aria-expanded="false"><i data-lucide="menu"></i></button>
    </div>
  </div>
</header>
<div class="mnav" id="menu" role="dialog" aria-modal="true" aria-label="Menu" hidden>
  <div class="wrap mtop">
    <a class="brand" href="index.html"><img class="night" src="assets/img/logo-h-branco.webp" alt="Bratecon" width="120" height="24"><img class="paper" src="assets/img/logo-h-cor.webp" alt="Bratecon" width="120" height="24"></a>
    <button type="button" class="ibtn" id="menuClose" aria-label="Fechar menu"><i data-lucide="x"></i></button>
  </div>
  <div class="wrap mbody">
    <nav class="list" aria-label="Páginas">{items}</nav>
    <div class="side">
      <div class="social">
        <a href="{WA}" target="_blank" rel="noopener"><span class="gl">⮡</span>WhatsApp comercial</a>
        <a href="https://instagram.com/bratecon_oficial" target="_blank" rel="noopener"><span class="gl">⮡</span>Instagram</a>
        <a href="https://movedata.com.br" target="_blank" rel="noopener"><span class="gl">⮡</span>Move Data</a>
      </div>
      <div class="tgl" role="group" aria-label="Tema"><button type="button" data-theme-set="dark" aria-pressed="true">Noite</button><button type="button" data-theme-set="light" aria-pressed="false">Papel</button></div>
      <span class="data">{FONE} · Salvador, Bahia</span>
    </div>
  </div>
  <div class="wrap mfoot"><span class="label">Engenharia da operação</span><span class="label">Transformamos desafios em soluções</span></div>
</div>'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="fgrid">
      <div><a class="brand" href="index.html" aria-label="Bratecon, página inicial"><img class="night" src="assets/img/logo-h-branco.webp" alt="Bratecon" style="height:22px;width:auto"><img class="paper" src="assets/img/logo-h-cor.webp" alt="Bratecon" style="height:22px;width:auto"></a><p>Engenharia da operação. Automação, logística e gestão que reduzem o custo da operação, em parceria com a Move Data.</p></div>
      <div><h5>Bratecon</h5><a href="empresa.html#historia">Nossa história</a><a href="empresa.html#proposito">Missão e visão</a><a href="empresa.html#parceria">Parceria</a><a href="empresa.html#time">Quem constrói</a></div>
      <div><h5>Trabalho</h5><a href="solucoes.html">Soluções</a><a href="metodo.html">Método</a><a href="casos.html">Casos</a><a href="produtos.html">Produtos</a></div>
      <div><h5>Contato</h5><a href="contato.html">Fale com a gente</a><a href="{WA}" target="_blank" rel="noopener">WhatsApp comercial</a><a href="https://instagram.com/bratecon_oficial" target="_blank" rel="noopener">Instagram</a><a href="https://movedata.com.br" target="_blank" rel="noopener">Move Data</a></div>
    </div>
    <div class="sign">
      <div><b>Bratecon</b><span>Murilo Lima · Pedro Rufino</span></div>
      <div><b>Move Data</b><span>Vitor Mendes · Parceria</span></div>
      <div><b>Salvador, Bahia</b><span>Tecnologia &amp; Consultoria</span></div>
    </div>
    <div class="topline"></div>
    <div class="fend" style="border-top:0"><span>© 2026 {seo.CO['legal']} · CNPJ {seo.CO['cnpj']}</span><span>Escritório virtual · {seo.ADDR_LINE}</span></div>
  </div>
</footer>'''

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    css = open(os.path.join(ROOT, 'assets/site.css')).read() + open(os.path.join(ROOT, 'src/extra.css')).read()
    open(os.path.join(OUT, 'assets/site.css'), 'w').write(css)
    for f, key, lbl, title, desc, gl in PAGES:
        body = open(os.path.join(ROOT, 'src/pages', f)).read()
        h = head(f, key, title, desc, f)
        page = (f'{nav(key)}\n<main id="conteudo">\n{body}\n</main>\n{footer()}\n{LIBS}\n' + (GL + '\n' if gl else ''))
        page = page.replace('{WA}', WA).replace('{FONE}', FONE)
        page = page.replace('{FAQ}', seo.faq_html(f)).replace('{RESUMO}', seo.resumo_html())
        page = page.replace('{PRODUCT_RAIL}', product_cards('rail')).replace('{PRODUCT_GRID}', product_cards('produtos'))
        page = page.replace('{WA}', WA).replace('{FONE}', FONE)
        h = h.replace('{FONE}', FONE)
        if MODE == 'artifact' and f == 'index.html':
            html = h + f'\n<div data-page="{key}" data-wa="{WA_NUM}" hidden></div>\n' + page
        else:
            html = (f'<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
                    f'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n{h}\n</head>\n'
                    f'<body data-page="{key}" data-wa="{WA_NUM}">\n{page}</body>\n</html>\n')
        open(os.path.join(OUT, f), 'w').write(html)
    if MODE != 'artifact':
        today = datetime.date.today().isoformat()
        open(os.path.join(OUT, 'robots.txt'), 'w').write(seo.robots())
        open(os.path.join(OUT, 'sitemap.xml'), 'w').write(seo.sitemap(today))
        open(os.path.join(OUT, 'llms.txt'), 'w').write(seo.llms(PRODUCTS, FONE).replace('{FONE}', FONE))
    print('ok', OUT)

build()
