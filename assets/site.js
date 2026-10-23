(function(){
"use strict";
var D=document,H=D.documentElement;
H.classList.add('js');
var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
var $=function(s,c){return (c||D).querySelector(s)};
var $$=function(s,c){return Array.prototype.slice.call((c||D).querySelectorAll(s))};
var WA=(function(){var l=D.querySelector('[data-wa]');return l?l.getAttribute('data-wa'):''})();
var pk=D.querySelector('[data-page]'),PAGE=pk?pk.getAttribute('data-page'):'';

if(window.lucide)lucide.createIcons({attrs:{'stroke-width':1.5}});

/* Tema: Noite é o padrão da marca; a escolha fica neste navegador */
function setTheme(t){
  if(t==='light')H.setAttribute('data-theme','light');else H.removeAttribute('data-theme');
  $$('[data-theme-set]').forEach(function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-theme-set')===t))});
  try{localStorage.setItem('bt-theme',t)}catch(e){}
}
$$('[data-theme-set]').forEach(function(b){b.addEventListener('click',function(){setTheme(b.getAttribute('data-theme-set'))})});
var saved=null;try{saved=localStorage.getItem('bt-theme')}catch(e){}
setTheme(saved==='light'?'light':'dark');

/* Menu: página atual marcada, painel em tela cheia no celular e pelo botão */
$$('[data-nav]').forEach(function(a){if(a.getAttribute('data-nav')===PAGE){a.classList.add('on');a.setAttribute('aria-current','page')}});
var menu=$('#menu'),mbtn=$('#menuBtn'),mclose=$('#menuClose');
function openMenu(o){if(!menu)return;menu.hidden=!o;H.classList.toggle('menu-open',o);mbtn&&mbtn.setAttribute('aria-expanded',String(o));
  if(window.__lenis){o?window.__lenis.stop():window.__lenis.start()}
  if(o){var f=$('.mitem.on',menu)||$('.mitem',menu);f&&f.focus();if(!RM&&window.gsap)gsap.from($$('.mitem',menu),{yPercent:40,opacity:0,duration:.7,stagger:.05,ease:'expo.out'})}else{mbtn&&mbtn.focus()}}
mbtn&&mbtn.addEventListener('click',function(){openMenu(true)});
mclose&&mclose.addEventListener('click',function(){openMenu(false)});
D.addEventListener('keydown',function(e){if(e.key==='Escape'&&menu&&!menu.hidden)openMenu(false)});

/* Abas: fundo deslizante, teclado e link direto (#token) */
var tabSets=$$('[data-tabs]');
function placeBg(set){var bg=$('.bg',set.bar),b=$('[aria-selected="true"]',set.bar);if(!bg||!b)return;bg.style.width=b.offsetWidth+'px';bg.style.transform='translateX('+(b.offsetLeft-5)+'px)'}
function selectTab(set,btn,focus,fromHash){
  set.tabs.forEach(function(t){var on=t===btn;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;var p=D.getElementById(t.getAttribute('aria-controls'));if(p)p.hidden=!on});
  placeBg(set);if(focus)btn.focus();
  btn.scrollIntoView&&btn.scrollIntoView({block:'nearest',inline:'center'});
  var p=D.getElementById(btn.getAttribute('aria-controls'));
  if(p&&!RM&&window.gsap&&!fromHash)gsap.from(p.children,{y:16,opacity:0,duration:.6,stagger:.06,ease:'power3.out'});
  if(window.ScrollTrigger)ScrollTrigger.refresh();
}
tabSets.forEach(function(el){
  var set={el:el,bar:$('[role="tablist"]',el),tabs:$$('[role="tab"]',el)};el.__set=set;
  set.tabs.forEach(function(t,i){
    t.addEventListener('click',function(){selectTab(set,t,false);try{history.replaceState(null,'','#'+t.id.replace(/^tab-/,''))}catch(e){}});
    t.addEventListener('keydown',function(e){var k=e.key,n=null;if(k==='ArrowRight')n=set.tabs[(i+1)%set.tabs.length];else if(k==='ArrowLeft')n=set.tabs[(i-1+set.tabs.length)%set.tabs.length];else if(k==='Home')n=set.tabs[0];else if(k==='End')n=set.tabs[set.tabs.length-1];if(n){e.preventDefault();selectTab(set,n,true)}});
  });
  requestAnimationFrame(function(){placeBg(set)});
});
addEventListener('resize',function(){tabSets.forEach(function(el){placeBg(el.__set)})});
function tabFromHash(){var h=(location.hash||'').slice(1);if(!h)return false;var t=D.getElementById('tab-'+h);if(!t)return false;var el=t.closest('[data-tabs]');selectTab(el.__set,t,false,true);return el}
var hashTabs=tabFromHash();
addEventListener('hashchange',function(){var el=tabFromHash();if(el)el.scrollIntoView({behavior:'smooth'})});

/* Formulário: escolhas viram mensagem pronta */
(function(){
  var f=$('#cfg');if(!f)return;
  function val(g){var b=$('[data-g="'+g+'"] [aria-pressed="true"]',f);return b?b.textContent:''}
  function upd(){var e=$('#empresa').value.trim();var msg='Olá, Bratecon. Vim pelo site e quero começar pela escuta. Ponto de partida: '+val('ponto')+'. Área: '+val('area')+'.'+(e?' Empresa: '+e+'.':'');$('#send').href='https://wa.me/'+WA+'?text='+encodeURIComponent(msg)}
  $$('.optrow',f).forEach(function(r){r.addEventListener('click',function(ev){var b=ev.target.closest('.opt');if(!b)return;$$('.opt',r).forEach(function(o){o.setAttribute('aria-pressed',String(o===b))});upd()})});
  var pre=(location.hash||'').slice(1);$$('[data-g="area"] .opt',f).forEach(function(o){if(o.getAttribute('data-k')===pre){$$('[data-g="area"] .opt',f).forEach(function(x){x.setAttribute('aria-pressed',String(x===o))})}});
  $('#empresa').addEventListener('input',upd);f.addEventListener('submit',function(e){e.preventDefault()});upd();
})();
$$('[data-copy]').forEach(function(b){b.addEventListener('click',function(){var t=D.getElementById(b.getAttribute('data-copy'));function ok(){b.textContent='Copiado';setTimeout(function(){b.textContent='Copiar'},1600)}function pick(){var r=D.createRange();r.selectNodeContents(t);var s=getSelection();s.removeAllRanges();s.addRange(r)}try{navigator.clipboard.writeText(t.textContent).then(ok,pick)}catch(e){pick()}})});


/* Cabeçalho muda ao sair do topo */
(function(){var nav=$('#nav'),top=$('#top');if(!nav||!top)return;new IntersectionObserver(function(es){nav.classList.toggle('scrolled',!es[0].isIntersecting)},{rootMargin:'-80px 0px 0px 0px'}).observe(top)})();

/* Título da sala e manifesto */
var roomChars=[];(function(){var rh=$('#roomH');if(!rh)return;var txt=rh.textContent;rh.textContent='';txt.split(' ').forEach(function(w,i,arr){var wd=D.createElement('span');wd.style.whiteSpace='nowrap';wd.style.display='inline-block';w.split('').forEach(function(c){var sp=D.createElement('span');sp.className='ch';sp.textContent=c;wd.appendChild(sp);roomChars.push(sp)});rh.appendChild(wd);if(i<arr.length-1)rh.appendChild(D.createTextNode(' '))})})();
var kWords=[];(function(){var k=$('#karaoke');if(!k)return;var t=k.textContent.trim();k.textContent='';t.split(' ').forEach(function(w,i,a){var s=D.createElement('span');s.className='w';s.textContent=w;k.appendChild(s);kWords.push(s);if(i<a.length-1)k.appendChild(D.createTextNode(' '))})})();


/* Padrão de barramento (herança MM) como fundo de seção.
   Trilhas paralelas com dobra em 45°, nós em anel e pulsos no gradiente circuito:
   o gradiente só aparece no que se move. */
function busBg(c){
  var ctx=c.getContext('2d'),W=0,Hh=0,L=[],on=false,raf=0;
  function cv(n){return getComputedStyle(H).getPropertyValue(n).trim()}
  function rnd(i){var x=Math.sin(i*99.13)*43758.5453;return x-Math.floor(x)}
  function build(){var d=Math.min(devicePixelRatio,2);W=c.clientWidth;Hh=c.clientHeight;c.width=W*d;c.height=Hh*d;ctx.setTransform(d,0,0,d,0,0);L=[];
    var gap=W<700?26:30,n=Math.floor((Hh-20)/gap);
    for(var i=0;i<n;i++){var y=14+i*gap,r=rnd(i+1),b1=W*(.12+.5*r),dy=(i%2?1:-1)*(gap*.8),b2=b1+W*(.18+.25*rnd(i+7));
      var pts=[[-10,y],[b1,y],[b1+Math.abs(dy),y+dy],[b2,y+dy]];
      if(rnd(i+3)>.45){pts.push([b2+Math.abs(dy),y],[W+10,y])}else pts.push([W+10,y+dy]);
      L.push({pts:pts,node:rnd(i+5)>.55,pulse:rnd(i+11)>.62,off:rnd(i+13),sp:.6+rnd(i+17)*.7})}}
  function len(p){var s=0;for(var i=1;i<p.length;i++)s+=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]);return s}
  function at(p,u){var t=u*len(p);for(var i=1;i<p.length;i++){var sl=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]);if(t<=sl){var k=t/sl;return[p[i-1][0]+(p[i][0]-p[i-1][0])*k,p[i-1][1]+(p[i][1]-p[i-1][1])*k]}t-=sl}return p[p.length-1]}
  function draw(t){ctx.clearRect(0,0,W,Hh);var line=cv('--line'),ls=cv('--line-strong'),bg=cv('--ground'),a=cv('--circ-a'),cc=cv('--circ-c');
    L.forEach(function(l){ctx.strokeStyle=line;ctx.lineWidth=1.4;ctx.beginPath();l.pts.forEach(function(p,k){k?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1])});ctx.stroke();
      if(l.node){var e=l.pts[3];ctx.beginPath();ctx.arc(e[0],e[1],4.2,0,7);ctx.fillStyle=bg;ctx.fill();ctx.strokeStyle=ls;ctx.lineWidth=1.4;ctx.stroke()}
      if(l.pulse&&!RM){var u=(t*.00005*l.sp+l.off)%1,p=at(l.pts,u),g=ctx.createRadialGradient(p[0],p[1],0,p[0],p[1],26);g.addColorStop(0,u<.5?a:cc);g.addColorStop(1,'rgba(0,0,0,0)');ctx.globalAlpha=.85;ctx.fillStyle=g;ctx.beginPath();ctx.arc(p[0],p[1],26,0,7);ctx.fill();ctx.globalAlpha=1;
        ctx.fillStyle=u<.5?a:cc;ctx.beginPath();ctx.arc(p[0],p[1],1.8,0,7);ctx.fill()}});
    raf=(on&&!RM)?requestAnimationFrame(draw):0}
  build();draw(0);
  if(window.ResizeObserver)new ResizeObserver(function(){build();if(!raf)draw(performance.now())}).observe(c);
  new MutationObserver(function(){if(!raf)draw(performance.now())}).observe(H,{attributes:true,attributeFilter:['data-theme']});
  new IntersectionObserver(function(es){on=es[0].isIntersecting;if(on&&!raf&&!RM)raf=requestAnimationFrame(draw)},{rootMargin:'100px'}).observe(c);
}
$$('canvas.bus-c').forEach(busBg);

