WSpath="../SMEFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"

quickstats limit_scan -i ${WSpath} --param_expr "cdp=-10_10_0.1"  --poi mu_XS_HH --outdir cdp_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "cp=-10_10_0.1"   --poi mu_XS_HH --outdir cp_limit_scan   --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "ctp=-10_10_0.1"  --poi mu_XS_HH --outdir ctp_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "ctG=-10_10_0.1"  --poi mu_XS_HH --outdir ctG_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "cpg=-10_10_0.1"  --poi mu_XS_HH --outdir cpg_limit_scan  --outname limits.json --blind --no-cache

python make_EFT_limit_scan.py --poi cdp --smeft
python make_EFT_limit_scan.py --poi cp  --smeft
python make_EFT_limit_scan.py --poi ctp --smeft
python make_EFT_limit_scan.py --poi ctG --smeft
python make_EFT_limit_scan.py --poi cpg --smeft