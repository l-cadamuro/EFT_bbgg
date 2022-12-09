import pickle
import os
import shutil 

### same binning and coefficients as previous PUB note
# yieldfile = 'fractions_SM_for_EFT.pkl'
# coeff_file_name = 'coeff_files/NLO-Ais-13TeV.txt'
# out_dir = "../EFT_workspaces"
# EFT_type = 'HEFT'

### new binning and new coefficients from Tom
# yieldfile = 'fractions_SM_for_EFT_newBinning.pkl'
# coeff_file_name = 'coeff_files/HEFT_coeffs_updated/muR_muF_1/HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_1.txt'
# out_dir = "../EFT_workspaces_newCoeffs"
# EFT_type = 'HEFT'

### for SMEFT
yieldfile = 'fractions_SM_for_EFT.pkl'
coeff_file_name = 'coeff_files/Weights_20_GeV_Bins.txt'
out_dir = "../SMEFT_workspaces"
EFT_type = 'SMEFT' # HEFT, SMEFT

# read_data = pickle.load( open( 'fractions_SM_for_EFT.pkl', "rb" ) )
# read_data = pickle.load( open( 'fractions_SM_for_EFT_newBinning.pkl', "rb" ) )
read_data = pickle.load( open( yieldfile, "rb" ) )
mHH_bins = read_data['mHH_bins']
yields   = read_data['yields']

print('[INFO] : doing EFT:', EFT_type)

print('[INFO] : input yield file', yieldfile)
print('       : read ', len(mHH_bins), 'input mHH bins')
print('       : read ', len(yields), 'yield entries')

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

# path to the input folder just above "config" : original cards to modify
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
# out_dir = "../EFT_workspaces"
# out_dir = "../EFT_workspaces_newCoeffs"
config_subdir = 'config'
categs_subdir = "categories"

# copy these folders to destination [0], copy location within out_dir [1]
folder_forward = [
    (f'{path_to}/config/models', f'{config_subdir}/models'),
    (f'{path_to}/config/data', f'{config_subdir}/data'),
]

print('[INFO] will save output into', out_dir)

if os.path.isdir(out_dir):
    print('[INFO] : directory', out_dir, 'exists. Do you want to delete it to continue? [Y/n]')
    rv = input()
    if rv == 'Y':
        print('[INFO] : will delete existing directory', out_dir)
        import shutil
        shutil.rmtree(out_dir, ignore_errors=True)
    else:
        print('[ERROR] : folder', out_dir, 'already exists, and will not be deleted')
        raise RuntimeError ('Folder exists')

if not os.path.isdir(out_dir+'/'+config_subdir+'/'+categs_subdir):
    print('[INFO] creating folders', out_dir+'/'+config_subdir+'/'+categs_subdir)
    os.makedirs(out_dir+'/'+config_subdir+'/'+categs_subdir)

if EFT_type == "HEFT":
    # the descritpion of the polynomial (prototype string)
    from HEFT_poly import poly_form, read_coeffs_ATLAS
    # mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS('coeff_files/NLO-Ais-13TeV.txt', 23)
    # mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS('coeff_files/HEFT_coeffs_updated/muR_muF_1/HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_1.txt', 23)
    mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS(coeff_file_name, 23)

    ####################################################
    poi_list = ['chhh', 'ctth', 'ctthh', 'cggh', 'cgghh']

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

    SM_vals = {
        'ctth'  : 1,
        'ctthh' : 0,
        'cgghh' : 0,
        'cggh'  : 0,
        'chhh'  : 1, 
    }


elif EFT_type == "SMEFT":
    from SMEFT_poly import poly_form, read_coeffs_ATLAS
    # mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS('coeff_files/NLO-Ais-13TeV.txt', 23)
    # mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS('coeff_files/HEFT_coeffs_updated/muR_muF_1/HEFT_dA_and_A_with_Binning_250_1050_41_Variable_Bins_1200_1400_muR_muF_1.txt', 23)
    mhh_bins_files, coeffs, inclusive_Ais = read_coeffs_ATLAS(coeff_file_name, 21)

    ####################################################
    ## keys: strings in poly_form
    ## values : name of the POIs to be created for the workspace

    poi_list = ['cdp', 'cp', 'ctp', 'ctG', 'cpg']

    poi_names = {
        'cdp'  : 'cdp',
        'cp'   : 'cp',
        'ctp'  : 'ctp',
        'ctG'  : 'ctG',
        'cpg'  : 'cpg'
    }

    # defined as in ROOFIT: start, min, max
    poi_ranges = {
        'cdp'  : '0, -10, 10',
        'cp'   : '0, -10, 10',
        'ctp'  : '0, -10, 10',
        'ctG'  : '0, -10, 10',
        'cpg'  : '0, -10, 10'
    }

    SM_vals = {
        'cdp'  : 0,
        'cp'   : 0,
        'ctp'  : 0,
        'ctG'  : 0,
        'cpg'  : 0, 
    }

