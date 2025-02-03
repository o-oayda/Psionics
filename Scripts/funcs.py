import yaml
import re

def name_to_ref(name, label=True, power=True):
    ref = name.lower().replace(' ', '-')
    key = 'pwr' if power else 'spl'
    if label:
        ref = '\\label{{{}:{}}}'.format(key, ref)
    else:
        ref = '\\nameref{{{}:{}}}'.format(key, ref)
    ref = ref.replace(',', '')
    ref = ref.replace('\'', '')
    return ref

def integer_to_ordinal(n: int) -> str:
    ordinal = "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    return ordinal

def load_yml(path: str) -> dict:
    with open(path) as stream:
        try:
            yml_info = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    return dict(sorted(yml_info.items()))\

def get_internal_latex(latex: str) -> str:
    ind1 = latex.find('\n')
    ind2 = latex.rfind('\n')
    return latex[ind1+1:ind2]

def mdlist_to_latex(text):
    if text:
        # Split the text into lines and iterate over
        lines = text.split('\n')
        print(lines)
        in_list = False
        result = []
        for line in lines:
            if re.match(r'^\s*-\s+', line):
                if not in_list:
                    result.append('\\begin{itemize}')
                    in_list = True
                result.append(re.sub(r'^\s*-\s+', r'\\item ', line))
            else:
                if in_list and (line == '}' or line == ''):
                    result.append('\\end{itemize}')
                    in_list = False
                result.append(line)
        if in_list:
            result.append('\\end{itemize}')
        return '\n'.join(result)
    return text