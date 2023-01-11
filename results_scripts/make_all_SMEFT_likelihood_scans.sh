## input
WSpath="../SMEFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"
AsimovWSpath="../SMEFT_workspaces/workspace/WS-bbyy-non-resonant_non_param_Asimov.root"


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
quickstats generate_standard_asimov -i ${WSpath} -o ${AsimovWSpath} -d combData -p mu_XS_HH --asimov_types "-2"

# make likelihood scans for each POI
dataset="asimovData_1_NP_Nominal"
snapshot="asimovData_1_NP_Nominal"
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cdp=-20_30_0.1"  --outdir cdp_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cp=-20_10_0.1"   --outdir cp_likelihood_scan   --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "ctp=-20_15_0.1"  --outdir ctp_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "ctG=-2_2_0.01"  --outdir ctG_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache
quickstats likelihood_scan -i ${AsimovWSpath} --param_expr "cpg=-0.1_0.1_0.01"  --outdir cpg_likelihood_scan  --outname likelihood_scan.json --data ${dataset} --snapshot ${snapshot} --no-cache

python make_likelihood_scan.py --input cdp_likelihood_scan/likelihood_scan.json   --poi cdp
python make_likelihood_scan.py --input cp_likelihood_scan/likelihood_scan.json    --poi cp
python make_likelihood_scan.py --input ctp_likelihood_scan/likelihood_scan.json   --poi ctp
python make_likelihood_scan.py --input ctG_likelihood_scan/likelihood_scan.json   --poi ctG
python make_likelihood_scan.py --input cpg_likelihood_scan/likelihood_scan.json   --poi cpg
