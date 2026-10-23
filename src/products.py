"""Produtos da Bratecon: fonte única dos cartões da Início (trilho) e da página Produtos (grade).

st: 'live' = com cliente em operação, 'sig' = em evolução ou em breve, None = sem selo de operação.
"""

PRODUCTS = [
    dict(id='frota', name='Frota Pilot', sector='Logística',
         head='<b>4</b> frentes da logística numa plataforma só.',
         text='Rastreamento, telemetria, entregas e gestão de frotas. O veículo aparece no mapa e o dado chega a quem decide.',
         tags=['Rastreamento', 'Telemetria', 'Entregas', 'Frotas'], st=None, label='Disponível', site='https://frotapilot.com.br'),
    dict(id='mdesk', name='Mdesk', sector='Sistema de gestão',
         head='<b>1</b> motor, <b>5</b> edições de setor.',
         text='A operação inteira num sistema próprio, com a identidade de cada empresa. Cada edição já chega pronta para o setor.',
         tags=['Agências', 'Marketing', 'Jurídico', 'SESMT', 'Engenharia'], st='live', label='Com cliente em operação', site='https://mdesk.movedata.com.br'),
    dict(id='barber', name='Barber OS', sector='Barbearias',
         head='<b>6</b> frentes da barbearia num sistema só.',
         text='Agenda, clientes, caixa, equipe, estoque e financeiro no mesmo lugar, para o dono parar de controlar tudo no caderno.',
         tags=['Agenda', 'Caixa', 'Estoque', 'Equipe'], st='live', label='Com cliente em operação', site='https://barberos.bratecon.com'),
    dict(id='kardapo', name='Kardapo', sector='Restaurantes',
         head='Cardápio no QR, <b>0</b> aplicativo para baixar.',
         text='O cliente lê o QR e o cardápio abre no navegador. O restaurante controla produtos, estoque e pedidos em tempo real, do celular.',
         tags=['QR code', 'Pedidos', 'Estoque'], st=None, label='Disponível', site='https://kardapo.bratecon.com'),
    dict(id='finance', name='Finance', sector='Gestão financeira',
         head='O financeiro da empresa num lugar <b>só</b>.',
         text='Gestão financeira construída na parceria. A primeira versão está em desenvolvimento.',
         tags=['Financeiro'], st='sig', label='Em evolução', site='https://finance.bratecon.com'),
    dict(id='easydoor', name='EasyDoor e MLINK', logos=['easydoor', 'mlink'], sector='Em breve',
         head='Dois lançamentos <b>em breve</b>.',
         text='EasyDoor e MLINK estão em evolução na parceria. Deixe o contato e avisamos quando estiverem prontos.',
         tags=[], st='sig', label='Em breve', site=None),
]

BUS_SVG = ('<svg class="bus" viewBox="0 0 120 120" aria-hidden="true"><path d="M6 114 V6 H114"/>'
           '<path d="M18 114 V18 H114"/><path d="M30 114 V48 L48 30 H114"/>'
           '<circle cx="30" cy="114" r="5"/><circle cx="114" cy="6" r="5"/></svg>')

ARROW = '<span class="ar"><i data-lucide="{0}"></i><i data-lucide="{0}"></i></span>'


def product_cards(where):
    """where='rail' liga para produtos.html#id; where='produtos' abre a aba na própria página."""
    out = []
    for p in PRODUCTS:
        if p.get('logos'):
            mark = ''.join(f'<img src="assets/img/{l}.webp" alt="{l.capitalize() if l != "mlink" else "MLINK"}" loading="lazy">' for l in p['logos'])
        else:
            mark = f'<i aria-hidden="true"></i>{p["name"]}'
        st = p['st']
        cls = {'live': '', 'sig': ' sig', None: ' none'}[st]
        dot = {'live': 'sdot live', 'sig': 'sdot sig', None: 'sdot'}[st]
        if p['site'] is None:
            link = '<a class="alink" href="contato.html"><u>Quero ser avisado</u>' + ARROW.format('arrow-right') + '</a>'
        elif where == 'produtos':
            link = f'<a class="alink" href="#{p["id"]}"><u>Por dentro</u>' + ARROW.format('arrow-down') + '</a>'
        else:
            link = f'<a class="alink" href="produtos.html#{p["id"]}"><u>Conhecer</u>' + ARROW.format('arrow-right') + '</a>'
        tags = ''.join(f'<li>{t}</li>' for t in p['tags'])
        tags = f'<ul class="ptags">{tags}</ul>' if tags else ''
        out.append(
            f'<article class="prod" data-st="{st or ""}">{BUS_SVG}'
            f'<div class="pmark">{mark}</div><span class="psec">{p["sector"]}</span>'
            f'<h3 class="phl">{p["head"]}</h3><p class="ptext">{p["text"]}</p>{tags}'
            f'<div class="pfoot"><span class="pst{cls}"><span class="{dot}"></span>{p["label"]}</span>{link}</div>'
            '</article>')
    return '\n'.join(out)
