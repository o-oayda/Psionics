import yaml
import os
from funcs import name_to_ref

with open("powers_final.yml") as stream:
    try:
        yml_powers = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

yml_powers = dict(sorted(yml_powers.items()))
strings = []
print('Reading {} powers.'.format(len(yml_powers)))
for key, val in yml_powers.items():
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    hdr = ordinal(int(val['Level'])) + '-level ' + val['Discipline']
    cost = 'MB {}, PD {}'.format(val['MB'], val['PD'])
    if val['Augment'] is not None:
        augment = rf'\augment{{{val['Augment']}}}'
    else:
        augment = ''
    ref = name_to_ref(key)
    title = '{}{}'.format(key, ref)

    long_power_string = f'''\DndPowerHeader%
    {{{title}}}
    {{{hdr}}}
    {{{val['Manifesting Time']}}}
    {{{val['Range']}}}
    {{{cost}}}
    {{{val['Duration']}}}
{val['Long Description'][:-1]}
{augment}'''
    strings.append(long_power_string)

print('Writing full list to powers_final.tex.')
with open('powers_final.tex', 'a') as f:
    open('powers_final.tex', 'w').close()
    for pwr in strings:
        f.write(pwr + os.linesep)