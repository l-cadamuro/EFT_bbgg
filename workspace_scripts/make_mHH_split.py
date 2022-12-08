import ROOT
import pickle

categs = [
    'SM_1',
    'SM_2',
    'SM_3',
    'BSM_1',
    'BSM_2',
    'BSM_3',
    'BSM_4',
]

# files = {
#     'SM_1' : 'inputNtuples/HH_SM_1.root',
#     'SM_2' : 'inputNtuples/HH_SM_2.root',
#     'SM_3' : 'inputNtuples/HH_SM_3.root',
#     'BSM_1' : 'inputNtuples/HH_BSM_1.root',
#     'BSM_2' : 'inputNtuples/HH_BSM_2.root',
#     'BSM_3' : 'inputNtuples/HH_BSM_3.root',
#     'BSM_4' : 'inputNtuples/HH_BSM_4.root',
# }

files = {
    'SM_1' : '../../inputNtuples/HHbbyy_cHHH01d0_SM_1.root',
    'SM_2' : '../../inputNtuples/HHbbyy_cHHH01d0_SM_2.root',
    'SM_3' : '../../inputNtuples/HHbbyy_cHHH01d0_SM_3.root',
    'BSM_1' : '../../inputNtuples/HHbbyy_cHHH01d0_BSM_1.root',
    'BSM_2' : '../../inputNtuples/HHbbyy_cHHH01d0_BSM_2.root',
    'BSM_3' : '../../inputNtuples/HHbbyy_cHHH01d0_BSM_3.root',
    'BSM_4' : '../../inputNtuples/HHbbyy_cHHH01d0_BSM_4.root',
}

treename = 'output'
mhh_branch_name = 'truth_m_hh'
weight_branch_name = 'total_weight'

##################################################

# # old binning (PUB note HEFT, SMEFT results)
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
# mHH_bins = [x - 10. for x in mHH_bins] # because the values from the coeffs are expressed as center, so shfit it by 1/2 bin width
# foutname = 'fractions_SM_for_EFT.txt'
# dboutname = 'fractions_SM_for_EFT.pkl'

##################################################

# new binning (from Tom)
mHH_bins = [
    250.,   270.,   290.,   310.,   330.,   350.,   370.,   390.,
    410.,   430.,   450.,   470.,   490.,   510.,   530.,   550.,
    570.,   590.,   610.,   630.,   650.,   670.,   690.,   710.,
    730.,   750.,   770.,   790.,   810.,   830.,   850.,   870.,
    890.,   910.,   930.,   950.,   970.,   990.,  1010.,  1030.,
    1050.,  1200.,  1400.]
mHH_bins = mHH_bins[:-1] # remove last edge, because for mHH > 1400 we use the values in bin [1200, 1400], so effectively we habe a single bin mHH > 1200
foutname = 'fractions_SM_for_EFT_newBinning.txt'
dboutname = 'fractions_SM_for_EFT_newBinning.pkl'

##################################################

output_data = {}
evt_counts = {}

print('[INFO] : considering a binning of', len(mHH_bins), 'bins :')
print('       : ', mHH_bins)

for c in categs:
    print ('... reading categ', c, 'from file', files[c])
    counts = {}
    slices = {}
    # fIn = ROOT.TFile.Open(files[c])
    # tIn = fIn.Get(treename)
    df = ROOT.RDataFrame (treename, files[c], [mhh_branch_name, weight_branch_name])
    for ib, b in enumerate(mHH_bins): # intermediate bin: b < mHH < b+1
        if b != mHH_bins[-1]:
            low_bound = 1000.*mHH_bins[ib]
            high_bound = 1000.*mHH_bins[ib+1] # since values in the ntuples are in MeV
            cond = f'{mhh_branch_name} >= {low_bound} && {mhh_branch_name} < {high_bound}'
        else: # last bin
            low_bound = 1000.*mHH_bins[ib]
            cond = f'{mhh_branch_name} >= {low_bound}'
        # print(cond)
        counts[b] = df.Filter(cond).Count() # booked op
        slices[b] = df.Filter(cond).Sum(weight_branch_name) # booked op
        # output_data[c][b] = y
    counts['total'] = df.Count()
    slices['total'] = df.Sum(weight_branch_name) 

    output_data[c] = {}
    evt_counts[c] = {}
    for b in mHH_bins:
        output_data[c][b] = slices[b].GetValue()
        evt_counts[c][b] = counts[b].GetValue()
    output_data[c]['total'] = slices['total'].GetValue()
    evt_counts[c]['total'] = counts['total'].GetValue()

# print values
print('... txt file with yields created as', foutname)
fout = open(foutname, 'w')
for c in categs:
    tot = 0
    tot_count = 0

    print('... CATEGORY : ', c)
    fout.write('... CATEGORY : ' + c + '\n')
    for b in mHH_bins:
        print ('{} : {} (nEv = {})'.format(b, output_data[c][b], evt_counts[c][b]))
        tot += output_data[c][b]
        tot_count += evt_counts[c][b]
        fout.write('{} : {} (nEv = {})'.format(b, output_data[c][b], evt_counts[c][b]) + '\n')
    print('---> TOTAL  : ', tot)
    # print('---> TOT xc : ', output_data[c]['total'])
    fout.write('---> TOTAL  : ' + str(tot) + '(nEv = {})'.format(tot_count) + '\n')
    fout.write('---> TOT xc : ' + str(output_data[c]['total']) + '(nEv = {})'.format(evt_counts[c]['total']) + '\n')

print('... dumping data to', dboutname)
saved_data = {'yields' : output_data, 'mHH_bins' : mHH_bins, 'counts' : evt_counts}
pickle.dump( saved_data, open( dboutname, "wb" ) )


