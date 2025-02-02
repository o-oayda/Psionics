from funcs import load_yml, integer_to_ordinal, get_internal_latex
from slugify import slugify
import re
import mdpd

PATH = 'md_powers/'
yml_powers = load_yml('powers_final.yml')
print('Reading {} powers.'.format(len(yml_powers)))

for key, val in yml_powers.items():
    file_title = slugify(key)
    ordinal = integer_to_ordinal(int(val['Level']))
    header = f'{ordinal}-level {val['Discipline']}'
    cost = f'MB {val['MB']}, PD {val['PD']}'
    
    # format long description to replace single line breaks with whitespace,
    # but keep double line breaks (so it appears properly in a markdown renderer)
    long_desc = val['Long Description'][:-1]
    long_desc = re.sub(r'([^\s|])\n(?!\n)', r'\1 ', long_desc)

    # format links to other powers and spells
    regex = re.compile(r'\\nameref{pwr:([^\s]*)}')
    ref_match = regex.search(long_desc)
    if ref_match:
        long_desc = re.sub(
            r'\\nameref{pwr:([^\s]*)}', r'[[\1]]', long_desc, flags=re.M
        )
    
    if val['Augment'] is not None:
        augment = f'''

**Augment.** {val['Augment'][:-1]}'''
    else:
        augment = ''

    long_power_string = f'''---
obsidianUIMode: preview
cssclasses: json5e-spell
tags:
- psionics
- power/level/{val['Level']}
- power/discipline/{val['Discipline']}
aliases: ["{key}"]
---
# {key}
*{header}*

- **Manifesting Time:** {val['Manifesting Time']}
- **Range:** {val['Range']}
- **Cost:** {cost}
- **Duration:** {val['Duration']}
- **Requirements:** {val['Requirements']}

{long_desc}{augment}'''
    
    fname = f'{file_title}.md'
    full_path = f'{PATH}{fname}'

    print(f'Creating {full_path}.')
    with open(full_path, 'w') as f:
        f.write(long_power_string)