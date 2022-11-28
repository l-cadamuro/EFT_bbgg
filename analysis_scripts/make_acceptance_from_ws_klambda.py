# python make_acceptance_from_ws_klambda.py --input ~/HH/EFT_bbgg/database/workspaces/NonResonant_Wisconsin/legacy_h027_stat_only/workspace/WS-bbyy-non-resonant-param.root --do-yield --export klambda.pkl

import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='input workspace root file')
parser.add_argument('--WS', default='combWS', help='input workspace name')
parser.add_argument('--x-min', default=-10, help="scanned poi range - min value")
parser.add_argument('--x-max', default=10, help="scanned poi range - max value")
parser.add_argument('--x-step', default=100, help="scanned poi range - number of steps to perform in range (will do N+1 to include endpoint)")
parser.add_argument('--do-yield', dest='do_eff', default=True, help="plot the absolute yield instead of acceptance (default: plot acceptance)", action='store_false')
parser.add_argument('--export', dest="export", default=None, help='export file of plotted data')
args = parser.parse_args()

if args.do_eff:
    raise RuntimeError('efficiency not yet implemented (need xs). TODO. For yield use --do-yield')

print('[INFO] : opening file', args.input)
fIn = ROOT.TFile.Open(args.input)
print('[INFO] : retrieving workspace', args.WS)
ws = fIn.Get(args.WS)
# ws.Print()

# modelconfig = ws.obj("ModelConfig")

# retrieve POIs
klambda  = ws.var('klambda')

categs = ['SM_1', 'SM_2', 'SM_3', 'BSM_1', 'BSM_2', 'BSM_3', 'BSM_4']

yield_name_proto = 'yield__HH_ggF_{categ}'
print(f'[INFO] : yields expressions are searched for as {yield_name_proto}')

yields_funcs = {}
for c in categs:
    yields_funcs[c] = ws.function(yield_name_proto.format(categ=c)) # get yield by doing getVal()

import numpy as np
xmin = args.x_min
xmax = args.x_max
print(f'[INFO] : scanning {args.x_step} points from {xmin} to {xmax}')
scan_points = np.linspace(xmin, xmax, args.x_step+1)

yields = {}
for sp in scan_points:
    ## set the only parameter to change here
    # chhh.setVal(sp)
    klambda.setVal (sp)
    yields[sp] = {}
    for c in categs:
        yields[sp][c] = yields_funcs[c].getVal()

### FIXME: here accepance if needed
if args.do_eff:
    pass
else:
    print(f'[INFO] : plotting total yield')
    denom_scale = np.ones(len(scan_points))    

import matplotlib.pyplot as plt

fig, axs = plt.subplots(2)
# axs = [axs,] # so easier to index more after

plt.ion()

tot_yield = np.zeros(len(scan_points))
curves = {}
curves['xdata'] = scan_points
for c in categs:
    data_points = [] # store yield for this category in steps of poi
    for x in scan_points:
        ytot = yields[x][c]
        data_points.append(ytot)
        # print(data_points)
    data_points = np.asarray(data_points)
    tot_yield = tot_yield + data_points
    data_points = data_points / denom_scale # this makes yield / tot_yield = acceptance, or leaves yield in case denom_scale was just oness
    axs[0].plot(scan_points, data_points, '-o', label=f'{c}')
    curves[c] = data_points

axs[0].set_xlabel(r'$\kappa_{\lambda}$')
axs[0].set_ylabel('Acceptance' if args.do_eff else 'Yield')
axs[0].legend(loc='upper left')

tot_yield = tot_yield / denom_scale
axs[1].plot(scan_points, tot_yield, '-o', label='Total')
curves['tot'] = tot_yield

axs[1].set_xlabel(r'$\kappa_{\lambda}$')
axs[1].set_ylabel('Acceptance' if args.do_eff else 'Yield')

fig.tight_layout()
typename = 'eff' if args.do_eff else 'yield'
fig.savefig(f'{typename}_klambda.pdf')

if args.export:
    import pickle
    fout = open(args.export, 'wb')
    odata = {'curves' : curves}
    pickle.dump(odata, fout)