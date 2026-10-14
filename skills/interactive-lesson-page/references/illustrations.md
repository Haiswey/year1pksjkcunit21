# Illustrations

## Recommended: Canva AI images (connector `generate-image`)

Needs the Canva connector at https://claude.ai/customize/connectors, connected before the session starts.
If it is missing, say so and carry on with everything else; use OpenMoji pictures meanwhile.

### Prompt recipe

One style line in every prompt keeps the set consistent:

> Children's picture-book illustration, flat colour vector cartoon style, thick friendly outlines, bright soft colours,
> no text. Scene: … Not scary, suitable for 7-year-old children, simple shapes.

- Aspect ratio `LANDSCAPE_16_9` for banners.
- **Say what each person's face looks like.** Without this the model smiles at everything.
  Example: "a worried, alarmed mother: eyebrows raised and drawn together, mouth open, NOT smiling".
  Also describe bystanders ("the man is not arms-crossed and not smiling; the child holds her hand and looks anxious").
- No blood or gore: "a small red cut", "no blood". No scary villains: a stranger has a neutral, expressionless face.
- Ask for what the scene teaches (a lifebuoy in the pool scene, an ambulance arriving) so the picture carries meaning.
- Generate several images in one go, then collect them with `get-generate-image-job` (wait if pending).
  A job returns only a ~200 px preview and a media id.

### Getting the full-size picture

Previews cannot be enlarged (signed URLs break when edited). Use a scratch Canva design:

1. `create-design` (format "Presentation (16:9)", brief "empty white page") once; note the design id.
2. `read-design` with `open_transaction: true` -> transaction id. `edit-design` `add_page` (1920x1080) for each
   picture, `read-design` the new pages to get page ids, then `insert_fill` each media id at 0,0 size 1920x1080,
   `finalize: commit`.
3. `export-design` as PNG, e.g. `{"type":"png","width":1280,"height":720,"pages":[n,...]}`. Download each returned URL
   with curl (needs the Canva hosts allowed, see `network-domains.md`). Name files by scene key (`fire.png`).
4. To replace a picture later, add new pages at the end rather than editing old ones, and export only those pages.

### Check every picture before using it

View each picture at full size (a 2x2 contact sheet at 640x360 is enough) and check, person by person:
faces match the situation (nobody smiling at a fire, a rescue, a stranger offering candy), bystanders are not bored
or amused, hands and details are plausible, nothing frightening. Regenerate failures with the expression spelled out.
In the original project, a smiling firefighter, a smiling mother beside a sparking hair dryer, a smiling teacher
next to a stranger, an excited-looking rescuer, and cold-looking bystanders at a car crash all had to be redone.
Smiling is correct only where it fits (a friendly policeman helping a lost child, a mother comforting a child
in a power cut, a child happy about candy).

### Embedding

`scripts/export_scenes.py` makes `scenes.json`. Defaults: 1280 px wide WebP, quality 85. The first version used 800 px
JPEG quality 80 to save size and looked soft on tablets and 3x phones. Report the total page size to the teacher.

## Fallbacks and small icons

- OpenMoji (CC BY-SA 4.0), `scripts/fetch_openmoji.py`: consistent flat icons, replaces system emoji. Credit it on the page.
- Openclipart (CC0) is reachable but its styles are inconsistent (old engravings next to cartoons); use only for single objects.
- Wikimedia Commons: check each file's licence page; mostly photos.
- Never use textbook scans, publisher images, Google Images results, or anything with a watermark or unclear licence.
- Pixabay blocks automatic downloads (403) unless a free API key is provided.

## Credit line

"Scene pictures made with Canva AI; icons from OpenMoji (openmoji.org, CC BY-SA 4.0)." Pass it to `build_page.py --credit`.
