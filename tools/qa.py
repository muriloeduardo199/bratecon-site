#!/usr/bin/env python3
"""Checagem do site no navegador: todas as páginas, desktop e celular, tema Noite e Papel.

Uso:  python3 build.py && python3 tools/qa.py
Sobe um servidor local em dist/, abre cada página com Playwright e falha se encontrar
erro de script, rolagem lateral ou imagem quebrada. As capturas ficam em qa/.
"""
import asyncio, os, sys, threading, http.server, functools
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST, OUT, PORT = os.path.join(ROOT, 'dist'), os.path.join(ROOT, 'qa'), 8799
PAGES = ['index', 'empresa', 'solucoes', 'metodo', 'casos', 'produtos', 'contato']
VIEWS = [('desk', 1440, 900), ('mob', 390, 844)]

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=DIST)
    http.server.ThreadingHTTPServer(('127.0.0.1', PORT), h).serve_forever()

async def main():
    os.makedirs(OUT, exist_ok=True)
    threading.Thread(target=serve, daemon=True).start()
    fails = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'])
        for page in PAGES:
            for name, w, h in VIEWS:
                for theme in ('dark', 'light'):
                    tag = f'{page}-{name}-{theme}'
                    pg = await b.new_page(viewport={'width': w, 'height': h})
                    pg.on('pageerror', lambda e, t=tag: fails.append(f'{t}: erro de script: {e}'))
                    await pg.add_init_script("try{sessionStorage.setItem('bt-intro','1');" + ("localStorage.setItem('bt-theme','light')" if theme == 'light' else "localStorage.removeItem('bt-theme')") + "}catch(e){}")
                    await pg.goto(f'http://127.0.0.1:{PORT}/{page}.html', wait_until='networkidle')
                    await pg.wait_for_timeout(900)
                    sw = await pg.evaluate('document.documentElement.scrollWidth')
                    if sw > w: fails.append(f'{tag}: rolagem lateral ({sw}px)')
                    broken = await pg.evaluate("[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&!i.closest('[hidden]')).map(i=>i.getAttribute('src'))")
                    if broken: fails.append(f'{tag}: imagem quebrada {broken}')
                    if theme == 'dark': await pg.screenshot(path=os.path.join(OUT, tag + '.png'))
                    await pg.close()
        await b.close()
    print('\n'.join(fails) if fails else f'ok: {len(PAGES) * len(VIEWS) * 2} combinações sem erro')
    sys.exit(1 if fails else 0)

asyncio.run(main())
