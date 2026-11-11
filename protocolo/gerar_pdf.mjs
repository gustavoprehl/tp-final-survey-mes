// Gera protocolo/protocolo.pdf (seções 1–8) e protocolo/apendices.pdf (matriz e pré-teste)
// a partir dos .md do repositório, usando o Chrome/Edge instalado em modo headless.
//
// Uso (na raiz do repositório):  node protocolo/gerar_pdf.mjs
// O conversor de Markdown cobre só o que os arquivos usam: títulos, parágrafos, listas,
// tabelas, citações, **negrito**, *itálico*, `código`, [links](url) e fórmulas $$…$$.

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const RAIZ = resolve(import.meta.dirname, '..');
const DIR = join(RAIZ, 'protocolo');

const NAVEGADORES = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
];

const escapar = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function inline(s) {
  const codigos = [];
  s = s.replace(/`([^`]+)`/g, (_, c) => `\u0000${codigos.push(escapar(c)) - 1}\u0000`);
  s = escapar(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\s][^*]*?)\*/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$1');  // links viram texto no PDF
  return s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${codigos[i]}</code>`);
}

// Fórmulas LaTeX simples usadas no protocolo, convertidas para texto
function formula(tex) {
  return tex
    .replace(/\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}/g, '($1) / $2')
    .replace(/\\sqrt\{(.+)\}/g, '√($1)')
    .replace(/\{,\}/g, ',')
    .replace(/\\times/g, '×')
    .replace(/[{}]/g, '')
    .replace(/1-p/g, '1 − p')
    .trim();
}

