# CLAUDE.md

Guidance for Claude when working in this repository and in any similar project
(online teaching material for young pupils, built as a single web page).

## About this project

- A self-paced online lesson for Year 1 SJKC pupils (PdPR, haze period).
  Unit 11, topic 10.1 急救常识, lesson 21 找谁来帮忙?
- Learning standards: 10.1.1 recognise emergencies, 10.1.2 handle them in a suitable way,
  10.1.3 practise asking for help.
- Page language: Simplified Chinese. Pupils are 7 years old: big tap targets, little text, read-aloud buttons.
- Live site: https://sjkctahun1pkunit11.vercel.app (Vercel project `year1-sjkc-unit11-zhao-shei-bang-mang`).
- Develop on branch `claude/pdpr-year1-sjkc-activities-9afvtm`. Do not open a pull request unless asked.
- `index.html` is the complete page (about 3 MB, pictures and voice embedded as base64 so it works offline).
  `source/index.readable.html` is the same code with the embedded data replaced by `<EMBEDDED-DATA-OMITTED>`.
  `tools/` holds the voice scripts and notebooks.

## Illustration rules (what gave the best results)

1. **Use the Canva connector (`generate-image`) for scene illustrations.**
   It must be connected at https://claude.ai/customize/connectors before the session starts.
2. **Use one style line in every prompt** so a set looks like one set:
   "Children's picture-book illustration, flat colour vector cartoon style, thick friendly outlines,
   bright soft colours, no text. ... Not scary, suitable for 7-year-old children, simple shapes."
3. **Use 16:9** (`LANDSCAPE_16_9`) for page banners.
4. **State every person's expression in the prompt.** The model draws smiles by default.
   Write the face you want, e.g. "worried, eyebrows drawn together, mouth closed, NOT smiling".
   Do this for bystanders too, not only the main character.
   Smiling is fine only where it fits (a friendly policeman, a mother comforting a child, a child happy about candy).
5. **No blood or gore.** Show injuries as small, gentle cuts or bandages. Keep scenes calm enough for 7-year-olds.
6. **Check every picture at full size, person by person**, before using it. Look at faces, hands, and background people.
   Regenerate any picture where an expression does not match the situation.
7. **Getting the full-size image out of Canva** (the tool only returns a ~200 px preview):
   - Put the generated image on a page of a Canva design (`read-design` with `open_transaction`,
     then `edit-design` with `add_page` and `insert_fill`, then `commit`).
   - Export with `export-design` as PNG (for example 1280x720, or larger for sharper results) and download the URL.
   - The signed preview URLs cannot be resized by editing the URL.
   - The scratch design used in this project: https://canva.link/2vhkmpvfkztn3t5
8. **Keep enough resolution when embedding.** Earlier pictures were shrunk to 800x450 JPEG (quality 80) and looked soft.
   Prefer 1280x720 (or larger) WebP at quality ~85, or JPEG quality 92 or more.
   Check how large the page becomes and tell the user the trade-off.
9. **Licences.** Prefer public domain / CC0, then CC-BY. Never use textbook scans, publisher images,
   Google Images results, or anything with a watermark or an unclear licence.
   Credit sources on the page (this project credits OpenMoji, CC BY-SA 4.0, and Canva AI for the scene pictures).
10. For small icons, OpenMoji SVGs (from `raw.githubusercontent.com/hfg-gmuend/openmoji`) give a consistent look.

## Voice (text to speech)

- Target voice: `zh-CN-XiaoxiaoNeural` via edge-tts, slightly slower (`-12%`) and brighter (`+4Hz`).
- From the cloud environment, Microsoft's speech server answers the audio request with **403**
  (the voice list works, the synthesis does not). Allowing `speech.platform.bing.com` is necessary but not enough.
- What worked: the user ran `tools/make_voice_local.py` on their own computer (home or school network),
  and sent back `voice.zip`. The page then embeds the clips as base64 and plays them.
