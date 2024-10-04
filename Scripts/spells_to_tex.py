import yaml
import os
from funcs import name_to_ref, load_yml, integer_to_ordinal

spells = load_yml('spells.yml')
strings = []

for key, val in spells.items():
    ordinal = integer_to_ordinal(int(val['Level']))
    hdr = f'{ordinal}-level {val['School']}'

    if val['Upcast'] is not None:
        upcast = rf'\upcast{{{val['Upcast']}}}'
    else:
        augment = ''
    
    ref = name_to_ref(key, power=False)
    title = f'{key}{ref}'

    long_spell_string = f'''\DndSpellHeader%
    {{{title}}}
    {{{hdr}}}
    {{{val['Casting Time']}}}
    {{{val['Range']}}}
    {{{val['Components']}}}
    {{{val['Duration']}}}
{val['Long Description'][:-1]}
{augment}'''
    strings.append(long_spell_string)

print('Writing full list to spells.tex.')
with open('spells.tex', 'a') as f:
    open('spells.tex', 'w').close()
    for spl in strings:
        f.write(spl + os.linesep)

# \DndSpellHeader%
#   {Beautiful Typesetting}
#   {4th-level illusion}
#   {1 action}
#   {5 feet}
#   {S, M (ink and parchment, which the spell consumes)}
#   {Until dispelled}
# You are able to transform a written message of any length into a beautiful scroll. All creatures within range that can see the scroll must make a wisdom saving throw or be charmed by you until the spell ends.

# While the creature is charmed by you, they cannot take their eyes off the scroll and cannot willingly move away from the scroll. Also, the targets can make a wisdom saving throw at the end of each of their turns. On a success, they are no longer charmed.