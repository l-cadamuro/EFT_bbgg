WSpath="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"

quickstats limit_scan -i ${WSpath} --param_expr "chhh=-10_10_0.1" --poi mu_XS_HH --outdir chhh_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "ctth=-2_2_0.1"   --poi mu_XS_HH --outdir ctth_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "cgghh=-5_5_0.1"  --poi mu_XS_HH --outdir cgghh_limit_scan --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "cggh=-10_10_0.1" --poi mu_XS_HH --outdir cggh_limit_scan  --outname limits.json --blind --no-cache
quickstats limit_scan -i ${WSpath} --param_expr "ctthh=-3_3_0.1"  --poi mu_XS_HH --outdir ctthh_limit_scan --outname limits.json --blind --no-cache

python make_EFT_limit_scan.py --poi chhh
python make_EFT_limit_scan.py --poi ctth --xmin 0.7 --xmax 1.3
python make_EFT_limit_scan.py --poi cgghh
python make_EFT_limit_scan.py --poi cggh
python make_EFT_limit_scan.py --poi ctthh