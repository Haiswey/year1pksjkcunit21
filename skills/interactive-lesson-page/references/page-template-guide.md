# Adapting `assets/example-lesson.src.html`

The example is the readable source of the finished page. It has no embedded pictures or voice: `scripts/build_page.py`
adds them. Copy it to `lesson.src.html` and edit the content, not the engine, unless a feature is needed.

## Structure

- `:root` tokens (colours, fonts) with `prefers-color-scheme: dark` and `[data-theme]` variants. Change the palette
  here only.
- Header with a score counter and progress dots (`#dots`, `#starCount`).
- Six `<section class="step">`: 0 welcome, 1 recognise quiz (`#quiz1`), 2 choose quiz (`#quiz2`), 3 match (`#match`),
  4 stories (`#scList`, `#chat`), 5 finish. Add or drop steps by adding sections and updating the `go()` navigation
  and `TOTAL` counts.
- One script block (an IIFE). `build_page.py` finds it by the exact start `<script>\n(function(){`, so keep that.

## Content blocks to replace

- **Quizzes** `buildQuiz(host, items, key)`. An item is
  `{scene:'key', pic:'🔥🏠', title:'…', sub:'…', opts:[{t,e,ok,hint}], why:'…'}`.
  `scene` selects a picture from `window.__SCENE`; `pic` (emoji) is only a fallback. The helper `yn(true|false)`
  creates the yes/no pair. Right options use `ok:true`; wrong ones carry a `hint`.
- **Match** arrays `MQ` (situations with the index of the right answer `a`) and `MA` (answers). Each row shuffles
  the answers differently.
- **Stories** `SC`: `{id, img:'sceneKey', ico, title, d, end, steps:[…]}` using helpers
  `N(text)` narration, `T(avatar, who, text)` spoken line, `C(question, [O(emoji, text, ok, hint)])` choice.
  A choice may have several right options. Wrong options are disabled with a hint, right ones add the pupil's bubble
  and continue.
- **Totals** `TOTAL={q1,q2,match,roles}`: update when counts change. `roles` is the number of stories.
- Welcome and finish texts, and `data-say` strings.

## Speech engine (leave as is unless you must)

`say(text)` returns a promise that resolves when the line ends. It normalises "999" to 九九九, stops the previous line,
plays `window.__AUD[text]` if present, else uses the device voice. If playback is rejected because it was interrupted,
the fallback must not start (this caused a double voice). At the end of a story the last character line plays, then
the praise line plays about 0.35 s after it ends. `stopSay()` runs when the pupil changes page or story.

## Emoji and pictures

System emoji are replaced by OpenMoji images at run time by the script `build_page.py` injects, so keep emoji as plain
characters in the source. Scene pictures are 16:9 `<img class="scene">` banners; the story list uses small thumbnails.

## After editing

Rebuild, run `test_lesson.js`, and re-run `extract_spoken_lines.js` if any spoken text changed.
