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
parser.add_argument('--other-pois', default=None,
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Values of the other pois (not scanned), passed as poi=value. "
                             "Do not put spaces before or after the = sign. "
                             "Separate multiple entries just with a space. Example: "
                             "--other-pois ctth=1 cgghh=2. "
                             "All parameters not explicitely set are assumed to be at SM value"
                    )
parser.add_argument('--xmin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--xmax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--ymin', default=None, help="x min poi scan range", type=float)
parser.add_argument('--ymax', default=None, help="x max poi scan range", type=float)
parser.add_argument('--output', default='limit_scan_2D_{xpoi}_{ypoi}_{cmap}.pdf', help="output file name. Use {xpoi}, {ypoi} to replace it with pois (defaults to likelihood_scan_2D_{xpoi}_{ypoi}.pdf")
parser.add_argument('--smeft', dest='do_heft', default=True, help="Do calculations for SMEFT (default is for HEFT)", action='store_false')
args = parser.parse_args()

data = json.load(open(args.input))
df = pd.DataFrame(data)

if args.do_heft:
    pois = ['chhh', 'ctth', 'cgghh', 'cggh', 'ctthh']
    SM_vals = {
        'chhh'  : 1.0,
        'ctth'  : 1.0,
        'cgghh' : 0.0,
        'cggh'  : 0.0,
        'ctthh' : 0.0
    }

    poi_names = {
        'chhh'  : '$c_{hhh}$',
        'ctth'  : '$c_{tth}$',
        'cgghh' : '$c_{gghh}$',
        'cggh'  : '$c_{ggh}$',
        'ctthh' : '$c_{tthh}$',
    }


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

else:
    pois = ['cdp', 'cp', 'ctp', 'ctG', 'cpg']
    SM_vals = {
        'cdp'  : 0,
        'cp'   : 0,
        'ctp'  : 0,
        'ctG'  : 0,
        'cpg'  : 0, 
    }

    # from matplotlib import rcParams
    # rcParams['text.usetex'] = True
    # rcParams['text.latex.preamble'] = r'\usepackage{txfonts}'

    poi_names     = {
        'cdp'   : r'$c_{H,box}$', ## cannot make \Box or \square here
        'cp'    : r'$C_{H}$',
        'ctp'   : r'$c_{tH}$',
        'ctG'   : r'$c_{tG}$',
        'cpg'   : r'$c_{HG}$',
    }

    def poly(cdp, cp, ctp, ctG, cpg, A):
        x =   A[0] \
            + A[1]*pow(cdp,2) \
            + A[2]*cdp + \
            + A[3]*cdp*cp  \
            + A[4]*cp  \
            + A[5]*pow(cp,2)  \
            + A[6]*pow(ctp,2)  \
            + A[7]*ctp  \
            + A[8]* ctp*ctG  \
            + A[9]*ctG  \
            + A[10]* pow(ctG,2)  \
            + A[11]*cdp*ctG  \
            + A[12]*ctG*cp  \
            + A[13]*cdp*ctp  \
            + A[14]*ctp*cp  \
            + A[15]*cpg  \
            + A[16]*pow(cpg,2)  \
            + A[17]*cpg*cdp  \
            + A[18]*cpg*cp  \
            + A[19]*cpg*ctp  \
            + A[20]*cpg*ctG
        return x

    Ais = [
        0.992652175833,
        0.0236062036428,
        -0.201518673732,
        -0.068558440664,
        0.385872898662,
        0.0648165003344,
        0.0277950718495,
        0.226535909757,
        -0.506589981683,
        -2.12463049612,
        3.92349636854,
        0.520249328466,
        -0.789027573599,
        -0.0481140193057,
        0.0604592832381,
        -31.22783335,
        1083.68344927,
        8.31836177423,
        -12.6761233883,
        -7.93244406495,
        129.887527593,
    ]    

fixed_pois = list(pois)
fixed_pois.remove(args.xpoi)
fixed_pois.remove(args.ypoi)
fixed_pois = {x : SM_vals[x] for x in fixed_pois} # convert to dictionary with SM values

# override values if needed
if args.other_pois:
    for elem in args.other_pois:
        poi, val = elem.split('=')
        if not poi in pois:
            raise RuntimeError("cannot parse {} : POI name {} not understood".format(elem, poi))
        if poi == scanned_poi:
            print(f'[WARNING] POI named {poi} is declared as the scanned POI, so its declaration as {elem} with --other-pois will be ignored')
            continue
        val = float(val)
        fixed_pois[poi] = val

# log info
print(f'\n[INFO] : scanning POI x : {args.xpoi}, y : {args.ypoi}')
print(f'       : the other POIs are set to the following values:')
for poi in pois:
    if poi != args.xpoi and poi != args.ypoi:
        print('       : {:<5} = {:.2f}'.format(poi, fixed_pois[poi]))



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


scales = []
for ientry in range(len(x_data)):
    xval = x_data[ientry]
    yval = y_data[ientry]
    poi_dict = {**fixed_pois, args.xpoi : xval, args.ypoi : yval}
    poi_dict['A'] = Ais
    s = poly(**poi_dict)
    scales.append(s)
import numpy as np
scales = np.asarray(scales)

df['0'] = df['0']*scales

table = df.pivot(args.ypoi, args.xpoi, '0')

ax = sns.heatmap(table, cmap=cmap, norm=LogNorm(), cbar_kws={'label': r'Expected 95% CL median upper limit [fb]'})
hep.atlas.text("Preliminary")
hep.atlas.label(data=True, lumi=139)

ax.invert_yaxis()

hep.atlas.set_xlabel(poi_names[args.xpoi])
hep.atlas.set_ylabel(poi_names[args.ypoi])

oname = args.output.format(xpoi=args.xpoi, ypoi=args.ypoi, cmap=cmap)
print(f'[INFO] : pdf output saved as {oname}')
fig.tight_layout()
fig.savefig(oname)
pngname = oname.replace('.pdf', '.png')
fig.savefig(pngname)
print(f'[INFO] : png output saved as {pngname}')


plt.close()