/* Placa "Em operação", no padrão de circuito do método: traços finos saem do barramento num feixe,
   dobram a 45° até cada cliente e levam um pulso com brilho radial. A linha aberta fica tracejada. */
(function(){
  var board=$('#board'),svg=$('#boardSvg');if(!board||!svg)return;
  var NS='http://www.w3.org/2000/svg',bus=$('.board-bus',board),cards=$$('.ncard',board),lines=[],drawn=false,on=false,raf=0,last=0;
  function el(n,a){var e=D.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}
  function layout(){
    $$('.tr,.via,.glow,.core',svg).forEach(function(n){n.remove()});lines=[];
    var br=board.getBoundingClientRect(),bb=bus.getBoundingClientRect(),x0=bb.right-br.left,mobile=br.width<900;
    var ps=cards.map(function(c){var p=$('.pin',c).getBoundingClientRect();return{x:p.left-br.left,y:p.top-br.top+p.height/2}});
    var mid=(ps[0].y+ps[ps.length-1].y)/2,gap=mobile?0:22,bend=x0+Math.max(36,(ps[0].x-x0)*.3);
    cards.forEach(function(c,i){
      var t=ps[i],yS=mobile?t.y:mid+(i-(cards.length-1)/2)*gap,dy=t.y-yS,x1=bend,x2=x1+Math.abs(dy);
      if(x2>t.x-28){x1=Math.max(x0+14,t.x-28-Math.abs(dy));x2=x1+Math.abs(dy)}
      var live=c.getAttribute('data-state')==='live';
      var path=el('path',{d:'M'+x0+' '+yS+' H'+x1+' L'+x2+' '+t.y+' H'+t.x,'class':'tr'+(live?' live':' open')});svg.appendChild(path);
      svg.appendChild(el('circle',{cx:x0,cy:yS,r:3.6,'class':'via'}));
      if(!mobile&&Math.abs(dy)>4){svg.appendChild(el('circle',{cx:x1,cy:yS,r:4.2,'class':'via'}));svg.appendChild(el('circle',{cx:x2,cy:t.y,r:4.2,'class':'via'}))}
      var L={c:c,path:path,len:path.getTotalLength(),live:live,u:(i*.29)%1,sp:1};
      if(live&&!RM){L.glow=el('circle',{r:26,'class':'glow',fill:'url(#gGlowA)'});L.core=el('circle',{r:2,'class':'core'});svg.appendChild(L.glow);svg.appendChild(L.core)}
      lines.push(L);
    });
    if(!drawn){lines.forEach(function(L){L.path.style.strokeDasharray=L.live?L.len:'4 6';if(L.live)L.path.style.strokeDashoffset=RM?0:L.len});if(RM)drawn=true}
    tick(0);
  }
  function reveal(){if(drawn)return;drawn=true;
    lines.forEach(function(L,i){if(!L.live)return;L.path.animate([{strokeDashoffset:L.len},{strokeDashoffset:0}],{duration:1400,delay:i*180,easing:'cubic-bezier(.16,1,.3,1)',fill:'forwards'}).onfinish=function(){L.path.style.strokeDashoffset=0;L.path.style.strokeDasharray='none'}});
    cards.forEach(function(c,i){c.animate([{opacity:.2,transform:'translateX(24px)'},{opacity:1,transform:'none'}],{duration:900,delay:250+i*160,easing:'cubic-bezier(.16,1,.3,1)',fill:'backwards'})})}
  function cv(n){return getComputedStyle(H).getPropertyValue(n).trim()}
  function tick(t){var dt=last?Math.min(.05,(t-last)/1000):0;last=t;var ca=cv('--circ-a'),cc=cv('--circ-c');
    lines.forEach(function(L){if(!L.core)return;L.u=(L.u+dt*L.sp*(300/Math.max(200,L.len)))%1;var p=L.path.getPointAtLength(L.u*L.len),a=drawn?Math.min(1,L.u/.08,(1-L.u)/.06):0,first=L.u<.5;
      L.glow.setAttribute('cx',p.x);L.glow.setAttribute('cy',p.y);L.glow.setAttribute('fill',first?'url(#gGlowA)':'url(#gGlowC)');L.glow.style.opacity=.85*a;
      L.core.setAttribute('cx',p.x);L.core.setAttribute('cy',p.y);L.core.style.fill=first?ca:cc;L.core.style.opacity=a});
    raf=(on&&!RM)?requestAnimationFrame(tick):0}
  cards.forEach(function(c,i){
    function hot(v){var L=lines[i];if(!L)return;L.path.classList.toggle('hot',v);c.classList.toggle('hot',v);L.sp=v?2.4:1}
    c.addEventListener('mouseenter',function(){hot(true)});c.addEventListener('mouseleave',function(){hot(false)});
    c.addEventListener('focusin',function(){hot(true)});c.addEventListener('focusout',function(){hot(false)});
  });
  layout();
  if(window.ResizeObserver)new ResizeObserver(function(){layout()}).observe(board);
  if(D.fonts&&D.fonts.ready)D.fonts.ready.then(layout);
  new IntersectionObserver(function(es){var e=es[0];on=e.isIntersecting;if(e.intersectionRatio>.25)reveal();if(on&&!raf&&!RM){last=0;raf=requestAnimationFrame(tick)}},{threshold:[0,.25]}).observe(board);
})();

