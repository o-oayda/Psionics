from funcs import load_yml, integer_to_ordinal
from slugify import slugify
import re
import os


PATH = 'md_powers/'
if not os.path.exists(PATH):
    os.makedirs(PATH)
yml_powers = load_yml('powers_final.yml')
print('Reading {} powers.'.format(len(yml_powers)))

for key, val in yml_powers.items():
    file_title = slugify(key)
    ordinal = integer_to_ordinal(int(val["Level"]))
    header = f"{ordinal}-level {val['Discipline']}"
    cost = f"MB {val['MB']}, PD {val['PD']}"
    discipline_slug = slugify(val["Discipline"], separator="_")
    
    # format long description to replace single line breaks with whitespace,
    # but keep double line breaks (so it appears properly in a markdown renderer)
    long_desc = val["Long Description"][:-1]
    long_desc = re.sub(r'([^\s|])\n(?!\n)', r'\1 ', long_desc)
    long_desc = long_desc.replace('`', "'")

    # format links to other powers and spells
    regex = re.compile(r'\\nameref{pwr:([^\s]*)}')
    ref_match = regex.search(long_desc)
    if ref_match:
        long_desc = re.sub(
            r'\\nameref{pwr:([^\s]*)}', r'[[\1]]', long_desc, flags=re.M
        )

    def replace_spell(match):
        spell_name = match.group(1).strip()
        spell_slug = slugify(spell_name, separator='-')
        return f"[[compendium/spells/{spell_slug}]]"

    long_desc = re.sub(r'\\spell\{([^}]+)\}', replace_spell, long_desc)
    
    if val["Augment"] is not None:
        augment_text = val["Augment"].rstrip('\n')
        augment_text = re.sub(r'([^\s|])\n(?!\n)', r'\1 ', augment_text)
        augment_text = augment_text.replace('`', "'")
        augment_text = re.sub(r'\\spell\{([^}]+)\}', replace_spell, augment_text)
        augment = f"""

**Augment.** {augment_text}"""
    else:
        augment = ''

    long_power_string = f'''---
obsidianUIMode: preview
cssclasses: json5e-spell
tags:
- psionics
- power/level/{val['Level']}
- power/discipline/{discipline_slug}
aliases: ["{key}"]
---
# {key}
*{header}*

- **Manifesting Time:** {val['Manifesting Time']}
- **Range:** {val['Range']}
- **Base Cost:** {cost}
- **Duration:** {val['Duration']}
- **Requirements:** {val['Requirements']}

{long_desc}{augment}'''
    
    fname = f'{file_title}.md'
    full_path = f'{PATH}{fname}'

    print(f'Creating {full_path}.')
    with open(full_path, 'w') as f:
        f.write(long_power_string)