function celulas(linha) {
  return linha.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

function markdown(md) {
  const linhas = md.replace(/\r/g, '').split('\n');
  const html = [];
  let i = 0;
  while (i < linhas.length) {
    const l = linhas[i];
    if (!l.trim()) { i++; continue; }

    if (l.trim().startsWith('$$')) {
      let tex = l.trim().slice(2);
      while (!tex.trim().endsWith('$$') && ++i < linhas.length) tex += ' ' + linhas[i].trim();
      html.push(`<p class="formula">${escapar(formula(tex.replace(/\$\$/g, '')))}</p>`);
      i++; continue;
    }
    const h = l.match(/^(#{1,4})\s+(.*)/);
    if (h) { html.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`); i++; continue; }

    if (l.trim().startsWith('|') && linhas[i + 1]?.match(/^\s*\|[\s:|-]+\|\s*$/)) {
      const cab = celulas(l);
      i += 2;
      const corpo = [];
      while (i < linhas.length && linhas[i].trim().startsWith('|')) corpo.push(celulas(linhas[i++]));
      html.push('<table><thead><tr>' + cab.map((c) => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>'
        + corpo.map((r) => '<tr>' + r.map((c) => `<td>${inline(c)}</td>`).join('') + '</tr>').join('')
        + '</tbody></table>');
      continue;
    }
    if (l.startsWith('>')) {
      const bloco = [];
      while (i < linhas.length && linhas[i].startsWith('>')) bloco.push(linhas[i++].replace(/^>\s?/, ''));
      html.push(`<blockquote>${markdown(bloco.join('\n'))}</blockquote>`);
      continue;
    }
    const lista = l.match(/^(\s*)([-*]|\d+\.)\s+/);
    if (lista) {
      const tag = /\d/.test(lista[2]) ? 'ol' : 'ul';
      const itens = [];
      while (i < linhas.length && linhas[i].match(/^\s*([-*]|\d+\.)\s+/)) {
        let item = linhas[i++].replace(/^\s*([-*]|\d+\.)\s+/, '');
        while (i < linhas.length && linhas[i].match(/^\s{2,}\S/) && !linhas[i].match(/^\s*([-*]|\d+\.)\s+/)) item += ' ' + linhas[i++].trim();
        itens.push(`<li>${inline(item)}</li>`);
      }
      html.push(`<${tag}>${itens.join('')}</${tag}>`);
      continue;
    }
    const par = [l.trim()];
    while (++i < linhas.length && linhas[i].trim() && !linhas[i].match(/^(#|\||>|\s*([-*]|\d+\.)\s|\$\$)/)) par.push(linhas[i].trim());
    html.push(`<p>${inline(par.join(' '))}</p>`);
  }
  return html.join('\n');
}

const CSS = `
  @page { size: A4; margin: 1.6cm 1.7cm; }
  body { font-family: "Segoe UI", Arial, sans-serif; font-size: 9.2pt; line-height: 1.32; color: #111; }
  h1 { font-size: 12.5pt; margin: 12pt 0 4pt; padding-bottom: 2pt; border-bottom: 1px solid #999; break-after: avoid; }
  h2 { font-size: 10.2pt; margin: 8pt 0 3pt; break-after: avoid; }
  p { margin: 3pt 0; text-align: justify; }
  ul, ol { margin: 3pt 0; padding-left: 16pt; } li { margin: 1pt 0; }
  table { width: 100%; border-collapse: collapse; margin: 4pt 0; font-size: 8.3pt; line-height: 1.22; }
  th, td { border: 1px solid #aaa; padding: 2pt 4pt; vertical-align: top; text-align: left; }
  th { background: #eee; }
  tr { break-inside: avoid; }
  code { font-family: Consolas, monospace; font-size: 8pt; }
  blockquote { margin: 4pt 0; padding: 2pt 8pt; border-left: 3px solid #bbb; color: #333; }
  .formula { text-align: center; font-size: 10pt; margin: 5pt 0; }
  .capa { text-align: center; margin-bottom: 8pt; }
  .capa .titulo { font-size: 14pt; font-weight: 700; margin: 0 0 3pt; text-align: center; }
  .capa p { text-align: center; margin: 1pt 0; }
`;

function documento(titulo, subtitulo, corpo) {
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>${titulo}</title><style>${CSS}</style></head><body>
<div class="capa">
  <p class="titulo">${titulo}</p>
  <p>${subtitulo}</p>
  <p>Medição e Experimentação de Software · PUC Minas · Arthur Panzera, Diogo Brunoro e Gustavo Prehl</p>
  <p>Repositório: github.com/gustavoprehl/tp-final-survey-mes · versão pré-registrada: tag <code>protocolo-v1</code></p>
</div>
${corpo}
</body></html>`;
}

function imprimir(html, nome) {
  const navegador = NAVEGADORES.find(existsSync);
  if (!navegador) throw new Error('Chrome ou Edge não encontrado.');
  const htmlPath = join(DIR, nome.replace(/\.pdf$/, '.html'));
  const pdfPath = join(DIR, nome);
  writeFileSync(htmlPath, html, 'utf8');
  execFileSync(navegador, ['--headless=new', '--disable-gpu', '--no-pdf-header-footer',
    `--print-to-pdf=${pdfPath}`, pathToFileURL(htmlPath).href], { stdio: 'ignore' });
  const paginas = (readFileSync(pdfPath, 'latin1').match(/\/Type\s*\/Page[^s]/g) || []).length;
  console.log(`${nome}: ${paginas} página(s)`);
  return paginas;
}

const secoes = readdirSync(DIR).filter((f) => /^\d\d_.*\.md$/.test(f)).sort();
const corpo = secoes.map((f) => markdown(readFileSync(join(DIR, f), 'utf8'))).join('\n');
const paginas = imprimir(documento(
  'Protocolo do survey: uso de métricas em produtos de dados e automação',
  'Parte 1 — Planejamento (pré-registro)', corpo), 'protocolo.pdf');
if (paginas > 6) console.warn('ATENÇÃO: o protocolo passou do limite de 6 páginas.');

const apendices = [
  ['Apêndice A — Matriz de rastreabilidade', 'questionario/matriz_rastreabilidade.md'],
  ['Apêndice B — Registro do pré-teste', 'questionario/pre-teste.md'],
].map(([titulo, arq]) => `<h1>${titulo}</h1>\n` + markdown(readFileSync(join(RAIZ, arq), 'utf8').replace(/^# .*\n/, '')))
  .join('\n');
imprimir(documento('Apêndices do protocolo', 'Parte 1 — Planejamento (pré-registro)', apendices), 'apendices.pdf');
