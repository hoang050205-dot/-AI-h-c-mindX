import re

with open('canva_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

title_m = re.search(r'<title>(.*?)</title>', html, re.I)
print('Title:', title_m.group(1) if title_m else 'None')

metas = re.findall(r'<meta[^>]+>', html, re.I)
for m in metas:
    if any(x in m.lower() for x in ['og:', 'twitter:', 'description', 'title']):
        print(m)

# Find if there are any image urls or thumbnail urls
images = re.findall(r'https?://[^\s\"\'<>]+\.(?:jpg|png|webp)', html)
print(f'Total images found: {len(images)}')
for img in images[:10]:
    print('Img:', img)
