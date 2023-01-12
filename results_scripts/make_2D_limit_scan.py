"""
3 January 2023

Started with make_2D_likelihood_scan.py 
Example usage: 

python3 make_2D_limit_scan.py --input chhh_ctthh_course/limits.json --xpoi chhh --ypoi ctthh
python3 make_2D_limit_scan.py --input chhh_cgghh_course/limits.json --xpoi chhh --ypoi cgghh
python3 make_2D_limit_scan.py --input cgghh_ctthh_course/limits.json --xpoi cgghh --ypoi ctthh
python3 make_2D_limit_scan.py --input ctth_cggh/limits.json --xpoi ctth --ypoi cggh
"""

import seaborn as sns
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np
import mplhep as hep 
plt.style.use(hep.style.ATLAS)  # https://github.com/scikit-hep/mplhep/blob/4534ba9df742154b9f5c279e549e260b8e3fe43e/src/mplhep/label.py

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

### now restructure the list of values in a 2D array
x_data = np.asarray(df[args.xpoi])
y_data = np.asarray(df[args.ypoi])
z_data = np.asarray(df['0'])

# we assume data are in a grid, so determine step
x_scan = np.unique(x_data)
y_scan = np.unique(y_data)
nx = x_scan.shape[0]
ny = y_scan.shape[0]

cmap = "viridis"
fig, ax = plt.subplots()

SM_XS = 31.05 

df['0'] = df['0']*SM_XS

print("Multiplying limit values by: ",SM_XS)

table = df.pivot(args.ypoi, args.xpoi, '0')

ax = sns.heatmap(table, cmap=cmap, norm=LogNorm(), cbar_kws={'label': r'Expected 95% CL median upper limit [fb]'})
hep.atlas.text("Preliminary")
hep.atlas.label(data=True, lumi=139)

ax.invert_yaxis()

hep.atlas.set_xlabel(poi_names[args.xpoi])
hep.atlas.set_ylabel(poi_names[args.ypoi])

oname = args.output.format(xpoi=args.xpoi, ypoi=args.ypoi, cmap=cmap)
fig.tight_layout()
fig.savefig(oname)
fig.savefig(oname.replace('.pdf', '.png'))

plt.close()