else:
    raise RuntimeError("EFT type not valid")


print('... Read coeffs files : ', len(coeffs), 'coeffs')

## The binning read from the Ai files cannot be directly compared here since the file reports the bin center and not the bin edges ...
# if mhh_bins_files != mHH_bins:
#     print('WARNING!!! coeffs read out and mHH_bins do not match! ', len(mHH_bins), len(mhh_bins_files))
#     print(" from Ai file : ", mhh_bins_files)
#     print(" from input yields : ", mHH_bins)
#     for i in range(len(mhh_bins_files)):
#         print(mHH_bins[i], mhh_bins_files[i])
#     raise RuntimeError('CHECK BINNING')

## ... so just check that the number of bins matches
if len(mHH_bins) != len(coeffs):
    print('ERROR! There is a mismatch between the number of mHH bins (used for yields) and the number of coefficients')
    print('num. of mHH bins:', len(mHH_bins), ' != num of coefficients', len(coeffs))


def format_poly(poly_form, Ai, poi_names):
    Ai_dict = {"A"+str(i+1) : Ai[i] for i in range(len(Ai))}
    full_dict = {**Ai_dict, **poi_names}
    s = poly_form.format(**full_dict)
    return s

####################################################
# compute SM values for normalization
print('... computing SM normalizations per bin')

SM_yields = {}
for ibin, mHH in enumerate(mHH_bins):
    s = format_poly(poly_form, coeffs[ibin], poi_names)
    p_string = eval(s, SM_vals)
    SM_yields[mHH] = p_string

