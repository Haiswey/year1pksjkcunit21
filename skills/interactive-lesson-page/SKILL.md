---
name: interactive-lesson-page
description: Build self-paced interactive lesson web pages for young pupils (primary school, remote learning or PdPR days), turning curriculum content and learning standards into tap-to-answer quizzes, matching games, branching chat stories, read-aloud voice, and child-friendly illustrations, then publish the page online. Use this whenever a teacher mentions online teaching activities, PdPR, home-based learning, haze or school closure lessons, learning standards (standard pembelajaran / 内容标准 / 学习标准), Year 1 to Year 6 pupils, SJKC or SK lessons, interactive worksheets, classroom games, "make this into an online activity", or needs illustrations, recorded voice, or hosting for a lesson page, even if they never say "skill" or "web page".
---

# Interactive lesson page for young pupils

Turn a lesson (textbook pages, content standard, learning standards) into one self-contained web page that
pupils open on a phone or tablet and finish alone at home. The page is a single HTML file: tap-to-answer
quizzes, a matching game, branching chat stories with pictures, read-aloud buttons with a recorded voice, a
star count, and a finish page. It works offline and is hosted at a link the teacher can send to parents.

This skill was distilled from a real project (Year 1 SJKC, "找谁来帮忙", emergencies). The finished example is in
`assets/example-lesson.src.html`; most of the work for a new lesson is replacing its content.

## How to work with the teacher

Teachers are usually new to Claude Code. Keep to this, because most delays in the original project came from
confusion about settings pages, not from the code:

- Use the teacher's language (often Chinese and English mixed). Explain one step at a time, plainly. Avoid jargon.
- Do everything that can be done from the cloud environment yourself. Say clearly, once, what only the teacher
  can do (environment network settings, connectors, sharing, running a script on her own computer).
- When a settings change is needed, list all the items at once with the exact click path. Do not ask repeatedly.
- Report outcomes honestly: say what you checked and what you did not. "Published" is not "I opened it and it works".
- If she says "don't change anything yet", only answer. Ask before deleting, making something public, or
  spending image-generation quota on a large batch. Do not open a pull request unless asked.

## Workflow

1. **Intake (ask before building).** Read `references/intake-and-design.md`. The few questions that matter:
   how pupils work (self-paced or live), what format, session length, devices and parent support, whether to add
   topic extras (haze, local examples), and whether to collect results. Look at the textbook images she attached
   but never copy them into the page.
2. **Plan activities from the learning standards.** Each standard gets at least one activity of a fitting type
   (recognise -> yes/no pictures; choose the right action -> two-option scenes and matching; practise -> chat
   stories). Show her the plan in a short table and adjust, then build.
3. **Build the page** from the example, following `references/page-template-guide.md`. Write the readable source
   first (`lesson.src.html`), assets are injected later by `scripts/build_page.py`.
4. **Illustrations.** Follow `references/illustrations.md`: Canva `generate-image`, one style line, explicit facial
   expressions, full-size export through a Canva design, and a person-by-person check of every picture.
   Fallback when Canva is not available: OpenMoji pictures only.
5. **Voice.** Follow `references/voice.md`. Collect every spoken sentence with `scripts/extract_spoken_lines.js`,
   make the recording kit with `scripts/make_voice_kit.py`, and ask the teacher to run it on her own computer
   (Microsoft's voice server refuses cloud machines). Embed the returned clips. Until then the page uses the
   device voice.
6. **Build and test.** `scripts/fetch_openmoji.py`, `scripts/export_scenes.py`, `scripts/build_page.py`, then
   `scripts/test_lesson.js`. Open the pictures yourself at full size and check faces (see
   `references/qa-and-publish.md`). Tests passing does not prove the pictures are right.
7. **Publish.** Publish a preview as a Claude artifact, push to the branch the teacher names, and deploy to
   Vercel from that branch (steps and pitfalls in `references/qa-and-publish.md`). Give her the live link and say
   what you could not verify.
8. **Hand over.** Send the finished file and a short summary: what each step does, what was checked, what was
   not, file size, and what she should look at herself. Offer the next improvement instead of asking open questions.

## Page conventions the scripts rely on

The scripts and tests find things by these names, so keep them when adapting the example:

- Pages: `<section class="step">` elements (`data-title`), moved with `data-go="N"` buttons, `go(i)`.
- Read-aloud: any `<button class="say" data-say="sentence">`. Every spoken line goes through one `say(text)` function
  that looks up `window.__AUD[text]` (recorded clip), falls back to the device voice, normalises numbers
  (999 -> 九九九), plays lines one at a time, and stops audio when the pupil navigates.
- Pictures: `window.__SCENE[key]` holds scene images; quiz items use `scene: 'key'`, stories use `img: 'key'`.
- Stories: story list `[data-sc]`, chat `#chat`, choices `#choices .opt`, end buttons `#endAct` with `#btnOther`
  ("try another story (N left)" / "back to list") and a "finish" button; the story list shows progress.
- Colour and spacing come from CSS tokens on `:root` with light and dark variants; the page must not scroll sideways
  at 390 px width.

## Useful commands (paths relative to this skill)

```bash
python3 scripts/fetch_openmoji.py lesson.src.html work/om            # small icons, credit OpenMoji (CC BY-SA 4.0)
python3 scripts/export_scenes.py work/full work/scenes.json          # 1280 px WebP q85 by default
NODE_PATH=$(npm root -g) node scripts/extract_spoken_lines.js lesson.src.html work/sentences.json
python3 scripts/make_voice_kit.py work/sentences.json work/voice-kit # files for the teacher's own computer
python3 scripts/build_page.py --src lesson.src.html --out index.html --emoji-map work/om/emoji_map.json \
        --scenes work/scenes.json --voice-dir work/voice --credit "插图：Canva AI 生成；图标：OpenMoji (CC BY-SA 4.0)"
NODE_PATH=$(npm root -g) node scripts/test_lesson.js index.html
```

Rerun `extract_spoken_lines.js` and the voice kit whenever any spoken sentence changes, because clips are looked up
by exact text.

## Reference files

- `references/intake-and-design.md`: questions to ask, activity types, wording and safety for young pupils.
- `references/page-template-guide.md`: how the example page is organised and what to change.
- `references/illustrations.md`: the Canva workflow, prompt recipe, expression rules, resolution, licences.
- `references/voice.md`: voice choice, why recording must happen on the teacher's computer, playback rules.
- `references/qa-and-publish.md`: checks before publishing, GitHub, artifact, Vercel, custom address.
- `references/network-domains.md`: which web addresses the environment must allow, grouped by reachable/blocked.
- `references/lessons-learned.md`: mistakes made in the original project and the fix for each. Read before building.
