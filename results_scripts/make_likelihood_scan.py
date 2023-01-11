import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help="input json file from poi scan")
parser.add_argument('--poi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--xmin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--xmax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--output', default='likelihood_scan_{poi}.pdf', help="output file name. Use {poi} to replace it with poi (defaults to limit_scan_{poi}.pdf)")
args = parser.parse_args()

data = json.load(open(args.input))
df = pd.DataFrame(data)

poi_names = {
    'chhh'  : '$c_{hhh}$',
    'ctth'  : '$c_{tth}$',
    'cgghh' : '$c_{gghh}$',
    'cggh'  : '$c_{ggh}$',
    'ctthh' : '$c_{tthh}$',
    ######
    'cdp'   : r'$c_{H,box}$',
    'cp'    : r'$C_{H}$',
    'ctp'   : r'$c_{tH}$',
    'ctG'   : r'$c_{tG}$',
    'cpg'   : r'$c_{HG}$',
}

### drop first point - it's the min not ordered
df = df.drop(0)

fig, ax = plt.subplots()
ax.plot(df[args.poi], df['qmu'], '-o', color='black', ms=2, lw=0.5)

ax.set_xlabel(poi_names[args.poi], loc='right', size=15)
ax.set_ylabel(r'-2$\Delta\ln(L)$', loc='top', size=15)

ax.set_ylim(0, 8)
xlim = ax.get_xlim()
if args.xmin:
    xlim = (args.xmin, xlim[1])
if args.xmax:
    xlim = (xlim[0], args.xmax)
ax.set_xlim(xlim)
ax.set_xlim(xlim)

ax.plot(xlim, [1,1], '--', color='black', lw=0.5)
ax.plot(xlim, [4,4], '--', color='black', lw=0.5)

oname = args.output.format(poi=args.poi)
print('... saving plot as', oname)
fig.savefig(oname)