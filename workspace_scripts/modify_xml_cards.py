import pickle
import os
import shutil 
## load fractions
read_data = pickle.load( open( 'fractions_SM_for_EFT.pkl', "rb" ) )
mHH_bins = read_data['mHH_bins']
yields   = read_data['yields']

# mHH_bins = [
#     250., 270.,290.,310.,330.,350.,370.,390.,
#     410.,430.,450.,470.,490.,
#     510.,530.,550.,570.,590.,
#     610.,630.,650.,670.,690.,
#     710.,730.,750.,770.,790.,
#     810.,830.,850.,870.,890.,
#     910.,930.,950.,970.,990.,
#     1010.,1030.
# ]

categs = [
    'SM_1',
    'SM_2',
    'SM_3',
    'BSM_1',
    'BSM_2',
    'BSM_3',
    'BSM_4',
]

# path to the folder just above "config"
path_to = '/homeijclab/cadamuro/HH/gitCode/database/workspaces/NonResonant_Wisconsin/legacy_h027_stat_only'

cards = {
    'SM_1' : f'{path_to}/config/categories/category_non_param_SM_1.xml',
    'SM_2' : f'{path_to}/config/categories/category_non_param_SM_2.xml',
    'SM_3' : f'{path_to}/config/categories/category_non_param_SM_3.xml',
    'BSM_1' : f'{path_to}/config/categories/category_non_param_BSM_1.xml',
    'BSM_2' : f'{path_to}/config/categories/category_non_param_BSM_2.xml',
    'BSM_3' : f'{path_to}/config/categories/category_non_param_BSM_3.xml',
    'BSM_4' : f'{path_to}/config/categories/category_non_param_BSM_4.xml',
}

master_card = f'{path_to}/config/input_non_param.xml'

# as input workspaces are indexed from 'config', keep in the destination structure, and run ws creation from above
out_dir = "../EFT_workspaces"
config_subdir = 'config'
categs_subdir = "categories"

# copy these folders to destination [0], copy location within out_dir [1]
folder_forward = [
    (f'{path_to}/config/models', f'{config_subdir}/models'),
    (f'{path_to}/config/data', f'{config_subdir}/data'),
]


print('[INFO] will save output into', out_dir)

if not os.path.isdir(out_dir+'/'+config_subdir+'/'+categs_subdir):
    print('[INFO] creating folders', out_dir+'/'+config_subdir+'/'+categs_subdir)
    os.makedirs(out_dir+'/'+config_subdir+'/'+categs_subdir)

# if not os.path.isdir(out_dir):
#     print('[INFO] creating folder', out_dir)
#     os.makedirs(out_dir)
# if not os.path.isdir(out_dir+'/'+config_subdircards_subdir):
#     print('[INFO] creating folder', out_dir+'/'+cards_subdir)
#     os.makedirs(out_dir+'/'+cards_subdir)
# for dstart, ddest in folder_forward:
#     if not os.path.isdir(out_dir+'/'+ddest):
#         print('[INFO] creating folder', out_dir+'/'+ddest)
#         os.makedirs(out_dir+'/'+ddest)

# <Sample Name="ggHH_250" InputFile="config/HH_bbgg_HEFT_workspace/model/signal_pdf_ggHH_HHyybb_mu_looseScore_HMass_1.xml" ImportSyst=":common:,ggHH" SharePdf="Sig_ggHH" MultiplyLumi="true">
#   <NormFactor Name="mu[1,-10,200]"/>
#   <NormFactor Name="mu_ggHH[1,-10,200]"/>
#   <NormFactor Name="yield_ggHH_250[0]"/>
#   <NormFactor Name="expr::poly250('(0.0343628*@1*@1*@1*@1 + 0.12094*@2*@2 + (0.0276386*@1*@1 + 0.0388548*@3*@3)*@0*@0 + 0.171954*@4*@4 + (-0.128178*@2 + -0.0612458*@1*@0)*@1*@1 + (0.115241*@1*@0 + 0.137035*@3*@0)*@2 + 0.288257*@2*@4 + (-0.0720075*@3*@0 + -0.151618*@4)*@1*@1 + (0.0655087*@0*@3 + 0.137107*@4)*@1*@0 + 0.163392*@3*@4*@0 + -0.000363312*@3*@1*@1*@1 + 0.00066654*@2*@1*@3 + 0.00142309*@1*@0*@3*@3 + 0.000861283*@1*@3*@4 + -0.00110765*@1*@1*@3*@3 + 0.00203213*@2*@3*@3 + 0.00129149*@0*@3*@3*@3 + 0.00262585*@4*@3*@3)/0.000755673',chhh,ctth,ctthh,cggh,cgghh)"/>
 
