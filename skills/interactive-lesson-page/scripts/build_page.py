#!/usr/bin/env python3
"""Build the final single-file lesson page from the readable source.

Usage:
  python3 build_page.py --src lesson.src.html --out page.html \
      [--emoji-map om/emoji_map.json] [--scenes scenes.json] [--voice-dir voice] \
      [--credit "图画来源说明"]

What it injects (all embedded as base64 so the page works offline):
  * OpenMoji pictures that replace system emoji at run time (from fetch_openmoji.py)
  * window.__SCENE  - scene illustrations {key: data-URI}, placed BEFORE the main script
  * window.__AUD    - recorded voice clips {exact spoken text: data-URI}, from voice/index.json + NNN.mp3
Missing inputs are simply skipped. The page falls back to system emoji and the device voice.
"""
import argparse, base64, json, os, re

EMO_JS = r'''
<script>
/* OpenMoji pictures (CC BY-SA 4.0, https://openmoji.org), embedded so the page works offline */
(function(){
  var EMO=__EMO__;
  var keys=Object.keys(EMO).sort(function(a,b){return b.length-a.length}).map(function(k){return k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&').split('').join('\uFE0F?')});
  var re=new RegExp('('+keys.join('|')+')\uFE0F?','g');
  function conv(root){
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,null),list=[],n;
    while((n=w.nextNode())){var p=n.parentNode;if(p&&p.nodeName!=='SCRIPT'&&p.nodeName!=='STYLE'&&p.nodeName!=='TITLE'&&re.test(n.nodeValue))list.push(n);re.lastIndex=0}
    list.forEach(function(t){
      var f=document.createDocumentFragment(),txt=t.nodeValue,last=0,m;re.lastIndex=0;
      while((m=re.exec(txt))){
        if(m.index>last)f.appendChild(document.createTextNode(txt.slice(last,m.index)));
        var k=m[1].replace(/\uFE0F/g,''),im=document.createElement('img');
        im.src=EMO[k];im.alt=k;im.className='emo';im.draggable=false;f.appendChild(im);last=m.index+m[0].length;
      }
      if(last<txt.length)f.appendChild(document.createTextNode(txt.slice(last)));
      t.parentNode.replaceChild(f,t);
    });
  }
  var busy=false;
  function run(){if(busy)return;busy=true;try{conv(document.body)}catch(e){}busy=false}
  new MutationObserver(run).observe(document.body,{childList:true,subtree:true,characterData:true});
  run();
})();
</script>
'''

CSS = ('.scene{display:block;width:100%;height:auto;aspect-ratio:16/9;border-radius:14px;background:var(--bg)}\n'
       '.q-pic{display:flex;flex-direction:row;gap:0;white-space:nowrap;font-size:2.1rem}\n'
       '.q-pic .emo{height:1em;width:1em}\n'
       '.emo{height:1.1em;width:1.1em;vertical-align:-.2em;display:inline-block;object-fit:contain}\n'
       '.credit{font-size:.8rem;color:var(--muted);text-align:center;margin-top:24px}\n')


def svg_uri(path):
    svg = re.sub(r'>\s+<', '><', open(path, encoding='utf8').read()).strip()
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--emoji-map')
    ap.add_argument('--scenes')
    ap.add_argument('--voice-dir')
    ap.add_argument('--credit', default='')
    a = ap.parse_args()

    s = open(a.src, encoding='utf8').read()
    s = s.replace('</style>', CSS + '</style>', 1)
    if a.credit:
        s = s.replace('</section>\n</div>\n\n<script>',
                      '</section>\n  <p class="credit">%s</p>\n</div>\n\n<script>' % a.credit, 1)

    notes = []
    if a.scenes and os.path.exists(a.scenes):
        scenes = json.load(open(a.scenes))
        main_script = '<script>\n(function(){'
        assert main_script in s, 'main script marker not found in source'
        s = s.replace(main_script, '<script>window.__SCENE=%s;</script>\n%s' % (json.dumps(scenes), main_script), 1)
        notes.append('%d scenes' % len(scenes))

    tail = ''
    if a.emoji_map and os.path.exists(a.emoji_map):
        emap = json.load(open(a.emoji_map))
        data = {e: svg_uri(p) for e, p in emap.items()}
        tail += EMO_JS.replace('__EMO__', json.dumps(data, ensure_ascii=False))
        notes.append('%d emoji pictures' % len(data))

    if a.voice_dir and os.path.exists(os.path.join(a.voice_dir, 'index.json')):
        sents = json.load(open(os.path.join(a.voice_dir, 'index.json'), encoding='utf8'))
        clips = {}
        for i, t in enumerate(sents):
            with open(os.path.join(a.voice_dir, '%03d.mp3' % i), 'rb') as f:
                clips[t] = 'data:audio/mpeg;base64,' + base64.b64encode(f.read()).decode()
        tail += '\n<script>window.__AUD=%s;</script>\n' % json.dumps(clips, ensure_ascii=False)
        notes.append('%d voice clips' % len(clips))

    s = s.rstrip() + '\n' + tail
    open(a.out, 'w', encoding='utf8').write(s)
    print('built', a.out, '%.1f MB' % (len(s.encode('utf8')) / 1e6), '|', ', '.join(notes) or 'nothing embedded')


if __name__ == '__main__':
    main()
