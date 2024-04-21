import yaml
import pandas as pd
import os
from funcs import name_to_ref

with open("powers_final.yml") as stream:
    try:
        yml_powers = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
n_powers = len(yml_powers)
chk_sum = 0

pwr_dict = {
    'psi_knight': [],
    'psion': [],
    'prescience': [],
    'prana_bindu': [],
    'voice': [],
    'metacreativity': [],
    'spacefolding': [],
    'psychokinesis': []
}

for key, val in yml_powers.items():
    # grab discipline sublist powers
    sublist = False
    if '-' in val['Class']:
        sublist = True
        match val['Class'].split('-')[1]:
            case 'P':
                pwr_dict['prescience'].append(val)
            case 'PB':
                pwr_dict['prana_bindu'].append(val)
            case 'V':
                pwr_dict['voice'].append(val)
            case 'M':
                pwr_dict['metacreativity'].append(val)
            case 'S':
                pwr_dict['spacefolding'].append(val)
            case 'PK':
                pwr_dict['psychokinesis'].append(val)
            case _:
                raise Exception('Unknown discipline detected.')

    # grab class powers
    if 'ppk' in val['Class']:
        pwr_dict['psi_knight'].append(val)
        pwr_dict['psion'].append(val)
        chk_sum += 1
    elif 'pk' in val['Class']:
        pwr_dict['psi_knight'].append(val)
        chk_sum += 1
    elif 'p' in val['Class'] and sublist:
        chk_sum += 1
        pass
    elif 'p' in val['Class'] and not sublist:
        pwr_dict['psion'].append(val)
        chk_sum += 1

if chk_sum != n_powers:
    raise Exception('One or more powers has been missed!')

remove_chars = [r'\begin{tabular}{lll}',
                r'\toprule',
                r'\midrule',
                r'\bottomrule',
                r'\end{tabular}']

print('Writing power subclass tables.')
for key, val in pwr_dict.items():
    powers_subset = pd.DataFrame(val)
    powers_subset = powers_subset[['Name', 'Level', 'Short Description']]
    powers_subset.sort_values(by=['Level', 'Name'],
                              ascending=[True, True],
                              inplace=True)
    
    for idx, row in powers_subset.iterrows():
        ref = name_to_ref(row['Name'], label=False)
        powers_subset.at[idx, 'Name'] = ref
    
    latex = powers_subset.to_latex(index=False)

    # remover latex table formatting
    for char in remove_chars:
        latex = latex.replace(char, '')

    # remove empty lines
    latex = os.linesep.join([s for s in latex.splitlines() if s])

    # remove last three characters (final \\ on table)
    latex = latex[:-3]

    # write to tex tile
    with open('Tables/{}.tex'.format(key), "w") as f:
        f.write(latex)