import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help="input json file from poi scan")
parser.add_argument('--xpoi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--ypoi', required=True, help="scanned poi (reported on y-axis of the plot)")
parser.add_argument('--xmin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--xmax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--ymin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--ymax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--output', default='limit_scan_2D_{xpoi}_{ypoi}.pdf', help="output file name. Use {xpoi}, {ypoi} to replace it with pois (defaults to likelihood_scan_2D_{xpoi}_{ypoi}.pdf")
args = parser.parse_args()

data = json.load(open(args.input))
df = pd.DataFrame(data)

poi_names = {
    'chhh'  : '$c_{hhh}$',
    'ctth'  : '$c_{tth}$',
    'cgghh' : '$c_{gghh}$',
    'cggh'  : '$c_{ggh}$',
    'ctthh' : '$c_{tthh}$',
}

SM_vals = {
    'chhh'  : 1,
    'ctth'  : 1,
    'cgghh' : 0,
    'cggh'  : 0,
    'ctthh' : 0,
}

### drop first point - it's the min not ordered
df = df.drop(0)

### now restructure the list of values in a 2D array
x_data = np.asarray(df[args.xpoi])
y_data = np.asarray(df[args.ypoi])
z_data = np.asarray(df['qmu'])

# we assume data are in a grid, so determine step
x_scan = np.unique(x_data)
y_scan = np.unique(y_data)
nx = x_scan.shape[0]
ny = y_scan.shape[0]
# dx = x_scan[1] - x_scan[0]
# dy = y_scan[1] - y_scan[0]
# x0 = x_scan[0]
# y0 = y_scan[0]
# i = ((y_data - y0) / dy).astype(int) # this fails because of float stuff
# j = ((x_data - x0) / dx).astype(int)
# dx = (x_scan[-1] - x_scan[0])/(nx-1)
# dy = (y_scan[-1] - y_scan[0])/(ny-1)
# xbins = np.linspace(x_scan[0], x_scan[-1], nx)
# ybins = np.linspace(y_scan[0], y_scan[-1], ny)

import seaborn as sns
from matplotlib.colors import LogNorm
fig, ax = plt.subplots()
#table = df.pivot(args.ypoi, args.xpoi, 'qmu')
table = df.pivot(args.ypoi, args.xpoi, '0')
ax = sns.heatmap(table, cmap="Blues", norm=LogNorm(), cbar_kws={'label': r'-2$\Delta\ln(L)$'})
ax.invert_yaxis()

# import seaborn as sns
# from matplotlib.colors import LogNorm
# fig, ax = plt.subplots()
# table = df.pivot(args.ypoi, args.xpoi, 'qmu')
# ax.pcolormesh(table)

# add SM marker
# SM_coords = (SM_vals[args.xpoi], SM_vals[args.ypoi])
# ax.scatter(SM_vals[args.xpoi], SM_vals[args.ypoi], marker='*', c='red', s=100)
# print(SM_vals[args.xpoi], SM_vals[args.ypoi])
# sns.scatterplot(x=[SM_vals[args.xpoi]], y=[SM_vals[args.ypoi]], marker='*', size=10)

oname = args.output.format(xpoi=args.xpoi, ypoi=args.ypoi)
fig.tight_layout()
fig.savefig(oname)
fig.savefig(oname.replace('.pdf', '.png'))

# nx = x_scan.shape[0]
# ny = y_scan.shape[0]
# z_array = np.nan * np.empty((ny,nx))
# z_array[i, j] = z_data

# fig, ax = plt.subplots()
# # ax.plot(df[args.poi], df['qmu'], '-o', color='black', ms=2, lw=0.5)
# ax.pcolormesh(x_scan, y_scan, z_array)


# ax.set_xlabel(poi_names[args.xpoi], loc='right', size=15)
# ax.set_ylabel(poi_names[args.ypoi], loc='top', size=15)

# ax.set_ylabel(r'-2$\Delta\ln(L)$', loc='top', size=15)

# ax.set_ylim(0, 8)
# xlim = ax.get_xlim()
# if args.xmin:
#     xlim = (args.xmin, xlim[1])
# if args.xmax:
#     xlim = (xlim[0], args.xmax)
# ax.set_xlim(xlim)
# ax.set_xlim(xlim)

# ax.plot(xlim, [1,1], '--', color='black', lw=0.5)
# ax.plot(xlim, [4,4], '--', color='black', lw=0.5)

# oname = args.output.format(poi=args.poi)
# print('... saving plot as', oname)
# fig.savefig(oname)