WSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"

# Course binning of parameters
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.5,ctthh=-3_3_0.5" --poi mu_XS_HH --outdir chhh_ctthh_course  --outname limits.json --blind # takes about 379 seconds (6 and a half minutes)
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.5,cgghh=-5_5_0.5" --poi mu_XS_HH --outdir chhh_cgghh_course  --outname limits.json --blind # 8.5 mins 
#quickstats limit_scan -i ${WSpath} --param_expr "cgghh=-5_5_0.5,ctthh=-3_3_0.5" --poi mu_XS_HH --outdir cgghh_ctthh_course  --outname limits.json --blind # 2 minutes 

# Finer binning
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.1,ctthh=-3_3_0.1" --poi mu_XS_HH --outdir chhh_ctthh  --outname limits.json --blind --cache 
#quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.1,cgghh=-5_5_0.1" --poi mu_XS_HH --outdir chhh_cgghh  --outname limits.json --blind 
#quickstats limit_scan -i ${WSpath} --param_expr "cgghh=-5_5_0.1,ctthh=-3_3_0.1" --poi mu_XS_HH --outdir cgghh_ctthh  --outname limits.json --blind 

# Non-negligible HEFT impact on single higgs 
#quickstats limit_scan -i ${WSpath} --param_expr "ctth=-3_3_0.5,cggh=-3_3_0.5" --poi mu_XS_HH --outdir ctth_cggh  --outname limits.json --blind 
