# python make_EFT_limit_scan.py --poi chhh --input EFT_workspaces/workspace/chhh_scan/chhh_scan.json

def poly(ctthh, cgghh, cggh, chhh, ctth, A):
    ct = ctth
    ctt = ctthh
    x =   A[0]*pow(ct,4) \
        + A[1]*pow(ctt,2) \
        + A[2]*pow(ct,2)*pow(chhh,2) \
        + A[3]*pow(cggh,2)*pow(chhh,2) \
        + A[4]*pow(cgghh,2) \
        + A[5]*ctt*pow(ct,2) \
        + A[6]*pow(ct,3)*chhh \
        + A[7]*ctt*ct*chhh \
        + A[8]*ctt*cggh*chhh \
        + A[9]*ctt*cgghh \
        + A[10]*pow(ct,2)*cggh*chhh \
        + A[11]*pow(ct,2)*cgghh \
        + A[12]*ct*pow(chhh,2)*cggh \
        + A[13]*ct*chhh*cgghh \
        + A[14]*cggh*chhh*cgghh \
        + A[15]*pow(ct,3)*cggh \
        + A[16]*ct*ctt*cggh \
        + A[17]*ct*pow(cggh,2)*chhh \
        + A[18]*ct*cggh*cgghh \
        + A[19]*pow(ct,2)*pow(cggh,2) \
        + A[20]*ctt*pow(cggh,2) \
        + A[21]*pow(cggh,3)*chhh \
        + A[22]*pow(cggh,2)*cgghh
    return x

# coefficients for the total XS
# FIXME: make available from file
Ais = [
    62.4026336568,
    344.8068589056,
    9.6151130789,
    9.7924812800,
    351.7609965122,
    -268.6369098975,
    -44.1858648211,
    96.3284178194,
    80.3578393535,
    466.4328720374,
    -35.2906404279,
    -163.8576045017,
    18.3369161655,
    80.3378763535,
    87.9907108439,
    -0.2292902802,
    0.5829126704,
    0.4713946837,
    0.8104480635,
    -0.7606517422,
    2.0347523220,
    0.4053251961,
    3.2468181114
]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input', help="proto input json file from limit scan (will replace bmname). If not specified, it defaults to limits_{bmname}.json", default='limits_{bmname}.json')
parser.add_argument('--output', default='benchmarks.pdf', help="output file name")
parser.add_argument('--export-csv', default=None, help="Export plotted data as .csv . Pass a file name")
args = parser.parse_args()

bmdef = {
    'SM'  : {'chhh' : 1   ,  'ctth' : 1   ,  'cggh' : 0            ,  'cgghh' : 0             , 'ctthh' : 0},
    'BM1' : {'chhh' : 3.94,  'ctth' : 0.94,  'cggh' : 0.5          ,  'cgghh' : 0.3333333333  , 'ctthh' : -0.3333333333},
    'BM2' : {'chhh' : 6.84,  'ctth' : 0.61,  'cggh' : 0            ,  'cgghh' : -0.3333333333 , 'ctthh' : 0.3333333333  },
    'BM3' : {'chhh' : 2.21,  'ctth' : 1.05,  'cggh' : 0.5          ,  'cgghh' : 0.5           , 'ctthh' : -0.3333333333},
    'BM4' : {'chhh' : 2.79,  'ctth' : 0.61,  'cggh' : -0.5         ,  'cgghh' : 0.16666666667 , 'ctthh' : 0.3333333333  },
    'BM5' : {'chhh' : 3.95,  'ctth' : 1.17,  'cggh' : 0.16666666667,  'cgghh' : -0.5          , 'ctthh' : -0.3333333333},
    'BM6' : {'chhh' : 5.68,  'ctth' : 0.83,  'cggh' : -0.5         ,  'cgghh' : 0.3333333333  , 'ctthh' : 0.3333333333},
    'BM7' : {'chhh' : -0.1,  'ctth' : 0.94,  'cggh' : 0.16666666667,  'cgghh' : -0.16666666667, 'ctthh' : 1},
}

