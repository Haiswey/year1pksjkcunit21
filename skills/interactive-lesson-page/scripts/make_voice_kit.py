#!/usr/bin/env python3
"""Create the files a teacher runs ON HER OWN COMPUTER to record the voice (edge-tts), from sentences.json.

Usage: python3 make_voice_kit.py sentences.json OUT_DIR [--voice zh-CN-XiaoxiaoNeural] [--rate -12%] [--pitch +4Hz]

Writes OUT_DIR/make_voice_local.py   (Windows/Mac: pip install edge-tts, then py make_voice_local.py)
       OUT_DIR/make_voice.ipynb      (Google Colab backup; may fail with 403 like the cloud does)
       OUT_DIR/make_voice_gtts.ipynb (Google voice backup, plainer sound)
The recordings must be made on her own computer because Microsoft's speech server refuses cloud servers (403).
She sends back voice.zip; unzip it and pass the folder to build_page.py --voice-dir (needs index.json + NNN.mp3).
"""
import argparse, json, os

ap = argparse.ArgumentParser()
ap.add_argument('sentences'); ap.add_argument('out_dir')
ap.add_argument('--voice', default='zh-CN-XiaoxiaoNeural')
ap.add_argument('--rate', default='-12%')
ap.add_argument('--pitch', default='+4Hz')
a = ap.parse_args()
os.makedirs(a.out_dir, exist_ok=True)
sents = json.load(open(a.sentences, encoding='utf8'))
S = json.dumps(sents, ensure_ascii=False, indent=1)

local = '''# Run on your own computer. Windows:  py -m pip install edge-tts   then   py make_voice_local.py
import asyncio, json, os, zipfile
import edge_tts

VOICE = "@V@"
RATE = "@R@"
PITCH = "@P@"

SENTENCES = @S@

async def main():
    os.makedirs("voice", exist_ok=True)
    for i, t in enumerate(SENTENCES):
        await edge_tts.Communicate(t, VOICE, rate=RATE, pitch=PITCH).save(f"voice/{i:03d}.mp3")
        print("done", i + 1, "/", len(SENTENCES), t[:20])
    with open("voice/index.json", "w", encoding="utf8") as f:
        json.dump(SENTENCES, f, ensure_ascii=False)
    with zipfile.ZipFile("voice.zip", "w") as z:
        for f in sorted(os.listdir("voice")):
            z.write("voice/" + f)
    print("All done. Send voice.zip back. File:", os.path.abspath("voice.zip"))

asyncio.run(main())
input("Press Enter to close")
'''.replace('@V@', a.voice).replace('@R@', a.rate).replace('@P@', a.pitch).replace('@S@', S)
open(os.path.join(a.out_dir, 'make_voice_local.py'), 'w', encoding='utf8').write(local)

colab = '''!pip -q install edge-tts
import edge_tts, json, os, zipfile
from google.colab import files
VOICE = "@V@"; RATE = "@R@"; PITCH = "@P@"
SENTENCES = @S@
os.makedirs("voice", exist_ok=True)
for i, t in enumerate(SENTENCES):
    await edge_tts.Communicate(t, VOICE, rate=RATE, pitch=PITCH).save(f"voice/{i:03d}.mp3")
json.dump(SENTENCES, open("voice/index.json", "w", encoding="utf8"), ensure_ascii=False)
with zipfile.ZipFile("voice.zip", "w") as z:
    for f in sorted(os.listdir("voice")): z.write("voice/" + f)
files.download("voice.zip")
'''.replace('@V@', a.voice).replace('@R@', a.rate).replace('@P@', a.pitch).replace('@S@', S)

gtts = '''!pip -q install gTTS
import json, os, zipfile
from gtts import gTTS
from google.colab import files
SENTENCES = @S@
os.makedirs("voice", exist_ok=True)
for i, t in enumerate(SENTENCES):
    gTTS(t, lang="zh-CN", slow=False).save(f"voice/{i:03d}.mp3")
json.dump(SENTENCES, open("voice/index.json", "w", encoding="utf8"), ensure_ascii=False)
with zipfile.ZipFile("voice.zip", "w") as z:
    for f in sorted(os.listdir("voice")): z.write("voice/" + f)
files.download("voice.zip")
'''.replace('@S@', S)

def nb(name, code, title):
    return {"nbformat": 4, "nbformat_minor": 5,
            "metadata": {"colab": {"name": name}, "kernelspec": {"name": "python3", "display_name": "Python 3"}},
            "cells": [{"cell_type": "markdown", "id": "a1", "metadata": {}, "source": [title]},
                      {"cell_type": "code", "id": "a2", "metadata": {}, "execution_count": None, "outputs": [],
                       "source": code.splitlines(True)}]}

json.dump(nb('make_voice.ipynb', colab, '# Make voice: Runtime > Run all, then send voice.zip'),
          open(os.path.join(a.out_dir, 'make_voice.ipynb'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
json.dump(nb('make_voice_gtts.ipynb', gtts, '# Make voice (Google voice): Runtime > Run all, then send voice.zip'),
          open(os.path.join(a.out_dir, 'make_voice_gtts.ipynb'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('wrote make_voice_local.py, make_voice.ipynb, make_voice_gtts.ipynb for', len(sents), 'sentences')
