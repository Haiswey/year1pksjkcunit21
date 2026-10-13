# CLAUDE.md (general rules for all my projects)

These rules apply to any project, whatever its subject. Project-specific details belong in that project's own notes.

## About me and how to work with me

- I am a teacher and new to Claude Code. Explain steps simply, one at a time, in the language I write in
  (I write in Chinese and English).
- Do things for me whenever they can be done from the cloud environment. Say clearly when something must be done on my
  own computer or on a settings page that only I can change (network access, connectors, sharing, domains).
  Never say something is done until it has been checked. Say what was checked and what was not.
- When I say "don't change anything yet", only answer. Ask before making any change.
- Ask before turning off protection, making something public, deleting, or spending quota on a large batch.
- Do not open a pull request unless I ask. Push only to the branch I name.

## Illustrations and images (what gave the best results)

1. **Use the Canva connector (`generate-image`) for illustrations.** It must be connected at
   https://claude.ai/customize/connectors before the session starts. If it is missing, tell me, and carry on with
   anything that does not depend on it.
2. **Use one style line in every prompt** so a set looks like one set. Example:
   "Children's picture-book illustration, flat colour vector cartoon style, thick friendly outlines,
   bright soft colours, no text. ... Not scary, suitable for 7-year-old children, simple shapes."
   Change the audience to match the project.
3. **Use 16:9** (`LANDSCAPE_16_9`) for page banners unless the layout needs another ratio.
4. **State every person's expression in the prompt.** The model draws smiles by default. Write the face you want, for example
   "worried, eyebrows drawn together, mouth closed, NOT smiling". Do this for bystanders too, not only the main character.
   Smiling is fine only where it fits the situation.
5. **No blood or gore.** Show injuries as small, gentle cuts or bandages. Keep scenes calm for young children.
6. **Check every picture at full size, person by person**, before using it. Look at faces, hands and background people.
   Regenerate any picture where an expression or detail does not match the situation.
7. **Getting the full-size image out of Canva** (the tool only returns a ~200 px preview):
   - Put the generated image on a page of a Canva design: `read-design` with `open_transaction`, then `edit-design`
     with `add_page` and `insert_fill`, then `finalize: commit`.
   - Export with `export-design` as PNG (for example 1280x720, or larger for sharper results) and download the URL.
   - Signed preview URLs cannot be resized by editing the URL.
8. **Keep enough resolution when embedding.** Shrinking to 800x450 JPEG (quality 80) looked soft.
   Prefer 1280x720 or larger as WebP at quality ~85, or JPEG at quality 92 or more. Check how large the page becomes
   and tell me the trade-off.
9. **Licences.** Prefer public domain or CC0, then CC-BY. Never use textbook scans, publisher images, Google Images results,
   or anything with a watermark or an unclear licence. Credit sources on the page.
10. For small icons, OpenMoji SVGs (from `raw.githubusercontent.com/hfg-gmuend/openmoji`) give a consistent look.
    Credit OpenMoji (CC BY-SA 4.0).

## Voice (text to speech)

- Preferred voice: `zh-CN-XiaoxiaoNeural` through edge-tts, slightly slower (`-12%`) and brighter (`+4Hz`) for young children.
- From the cloud environment, Microsoft's speech server answers the audio request with **403**. The voice list works,
  the synthesis does not. Allowing `speech.platform.bing.com` is necessary but not enough.
- What worked: give me a ready script (and a Colab notebook as backup) that I run on my own computer, then I send back
  the audio zip. Embed the clips in the page as base64 so it works offline.
- Spoken text should be normalised before recording (for example read "999" as 九九九). Look clips up by exact sentence text,
  so changing a sentence means the audio list must be regenerated.
- Fall back to the device voice when a clip is missing. Play lines one after another, never at the same time,
  and ignore the aborted-play error so the fallback voice does not start on top of a recording.

## Building and publishing web pages

- Check pages at phone width (about 390 px) in light and dark themes. No sideways scrolling.
- Test the page logic with a headless browser (Playwright) before publishing, including every path a user can take.
- Embed images and audio when the page must work offline. Report the final file size.
- Publish a preview as a Claude artifact when useful, push to the named branch, then deploy (for example to Vercel from the branch).
- Vercel projects start with login protection. Turning it off makes the page public, so confirm with me first
  when the page was not already meant for public use.
- Say honestly if a deployed page could not be opened from here.

## Network domains (Allowed domains in the environment's Network access settings)

Only I can change these settings: environment menu, Edit, Network access, Allowed domains.
Steps: https://code.claude.com/docs/en/cloud-environments#network-access
They belong to the environment, so every project that uses that environment shares them. Keep "Allow package managers" ticked.
New sessions may be needed for changes to take effect. When a new domain is needed, list all of them at once and say why.
Test a domain with `curl`: code 000 means blocked by the proxy; any other code means it is reachable.

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
  Adding it does not help unless I provide a free Pixabay API key.
- **Domains do not fix quality by themselves.** The biggest quality gains came from the Canva route, one consistent style prompt,
  explicit facial expressions, full-size export, and checking every person.
- Every domain added gives every session in that environment access to it. A broader "any website" level avoids managing a list,
  but protection is weaker and my school or organisation may not allow it.
- Reachable does not mean it works: the Microsoft speech host is reachable but still refuses synthesis.