- Spoken text is normalised: "999" is read as 九九九. Clips are looked up by exact sentence text,
  so change a sentence in the page and the voice list must be regenerated.
- If a clip is missing, the page falls back to the device voice.
- Play lines one after another, never at the same time. Ignore the aborted-play error so the fallback
  voice does not start on top of a recording.

## Build and deploy notes

- Check pages at phone width (about 390 px) in both light and dark themes. The page must not scroll sideways.
- Test the page logic with a headless browser (Playwright) before publishing, including each story path.
- Publish the same page as a Claude artifact for preview, push to the branch, then redeploy to Vercel
  (git deployment from the branch). Vercel's login protection was turned off on purpose so pupils can open the link.
- Do not claim a deployment is live until it has been checked. If it cannot be opened from here, say so.

## Network domains (Allowed domains in the environment's Network access settings)

Only the user can change these settings: environment menu, Edit, Network access, Allowed domains.
Steps: https://code.claude.com/docs/en/cloud-environments#network-access
They belong to the environment, so every project that uses that environment shares them.
Keep "Allow package managers" ticked. New sessions may be needed for changes to take effect.
Domains are tested with `curl`: code 000 means blocked by the proxy; any other code means reachable.

### Group 1: reachable when last tested (nothing to add)

```
www.canva.com
media.canva.com
export-download.canva.com
speech.platform.bing.com
openclipart.org
commons.wikimedia.org
upload.wikimedia.org
raw.githubusercontent.com
github.com
objects.githubusercontent.com
release-assets.githubusercontent.com
pypi.org
registry.npmjs.org
fonts.googleapis.com
fonts.gstatic.com
```

### Group 2: blocked when last tested, worth adding for better images and quality

```
api.openverse.org
openverse.org
cdn.jsdelivr.net
unpkg.com
cdnjs.cloudflare.com
api.iconify.design
huggingface.co
cdn-lfs.huggingface.co
cdn-lfs-us-1.hf.co
images.pexels.com
www.pexels.com
images.unsplash.com
unsplash.com
kenney.nl
opengameart.org
undraw.co
```

What they are for:

- `api.openverse.org`, `openverse.org`: search for openly licensed and public-domain images (includes Wikimedia).
- `cdn.jsdelivr.net`, `unpkg.com`, `cdnjs.cloudflare.com`: files from npm packages and libraries
  (icon sets, emoji sets such as OpenMoji and Twemoji, illustration packs, JavaScript libraries).
- `api.iconify.design`: more than 200,000 open-source icons in one API.
- `huggingface.co` and its file hosts: open-source models (image generation, upscaling, voices such as Kokoro).
- Pexels and Unsplash hosts: free real photos under their own licences (not CC0). Use only when photos are wanted.
- `kenney.nl`, `opengameart.org`: CC0 game-style art for pupil games.
- `undraw.co`: free flat illustrations, mostly office-style rather than child scenes.

### Group 3: notes

- **Pixabay** (`pixabay.com`, `cdn.pixabay.com`) is reachable but returns 403 to automatic downloads.
  Adding it does not help unless the user provides a free Pixabay API key.
- **Domains do not fix quality by themselves.** The biggest quality gains came from the Canva route,
  one consistent style prompt, explicit facial expressions, full-size export, and checking every person.
- Every domain added gives every session in that environment access to it. A broader "any website" level
  avoids managing a list, but protection is weaker and the user's school or organisation may not allow it.
- Reachable does not mean it works: the Microsoft speech host is reachable but still refuses synthesis.

## Working with this user

- The user is a teacher and is new to Claude Code. Explain steps simply, one at a time, and in the language they use
  (they write in Chinese and English).
- Do things for them when this can be done from the cloud environment. Say clearly when something must be done on their
  own computer or in a settings page that only they can change (network access, connectors, sharing).
- Ask before changing anything when the user says not to change anything yet, and report what was and was not checked.
