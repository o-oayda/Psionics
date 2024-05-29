import yaml

with open("powers_final.yml") as stream:
    try:
        yml_powers = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for key, val in yml_powers.items():

    # n-th level discipline
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    subtitle = ordinal(int(val['Level'])) + '-level ' + val['Discipline']
    
    # handle markdown frontmatter (identical to yaml)
    frontmatter = '---\n'
    for feature, entry in val.items():
        if feature in ['Long Description', 'Augment']:
            pass
        else:
            frontmatter += f'{feature}: {entry}\n'
    frontmatter += '---'

    mdown = f'''{frontmatter}
# {val['Name']}
*{subtitle}*\\
**Manifesting Time:** {val['Manifesting Time']}\\
**Range:** {val['Range']}\\
**Cost:** MB {val['MB']}, PD {val['PD']}\\
**Duration:** {val['Duration']}\\
**Requirements:** {val['Requirements']}

{val['Long Description']}'''
    formatted_name = val['Name'].lower().replace(" ", "_").replace(",", "")
    with open(f'docs/_powers/{formatted_name}.md', 'w') as md_file:
        md_file.write(mdown)