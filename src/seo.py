"""SEO, GEO e AEO da Bratecon: fonte única dos dados oficiais, metadados, FAQ e schema.

Tudo o que buscadores e IAs leem sai daqui: título e descrição de cada página, JSON-LD,
FAQ (HTML e FAQPage), bloco "Em resumo", llms.txt, sitemap.xml e robots.txt.
Regra: só entra fato confirmado. O que não foi confirmado fica fora, sem chute.
"""
import json, html

SITE = 'https://www.bratecon.com/'

CO = dict(
    name='Bratecon',
    legal='Bratecon Serviços de Tecnologia Ltda.',
    cnpj='65.842.938/0001-02',
    founded='2026-03-20', founded_br='20/03/2026', year='2026',
    cnae='Desenvolvimento e licenciamento de programas de computador customizáveis (CNAE 6202-3/00)',
    street='Avenida Tancredo Neves, 2539', district='Caminho das Árvores',
    city='Salvador', state='BA', cep='41820-021', country='BR',
    phone='+55-71-99239-1326',
    instagram='https://instagram.com/bratecon_oficial',
    partner=('Move Data', 'https://movedata.com.br'),
)
ADDR_LINE = f"{CO['street']}, {CO['district']}, {CO['city']}, {CO['state']}, CEP {CO['cep'][:2]}.{CO['cep'][2:]}"
IDENTITY = ('A Bratecon é uma empresa de tecnologia e consultoria de Salvador, na Bahia, fundada em 2026. Trabalha 100% de forma remota e atende empresas dentro e fora da Bahia. '
            'Desenvolve automação de processos, sistemas de logística e gestão de frotas, integração de dados, '
            'agentes de IA e sistemas sob medida, sempre medidos pelo custo da operação do cliente. '
            'Trabalha em parceria com a Move Data e conduz cada projeto pelo método Move OS.')

# arquivo: (título, descrição, nome curto para a trilha)
META = {
    'index.html':    ('Bratecon | Tecnologia, automação e logística em Salvador',
                      'Empresa de tecnologia e consultoria em Salvador. Automação, logística, agentes de IA, engenharia de dados e sistemas sob medida que reduzem o custo da operação.',
                      'Início'),
    'empresa.html':  ('Sobre a Bratecon | Empresa de tecnologia em Salvador',
                      'Bratecon Serviços de Tecnologia, em Salvador desde 2026: história, missão, visão e valores, a parceria com a Move Data e quem constrói cada projeto.',
                      'A Bratecon'),
    'solucoes.html': ('Automação, logística e sistemas sob medida | Bratecon',
                      'Logística e gestão de frotas, automação de processos, integração de dados, agentes de IA no WhatsApp, consultoria e sistemas sob medida para empresas.',
                      'Soluções'),
    'metodo.html':   ('Move OS, o método de cada projeto | Bratecon',
                      'O Move OS, Método de Otimização e Valorização Empresarial: cinco movimentos em ordem, cada um com uma entrega que o cliente confere sozinho.',
                      'Método'),
    'casos.html':    ('Casos de clientes: Clean 24h e BahiaFix | Bratecon',
                      'Como a Bratecon levou o sistema da Clean 24h para um banco central em tempo real e colocou o marketing da BahiaFix no Mdesk.',
                      'Casos'),
    'produtos.html': ('Frota Pilot, Mdesk e sistemas prontos | Bratecon',
                      'Frota Pilot para logística, Mdesk para gestão, Barber OS para barbearias e Kardapo para restaurantes: sistemas prontos com a marca da sua empresa.',
                      'Produtos'),
    'contato.html':  ('Contato e WhatsApp | Bratecon em Salvador',
                      'Fale com a Bratecon pelo WhatsApp (71) 99239-1326. Atendimento 100% remoto, para empresas da Bahia e de outros estados. A primeira conversa não tem compromisso.',
                      'Contato'),
}

