WSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"

# get 2d limit scan values by providing comma separated parameter ranges

#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.5,ctthh=-3_3_0.5" --poi mu_XS_HH --outdir chhh_ctthh_course  --outname limits.json --blind 
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.5,cgghh=-5_5_0.5" --poi mu_XS_HH --outdir chhh_cgghh_course  --outname limits.json --blind 
#quickstats limit_scan -i ${WSpath} --param_expr "cgghh=-5_5_0.5,ctthh=-3_3_0.5" --poi mu_XS_HH --outdir cgghh_ctthh_course  --outname limits.json --blind 

quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.1,ctthh=-3_3_0.1" --poi mu_XS_HH --outdir chhh_ctthh  --outname limits.json --blind 
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.1,cgghh=-5_5_0.1" --poi mu_XS_HH --outdir chhh_cgghh  --outname limits.json --blind 
#quickstats limit_scan -i ${WSpath} --param_expr "cgghh=-5_5_0.1,ctthh=-3_3_0.1" --poi mu_XS_HH --outdir cgghh_ctthh  --outname limits.json --blind 

#python make_EFT_limit_scan.py --poi chhh