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
parser.add_argument('--input', help="input json file from limit scan. If not specified, it defaults to {poi}_limit_scan/limits.json", default='{poi}_limit_scan/limits.json')
parser.add_argument('--poi', required=True, help="scanned poi (reported on x-axis of the plot)")
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
parser.add_argument('--output', default='limit_scan_{poi}.pdf', help="output file name. Use {poi} to replace it with poi (defaults to limit_scan_{poi}.pdf)")
parser.add_argument('--export-csv', default=None, help="Export plotted data as .csv . Pass a file name")
args = parser.parse_args()

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

scanned_poi = args.poi
fixed_pois = list(pois)
fixed_pois.remove(scanned_poi)
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
print(f'\n[INFO] : scanning POI {scanned_poi}')
print(f'       : the other POIs are set to the following values:')
for poi in pois:
    if poi != scanned_poi:
        print('       : {:<5} = {:.2f}'.format(poi, fixed_pois[poi]))

# read input data
import json
import pandas as pd
inputfile = args.input.format(poi=scanned_poi)
print(f'\n[INFO] : reading file {inputfile}')
limit_data = json.load(open(inputfile))
limit_df = pd.DataFrame(limit_data)

# limits are on mu, but we need to display limits on xs -> scale with the theoretical xs
# scales = np.asarray([poly(chhh=x, ctth=1, cgghh=0, ctthh=0, cggh=0, A=Ais) for x in xvals])

scales = []
for poival in limit_df[scanned_poi]:
    poi_dict = {**fixed_pois, scanned_poi : poival}
    poi_dict['A'] = Ais
    s = poly(**poi_dict)
    scales.append(s)

import numpy as np
scales = np.asarray(scales)

# scales now encode the parametrised xs at NLO. Signal was normalised at the NNLO-FTapprox xs, so we have to compensate for this value
# sigma_NNLO_SM = 31.05
# BR       = 0.26/100.
# print(f'[INFO] : EFT limits are converted from sig strength to xs considering the following values:')
# print(f'       : SM gg->HH xs {sigma_SM} fb - used for SM sample normalisation')
# print(f'       : BR (HH->bbgg) {BR} - used to express limits on HH')

# scales = 

# rescale all UL on mu by the scales, and express as limit on HH xs (divide by BR)
limit_df['-2']   = limit_df['-2'] * scales
limit_df['-1']   = limit_df['-1'] * scales
limit_df['0']    = limit_df['0'] * scales
limit_df['1']    = limit_df['1'] * scales
limit_df['2']    = limit_df['2'] * scales
limit_df['obs']  = limit_df['obs'] * scales

import matplotlib.pyplot as plt
fig, ax = plt.subplots()

ax.fill_between(limit_df[scanned_poi], limit_df['-2'], limit_df['2'], color='#00cc00')
ax.fill_between(limit_df[scanned_poi], limit_df['-1'], limit_df['1'], color='#ffcc00')
ax.plot(limit_df[scanned_poi], limit_df['0'], '-o', color='black', ms=2, lw=0.5)

xlim = ax.get_xlim()
if args.xmin:
    xlim = (args.xmin, xlim[1])
if args.xmax:
    xlim = (xlim[0], args.xmax)
ax.set_xlim(xlim)

ax.set_yscale('log')
# ax.set_ylim((10, 100000))

ax.set_xlabel(poi_names[scanned_poi], loc='right', size=15)
ax.set_ylabel(r'95% CL UL on $\sigma (pp \rightarrow HH)$ [fb]', loc='top', size=15)

fig.tight_layout()
# print(limit_df[limit_df[scanned_poi] == 1])
outname = args.output.format(poi=scanned_poi)
print(f'[INFO] : output saved as {outname}')
fig.savefig(outname)

if args.export_csv:
    print(f'[INFO] : exporting plotted data frame as {args.export_csv}')
    limit_df.to_csv(args.export_csv, index=False)