# Perguntas frequentes. Resposta na primeira frase, até ~60 palavras, só fatos confirmados.
FAQ = {
    'index.html': ('Perguntas frequentes', 'O que as pessoas perguntam <em class="it">antes</em> de começar.', [
        ('O que a Bratecon faz?',
         'A Bratecon desenvolve tecnologia para a operação das empresas: automação de processos, sistemas de logística e gestão de frotas, integração de dados, agentes de IA e sistemas sob medida. Cada solução é medida pelo custo e pela eficiência da operação do cliente.'),
        ('Onde fica a Bratecon?',
         f'A Bratecon trabalha 100% de forma remota, com escritório virtual em Salvador, na {CO["street"]}, {CO["district"]}. O primeiro contato é pelo WhatsApp comercial, {{FONE}}, e quem responde é um diretor da Bratecon.'),
        ('A Bratecon atende empresas fora da Bahia?',
         'Sim. Como a Bratecon trabalha 100% de forma remota, atende empresas da Bahia e de outros estados do mesmo jeito: escuta, acompanhamento e entregas acontecem a distância.'),
        ('Vocês aproveitam um sistema que a minha equipe já começou?',
         'Sim. Aproveitamos o que já funciona e levamos para produção. Foi o que aconteceu com a Clean 24h: o sistema feito com IA rodava em cada computador e passou a rodar num banco central, com login individual e atualização em tempo real.'),
        ('Qual a relação entre a Bratecon e a Move Data?',
         'Bratecon e Move Data são parceiras. As duas decidem juntas e constroem juntas, sem repassar trabalho uma para a outra. Mdesk e Frota Pilot são produtos da parceria, e o método Move OS conduz os projetos das duas.'),
        ('Como começo um projeto com a Bratecon?',
         'Todo projeto começa pela escuta, uma conversa sem compromisso sobre como a sua operação funciona hoje. Você chama no WhatsApp, conta o ponto de partida e a área que mais pesa no custo, e um diretor da Bratecon responde.'),
    ]),
    'solucoes.html': ('Perguntas frequentes', 'Dúvidas sobre as <em class="it">soluções</em>.', [
        ('Que tipo de empresa a Bratecon atende?',
         'Empresas de qualquer porte ou segmento. O site não é dividido por setor porque o critério é sempre o mesmo: onde a operação perde tempo e dinheiro. A Bratecon começa pela logística, pelo transporte e pela gestão.'),
        ('Quanto custa um projeto?',
         'O valor é definido depois da escuta, quando já sabemos o que existe na sua operação e o que falta. A Bratecon não tem tabela pública, e a primeira conversa não tem compromisso.'),
        ('Quanto tempo leva um projeto?',
         'O prazo também é definido depois da escuta, porque depende do que já existe. A entrega é feita por partes, e a equipe usa o sistema desde a primeira versão, com cada mudança registrada.'),
        ('A Bratecon faz agentes de IA para WhatsApp?',
         'Sim. Os agentes respondem no WhatsApp e nos sistemas internos com a informação real da operação, como pedidos, estoque ou agenda, e registram cada conversa. Quando o caso pede uma pessoa, a conversa chega a ela com o histórico.'),
        ('Vocês integram com o ERP e as planilhas que a empresa já usa?',
         'Sim. ERP, CRM, PDV, planilhas e sistemas próprios passam a trocar dados com uma base central em horário marcado, e ninguém precisa digitar a mesma informação duas vezes.'),
    ]),
    'metodo.html': ('Perguntas frequentes', 'O que é o Move OS, <em class="it">direto</em>.', [
        ('O que é o Move OS?',
         'O Move OS, Método de Otimização e Valorização Empresarial, é o método que conduz todo projeto da Bratecon. São cinco movimentos em ordem, Escuta, Montagem, Identidade, Diferença e Rito, e cada um termina com uma entrega que o cliente confere sozinho.'),
        ('Quem criou o Move OS?',
         'O Move OS foi desenvolvido com a Move Data, parceira da Bratecon, e as duas empresas trabalham com ele.'),
        ('O que acontece se um movimento não ficar pronto?',
         'O próximo não começa. Essa é a regra do portão: um movimento só abre quando o anterior entregou algo que o cliente consegue conferir sozinho.'),
        ('O que a minha operação ensina vai para outros clientes?',
         'Só o que serve para o setor inteiro. Uma solução para um problema do mercado entra no motor e chega a todos. Estratégia, dados, precificação e funil de cada cliente nunca saem do ambiente dele.'),
    ]),
    'produtos.html': ('Perguntas frequentes', 'Dúvidas sobre os <em class="it">produtos</em>.', [
        ('O que é o Frota Pilot?',
         'O Frota Pilot é a plataforma de logística da parceria entre Bratecon e Move Data. Reúne rastreamento, telemetria, entregas e gestão de frotas num lugar só.'),
        ('O que é o Mdesk?',
         'O Mdesk é um sistema de gestão com um motor e cinco edições por setor: Agências, Marketing, Jurídico, SESMT e Engenharia. A BahiaFix usa a edição Marketing.'),
        ('Posso usar os produtos com a marca da minha empresa?',
         'Sim. Cada produto recebe a identidade e as regras da sua empresa, e o trabalho começa do que já está pronto.'),
        ('O Kardapo precisa de aplicativo?',
         'Não. O cliente lê o QR code e o cardápio abre no navegador. O restaurante controla produtos, estoque e pedidos em tempo real, do celular.'),
    ]),
}


