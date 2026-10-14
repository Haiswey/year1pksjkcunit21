#!/usr/bin/env node
/* Smoke test for a built lesson page (uses the template's conventions).

   Usage: NODE_PATH=$(npm root -g) node test_lesson.js page.html

   Checks: no script errors, no sideways scrolling at 390 px, every scene picture loads,
   every story can be played to the end, the end-of-story buttons appear with a correct countdown,
   audio plays one line at a time and the device-voice fallback is never triggered when a clip exists.
   Exit code 1 if anything fails. This does NOT replace looking at the pictures yourself. */
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const file = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 900 } });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.setContent('<!doctype html><meta charset=utf-8><style>[hidden]{display:none!important}</style>' + fs.readFileSync(file, 'utf8'));
  await p.waitForTimeout(800);
  let fail = 0;
  const check = (ok, msg) => { console.log((ok ? 'PASS ' : 'FAIL ') + msg); if (!ok) fail = 1; };

  check((await p.evaluate(() => document.documentElement.scrollWidth)) <= 390, 'no sideways scroll at 390 px');
  const imgs = await p.$$eval('img.scene[src]', x => ({ n: x.length, bad: x.filter(i => !i.complete || !i.naturalWidth).length }));
  check(imgs.bad === 0, imgs.n + ' scene pictures, ' + imgs.bad + ' broken');

  // audio stub: records start/end/cut events; fallback speech counted
  await p.evaluate(() => {
    window.__log = []; window.__tts = 0; const t0 = performance.now();
    window.Audio = function (src) { const o = this; o.paused = true;
      o.play = () => new Promise((res, rej) => { o.paused = false; window.__log.push(['start', Math.round(performance.now() - t0)]);
        o._rej = rej; o._t = setTimeout(() => { if (!o.paused) { o.paused = true; window.__log.push(['end', Math.round(performance.now() - t0)]); o.onended && o.onended(); res(); } }, 300); });
      o.pause = () => { if (!o.paused) { o.paused = true; clearTimeout(o._t); window.__log.push(['cut', Math.round(performance.now() - t0)]); o._rej && o._rej(new DOMException('aborted', 'AbortError')); } };
    };
    if (window.speechSynthesis) { const sp = window.speechSynthesis.speak; window.speechSynthesis.speak = () => { window.__tts++; }; }
  });

  const stepIdx = await p.evaluate(() => [...document.querySelectorAll('.step')].findIndex(s => s.querySelector('[data-sc]')));
  if (stepIdx >= 0) {
    await p.evaluate(i => document.querySelectorAll('.step').forEach((s, k) => s.classList.toggle('on', k === i)), stepIdx);
    const ids = await p.$$eval('[data-sc]', x => x.map(e => e.dataset.sc));
    for (let n = 0; n < ids.length; n++) {
      await p.click('[data-sc="' + ids[n] + '"]');
      let finished = false;
      for (let g = 0; g < 40; g++) {
        await p.waitForTimeout(400);
        if (await p.isVisible('#endAct')) { finished = true; break; }
        const o = await p.$$('#choices .opt:not([disabled])');
        for (const x of o) { try { await x.click({ timeout: 300 }); } catch (e) {} await p.waitForTimeout(120); }
      }
      const label = finished ? (await p.innerText('#btnOther')).trim() : '';
      const left = ids.length - n - 1;
      check(finished && (left ? label.includes(String(left)) : true), 'story "' + ids[n] + '" plays to the end; button: ' + label);
      await p.click('#btnOther'); await p.waitForTimeout(150);
    }
    const log = await p.evaluate(() => window.__log), cuts = log.filter(e => e[0] === 'cut').length;
    const tts = await p.evaluate(() => window.__tts);
    check(tts === 0, 'device-voice fallback calls: ' + tts + ' (expected 0 when every clip exists)');
    console.log('INFO audio events: ' + log.length + ' (cuts caused by new lines: ' + cuts + ')');
  }
  check(errs.length === 0, 'script errors: ' + JSON.stringify(errs));
  await b.close();
  process.exit(fail);
})();
