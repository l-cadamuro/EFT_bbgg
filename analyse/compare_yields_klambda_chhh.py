import pickle
import matplotlib.pyplot as plt

fchhh = 'chhh_yield.pkl'
fklambda = 'klambda_yield.pkl'

print('chhh yields read from: ', fchhh)
print('klambda yields read from: ', fklambda)

c_chhh = pickle.load(open(fchhh, 'rb'))['curves']
c_klambda = pickle.load(open(fklambda, 'rb'))['curves']

categs = ['SM_1', 'SM_2', 'SM_3', 'BSM_1', 'BSM_2', 'BSM_3', 'BSM_4', 'tot']

fig, axs = plt.subplots(2, 4, figsize=(12,6))

for ic, c in enumerate(categs):
    irow = ic//4
    icol = ic%4
    axs[irow][icol].plot(c_chhh['xdata'], c_chhh[c], label='chhh')
    axs[irow][icol].plot(c_klambda['xdata'], c_klambda[c], label='klambda')
    axs[irow][icol].legend(loc='best')
    axs[irow][icol].set_xlabel('chhh or klambda')
    axs[irow][icol].set_ylabel('Parametrised yield')
    axs[irow][icol].set_title(c)
    
    chhh_mask = (c_chhh['xdata'] == 1)
    klambda_mask = (c_klambda['xdata'] == 1)
    masked_chhh = c_chhh[c][chhh_mask]
    masked_klambda = c_klambda[c][klambda_mask]
    print('cat', c, 'SM yield: chhh = {}, klambda = {}, diff = {}'.format(masked_chhh, masked_klambda, masked_chhh-masked_klambda))

fig.tight_layout()
oname = 'comparison_chhh_klambda.pdf'
print('... saving comparison plot as', oname)
fig.savefig(oname)