def faq_html(page):
    if page not in FAQ:
        return ''
    eyebrow, h2, items = FAQ[page]
    qs = '\n'.join(
        f'<details class="qa"{" open" if i == 0 else ""}><summary><i class="qn" aria-hidden="true"></i><h3>{html.escape(q)}</h3>'
        f'<span class="qi" aria-hidden="true"></span></summary><div class="qa-a"><p>{html.escape(a)}</p></div></details>'
        for i, (q, a) in enumerate(items))
    return (f'<section class="sec" id="faq">\n  <div class="wrap faqw">\n    <div class="sechead"><span class="num">{eyebrow}</span>'
            f'<h2 class="h2">{h2}</h2></div>\n    <div class="faq">\n{qs}\n    </div>\n  </div>\n</section>')


def resumo_html():
    rows = [('Razão social', CO['legal']), ('CNPJ', CO['cnpj']), ('Fundação', CO['founded_br']),
            ('Escritório virtual', ADDR_LINE), ('Atividade', CO['cnae']), ('Parceria', 'Move Data, com o método Move OS'),
            ('Atendimento', '100% remoto, pelo WhatsApp {FONE}')]
    dl = ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in rows)
    return (f'<div class="resumo"><div class="rs-txt"><span class="eyebrow line">Em resumo</span><p class="rs-id">{IDENTITY}</p></div>'
            f'<dl class="rs-dl">{dl}</dl></div>')


# ---------- JSON-LD
ORG_ID = SITE + '#org'
PEOPLE = [
    dict(id='murilo', name='Murilo Lima', job='Cofundador e diretor', org='bt',
         desc='Mestrando em Ciência da Computação na UFBA, com MBA em Engenharia de Software e pós-graduação em Big Data. Especialista em integração e orquestração de dados.',
         about=['Engenharia de software', 'Integração de dados', 'Governança de dados']),
    dict(id='pedro', name='Pedro Rufino', job='Cofundador e diretor', org='bt',
         desc='Desenvolve redes neurais desde os 15 anos e atua em projetos full stack, com visão computacional, NLP e modelos de linguagem.',
         about=['Inteligência artificial', 'Desenvolvimento full stack', 'Design de interface']),
    dict(id='vitor', name='Vitor Mendes', job='Fundador da Move Data', org='md',
         desc='Formado em Redes, com MBAs em Telecomunicações e em Business Intelligence.',
         about=['Infraestrutura', 'Dados', 'Estratégia']),
]


def org():
    return {
        '@type': 'ProfessionalService', '@id': ORG_ID, 'name': CO['name'], 'legalName': CO['legal'],
        'alternateName': 'Bratecon Tecnologia & Consultoria', 'url': SITE,
        'logo': SITE + 'assets/og/logo.png', 'image': SITE + 'assets/og/inicio.png',
        'description': IDENTITY, 'slogan': 'Transformamos desafios em soluções. Tecnologia em resultados.',
        'taxID': CO['cnpj'], 'foundingDate': CO['founded'], 'telephone': CO['phone'],
        'address': {'@type': 'PostalAddress', 'streetAddress': f"{CO['street']}, {CO['district']}",
                    'addressLocality': CO['city'], 'addressRegion': CO['state'], 'postalCode': CO['cep'], 'addressCountry': CO['country']},
        'areaServed': {'@type': 'Country', 'name': 'Brasil'},
        'founder': [{'@id': SITE + 'empresa.html#murilo'}, {'@id': SITE + 'empresa.html#pedro'}],
        'sameAs': [CO['instagram']],
        'knowsAbout': ['Automação de processos', 'Logística', 'Gestão de frotas', 'Telemetria', 'Engenharia de dados',
                       'Integração de sistemas', 'Agentes de IA', 'Consultoria em tecnologia', 'Desenvolvimento de software sob medida'],
        'contactPoint': {'@type': 'ContactPoint', 'telephone': CO['phone'], 'contactType': 'sales', 'availableLanguage': 'Portuguese'},
    }


def person(p):
    works = {'@id': ORG_ID} if p['org'] == 'bt' else {'@type': 'Organization', 'name': CO['partner'][0], 'url': CO['partner'][1]}
    return {'@type': 'Person', '@id': SITE + 'empresa.html#' + p['id'], 'name': p['name'], 'jobTitle': p['job'],
            'worksFor': works, 'description': p['desc'], 'knowsAbout': p['about'],
            'image': SITE + f"assets/img/{p['id']}.webp"}


