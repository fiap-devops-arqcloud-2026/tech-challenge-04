// QA documental local. Usa o runtime já instalado e Mermaid via CDN somente na validação.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL, fileURLToPath } from 'node:url';

const require = createRequire('C:/Users/Gabriel/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/package.json');
const { chromium } = require('playwright');
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const work = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(work, '../..');
const qa = path.join(work, 'qa-readme-2026-10-22');
fs.mkdirSync(qa, { recursive: true });
const markdown = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
const executablePath = [
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
].find((p) => fs.existsSync(p));
if (!executablePath) throw new Error('Chrome/Edge não encontrado para a verificação visual.');
const browser = await chromium.launch({ executablePath, headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.setContent(`<!doctype html><html lang="pt-BR"><meta charset="utf-8"><style>
    body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:36px auto;padding:0 24px;color:#202630}
    table{border-collapse:collapse;width:100%;font-size:14px}td,th{border:1px solid #ccd3db;padding:8px;text-align:left}
    code{background:#eef1f5;padding:2px 4px}pre{padding:16px;background:#eef1f5;overflow:auto}
    .diagram{background:white;border:1px solid #ccd3db;padding:12px;margin:20px 0}.diagram svg{max-width:100%;height:auto}
  </style><body>${marked.parse(markdown)}</body></html>`);
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js' });
  const diagrams = await page.evaluate(async () => {
    mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'default' });
    const blocks = [...document.querySelectorAll('code.language-mermaid')];
    if (blocks.length !== 3) throw new Error(`Esperados três diagramas, encontrados ${blocks.length}`);
    for (let i = 0; i < blocks.length; i++) {
      const source = blocks[i].textContent;
      await mermaid.parse(source);
      const { svg } = await mermaid.render(`readme-diagram-${i}`, source);
      const div = document.createElement('div');
      div.className = 'diagram';
      div.innerHTML = svg;
      blocks[i].parentElement.replaceWith(div);
    }
    return blocks.length;
  });
  for (let i = 0; i < diagrams; i++) {
    await page.locator('.diagram').nth(i).screenshot({ path: path.join(qa, `diagrama-${i + 1}.png`) });
  }
  fs.writeFileSync(path.join(qa, 'readme-preview.html'), await page.content(), 'utf8');
  const result = { diagrams, parser: 'Mermaid major 11 via jsDelivr', browser: browser.version(), readmeRendered: true };
  fs.writeFileSync(path.join(work, 'resultado-render-readme-2026-10-22_v01.json'), JSON.stringify(result, null, 2), 'utf8');
  process.stdout.write(`${JSON.stringify(result)}\n`);
} finally {
  await browser.close();
}
