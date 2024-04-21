def name_to_ref(name, label=True):
    ref = name.lower().replace(' ', '_')
    if label:
        ref = '\\label{{pwr:{}}}'.format(ref)
    else:
        ref = '\\nameref{{pwr:{}}}'.format(ref)
    ref = ref.replace(',', '')
    ref = ref.replace('\'', '')
    return ref