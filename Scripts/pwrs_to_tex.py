import os
from funcs import name_to_ref, integer_to_ordinal, load_yml

yml_powers = load_yml('powers_final.yml')

strings = []
print('Reading {} powers.'.format(len(yml_powers)))

for key, val in yml_powers.items():
    ordinal = integer_to_ordinal(int(val['Level']))
    hdr = f'{ordinal}-level {val['Discipline']}'
    cost = f'MB {val['MB']}, PD {val['PD']}'
    
    if val['Augment'] is not None:
        augment = rf'\augment{{{val['Augment']}}}'
    else:
        augment = ''
    
    ref = name_to_ref(key, power=True)
    title = '{}{}'.format(key, ref)

    long_power_string = f'''\DndPowerHeader%
    {{{title}}}
    {{{hdr}}}
    {{{val['Manifesting Time']}}}
    {{{val['Range']}}}
    {{{cost}}}
    {{{val['Duration']}}}
    {{{val['Requirements']}}}
{val['Long Description'][:-1]}
{augment}'''
    strings.append(long_power_string)

print('Writing full list to powers_final.tex.')
with open('powers_final.tex', 'a') as f:
    open('powers_final.tex', 'w').close()
    for pwr in strings:
        f.write(pwr + os.linesep)