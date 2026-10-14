#!/usr/bin/env python3
"""Turn a folder of full-size illustration PNGs into scenes.json for build_page.py.

Usage: python3 export_scenes.py IMG_DIR scenes.json [--width 1280] [--quality 85] [--format webp|jpeg]
File name (without extension) becomes the scene key, e.g. fire.png -> "fire".
Defaults favour sharpness: 1280 px wide WebP at quality 85. The first version of this project used
800 px JPEG at quality 80 and looked soft on tablets and 3x phones.
Prints the total size so you can tell the teacher the trade-off.
"""
import argparse, base64, io, json, os
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('img_dir'); ap.add_argument('out')
ap.add_argument('--width', type=int, default=1280)
ap.add_argument('--quality', type=int, default=85)
ap.add_argument('--format', choices=['webp', 'jpeg'], default='webp')
a = ap.parse_args()

out, total = {}, 0
for name in sorted(os.listdir(a.img_dir)):
    base, ext = os.path.splitext(name)
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp'):
        continue
    im = Image.open(os.path.join(a.img_dir, name)).convert('RGB')
    if im.width > a.width:
        im = im.resize((a.width, round(im.height * a.width / im.width)), Image.LANCZOS)
    b = io.BytesIO()
    if a.format == 'webp':
        im.save(b, 'WEBP', quality=a.quality, method=6); mime = 'image/webp'
    else:
        im.save(b, 'JPEG', quality=a.quality, optimize=True, progressive=True); mime = 'image/jpeg'
    total += len(b.getvalue())
    out[base] = 'data:%s;base64,%s' % (mime, base64.b64encode(b.getvalue()).decode())
json.dump(out, open(a.out, 'w'))
print(len(out), 'scenes,', '%.0f KB' % (total / 1024), 'before base64 overhead')
