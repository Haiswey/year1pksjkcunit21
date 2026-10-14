#!/usr/bin/env python3
"""Download the OpenMoji colour SVG for every emoji used in a lesson page source.

Usage: python3 fetch_openmoji.py SRC_HTML OUT_DIR
Writes OUT_DIR/<HEX>.svg and OUT_DIR/emoji_map.json ({emoji: svg path}).
OpenMoji is CC BY-SA 4.0: credit it on the page. Files come from raw.githubusercontent.com.
Plain text symbols that should stay text are skipped (SKIP below).
"""
import json, os, re, subprocess, sys

SKIP = {'☆', '✔', '➜'}
PAT = re.compile(r'(?:[\u2600-\u27bf\u25b6\u2b50\U0001F000-\U0001FAFF](?:\uFE0F)?'
                 r'(?:\u200d[\u2600-\u27bf\U0001F000-\U0001FAFF]\uFE0F?)*)')
URL = 'https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/color/svg/{}.svg'


def main(src, out):
    os.makedirs(out, exist_ok=True)
    text = open(src, encoding='utf8').read()
    found = sorted({m.group(0).replace('\uFE0F', '') for m in PAT.finditer(text)} - SKIP)
    ok, missing = {}, []
    for e in found:
        h = '-'.join('%X' % ord(c) for c in e)
        f = os.path.join(out, h + '.svg')
        if not os.path.exists(f):
            for attempt in range(2):            # a second try covers one-off network hiccups
                for cand in (h, h + '-FE0F'):
                    r = subprocess.run(['curl', '-s', '-f', '--max-time', '20', '-o', f, URL.format(cand)])
                    if r.returncode == 0:
                        break
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(f):
                    break
        if os.path.exists(f):
            ok[e] = f
        else:
            missing.append(e)
    json.dump(ok, open(os.path.join(out, 'emoji_map.json'), 'w'), ensure_ascii=False)
    print(len(ok), 'downloaded; missing (will stay as system emoji):', missing)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