bm_names = {
    'SM' : 'SM',
    'BM1' : 'BM 1',
    'BM2' : 'BM 2',
    'BM3' : 'BM 3',
    'BM4' : 'BM 4',
    'BM5' : 'BM 5',
    'BM6' : 'BM 6',
    'BM7' : 'BM 7',
}

bm_toplot = ['SM','BM1','BM2','BM3','BM4','BM5','BM6','BM7']

input_files = {}
for bm in bm_toplot:
    input_files[bm] = args.input.format(bmname=bm)

# read input data
import json
import pandas as pd

dataframes = {}
for bm in bm_toplot:
    inputfile = input_files[bm]
    print(f'\n[INFO] : for benchmark {bm} reading file {inputfile}')
    limit_data = json.load(open(inputfile))
    print (limit_data)
    limit_df = pd.DataFrame(limit_data, index=[0])
    dataframes[bm] = limit_df

# limits are on mu, but we need to display limits on xs -> scale with the theoretical xs
# scales = np.asarray([poly(chhh=x, ctth=1, cgghh=0, ctthh=0, cggh=0, A=Ais) for x in xvals])

scales = {}
for bm in bm_toplot:
    poi_dict = {**bmdef[bm]}
    poi_dict['A'] = Ais
    s = poly(**poi_dict)
    scales[bm] = s

# import numpy as np
# scales = np.asarray(scales)

# scales now encode the parametrised xs at NLO. Signal was normalised at the NNLO-FTapprox xs, so we have to compensate for this value
# sigma_NNLO_SM = 31.05
# BR       = 0.26/100.
# print(f'[INFO] : EFT limits are converted from sig strength to xs considering the following values:')
# print(f'       : SM gg->HH xs {sigma_SM} fb - used for SM sample normalisation')
# print(f'       : BR (HH->bbgg) {BR} - used to express limits on HH')

# scales = 

# rescale all UL on mu by the scales, and express as limit on HH xs (divide by BR)
for bm in bm_toplot:
    dataframes[bm]['-2']   = dataframes[bm]['-2'] * scales[bm]
    dataframes[bm]['-1']   = dataframes[bm]['-1'] * scales[bm]
    dataframes[bm]['0']    = dataframes[bm]['0'] * scales[bm]
    dataframes[bm]['1']    = dataframes[bm]['1'] * scales[bm]
    dataframes[bm]['2']    = dataframes[bm]['2'] * scales[bm]
    dataframes[bm]['obs']  = dataframes[bm]['obs'] * scales[bm]

import matplotlib.pyplot as plt
fig, ax = plt.subplots()

# graphic parameters
step  = 1 # basic unit separating benchmarks, don't change
width = 0.2 # width of the benchmark band

for ibm, bm in enumerate(bm_toplot):
    df = dataframes[bm]
    x = ibm*step
    xmin = x - width
    xmax = x + width
    ax.fill_between((xmin, xmax), df['-2'], df['2'], color='#00cc00')
    ax.fill_between((xmin, xmax), df['-1'], df['1'], color='#ffcc00')
    ax.plot((xmin, xmax), (df['0'], df['0']), '-', color='black', ms=2, lw=0.5)

# xlim = ax.get_xlim()
# if args.xmin:
#     xlim = (args.xmin, xlim[1])
# if args.xmax:
#     xlim = (xlim[0], args.xmax)
# ax.set_xlim(xlim)

# ax.set_yscale('log')
# ax.set_ylim((10, 100000))

# ax.set_xlabel(poi_names[scanned_poi], loc='right', size=15)

labels = [bm_names[bm] for bm in bm_toplot]
ax.set_xticks([i for i in range(len(bm_toplot))])
ax.set_xticklabels(labels)
ax.set_ylabel(r'95% CL UL on $\sigma (pp \rightarrow HH)$ [fb]', loc='top', size=15)

fig.tight_layout()
# print(limit_df[limit_df[scanned_poi] == 1])
outname = args.output
print(f'[INFO] : output saved as {outname}')
fig.savefig(outname)

if args.export_csv:
    print(f'[INFO] : exporting plotted data frame as {args.export_csv}')
    limit_df.to_csv(args.export_csv, index=False)