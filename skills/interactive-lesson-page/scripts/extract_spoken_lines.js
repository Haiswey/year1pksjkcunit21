#!/usr/bin/env node
/* Collect every sentence a lesson page speaks, so the voice recordings match it exactly.

   Usage: NODE_PATH=$(npm root -g) node extract_spoken_lines.js lesson.src.html sentences.json

   How: the page looks clips up in window.__AUD[text]. We install a Proxy there that logs every key,
   then click every read-aloud button, play every story with every option, and open the finish page.
   Requires the template's conventions: .step, .say, [data-sc] story buttons, #choices .opt, #chat, #scList.
   Run it again whenever any spoken sentence changes. */
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [src, out] = process.argv.slice(2);
  if (!src || !out) { console.error('usage: extract_spoken_lines.js SRC.html OUT.json'); process.exit(1); }
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 900 } });
  await p.setContent('<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>' + fs.readFileSync(src, 'utf8'));
  await p.evaluate(() => {
    window.__heard = [];
    window.__AUD = new Proxy({}, { get: (o, k) => { if (typeof k === 'string') window.__heard.push(k); return undefined; } });
    /* device-voice fallback: pretend each line finishes quickly so the page continues to the next spoken line */
    if (window.speechSynthesis) window.speechSynthesis.speak = u => { setTimeout(() => { u && u.onend && u.onend(); }, 40); };
  });
  await p.waitForTimeout(300);
  const steps = await p.$$eval('.step', x => x.length);
  const show = i => p.evaluate(i => document.querySelectorAll('.step').forEach((s, k) => s.classList.toggle('on', k === i)), i);
  for (let i = 0; i < steps; i++) {
    await show(i);
    if (i === steps - 1) await p.evaluate(() => { const g = document.querySelector('[data-go]'); });
    const n = (await p.$$('.step.on .say')).length;
    for (let j = 0; j < n; j++) { const els = await p.$$('.step.on .say'); try { await els[j].click({ force: true, timeout: 1000 }); } catch (e) {} }
  }
  // finish page speaks a line when it opens: trigger through the page's own navigation if present
  await p.evaluate(() => { const last = document.querySelectorAll('[data-go]'); last.forEach(b => { if (+b.dataset.go === document.querySelectorAll('.step').length - 1) b.click(); }); });
  await p.waitForTimeout(300);
  // stories
  const stepIdx = await p.evaluate(() => [...document.querySelectorAll('.step')].findIndex(s => s.querySelector('[data-sc]')));
  if (stepIdx >= 0) {
    await show(stepIdx);
    const ids = await p.$$eval('[data-sc]', x => x.map(e => e.dataset.sc));
    for (const id of ids) {
      await p.evaluate(() => { document.getElementById('chat').hidden = true; document.getElementById('scList').hidden = false; });
      await p.click('[data-sc="' + id + '"]');
      for (let g = 0; g < 40; g++) {
        await p.waitForTimeout(450);
        const o = await p.$$('#choices .opt:not([disabled])');
        if (!o.length) break;
        for (const x of o) { try { await x.click({ timeout: 300 }); } catch (e) {} await p.waitForTimeout(120); }
      }
      await p.waitForTimeout(1800);
    }
  }
  const heard = await p.evaluate(() => window.__heard);
  const uniq = [...new Set(heard)];
  fs.writeFileSync(out, JSON.stringify(uniq, null, 1));
  console.log(uniq.length + ' sentences written to ' + out);
  uniq.forEach(t => console.log('-', t));
  await b.close();
})();
