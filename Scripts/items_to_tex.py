import yaml
import os

# load in abilities from YAML
with open("psionic_items.yml") as stream:
    try:
        items = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# abilities is a list of dicts
items = sorted(items, key=lambda d: d['name'])
strings = []
print('Reading {} items.'.format(len(items)))

for item in items:
    long_item_string = f'''\\DndFeatHeader{{{item['name']}}}[%
    {item['subtitle']}]
{item['long_description']}
'''
    strings.append(long_item_string)

print('Writing full list to Tables/psionic_items.tex.')
with open('Tables/psionic_items.tex', 'a') as f:
    open('Tables/psionic_items.tex', 'w').close()
    for item in strings:
        f.write(item)