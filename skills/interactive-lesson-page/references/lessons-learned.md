# Lessons learned (read before building)

| What went wrong | Cause | Fix |
|---|---|---|
| Two voices at the end of a story | The last character line and the praise line started together, the browser cancelled the first, the fallback read it aloud | `say()` returns a promise, new lines stop old ones, interrupted play never triggers the fallback, praise waits for the last line |
| Smiling faces in emergencies (fire, rescue, stranger, hair dryer) | Image model smiles by default | Spell out each expression, including bystanders, and check every person at full size |
| Pictures looked soft | Exported at 1280 then shrunk to 800 px JPEG q80, shown full width | Keep 1280 px WebP q85 (`export_scenes.py`), tell the teacher the page size |
| Canva image only 199 px | The tool returns a preview and signed URLs cannot be resized | Place on a Canva page and export with `export-design` |
| Two small icons beside each other looked odd | Emoji pairs as "pictures" | Use real scene illustrations |
| Fog and smoke icons had white boxes | The OpenMoji fog glyph has an opaque background | Draw soft grey clouds instead |
| Two-tap matching confused pupils | Select left, then right | One scene with a "?" slot and three answer buttons |
| Pupils could not choose another story | Only a bottom "finish" button | After each story: "try another story (N left)" and "finish", with progress |
| 999 read as "nine hundred ninety-nine" | Number normalisation missing | Normalise to 九九九 for speech and lookup |
| Voice synthesis 403 | Microsoft refuses cloud machines (also Colab) | Teacher runs the script on her own computer |
| Pasted setup looked confusing | Instructions pointed at menus I could not see | Ask for a screenshot, name the exact label, one step per message |
| Vercel link asked for login | New projects have login protection | Turn it off after confirming the page is meant to be public |
| Search results unusable on Openclipart | Mixed styles, many irrelevant hits | Use it only for single objects, not scenes |
| Sandbox timeouts on long downloads | Foreground commands limited to ~2 minutes | Run long downloads in the background and poll |

## Habits that paid off

- Test the whole page logic with Playwright, including every story path and the end buttons.
- Extract spoken lines by running the page (not by reading code) so recordings always match.
- Check the picture of every person, not only the main character.
- Say honestly when a deployment could not be opened from the cloud environment.
