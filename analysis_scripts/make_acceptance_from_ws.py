# python make_acceptance_from_ws.py --i EFT_workspaces/workspace/WS-bbyy-non-resonant-non-param.root --poi chhh
# for p in chhh cggh cgghh ctthh ctth; do python  make_acceptance_from_ws.py --i EFT_workspaces/workspace/WS-bbyy-non-resonant-non-param.root --poi $p ; done

import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='input workspace root file')
parser.add_argument('--WS', default='combWS', help='input workspace name')
parser.add_argument('--poi', required=True, help="scanned poi (reported on x-axis of the plot)")
parser.add_argument('--x-min', default=None, help="scanned poi range - min value (defaults are chosen depending on POI for SM config)")
parser.add_argument('--x-max', default=None, help="scanned poi range - max value (defaults are chosen depending on POI for SM config)")
parser.add_argument('--x-step', default=100, help="scanned poi range - number of steps to perform in range (will do N+1 to include endpoint)")
parser.add_argument('--do-yield', dest='do_eff', default=True, help="plot the absolute yield instead of acceptance (default: plot acceptance)", action='store_false')
parser.add_argument('--export', dest="export", default=None, help='export file of plotted data')
parser.add_argument('--other-pois', default=None,
                        metavar="KEY=VALUE",
                        nargs='+',
                        help="Values of the other pois (not scanned), passed as poi=value. "
                             "Do not put spaces before or after the = sign. "
                             "Separate multiple entries just with a space. Example: "
                             "--other-pois ctth=1 cgghh=2. "
                             "All parameters not explicitely set are assumed to be at SM value"
                    )

args = parser.parse_args()

pois = ['chhh', 'ctth', 'cgghh', 'cggh', 'ctthh']
SM_vals = {
    'chhh'  : 1.0,
    'ctth'  : 1.0,
    'cgghh' : 0.0,
    'cggh'  : 0.0,
    'ctthh' : 0.0
}

