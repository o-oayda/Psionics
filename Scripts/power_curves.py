import matplotlib.pyplot as plt
import numpy as np

levels = np.linspace(1,20,20)
pd_dict = {
    'psion': [2,5,10,13,23,28,35,42,58,67,78,
              78,91,91,106,106,123,132,143,156],
    'psi_knight': [1,2,3,4,6,9,12,15,18,21,25,29,
                   33,37,42,47,52,58,64,70],
    'cost_pwr_level': np.linspace(1, 17, 9)
}

for key, val in pd_dict.items():
    if key in ['psion', 'psi_knight']:
        plt.plot(levels, val, label=key)
    # elif key == 'cost_pwr_level':
        # [plt.axhline(y=i, label='Level {}'.format(i),
                        # linestyle='dashed') for i in val]

alpha_pk = 1.1
alpha_p = 1.55
pk_new = [int(i) for i in levels ** alpha_pk]
p_new = [int(i) for i in levels ** alpha_p]
plt.plot(levels, pk_new, label='psi_knight_new')
plt.plot(levels, p_new, label='psion_new')
print(pk_new)
print(p_new)

plt.legend()
plt.show()