# expr::poly250('(0.0343628*@1*@1*@1*@1 + 0.12094*@2*@2 + (0.0276386*@1*@1 + 0.0388548*@3*@3)*@0*@0 + 0.171954*@4*@4 + (-0.128178*@2 + -0.0612458*@1*@0)*@1*@1 + (0.115241*@1*@0 + 0.137035*@3*@0)*@2 + 0.288257*@2*@4 + (-0.0720075*@3*@0 + -0.151618*@4)*@1*@1 + (0.0655087*@0*@3 + 0.137107*@4)*@1*@0 + 0.163392*@3*@4*@0 + -0.000363312*@3*@1*@1*@1 + 0.00066654*@2*@1*@3 + 0.00142309*@1*@0*@3*@3 + 0.000861283*@1*@3*@4 + -0.00110765*@1*@1*@3*@3 + 0.00203213*@2*@3*@3 + 0.00129149*@0*@3*@3*@3 + 0.00262585*@4*@3*@3)/0.000755673',chhh,ctth,ctthh,cggh,cgghh)
# 0,1,2,3,4 : chhh,ctth,ctthh,cggh,cgghh
# from 
poly_form = (
"{A1}*{ctth}*{ctth}*{ctth}*{ctth} +"
"{A2}*{ctthh}*{ctthh} +"
"({A3}*{ctth}*{ctth} + {A4}*{cggh}*{cggh})*{chhh}*{chhh} +"
"{A5}*{cgghh}*{cgghh} +"
"({A6}*{ctthh} + {A7}*{ctth}*{chhh})*{ctth}*{ctth} +"
"({A8}*{ctth}*{chhh} + {A9}*{cggh}*{chhh})*{ctthh} +"
"{A10}*{ctthh}*{cgghh} +"
"({A11}*{cggh}*{chhh} + {A12}*{cgghh})*{ctth}*{ctth} +"
"({A13}*{chhh}*{cggh} + {A14}*{cgghh})*{ctth}*{chhh} +"
"{A15}*{cggh}*{cgghh}*{chhh} +"
"{A16}*{cggh}*{ctth}*{ctth}*{ctth} +"
"{A17}*{ctthh}*{ctth}*{cggh} +"
"{A18}*{ctth}*{chhh}*{cggh}*{cggh} +"
"{A19}*{ctth}*{cggh}*{cgghh} +"
"{A20}*{ctth}*{ctth}*{cggh}*{cggh} +"
"{A21}*{ctthh}*{cggh}*{cggh} +"
"{A22}*{chhh}*{cggh}*{cggh}*{cggh} +"
"{A23}*{cgghh}*{cggh}*{cggh}"
)

####################################################
def read_coeffs_ATLAS(fname, nAi):
    """ read the coefficients in the ATLAS format """
    fIn = open(fname, 'r')
    bins = []
    data = []
    for l in fIn:
        l = l.strip()
        if not l:
            continue
        tokens = l.split()
        tokens = [float(i) for i in tokens]
        if len(tokens) == nAi + 1: ## coeffs + mHH bin center
            # data.append(tokens)
            bins.append(tokens[0])
            data.append(tokens[1:])
        elif len(tokens) == nAi: ## the last line seems to be an overflow bin
            # data.append([999999,] + tokens)
            bins.append(999999,)
            data.append(tokens)

        else:
            raise RuntimeError("Cannot parse coefficients")
    return bins, data