/* Trilho de produtos: setas rolam um cartão por vez; a máscara some no fim do trilho */
(function(){var t=$('#ptrack');if(!t)return;var pv=$('#pPrev'),nx=$('#pNext');
  function step(){var c=$('.prod',t);return c?c.getBoundingClientRect().width+16:320}
  function upd(){var end=t.scrollLeft+t.clientWidth>=t.scrollWidth-4;t.classList.toggle('end',end);if(pv)pv.disabled=t.scrollLeft<4;if(nx)nx.disabled=end}
  pv&&pv.addEventListener('click',function(){t.scrollBy({left:-step(),behavior:RM?'auto':'smooth'})});
  nx&&nx.addEventListener('click',function(){t.scrollBy({left:step(),behavior:RM?'auto':'smooth'})});
  t.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
})();

/* A Bratecon: a página é um circuito. A história nasce ligada; ligar um trecho dispara a corrente,
   que percorre a espinha e acende cada trecho anterior até chegar nele. */
(function(){
  var board=$('#icBoard'),svg=$('#icSvg');if(!board||!svg)return;
  var NS='http://www.w3.org/2000/svg',chs=$$('.ic-ch',board),mapB=$$('.ic-map [data-go]'),seps=$$('.ic-map .sep'),cnt=$('#icOn');
  var level=0,busy=false,P=[],segs=[],brs=[],vias=[],glow,core,spark,sparkCore,on=false,raf=0,last=0,u=0;
  function el(n,a){var e=D.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);return e}
  function idx(id){for(var i=0;i<chs.length;i++)if(chs[i].id===id)return i;return -1}
  chs.forEach(function(c,i){if(i>0)$('.ic-body',c).inert=true});
  function layout(){
    $$('.dyn',svg).forEach(function(n){n.remove()});segs=[];brs=[];vias=[];
    var br=board.getBoundingClientRect(),W=br.width;
    P=chs.map(function(c){var n=$('.ic-node',c).getBoundingClientRect(),h=$('.ic-head',c).getBoundingClientRect();
      return{x:n.left-br.left+n.width/2,y:n.top-br.top+n.height/2,r:n.width/2,hy:h.bottom-br.top-1}});
    var x=P[0].x,y0=P[0].y,yN=P[P.length-1].y;
    [-8,8].forEach(function(o){svg.appendChild(el('path',{d:'M'+(x+o)+' '+(y0-30)+' V'+(yN+60),'class':'icbus dyn'}))});
    for(var i=1;i<P.length;i++){var sp=el('path',{d:'M'+x+' '+(P[i-1].y+P[i-1].r)+' V'+(P[i].y-P[i].r),'class':'seg dyn'+(i<=level?' on':'')});svg.appendChild(sp);segs.push(sp)}
    var cx=$('.ic-head > div',chs[0]).getBoundingClientRect().left-br.left;
    P.forEach(function(p,i){var j=Math.min(26,cx-x-12),y=p.hy+8,end=Math.min(W-6,cx+Math.max(160,(W-cx)*.55));
      var b=el('path',{d:'M'+x+' '+(y-j)+' L'+(x+j)+' '+y+' H'+end,'class':'br dyn'+(i<=level?' on':'')});svg.appendChild(b);brs.push(b);
      svg.appendChild(el('circle',{cx:x,cy:y-j,r:3.2,'class':'via dyn'}));
      var v=el('circle',{cx:end,cy:y,r:4.2,'class':'via dyn'+(i<=level?' on':'')});svg.appendChild(v);vias.push(v)});
    glow=el('circle',{r:28,fill:'url(#gIcA)','class':'dyn'});core=el('circle',{r:2.2,'class':'dyn'});core.style.fill='var(--circ-a)';
    spark=el('circle',{r:40,fill:'url(#gIcA)','class':'dyn'});sparkCore=el('circle',{r:3.2,'class':'dyn'});sparkCore.style.fill='var(--circ-a)';spark.style.opacity=0;sparkCore.style.opacity=0;
    [glow,core,spark,sparkCore].forEach(function(n){svg.appendChild(n)});
    tick(0);
  }
  function tick(t){var dt=last?Math.min(.05,(t-last)/1000):0;last=t;
    if(P.length&&level>0&&!RM){var yA=P[0].y,yB=P[level].y;u=(u+dt*120/Math.max(120,yB-yA))%1;var y=yA+(yB-yA)*u,a=Math.min(1,u/.08,(1-u)/.08)*(busy?0:1);
      glow.setAttribute('cx',P[0].x);glow.setAttribute('cy',y);core.setAttribute('cx',P[0].x);core.setAttribute('cy',y);glow.style.opacity=.9*a;core.style.opacity=a}
    else if(glow){glow.style.opacity=0;core.style.opacity=0}
    raf=(on&&!RM)?requestAnimationFrame(tick):0}
  function sync(){chs.forEach(function(c,i){var o=i<=level;c.classList.toggle('on',o);c.classList.toggle('off',!o);$('.ic-node',c).setAttribute('aria-expanded',String(o));$('.ic-body',c).inert=!o});
    segs.forEach(function(sg,i){sg.classList.toggle('on',i+1<=level)});brs.forEach(function(b,i){b.classList.toggle('on',i<=level)});vias.forEach(function(v,i){v.classList.toggle('on',i<=level)});
    mapB.forEach(function(b,i){b.classList.toggle('on',i<=level)});seps.forEach(function(s,i){s.classList.toggle('on',i+1<=level)});
    if(cnt)cnt.textContent=level+1}
  function power(k){level=k;sync();var c=chs[k];setTimeout(function(){c.classList.add('done');if(window.ScrollTrigger)ScrollTrigger.refresh()},RM?0:1000)}
  function travel(k,done){if(RM){power(k);done();return}
    var a=P[k-1],b=P[k],t0=0,dur=700;spark.style.opacity=1;sparkCore.style.opacity=1;
    (function step(t){if(!t0)t0=t;var q=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-q,3),y=a.y+(b.y-a.y)*e;
      spark.setAttribute('cx',a.x);spark.setAttribute('cy',y);sparkCore.setAttribute('cx',a.x);sparkCore.setAttribute('cy',y);
      if(q<1)requestAnimationFrame(step);else{spark.style.opacity=0;sparkCore.style.opacity=0;power(k);setTimeout(done,320)}})(performance.now())}
  function go(k,scroll){if(k<=level){if(scroll)to(k);return}if(busy)return;busy=true;
    (function next(){if(level>=k){busy=false;if(scroll)setTimeout(function(){to(k)},RM?0:450);return}travel(level+1,next)})()}
  function to(k){var t=chs[k],pn=$('.ic-panel'),off=-((pn?pn.getBoundingClientRect().height:60)+110);if(window.__lenis)window.__lenis.scrollTo(t,{offset:off,duration:1.2});else window.scrollTo({top:t.getBoundingClientRect().top+scrollY+off,behavior:RM?'auto':'smooth'})}
  chs.forEach(function(c,i){$('.ic-node',c).addEventListener('click',function(){go(i,false)});var g=$('.ic-go',c);g&&g.addEventListener('click',function(){go(i,false)})});
  mapB.forEach(function(b){b.addEventListener('click',function(){go(idx(b.getAttribute('data-go')),true)})});
  var all=$('#icAll');all&&all.addEventListener('click',function(){go(chs.length-1,false)});
  function fromHash(){var k=idx((location.hash||'').slice(1));if(k<1)return;level=k;sync();chs.forEach(function(c,i){if(i<=k)c.classList.add('done')});layout();setTimeout(function(){to(k)},80)}
  addEventListener('hashchange',function(){var k=idx((location.hash||'').slice(1));if(k>=0)go(k,true)});
  layout();fromHash();
  if(window.ResizeObserver)new ResizeObserver(function(){layout()}).observe(board);
  if(D.fonts&&D.fonts.ready)D.fonts.ready.then(layout);
  new IntersectionObserver(function(es){on=es[0].isIntersecting;if(on&&!raf&&!RM){last=0;raf=requestAnimationFrame(tick)}}).observe(board);
})();

