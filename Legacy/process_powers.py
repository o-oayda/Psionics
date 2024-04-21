import pandas as pd
import os

# read all powers and sort
powers = pd.read_csv('powers.csv', header=0)
powers.sort_values(by='Name', inplace=True)
n_powers = len(powers)
chk_sum = 0

# parse class (I regret my choice of class flags...)
idx_dict = {
    'psi_knight': [],
    'psion': [],
    'prescience': [],
    'prana_bindu': [],
    'voice': [],
    'metacreativity': [],
    'spacefolding': [],
    'psychokinesis': []
}

for idx, class_identifier in enumerate(powers['Class']):
    # grab discipline sublist powers
    sublist = False
    if '-' in class_identifier:
        sublist = True
        match class_identifier.split('-')[1]:
            case 'P':
                idx_dict['prescience'].append(idx)
            case 'PB':
                idx_dict['prana_bindu'].append(idx)
            case 'V':
                idx_dict['voice'].append(idx)
            case 'M':
                idx_dict['metacreativity'].append(idx)
            case 'S':
                idx_dict['spacefolding'].append(idx)
            case 'PK':
                idx_dict['psychokinesis'].append(idx)
            case _:
                raise Exception('Unknown discipline detected.')

    # grab class powers
    if 'ppk' in class_identifier:
        idx_dict['psi_knight'].append(idx)
        idx_dict['psion'].append(idx)
        chk_sum += 1
    elif 'pk' in class_identifier:
        idx_dict['psi_knight'].append(idx)
        chk_sum += 1
    elif 'p' in class_identifier and sublist:
        chk_sum += 1
        pass
    elif 'p' in class_identifier and not sublist:
        idx_dict['psion'].append(idx)
        chk_sum += 1

if chk_sum != n_powers:
    raise Exception('One or more powers has been missed!')

remove_chars = [r'\begin{tabular}{lrl}',
                r'\toprule',
                r'\midrule',
                r'\bottomrule',
                r'\end{tabular}']

for key, val in idx_dict.items():
    powers_subset = powers.iloc[val][
        ['Name', 'Level', 'Short Description']]
    powers_subset.sort_values(by=['Level', 'Name'],
                              ascending=[True, True],
                              inplace=True)
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