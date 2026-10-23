# Site da Bratecon

Site estático em HTML, CSS e JavaScript, sem framework e sem etapa de bundler. Segue o Design System Bratecon V1.

## Estrutura

| Caminho | O que é |
|---|---|
| `src/pages/*.html` | O conteúdo de cada página (só o miolo, entre o cabeçalho e o rodapé) |
| `build.py` | Monta as páginas: cabeçalho, menu, rodapé, metadados de SEO e o número de contato |
| `assets/site.css` | Estilos do design system usados pelo site |
| `src/extra.css` | Estilos próprios do site (menu, abas, método, placa Em operação, Quem constrói); o build junta com o `site.css` |
| `assets/site.js` | Tema, menu, abas, formulário, rolagem, abertura em vídeo, placa Em operação e fundo de barramento |
| `assets/gl.js` | Cenas 3D (capa com o B e as três máquinas da Clean 24h), carregadas só na Início e em Casos |
| `assets/intro*.mp4` | Abertura em vídeo (desktop e celular) |
| `tools/qa.py` | Checagem automática no navegador |

## Comandos

```bash
python3 build.py            # gera dist/, pronto para a VPS
python3 build.py artifact   # gera artifact/, para publicar a prévia no Claude
python3 tools/qa.py         # abre todas as páginas no navegador e aponta erros
```

## Rodar com Docker

Com o Docker Desktop iniciado e usando contêineres Linux, execute na raiz do projeto:

```bash
docker compose up --build -d
```

Abra http://localhost:8096. A imagem gera o site com Python e serve o conteúdo de `dist/` com Nginx. Não é necessário instalar Python na máquina.

Depois de editar o código, execute o mesmo comando para reconstruir a imagem e atualizar o contêiner.

```bash
docker compose logs -f site   # acompanhar logs
docker compose down           # parar e remover o contêiner
```

A porta fica disponível apenas na própria máquina. Para trocar a porta no PowerShell:

```powershell
$env:PORT = '8096'
docker compose up --build -d
```

Fontes e bibliotecas carregadas de CDNs continuam precisando de acesso à internet no navegador.

## Onde trocar cada coisa

- **WhatsApp comercial:** `WA_NUM` e `FONE` no topo do `build.py`. É o único lugar onde o número aparece.
- **Título e descrição de cada página (SEO):** lista `PAGES` no `build.py`.
- **Duração da abertura:** atributo `data-cut` em `src/pages/index.html` (hoje 8,5 s, antes do clarão branco do vídeo).

## Regras de texto

Sem travessões e sem "tá". Move OS aparece expandido na primeira menção de cada página (Método de Otimização e Valorização Empresarial). Os números da operação de cada cliente não vão para o site.

## Padrão de circuito

Todo circuito do site segue o mesmo desenho, que nasceu na página do Método e foi aprovado como padrão em 23/10/2026:

- Traço fino de 1,5px na cor `--line-strong`; linha ativa um pouco mais clara (`--cx-live`), linha aberta tracejada (4 por 6).
- Dobras sempre a 45°, nunca em curva.
- Nó pequeno em anel (4px) nas dobras; nó grande de 28px com miolo de 8px no destino. Nó com miolo = em operação, anel vazio = conexão possível.
- Pulso com brilho radial no gradiente circuito (`--circ-a` para `--circ-c`), só no que se move.
- Sem barra cheia e sem preenchimento azul em traço.

Implementações: fundo de barramento (`canvas.bus-c` + `busBg` no `site.js`), percurso do método (`.moves`, `.catraca`), placa Em operação (`#board`) e a página A Bratecon, que é um circuito inteiro (`#icBoard`): a história nasce ligada e ligar um trecho acende todos os anteriores. Links diretos `empresa.html#proposito`, `#parceria` e `#time` já chegam com o circuito ligado até ali.

## SEO, GEO e AEO

Tudo o que buscadores e IAs leem sai de `src/seo.py`: dados oficiais da empresa, título e descrição de cada página, FAQ, schema (JSON-LD) e os arquivos `robots.txt`, `sitemap.xml` e `llms.txt`, que o build grava em `dist/`. Regra: só entra fato confirmado.

As imagens de compartilhamento ficam em `assets/og/` e são geradas por `python3 tools/og.py`. Rodar de novo quando um título mudar.

Depois de publicar: cadastrar o site no Google Search Console e no Bing Webmaster Tools, enviar o `sitemap.xml` e testar o schema em https://search.google.com/test/rich-results.