# ranges for nice plots (tuned to SM other pois)
pois_ranges = {
    'chhh'  : (-10, 10),
    'ctth'  : (-2, 2),
    'cgghh' : (-5, 5),
    'cggh'  : (-10, 10),
    'ctthh' : (-3, 3),    
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
print(f'[INFO] : scanning POI {scanned_poi}')
print(f'       : the other POIs are set to the following values:')
for poi in pois:
    if poi != scanned_poi:
        print('       : {:<5} = {:.2f}'.format(poi, fixed_pois[poi]))


# fIn = ROOT.TFile.Open('EFT_workspaces/workspace/WS-bbyy-non-resonant-non-param.root')

print('[INFO] : opening file', args.input)
fIn = ROOT.TFile.Open(args.input)
print('[INFO] : retrieving workspace', args.WS)
ws = fIn.Get(args.WS)
# ws.Print()

# modelconfig = ws.obj("ModelConfig")

# retrieve POIs
chhh  = ws.var('chhh')
ctth  = ws.var('ctth')
ctthh = ws.var('ctthh')
cggh  = ws.var('cggh')
cgghh = ws.var('cgghh')

categs = ['SM_1', 'SM_2', 'SM_3', 'BSM_1', 'BSM_2', 'BSM_3', 'BSM_4']
print(f'[INFO] : the following categories are searched: {categs}')
mHH_bins = [
    250, 270,290,310,330,350,370,390,
    410,430,450,470,490,
    510,530,550,570,590,
    610,630,650,670,690,
    710,730,750,770,790,
    810,830,850,870,890,
    910,930,950,970,990,
    1010,1030
]
print(f'[INFO] : the are {len(mHH_bins)} considered, first edge = {mHH_bins[0]}, last edge = {mHH_bins[-1]}')

# yields are named like this
# yield__HH_ggF_250_SM_2

yield_name_proto = 'yield__HH_ggF_{bin}_{categ}'
print(f'[INFO] : yields expressions are searched for as {yield_name_proto}')

yields_funcs = {}
for c in categs:
    yields_funcs[c] = {}
    for m in mHH_bins:
        yields_funcs[c][m] = ws.function(yield_name_proto.format(bin=m, categ=c)) # get yield by doing getVal()

import numpy as np
xmin = pois_ranges[args.poi][0] if not args.x_min else args.x_min
xmax = pois_ranges[args.poi][1] if not args.x_max else args.x_max
print(f'[INFO] : scanning {args.x_step} points from {xmin} to {xmax}')
scan_points = np.linspace(xmin, xmax, args.x_step+1)

yields = {}

start_vals = {**fixed_pois, **{args.poi : SM_vals[args.poi]}}
# initialize POIs
chhh.setVal (start_vals['chhh'])
ctth.setVal (start_vals['ctth'])
ctthh.setVal(start_vals['ctthh'])
cggh.setVal (start_vals['cggh'])
cgghh.setVal(start_vals['cgghh'])

roofit_pois = {
    'chhh'  : chhh,
    'ctth'  : ctth,
    'ctthh' : ctthh,
    'cggh'  : cggh,
    'cgghh' : cgghh,
}

for sp in scan_points:
    ## set the only parameter to change here
    # chhh.setVal(sp)
    roofit_pois[args.poi].setVal(sp)
    yields[sp] = {}
    for c in categs:
        yields[sp][c] = {}
        for m in mHH_bins:
            yields[sp][c][m] = yields_funcs[c][m].getVal()

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


if args.do_eff:
    # fixme: check values
    lumi     = 138.
    sigma_SM = 31.05
    BR       = 0.26/100.
    print(f'[INFO] : plotting total acceptance. For the total xs calculation we will consider the following values:')
    print(f'       : lumi = {lumi} fb-1')
    print(f'       : SM gg->HH xs {sigma_SM} fb')
    print(f'       : BR (HH->bbgg) {BR}')
    # BSM_xs = np.asarray([poly(chhh=x, ctth=1, cgghh=0, ctthh=0, cggh=0, A=Ais) for x in scan_points])
    BSM_xs = []
    for poival in scan_points:
        poi_dict = {**fixed_pois, scanned_poi : poival}
        poi_dict['A'] = Ais
        s = poly(**poi_dict)
        BSM_xs.append(s)
    BSM_xs = np.asarray(BSM_xs)
    SM_NLO_xs = poly(**{**SM_vals, **{'A' : Ais}})
    denom_scale = (BSM_xs/SM_NLO_xs)*lumi*sigma_SM*BR
else:
    print(f'[INFO] : plotting total yield')
    denom_scale = np.ones(len(scan_points))


import matplotlib.pyplot as plt

fig, axs = plt.subplots(2) # this has a small conflict with ROOFIT and raises a warning about "the smallest subnormal for <class 'numpy.float64'> type is zero" that can be ignored
# axs = [axs,] # so easier to index more after

plt.ion()

tot_yield = np.zeros(len(scan_points))
curves = {}
curves['xdata'] = scan_points
for c in categs:
    data_points = [] # store yield for this category in steps of poi
    for x in scan_points:
        ytot = sum(yields[x][c].values())
        data_points.append(ytot)
        # print(data_points)
    data_points = np.asarray(data_points)
    tot_yield = tot_yield + data_points
    data_points = data_points / denom_scale # this makes yield / tot_yield = acceptance, or leaves yield in case denom_scale was just oness
    axs[0].plot(scan_points, data_points, '-o', label=f'{c}')
    curves[c] = data_points

axs[0].set_xlabel(args.poi)
axs[0].set_ylabel('Acceptance' if args.do_eff else 'Yield')
axs[0].legend(loc='upper left')

tot_yield = tot_yield / denom_scale
axs[1].plot(scan_points, tot_yield, '-o', label='Total')
curves['tot'] = tot_yield

axs[1].set_xlabel(args.poi)
axs[1].set_ylabel('Acceptance' if args.do_eff else 'Yield')

fig.tight_layout()
typename = 'eff' if args.do_eff else 'yield'
fig.savefig(f'{typename}_{args.poi}.pdf')

if args.export:
    import pickle
    fout = open(args.export, 'wb')
    odata = {'curves' : curves}
    pickle.dump(odata, fout)