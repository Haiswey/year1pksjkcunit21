# Network domains

Only the teacher can change these: environment menu in the session title bar -> Edit -> Network access ->
Allowed domains (keep "Allow package managers" ticked). Steps: https://code.claude.com/docs/en/cloud-environments#network-access
They belong to the environment, so every project using that environment shares them. New sessions may be needed.
List every missing domain at once. Test with `curl -s -o /dev/null -w '%{http_code}' https://host`; 000 means blocked.

## Group 1: reachable when last tested

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

## Group 2: blocked when last tested, worth adding

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

Openverse: search openly licensed images. jsDelivr/unpkg/cdnjs: npm package files and libraries. Iconify: icons.
Hugging Face: open-source models (voices, upscalers). Pexels/Unsplash: photos under their own licences.
Kenney/OpenGameArt: CC0 game art. unDraw: flat office-style illustrations.

## Notes

- Pixabay is reachable but returns 403 to automation; it needs a free API key.
- Reachable does not mean it works: the Microsoft speech host is reachable but synthesis is refused (403).
- Canva hosts must be allowed to download exported pictures (`export-download.canva.com`, `media.canva.com`).
- A broader "any website" level avoids the list but weakens protection and may be disallowed by the school.
- The Canva and Vercel connectors are account level (https://claude.ai/customize/connectors); the network list is per environment.
