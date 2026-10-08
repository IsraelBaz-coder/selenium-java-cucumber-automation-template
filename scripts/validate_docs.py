from pathlib import Path
import re, unicodedata
from urllib.parse import unquote
root=Path(__file__).resolve().parents[1]
files=[*root.glob('*.md'),*root.glob('docs/*.md'),*root.glob('docs_en/*.md')]
def slug(s):
    s=s.lower().strip()
    s=re.sub(r'<[^>]*>','',s)
    s=re.sub(r'[^\w\- ]','',s)
    return re.sub(r'\s+','-',s)
errors=[]; count=0
for f in files:
    body=f.read_text(encoding='utf-8-sig')
    for target in re.findall(r'(?<!!)\[[^]]+\]\(([^)]+)\)',body):
        if re.match(r'^[a-z]+:',target) or target.startswith('mailto:'): continue
        t,a=(target.split('#',1)+[''])[:2] if '#' in target else (target,'')
        p=(f.parent/unquote(t)).resolve() if t else f
        count+=1
        if not p.exists(): errors.append(f'{f.relative_to(root)} -> {target}: missing file'); continue
        if a and p.suffix.lower()=='.md':
            heads={slug(x) for x in re.findall(r'^#{1,6}\s+(.+?)\s*$',p.read_text(encoding='utf-8-sig'),re.M)}
            if unquote(a) not in heads: errors.append(f'{f.relative_to(root)} -> {target}: missing anchor')
print(f'{len(files)} Markdown files; {count} internal links; {len(errors)} errors')
print('\n'.join(errors))
es = {path.name for path in (root / 'docs').glob('*.md')}
en = {path.name for path in (root / 'docs_en').glob('*.md')}
if es != en:
    print(f'Documentation trees differ: Spanish-only={sorted(es-en)}, English-only={sorted(en-es)}')
    errors.append('documentation structure mismatch')
if errors:
    raise SystemExit(1)
