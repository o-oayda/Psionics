import pandas as pd

powers = pd.read_csv('powers.csv', header=0)
powers.sort_values(by='Name', inplace=True)

psi_knight_powers = powers[(powers['Class'] == 'pk') |\
                                (powers['Class'] == 'ppk')]
psion_powers = powers[(powers['Class'] == 'p') |\
                                (powers['Class'] == 'ppk')]

psi_knight_powers.sort_values(by=['Level', 'Name'],
                              ascending=[True, True],
                              inplace=True)
psi_knight_powers[
    ['Name', 'Level', 'Short Description']].\
        to_latex('Tables/psi_knight.tex',
                 index=False)

psion_powers.sort_values(by=['Level', 'Name'],
                         ascending=[True, True],
                         inplace=True)
psion_powers[
    ['Name', 'Level', 'Short Description']].\
        to_latex('Tables/psion.tex',
                 index=False)