import re, urllib.parse, os, requests

with open('canva_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all thumbnail urls
thumbnails = re.findall(r'(https://media\.canva\.com/v2/document-image/[^\s\"\'<>]+)', html)
print(f'Total thumbnails found: {len(thumbnails)}')

# Also look for json data
json_matches = re.findall(r'(\{\"id\":\"DAHV7QSTT40\"[^\}]+\})', html)
print(f'JSON matches: {len(json_matches)}')

os.makedirs('canva_slides', exist_ok=True)
downloaded = []
for i, t in enumerate(thumbnails):
    # unescape html entities if any
    clean_url = t.replace('&amp;', '&')
    match_num = re.search(r'000(\d+)\.png', clean_url)
    idx = match_num.group(1) if match_num else str(i+1)
    filename = f'canva_slides/slide_{idx}.png'
    if filename not in downloaded:
        print(f'Downloading slide {idx}: {clean_url[:120]}...')
        try:
            r = requests.get(clean_url, timeout=15)
            if r.status_code == 200:
                with open(filename, 'wb') as img_f:
                    img_f.write(r.content)
                downloaded.append(filename)
                print(f'Saved {filename} ({len(r.content)} bytes)')
        except Exception as e:
            print(f'Error downloading {filename}: {e}')

print('Downloaded files:', os.listdir('canva_slides'))