def jsonld(page, products):
    url = SITE + ('' if page == 'index.html' else page)
    title, desc, crumb = META[page]
    g = [org(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': title, 'description': desc,
                 'inLanguage': 'pt-BR', 'isPartOf': {'@id': SITE + '#site'}, 'about': {'@id': ORG_ID},
                 'primaryImageOfPage': SITE + 'assets/og/' + page.replace('.html', '') + '.png'}]
    if page == 'index.html':
        g.append({'@type': 'WebSite', '@id': SITE + '#site', 'url': SITE, 'name': 'Bratecon', 'inLanguage': 'pt-BR', 'publisher': {'@id': ORG_ID}})
    else:
        g.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Início', 'item': SITE},
            {'@type': 'ListItem', 'position': 2, 'name': crumb, 'item': url}]})
    if page == 'empresa.html':
        g += [person(p) for p in PEOPLE]
    if page == 'metodo.html':
        g.append({'@type': 'DefinedTerm', '@id': SITE + 'metodo.html#move-os', 'name': 'Move OS',
                  'alternateName': 'Método de Otimização e Valorização Empresarial',
                  'description': 'Método de cinco movimentos em ordem (Escuta, Montagem, Identidade, Diferença e Rito), em que cada movimento termina com uma entrega que o cliente confere sozinho. Desenvolvido com a Move Data e usado pela Bratecon e pela Move Data.',
                  'url': SITE + 'metodo.html'})
    if page == 'produtos.html':
        g.append({'@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'item': {
                '@type': 'SoftwareApplication', 'name': p['name'], 'applicationCategory': 'BusinessApplication',
                'operatingSystem': 'Web', 'description': p['text'], 'provider': {'@id': ORG_ID},
                **({'url': p['site']} if p.get('site') else {})}}
            for i, p in enumerate(products) if p['id'] != 'easydoor']})
    if page in FAQ:
        g.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ[page][2]]})
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False) + '</script>'


# ---------- arquivos para robôs
def robots():
    return ('User-agent: *\nAllow: /\n\n'
            '# Buscadores de IA também são bem-vindos\nUser-agent: GPTBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\n'
            'User-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\n'
            f'Sitemap: {SITE}sitemap.xml\n')


def sitemap(date):
    pri = {'index.html': '1.0', 'solucoes.html': '0.9', 'produtos.html': '0.9', 'metodo.html': '0.8',
           'empresa.html': '0.8', 'casos.html': '0.8', 'contato.html': '0.7'}
    urls = ''.join(f'  <url><loc>{SITE}{"" if p == "index.html" else p}</loc><lastmod>{date}</lastmod><priority>{pri[p]}</priority></url>\n' for p in META)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'


def llms(products, fone):
    prods = '\n'.join(f"- **{p['name']}** ({p['sector']}): {p['text']}" + (f" {p['site']}" if p.get('site') else '') for p in products)
    qa = '\n\n'.join(f'### {q}\n{a}' for pg in FAQ.values() for q, a in pg[2])
    return f"""# Bratecon

> {IDENTITY}

## Dados oficiais
- Razão social: {CO['legal']}
- CNPJ: {CO['cnpj']}
- Fundação: {CO['founded_br']}
- Atendimento: 100% remoto, para empresas da Bahia e de outros estados
- Escritório virtual: {ADDR_LINE}
- Atividade principal: {CO['cnae']}
- WhatsApp comercial: {fone}
- Instagram: {CO['instagram']}
- Parceira: Move Data ({CO['partner'][1]})

## Páginas
- [Início]({SITE}): o que a Bratecon faz e para quem
- [A Bratecon]({SITE}empresa.html): história, missão, visão, valores, parceria e equipe
- [Soluções]({SITE}solucoes.html): logística e transporte, automação, dados e integração, agentes de IA, consultoria e sistemas sob medida
- [Método]({SITE}metodo.html): o Move OS, cinco movimentos em ordem
- [Casos]({SITE}casos.html): Clean 24h e BahiaFix
- [Produtos]({SITE}produtos.html): Frota Pilot, Mdesk, Barber OS, Kardapo, Finance, EasyDoor e MLINK
- [Contato]({SITE}contato.html): WhatsApp e endereço

## Equipe
- Murilo Lima, cofundador e diretor da Bratecon: engenharia, integração e governança de dados.
- Pedro Rufino, cofundador e diretor da Bratecon: inteligência artificial, full stack e design.
- Vitor Mendes, fundador da Move Data, parceira da Bratecon: infraestrutura, dados e estratégia.

## Método Move OS
Método de Otimização e Valorização Empresarial. Cinco movimentos em ordem: Escuta, Montagem, Identidade, Diferença e Rito. Cada movimento termina com uma entrega que o cliente confere sozinho, e o seguinte só começa depois dela.

## Produtos
{prods}

## Perguntas frequentes

{qa}
"""
