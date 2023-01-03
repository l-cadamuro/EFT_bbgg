"""
3 January 2023

Started with make_2D_likelihood_scan.py 
Example usage: 

python3 make_2D_limit_scan.py --input chhh_ctthh_course/limits.json --xpoi chhh --ypoi ctthh
python3 make_2D_limit_scan.py --input chhh_cgghh_course/limits.json --xpoi chhh --ypoi cgghh
python3 make_2D_limit_scan.py --input cgghh_ctthh_course/limits.json --xpoi cgghh --ypoi ctthh
"""

import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import mplhep as hep 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help="input json file from poi scan")
parser.add_argument('--xpoi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--ypoi', required=True, help="scanned poi (reported on y-axis of the plot)")
parser.add_argument('--xmin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--xmax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--ymin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--ymax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--output', default='limit_scan_2D_{xpoi}_{ypoi}_{cmap}.pdf', help="output file name. Use {xpoi}, {ypoi} to replace it with pois (defaults to likelihood_scan_2D_{xpoi}_{ypoi}.pdf")
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
#df = df.drop(0)

### now restructure the list of values in a 2D array
x_data = np.asarray(df[args.xpoi])
y_data = np.asarray(df[args.ypoi])
z_data = np.asarray(df['0'])

# we assume data are in a grid, so determine step
x_scan = np.unique(x_data)
y_scan = np.unique(y_data)
nx = x_scan.shape[0]
ny = y_scan.shape[0]

import seaborn as sns
from matplotlib.colors import LogNorm

plt.style.use(hep.style.ATLAS) 

cmap = "viridis"
fig, ax = plt.subplots()
hep.atlas.text("Preliminary")
table = df.pivot(args.ypoi, args.xpoi, '0')

ax = sns.heatmap(table, cmap=cmap, norm=LogNorm(), cbar_kws={'label': r'Expected 95% CL median upper limit [$\frac{\sigma}{\sigma_{SM}}$]'})
ax.invert_yaxis()

ax.set_xlabel(poi_names[args.xpoi])
ax.set_ylabel(poi_names[args.ypoi])

oname = args.output.format(xpoi=args.xpoi, ypoi=args.ypoi, cmap=cmap)
fig.savefig(oname)
fig.savefig(oname.replace('.pdf', '.png'))

plt.close()


# fig, ax = plt.subplots()
# table = df.pivot(args.ypoi, args.xpoi, '0')

# print("table:",table)

# cmaps = [
    # 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'
# ]

# for cmap in cmaps:
    # print("On cmap:",cmap)