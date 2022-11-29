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
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "chhh=-10_10_0.1" --outdir chhh_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "ctth=-3_3_0.1"   --outdir ctth_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cggh=-5_5_0.1"   --outdir cggh_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "ctthh=-3_3_0.1"  --outdir ctthh_likelihood_scan --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cgghh=-5_5_0.1"  --outdir cgghh_likelihood_scan --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache

python make_likelihood_scan.py --input chhh_likelihood_scan/likelihood_scan.json   --poi chhh  --xmin -5 --xmax 10
python make_likelihood_scan.py --input ctth_likelihood_scan/likelihood_scan.json   --poi ctth  --xmin -2 --xmax 2
python make_likelihood_scan.py --input cgghh_likelihood_scan/likelihood_scan.json  --poi cgghh --xmin -1 --xmax 1
python make_likelihood_scan.py --input cggh_likelihood_scan/likelihood_scan.json   --poi cggh
python make_likelihood_scan.py --input ctthh_likelihood_scan/likelihood_scan.json  --poi ctthh --xmin -1 --xmax 1
