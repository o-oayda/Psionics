import os
from funcs import (
    name_to_ref, integer_to_ordinal, load_yml, get_internal_latex
)
import re
import mdpd

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

    # check for tables in description (search for all chars between two pipes)
    long_description = val['Long Description'][:-1]
    regexp = re.compile(r'(\|[\S\s]*\|)')
    match = regexp.search(long_description)
    if match:
        df = mdpd.from_md(match[0])
        latex_table = df.style.hide(axis='index').to_latex()[:-1]
        internal_latex = get_internal_latex(latex_table)
        internal_latex = internal_latex.replace('\\\\', '\\\\\\')
        dnd_table_string = fr'''\\begin{{table}}[htbp]%
    \\begin{{DndTable}}[
        width=\\columnwidth,
        header={val['Table Header']}
    ]{{{val['Table Align']}}}
        {internal_latex}
    \\end{{DndTable}}
\\end{{table}}'''
        long_description = regexp.sub(
            repl=dnd_table_string, string=long_description
        )
    
    # replace subparagraph (bold and italics, e.g. ***Cold.***)
    long_description = re.sub(
        pattern=r'\*\*\*([\S\s]*?)\.\*\*\*',
        repl=r'\\subparagraph{\1}',
        string=long_description
    )

    # replace italics, e.g. *Exception.*
    long_description = re.sub(
        pattern=r'\*([\S\s]*?)\*',
        repl=r'\\emph{\1}',
        string=long_description
    )

    long_power_string = f'''\DndPowerHeader%
    {{{title}}}
    {{{hdr}}}
    {{{val['Manifesting Time']}}}
    {{{val['Range']}}}
    {{{cost}}}
    {{{val['Duration']}}}
    {{{val['Requirements']}}}
{long_description}
{augment}'''
    strings.append(long_power_string)

print('Writing full list to powers_final.tex.')
with open('powers_final.tex', 'a') as f:
    open('powers_final.tex', 'w').close()
    for pwr in strings:
        f.write(pwr + os.linesep)