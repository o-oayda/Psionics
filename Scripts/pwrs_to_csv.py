from funcs import load_yml
import pandas as pd

powers = load_yml('powers_final.yml')
df = pd.DataFrame.from_dict(powers).T
df.to_csv('export/all_powers.csv', index=False)
