#!/usr/bin/env python3
"""Gera as imagens de compartilhamento (og:image) de cada página, 1200x630, no padrão do design system.

Uso:  python3 tools/og.py   ->  assets/og/<chave>.png e assets/og/logo.png
Rodar de novo só quando um título mudar. As imagens ficam versionadas em assets/og/.
"""
import asyncio, base64, os
from PIL import Image
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'og')
IMG = os.path.join(ROOT, 'assets', 'img')

CARDS = {
    'inicio':   ('Engenharia da operação', 'Tecnologia, automação e logística em <em>Salvador</em>.'),
    'empresa':  ('A Bratecon', 'Tecnologia e consultoria perto da <em>operação</em>.'),
    'solucoes': ('Soluções', 'Automação, logística e sistemas <em>sob medida</em>.'),
    'metodo':   ('Método Move OS', 'Cinco movimentos numa <em>ordem</em> que não se pula.'),
    'casos':    ('Casos', 'Clean 24h e BahiaFix, em <em>operação</em>.'),
    'produtos': ('Produtos', 'Frota Pilot, Mdesk, Barber OS e <em>Kardapo</em>.'),
    'contato':  ('Contato', 'Todo projeto começa pela <em>escuta</em>.'),
}


def b64(name):
    return 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(IMG, name), 'rb').read()).decode()


TPL = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,300..900;1,62..125,300..900&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;background:#061425;color:#E9F1F9;font-family:Archivo,Arial,sans-serif;position:relative}
.glow{position:absolute;left:-200px;top:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(52,117,221,.38),transparent 62%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:48px 48px;-webkit-mask:radial-gradient(80% 90% at 30% 40%,#000,transparent)}
.b{position:absolute;right:-120px;top:-90px;height:820px;aspect-ratio:889/1000;transform:rotate(-9deg);background:linear-gradient(155deg,#3475DD,#214C91 75%);-webkit-mask:url(MASK) center/contain no-repeat;opacity:.34}
.logo{position:absolute;left:72px;top:64px;height:34px}
.k{position:absolute;left:72px;top:212px;font:500 18px/1 'IBM Plex Mono',monospace;letter-spacing:.24em;text-transform:uppercase;color:#4FA3E3;display:flex;gap:16px;align-items:center}
.k:before{content:"";width:34px;height:2px;background:#4FA3E3}
h1{position:absolute;left:72px;top:258px;width:860px;font-weight:880;font-stretch:108%;font-size:72px;line-height:1.02;letter-spacing:-.03em}
h1 em{font-style:italic;font-weight:300;color:#8AC8F6}
.f{position:absolute;left:72px;right:72px;bottom:56px;display:flex;justify-content:space-between;align-items:center;font:500 17px/1 'IBM Plex Mono',monospace;letter-spacing:.16em;text-transform:uppercase;color:#9AB2C9}
svg{position:absolute;left:0;bottom:104px;width:1200px;height:60px}
</style></head><body>
<div class="glow"></div><div class="grid"></div><div class="b"></div>
<img class="logo" src="LOGO">
<svg viewBox="0 0 1200 60"><path d="M72 30 H520 L548 6 H760" fill="none" stroke="#56789E" stroke-width="2"/><path d="M72 30 H300" fill="none" stroke="#31EAA9" stroke-width="2.5"/><circle cx="760" cy="6" r="6" fill="#061425" stroke="#56789E" stroke-width="2"/><circle cx="300" cy="30" r="7" fill="#31EAA9"/></svg>
<div class="k">KICK</div><h1>TITLE</h1>
<div class="f"><span>bratecon.com</span><span>Salvador · Bahia</span></div>
</body></html>"""


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        for key, (kick, title) in CARDS.items():
            html = TPL.replace('MASK', b64('b-mask.webp')).replace('LOGO', b64('logo-h-branco.webp')).replace('KICK', kick).replace('TITLE', title)
            await pg.set_content(html, wait_until='networkidle')
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=os.path.join(OUT, key + '.png'))
            print('ok', key)
        await b.close()
    # logo quadrado para o schema da empresa
    sym = Image.open(os.path.join(IMG, 'simbolo-cor.webp')).convert('RGBA')
    canvas = Image.new('RGBA', (512, 512), (255, 255, 255, 255))
    sym.thumbnail((380, 380))
    canvas.alpha_composite(sym, ((512 - sym.width) // 2, (512 - sym.height) // 2))
    canvas.convert('RGB').save(os.path.join(OUT, 'logo.png'), optimize=True)
    # comprime para ficar leve no WhatsApp e no LinkedIn (abaixo de ~300 KB)
    for key in CARDS:
        f = os.path.join(OUT, key + '.png')
        Image.open(f).convert('RGB').quantize(colors=192, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG).save(f, optimize=True)
    print('ok logo')

asyncio.run(main())