mhh_bins_files, coeffs = read_coeffs_ATLAS('coeff_files/NLO-Ais-13TeV.txt', 23)

if mhh_bins_files[:-1] != mHH_bins: # mhh_bins_files also contains an overflow entry at 999999
    print('WARNING!!! coeffs read out and mHH_bins do not match! ', len(mHH_bins), len(mhh_bins_files))
    for i in range(len(mhh_bins_files)):
        print(mHH_bins[i], mhh_bins_files[i])
    raise RuntimeError('CHECK BINNING')

####################################################
## keys: strings in poly_form 'ctth','ctthh','cgghh','cggh','chhh',
## values : name of the POIs to be created for the workspace
poi_names = {
    'ctth'  : 'ctth',
    'ctthh' : 'ctthh',
    'cgghh' : 'cgghh',
    'cggh'  : 'cggh',
    'chhh'  : 'chhh'
}

# defined as in ROOFIT: start, min, max
poi_ranges = {
    'ctth'  : '1, -20, 20',
    'ctthh' : '1, -20, 20',
    'cgghh' : '0, -20, 20',
    'cggh'  : '0, -20, 20',
    'chhh'  : '0, -20, 20'
}

def format_poly(poly_form, Ai, poi_names):
    Ai_dict = {"A"+str(i+1) : Ai[i] for i in range(len(Ai))}
    full_dict = {**Ai_dict, **poi_names}
    s = poly_form.format(**full_dict)
    return s

####################################################
# compute SM values for normalization
print('... computing SM normalizations per bin')
SM_vals = {
    'ctth'  : 1,
    'ctthh' : 0,
    'cgghh' : 0,
    'cggh'  : 0,
    'chhh'  : 1, 
}
SM_yields = {}
for ibin, mHH in enumerate(mHH_bins):
    s = format_poly(poly_form, coeffs[ibin], poi_names)
    p_string = eval(s, SM_vals)
    SM_yields[mHH] = p_string



