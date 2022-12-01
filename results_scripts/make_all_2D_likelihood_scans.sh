## input
WSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"
AsimovWSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param_Asimov.root"


# generate the Asimov dataset for nominal NP and klambda set to 1 (SM signal)
# recall the meaning of the Asimov type:
# -t, --asimov_types TEXT         Types of asimov dataset to generate separated by commas.
#                                  0: fit with POI fixed to 0
#                                  1: fit with POI fixed to 1
#                                  2: fit with POI free and set POI to 1 after fit
#                                  3: fit with POI and constrained NP fixed to 0
#                                  4: fit with POI fixed to 1 and constrained NP fixed to 0
#                                  5: fit with POI free and constrained NP fixed to 0 and set POI to 1 after fit
#                                  -1: nominal NP with POI set to 0
#                                  -2: nominal NP with POI set to 1  [default: 0,1,2]
quickstats generate_standard_asimov -i ${WSpath} -o ${AsimovWSpath} -d combData -p chhh --asimov_types "-2"

# make likelihood scans for each POI
dataset="asimovData_1_NP_Nominal"
snapshot="asimovData_1_NP_Nominal"

# note: a scan of 12000 points takes about 3 minutes, and results in about 110 MB of output data

quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "chhh=-10_10_0.1,ctth=-3_3_0.1" --outdir chhh_ctth_2D_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "chhh=-10_10_0.1,cgghh=-5_5_0.1" --outdir chhh_cgghh_2D_likelihood_scan   --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "chhh=-10_10_0.1,ctthh=-3_3_0.1" --outdir chhh_ctthh_2D_likelihood_scan   --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cgghh=-5_5_0.1,ctthh=-3_3_0.1"  --outdir cgghh_ctthh_2D_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache

python make_2D_likelihood_scan.py --input chhh_ctth_2D_likelihood_scan/likelihood_scan.json   --xpoi chhh --ypoi ctth
python make_2D_likelihood_scan.py --input chhh_cgghh_2D_likelihood_scan/likelihood_scan.json  --xpoi chhh --ypoi cgghh
python make_2D_likelihood_scan.py --input chhh_ctthh_2D_likelihood_scan/likelihood_scan.json  --xpoi chhh --ypoi ctthh
python make_2D_likelihood_scan.py --input cgghh_ctthh_2D_likelihood_scan/likelihood_scan.json --xpoi cgghh --ypoi ctthh