var G=!RM&&window.gsap&&window.ScrollTrigger;
if(!G){roomChars.forEach(function(c){c.classList.add('on')});kWords.forEach(function(w){w.classList.add('past')});initIntro(function(){});return}

gsap.registerPlugin(ScrollTrigger);
var lenis=null;
if(window.Lenis){lenis=new Lenis({duration:1.15,smoothWheel:true});window.__lenis=lenis;lenis.on('scroll',ScrollTrigger.update);gsap.ticker.add(function(t){lenis.raf(t*1000)});gsap.ticker.lagSmoothing(0)}
$$('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(e){var id=a.getAttribute('href');if(id.length<2)return;var t=D.querySelector(id);if(!t)return;e.preventDefault();if(lenis)lenis.scrollTo(t,{offset:id==='#top'?0:-72,duration:1.2});else t.scrollIntoView({behavior:'smooth'})})});
if(hashTabs)setTimeout(function(){if(lenis)lenis.scrollTo(hashTabs,{offset:-96,immediate:true});else hashTabs.scrollIntoView()},60);

/* Capa: entra depois do vídeo de abertura */
function capaIn(){
  if(!$('#hword'))return;
  gsap.from('#hword',{yPercent:112,duration:1.3,ease:'expo.out',delay:.15});
  gsap.from('#hmark i',{xPercent:8,yPercent:6,scale:.92,duration:1.8,ease:'expo.out',delay:.1});
  gsap.from('.hmodel,.htag,.hsub,.hacts,.stamps',{y:22,duration:1,stagger:.12,ease:'power3.out',delay:.5});
}
function pheadIn(){var p=$('.phead');if(!p)return;gsap.from($$('.phead .crumbs,.phead h1,.phead .lede,.phead .phead-meta',p),{y:26,duration:1.1,stagger:.1,ease:'expo.out',delay:.1})}
initIntro(capaIn);pheadIn();
if($('#hmark'))gsap.to('#hmark',{yPercent:10,rotate:-5,ease:'none',scrollTrigger:{trigger:'#top',start:'top top',end:'bottom top',scrub:true}});
if($('#heroStage')&&matchMedia('(pointer:fine)').matches){var hero=$('#heroStage'),hw=$('#hword'),hs=$('#hmark i');var qx=gsap.quickTo(hw,'x',{duration:1.1,ease:'power3'}),qs=gsap.quickTo(hs,'x',{duration:1.4,ease:'power3'}),qy=gsap.quickTo(hs,'y',{duration:1.4,ease:'power3'});
  hero.addEventListener('mousemove',function(e){var x=e.clientX/innerWidth-.5,y=e.clientY/innerHeight-.5;qx(x*14);qs(x*-28);qy(y*-18)})}

/* Revelações: sobem a partir de um estado já visível */
$$('.sechead,.demo,.sub,.bento,.sheets,.overview,.awards,.team,.reserve,.tabs-bar,.cta-band,.g3,.pgrid,.chan,.prod-grid,.prail,.prin,.pco,.howband').forEach(function(el){gsap.from(el,{y:28,duration:1,ease:'power3.out',scrollTrigger:{trigger:el,start:'top 92%',once:true}})});

/* Órbita horizontal (desktop) */
var mm=gsap.matchMedia();
if($('#otrack'))mm.add('(min-width:901px)',function(){var track=$('#otrack'),n=$$('.oslide',track).length,bar=$('#oBar'),idx=$('#oIdx');
  var tw=gsap.to(track,{x:function(){return -(track.scrollWidth-innerWidth)},ease:'none',scrollTrigger:{trigger:'#conveyor',start:'top top',end:'bottom bottom',scrub:.6,invalidateOnRefresh:true,snap:{snapTo:1/(n-1),duration:{min:.25,max:.6},delay:.12,ease:'power2.inOut'},onUpdate:function(s){bar.style.transform='translateX('+(s.progress*(n-1)*100)+'%)';idx.textContent='0'+Math.min(n,1+Math.round(s.progress*(n-1)))+' / 0'+n}}});
  $$('.oslide').forEach(function(s){gsap.fromTo($('.oplate',s),{xPercent:-5},{xPercent:5,ease:'none',scrollTrigger:{trigger:'#conveyor',start:'top top',end:'bottom bottom',scrub:true}});gsap.fromTo($('.scontent',s),{x:60},{x:-60,ease:'none',scrollTrigger:{trigger:'#conveyor',start:'top top',end:'bottom bottom',scrub:true}})});
  return function(){tw.scrollTrigger&&tw.scrollTrigger.kill()}});

if($('#sala')){ScrollTrigger.create({trigger:'#sala',start:'top 55%',once:true,onEnter:function(){roomChars.forEach(function(c,i){setTimeout(function(){c.classList.add('on')},i*45)})}});
  gsap.fromTo('.room .bgB',{yPercent:-58,rotate:-12},{yPercent:-42,rotate:-6,ease:'none',scrollTrigger:{trigger:'#sala',start:'top bottom',end:'bottom top',scrub:true}})}
if($('#manifesto')&&kWords.length)ScrollTrigger.create({trigger:'#manifesto',start:'top 70%',end:'bottom 45%',scrub:true,onUpdate:function(s){var a=Math.floor(s.progress*kWords.length);kWords.forEach(function(w,i){w.classList.toggle('past',i<a);w.classList.toggle('act',i===a)})},onLeave:function(){kWords.forEach(function(w){w.classList.remove('act');w.classList.add('past')})}});
addEventListener('load',function(){ScrollTrigger.refresh()});

/* ============ Abertura em vídeo ============
   Toca uma vez por visita, só na página inicial. No quadro em que o B acende no
   circuito, o vídeo se dissolve e a capa monta o mesmo B em 3D por cima. */
function initIntro(done){
  var box=$('#intro');
  function finish(){window.__btHold=false;H.classList.remove('intro-on');if(lenis)lenis.start();D.dispatchEvent(new Event('bt:intro'));done()}
  if(!box||!window.__btHold){if(box)box.remove();window.__btHold=false;done();return}
  var v=$('video',box),skip=$('#introSkip'),bar=$('#introBar'),CUT=parseFloat(box.getAttribute('data-cut'))||8.5,ended=false,started=false;
  H.classList.add('intro-on');if(lenis)lenis.stop();
  try{sessionStorage.setItem('bt-intro','1')}catch(e){}
  function out(){if(ended)return;ended=true;
    if(window.gsap){gsap.timeline({onComplete:function(){box.remove()}})
      .call(finish,null,.25)
      .to(v,{scale:1.06,filter:'blur(6px)',duration:1.1,ease:'power2.in'},0)
      .to(box,{opacity:0,duration:1.1,ease:'power2.inOut'},.05)}
    else{box.remove();finish()}}
  v.addEventListener('timeupdate',function(){if(bar)bar.style.transform='scaleX('+Math.min(1,v.currentTime/CUT)+')';if(v.currentTime>=CUT-.05)out()});
  v.addEventListener('playing',function(){started=true});
  v.addEventListener('ended',out);v.addEventListener('error',out);
  skip&&skip.addEventListener('click',out);
  box.addEventListener('keydown',function(e){if(e.key==='Escape')out()});
  addEventListener('keydown',function(e){if(e.key==='Escape')out()});
  v.preload='auto';v.load();var p=v.play();if(p&&p.catch)p.catch(out);
  setTimeout(function(){if(!started)out()},3500);
  setTimeout(out,(CUT+3)*1000);
  skip&&skip.focus({preventScroll:true});
}
})();