# split_signals : one signal (yield x pdf) is created for each mHH bin, the pdf is common
#               : S = poly(A_0, c_i) x yield_0 x pdf + poly(A_1, c_i) x yield_1 x pdf + ...
# merged_yields : a single signal (sum(yields) x pdf) is created. Partial contributions are aggregated
#               : S = sum_Ncoeffs [sum_bins(Ai x yield_i)] poly_term_j ]
implementation_type = 'merged_yields'

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
    # POIs_lines = [
    #     '  <Item Name="{}[{}]"/>\n'.format(poi_names['chhh'] , poi_ranges['chhh']),
    #     '  <Item Name="{}[{}]"/>\n'.format(poi_names['ctth'] , poi_ranges['ctth']),
    #     '  <Item Name="{}[{}]"/>\n'.format(poi_names['ctthh'], poi_ranges['ctthh']),
    #     '  <Item Name="{}[{}]"/>\n'.format(poi_names['cggh'] , poi_ranges['cggh']),
    #     '  <Item Name="{}[{}]"/>\n'.format(poi_names['cgghh'], poi_ranges['cgghh']),
    # ]
    # generates the list of POIs to be inserted in the workspace
    POIs_lines = ['  <Item Name="{}[{}]"/>\n'.format(poi_names[pname] , poi_ranges[pname]) for pname in poi_list]
    POIs_string = ','.join(['{%s}'%pname for pname in poi_list]) # {chhh},{ctth},{ctthh},{cggh},{cgghh}
    POI_dict = {poi_list[ipoi] : '@%i' % ipoi for ipoi in range(len(poi_list))} # {'chhh':'@0', 'ctth':'@1', 'ctthh':'@2', 'cggh':'@3', 'cgghh':'@4'}

    if i_firstSample < istart:
        new_card = all_lines[0:i_firstSample] + POIs_lines + all_lines[i_firstSample:istart] # insert POIs here
    elif i_firstSample == istart:
        new_card = all_lines[0:istart] + POIs_lines  # forward everything until new block
    else:
        raise RuntimeError(f'first same location inconsistent : {i_firstSample} {istart}')

    ##########################################################################

    if implementation_type == 'split_signals':
        for ibin, mHH in enumerate(mHH_bins):
            mHH_int = int(mHH)
            protos =   [
                '  <Sample Name="{signame}" XSection="1" SelectionEff="1" InputFile="config/models/HH_ggF_{categ}.xml" ImportSyst=":common:,{signame}" MultiplyLumi="1">\n',
                '    <NormFactor Name="yield_{signame}[{evtyield}]" />\n',
                '    <NormFactor Name="mu_XS_HH_ggF[1]" />\n',
                '    <NormFactor Name="mu_XS_HH[1]" />\n',
                '    <NormFactor Name="mu_XS_HH_{categ}[1]" />\n',
                '    <NormFactor Name="mu_XS_{categ}[1]" />\n',
                '    <NormFactor Name="mu[1]" />\n',
                # '    <NormFactor Name="expr::{polyname}(\'({polyfunc})/{SMnorm}\',{chhh},{ctth},{ctthh},{cggh},{cgghh})"/>\n'
                '    <NormFactor Name="expr::{polyname}(\'({polyfunc})/{SMnorm}\',%s)"/>\n' % POIs_string,
                '  </Sample>\n',
            ]
            formatdata = {
                'categ'    : categ,
                'signame'  : f'HH_ggF_{mHH_int}',
                'evtyield' : yields[categ][mHH],
                'polyname' : f'poly{mHH_int}',
                'SMnorm'   : SM_yields[mHH],
                # 'polyfunc' : format_poly(poly_form, coeffs[ibin], {'chhh':'@0', 'ctth':'@1', 'ctthh':'@2', 'cggh':'@3', 'cgghh':'@4'})
                'polyfunc' : format_poly(poly_form, coeffs[ibin], POI_dict)
            }
            formatdata = {**formatdata, **poi_names}
            newstrs = [x.format(**formatdata) for x in protos]
            new_card += newstrs

    elif implementation_type == 'merged_yields':
        protos =   [
            '  <Sample Name="HH_ggF" XSection="1" SelectionEff="1" InputFile="config/models/HH_ggF_{categ}.xml" ImportSyst=":common:,HH_ggF" MultiplyLumi="1">\n',
            # '    <NormFactor Name="yield_HH_ggF[{evtyield}]" />\n',
            '    <NormFactor Name="mu_XS_HH_ggF[1]" />\n',
            '    <NormFactor Name="mu_XS_HH[1]" />\n',
            '    <NormFactor Name="mu_XS_HH_{categ}[1]" />\n',
            '    <NormFactor Name="mu_XS_{categ}[1]" />\n',
            '    <NormFactor Name="mu[1]" />\n',
            # '    <NormFactor Name="expr::yield_EFT(\'({polyfunc})/{SMnorm}\',{chhh},{ctth},{ctthh},{cggh},{cgghh})"/>\n'
            # '    <NormFactor Name="expr::yield_HH_ggF_EFT(\'{polyfunc}\',{chhh},{ctth},{ctthh},{cggh},{cgghh})"/>\n'
            '    <NormFactor Name="expr::yield_HH_ggF_EFT(\'{polyfunc}\',%s)"/>\n' % POIs_string,
            '  </Sample>\n',
        ]
        if EFT_type == 'HEFT':
            from HEFT_poly import ci_func_vector, coeffs_vector
        elif EFT_type == 'SMEFT':
            from SMEFT_poly import ci_func_vector, coeffs_vector
        else:
            raise RuntimeError("EFT type not valid")

        poly_parts = []
        for ifunc, func in enumerate(ci_func_vector): # looping on each "piece" of the polynomial
            tot = 0
            # building A0_bin0 x yield_bin0 / SMyield_bin0 + ... + A0_binM x yield_binM / SMyield_binM +
            for ibin, mHH in enumerate(mHH_bins):
                tot += coeffs[ibin][ifunc] * yields[categ][mHH] / SM_yields[mHH]
            poly_parts.append(tot)
        formatdata = {
            'categ'    : categ,
            # 'polyfunc' : format_poly(poly_form, poly_parts, {'chhh':'@0', 'ctth':'@1', 'ctthh':'@2', 'cggh':'@3', 'cgghh':'@4'})
            'polyfunc' : format_poly(poly_form, poly_parts, POI_dict)
        }
        formatdata = {**formatdata, **poi_names}
        newstrs = [x.format(**formatdata) for x in protos]
        new_card += newstrs


    ##########################################################################

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
        setup_cmd = ','.join(['%s=%.0f' % (poiname, SM_vals[poiname]) for poiname in poi_list])
        setup_str = 'Setup="{},'.format(setup_cmd)
        # newl = l.replace('Setup="', 'Setup="{n_chhh}=1,{n_ctth}=1,{n_cgghh}=0,{n_cggh}=0,{n_ctthh}=0,'.format(n_chhh=poi_names['chhh'], n_ctth=poi_names['ctth'], n_cgghh=poi_names['cgghh'], n_cggh=poi_names['cggh'], n_ctthh=poi_names['ctthh']))
        newl = l.replace('Setup="', setup_str)
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