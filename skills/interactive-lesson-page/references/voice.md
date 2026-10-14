# Voice (read-aloud)

## Choice

`zh-CN-XiaoxiaoNeural` (edge-tts), rate `-12%`, pitch `+4Hz`: warm, slightly slower and brighter for young pupils.
The teacher judged it good. Device voices vary by phone and sound robotic; use them only as the fallback.

## Why recordings are made on the teacher's computer

From cloud machines (and from Google Colab) Microsoft's speech server answers the audio request with HTTP 403.
Fetching the voice list works, synthesis does not. Newer browser version strings do not help and guessing them is not
appropriate. Allowing `speech.platform.bing.com` is necessary but not sufficient. What worked: the teacher ran a ready
script on her own Windows computer and sent back `voice.zip`.
Open-source voices on Hugging Face (Kokoro) are blocked unless `huggingface.co` hosts are allowed and were never tested.
Google's gTTS via Colab is a plainer-sounding backup.

## Steps

1. Collect all sentences: `scripts/extract_spoken_lines.js` (it also catches the closing praise lines).
2. Build the kit: `scripts/make_voice_kit.py sentences.json kit/` -> `make_voice_local.py` (+ Colab notebooks).
3. Send `make_voice_local.py` to the teacher with these steps (Windows, new to Python):
   - Install Python from the Microsoft Store installer: click "Install Python"; no PATH checkbox exists in this installer.
   - Open Command Prompt: `py -m pip install edge-tts`, then `cd %USERPROFILE%\Downloads`, then `py make_voice_local.py`
     with the script saved in Downloads. If `py` is not recognised use `python`.
   - It prints "done n / N", then creates `voice.zip` in the same folder; she attaches it to the chat.
4. Unzip (check names for path traversal first), confirm `index.json` equals your sentence list, pass the folder to
   `build_page.py --voice-dir`. Run `test_lesson.js`.

## Text rules

- Normalise numerals for speech (999 -> 九九九). The page does the same when looking clips up.
- Clips are looked up by exact text, so any edit of a spoken sentence needs new recordings.
- Avoid double punctuation when joining title and subtitle (`房子着火了！` + `浓烟冒出来。`).

## Playback rules (each fixed a real bug)

- One line at a time. A new line stops the old one.
- If the browser rejects play() because it was interrupted, do not start the device voice. The fallback fires only on
  real failures. Otherwise the pupil hears a recording and a robot voice together.
- At the end of a story, wait for the last character line to finish before the praise line.
- Stop audio when the pupil changes page or leaves a story.
- Always have the device-voice fallback for missing clips.
