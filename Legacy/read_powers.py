import yaml

with open('powers.tex') as file:
    lines = [line.rstrip() for line in file]

powers = []
augments = []
m_times = []
ranges = []
durations = []
names = []
flag = None
augment_flag = False
for k, line in enumerate(lines):
    if flag == 'power_start':
        if i == 0:
            line = line.replace('{', '')
            line = line.replace('}', '')
            line = line.replace('$^*$', '')
            names.append(line.strip())
        if i == 2:
            line = line.replace('{', '')
            line = line.replace('}', '')
            m_times.append(line.strip())
        if i == 3:
            line = line.replace('{', '')
            line = line.replace('}', '')
            ranges.append(line.strip())
        if i == 5:
            line = line.replace('{', '')
            line = line.replace('}', '')
            durations.append(line.strip())
        if i == 6:
            flag = 'power_body'
            line += ' '
            long_string += line
        else:
            i += 1
    elif flag == 'power_body':
        if r'\augment' in line:
            augment_flag = True
            augment_string = ''
            augment_string += line
        elif 'DndPowerHeader' in line:
            flag = 'power_start'
            if augment_flag:
                augments.append(augment_string)
            else:
                augments.append(None)
            powers.append(long_string)
            augment_string = ''
            i = 0
            long_string = ''
            augment_flag = False
        elif '% P' in line:
            pass
        elif augment_flag:
            # line += ' '
            augment_string += line
        else:
            line += ' '
            long_string += line
            if k == len(lines) - 1:
                powers.append(long_string)
                augments.append(None)
    elif 'DndPowerHeader' in line:
        flag = 'power_start'
        i = 0
        long_string = ''
    else:
        pass

# turn double white spaces to new lines
processed_powers = []
for pwr_string in powers:
    pwr_string = pwr_string.replace('  ', '\n')
    processed_powers.append(pwr_string)

processed_augments = []
for aug_string in augments:
    if aug_string is not None:
        aug_string = aug_string.replace('\\augment{', '')
        aug_string = aug_string.replace('}', '')
    processed_augments.append(aug_string)

with open("powers.yml") as stream:
    try:
        yml_powers = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

yml_powers_named = {}
for power_dct in yml_powers:
    yml_powers_named[power_dct['Name']] = power_dct

j = 0
for dur, ran, m_time, nm in zip(durations, ranges, m_times, names):
    yml_powers_named[nm]['Duration'] = dur
    yml_powers_named[nm]['Range'] = ran
    yml_powers_named[nm]['Manifesting Time'] = m_time
    yml_powers_named[nm]['Long Description'] = processed_powers[j]
    yml_powers_named[nm]['Augment'] = processed_augments[j]
    j += 1

yml_order = ['Name', 'Class', 'Level', 'Discipline', 'MB', 'PD',
             'Manifesting Time', 'Range', 'Duration', 'Short Description',
             'Long Description', 'Augment']

# # sort by order defined above
for key, val in yml_powers_named.items():
    yml_powers_named[key] = {k: yml_powers_named[key][k] for k in yml_order}

with open('powers2.yml', 'w', encoding='utf8') as outfile:
    yaml.dump(yml_powers_named, outfile,
              default_flow_style=False, allow_unicode=True,
              width=60, sort_keys=False)