newcards = {}
####################################################
#### run on input cards
for categ in categs:
    print('[INFO] doing categ', categ)
    print('       - original card', cards[categ])
    new_card = [] # list of txt lines
    all_lines = open(cards[categ]).readlines()
    
    # find gg HH lines
    istart = -1
    istop = -1
    i_firstSample = -1
    for i, l in enumerate(all_lines):
        if '<Sample' in l and i_firstSample == -1:
            i_firstSample = i
        if '<Sample' in l and 'Name="HH_ggF"' in l:
            istart = i
        if istart >= 0 and '</Sample>' in l: # first occurrence of a new sample after istart
            istop = i
            break
    POIs_lines = [
        '  <Item Name="{}[{}]"/>\n'.format(poi_names['chhh'] , poi_ranges['chhh']),
        '  <Item Name="{}[{}]"/>\n'.format(poi_names['ctth'] , poi_ranges['ctth']),
        '  <Item Name="{}[{}]"/>\n'.format(poi_names['ctthh'], poi_ranges['ctthh']),
        '  <Item Name="{}[{}]"/>\n'.format(poi_names['cggh'] , poi_ranges['cggh']),
        '  <Item Name="{}[{}]"/>\n'.format(poi_names['cgghh'], poi_ranges['cgghh']),
    ]

    if i_firstSample < istart:
        new_card = all_lines[0:i_firstSample] + POIs_lines + all_lines[i_firstSample:istart] # insert POIs here
    elif i_firstSample == istart:
        new_card = all_lines[0:istart] + POIs_lines  # forward everything until new block
    else:
        raise RuntimeError(f'first same location inconsistent : {i_firstSample} {istart}')

    for ibin, mHH in enumerate(mHH_bins):
        mHH_int = int(mHH)
        protos =   [
            '  <Sample Name="{signame}" XSection="1" SelectionEff="1" InputFile="config/models/HH_ggF_BSM_4.xml" ImportSyst=":common:,{signame}" MultiplyLumi="1">\n',
            '    <NormFactor Name="yield_{signame}[{evtyield}]" />\n',
            '    <NormFactor Name="mu_XS_HH_ggF[1]" />\n',
            '    <NormFactor Name="mu_XS_HH[1]" />\n',
            '    <NormFactor Name="mu_XS_HH_BSM_4[1]" />\n',
            '    <NormFactor Name="mu_XS_BSM_4[1]" />\n',
            '    <NormFactor Name="mu[1]" />\n',
            '    <NormFactor Name="expr::{polyname}(\'({polyfunc})/{SMnorm}\',{chhh},{ctth},{ctthh},{cggh},{cgghh})"/>\n'
            '  </Sample>\n',
        ]
        formatdata = {
            'signame'  : f'HH_ggF_{mHH_int}',
            'evtyield' : yields[categ][mHH],
            'polyname' : f'poly{mHH_int}',
            'SMnorm'   : SM_yields[mHH],
            'polyfunc' : format_poly(poly_form, coeffs[ibin], {'chhh':'@0', 'ctth':'@1', 'ctthh':'@2', 'cggh':'@3', 'cgghh':'@4'})
        }
        formatdata = {**formatdata, **poi_names}
        newstrs = [x.format(**formatdata) for x in protos]
        new_card += newstrs

    ## finally forward everything else in the card
    new_card += all_lines[istop+1:]
    output_card_name = '{}/{}/EFT_{}.xml'.format(config_subdir, categs_subdir, categ)
    newcards[categ] = output_card_name
    cardLFN = out_dir + '/' + output_card_name
    print('       - saving xml as', cardLFN)
    fout = open(cardLFN, 'w')
    for l in new_card:
        fout.write(l)


## now edit the master card to add new POIs
print('[INFO] editing master card from', master_card)
new_card = [] # list of txt lines
all_lines = open(master_card).readlines()
inputs_replaced = False
for l in all_lines:
    if '<Input>' in l:
        if not inputs_replaced:
            for categ in categs:
                newl = '<Input>{}</Input>\n'.format(newcards[categ])
                new_card.append(newl)
                inputs_replaced = True
        else:
            pass # skip this line
    # prepend pois
    # elif '<POI>' in l:
    #     newl = l.replace('<POI>', '<POI>{},{},{},{},{},'.format(*poi_names.values()))
    #     new_card.append(newl)
    # append pois
    elif '</POI>' in l:
        newl = l.replace('</POI>', ',{},{},{},{},{}</POI>'.format(*poi_names.values()))
        new_card.append(newl)
    # update the default setup of the model
    elif '<Asimov' in l and 'Name="setup"' in l and 'Setup="' in l:
        newl = l.replace('Setup="', 'Setup="{n_chhh}=1,{n_ctth}=1,{n_cgghh}=0,{n_cggh}=0,{n_ctthh}=0,'.format(n_chhh=poi_names['chhh'], n_ctth=poi_names['ctth'], n_cgghh=poi_names['cgghh'], n_cggh=poi_names['cggh'], n_ctthh=poi_names['ctthh']))
        new_card.append(newl)
    else:
        new_card.append(l)
output_card_name = '{}/{}/master_EFT.xml'.format(out_dir, config_subdir)
print('       - saving xml as', output_card_name)
fout = open(output_card_name, 'w')
for l in new_card:
    fout.write(l)


print('[INFO] forwarding other content')
for dstart, ddest in folder_forward:
    print('[INFO] copying', dstart)
    print('       ->', out_dir+'/'+ddest)
    shutil.copytree(dstart, out_dir+'/'+ddest)