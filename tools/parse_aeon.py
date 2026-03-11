import json
from pathlib import Path

with open(r'C:\Users\jose_\Downloads\JSON aeon timeline lore.tsf', 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['data']['items']
events = []
for item in items:
    if item.get('start') and item.get('label') and item['label'].strip():
        events.append({
            'label': item['label'],
            'start': item['start'],
            'end': item.get('end', ''),
            'summary': item.get('propertyValues', {}).get('summary', ''),
            'tags': item.get('propertyValues', {}).get('tags', ''),
        })

events.sort(key=lambda x: x['start'])

out = Path(r'C:\Users\jose_\.openclaw\workspace\star-atlas-lore\batch15_events.txt')
with open(out, 'w', encoding='utf-8') as f:
    for i, e in enumerate(events, 1):
        if i >= 251:
            f.write(f"E{i} ({e['start']}): {e['label']}\n")
            if e['summary']:
                f.write(f"  SUMMARY: {e['summary']}\n")
            if e['tags']:
                f.write(f"  TAGS: {e['tags']}\n")
            f.write("\n")

print(f"Done - wrote events 251+ to {out}")
