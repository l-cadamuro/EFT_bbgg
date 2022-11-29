# EFT_bbgg
Tools for EFT interpretation in the ATLAS HH->bbgg analysis

## Installation
1. Install Roofit extensions (if needed), instructions here https://gitlab.cern.ch/atlas_higgs_combination/software/RooFitExtensions
2. Install quickstats : https://gitlab.cern.ch/clcheng/quickstats/-/tree/master/
3. Download the input workspaces from the bbgg analysis: https://gitlab.cern.ch/atlas-physics/HDBS/DiHiggs/yybb/database/-/tree/master
4. Download this repository


## Modification of a workspace to include EFT effects - ``workspace_scripts``

You first need to determine the yield for each mHH bin. This is done with the script ``make_mHH_split.py`` that generates a file containing the information split by mHH bin.

The input ntuples can be downloaded from : ``/eos/user/c/chlcheng/analysis/bbyy/VBF_optimization/preselected_h027_01_04_2022/outputs/h027_final_legacy/minitrees``.

Then xml workspace description files are converted running the script ``modify_xml_cards.py`` (no command line options needed, all is configured in the script body). This script uses the following input:

- xml input cards (path set in the script)
- Ai coefficient files (stored in ``coeff_files``)
- the yields per mHH bin (read from the previous step)

The workspace can be built as n_mHHbins independent signals (all with the same CrystalBallPDF in a given category), or as a single signal composed as sum(yields) x CrystalBallPDF in a given category.
Select the behaviour with ``implementation_type = 'split_signals'`` (first case) or ``implementation_type = 'merged_yields'`` (second case).

## Compiling the workspace

The workspace is built with ``quickstats``: 
```
cd EFT_workspaces
quickstats build_xml_ws -i config/master_EFT.xml --basedir ./
```

This will create a new folder named ``workspace`` with the ROOT workspace file.


## Verification of the workspace

The folder ``analysis_scripts`` contains tools to characterize the EFT workspace:

- ``make_acceptance_from_ws.py`` uses the functions for the yield scalings to plot yield or acceptance as function of a given POI. Example of usage ``python make_acceptance_from_ws.py --input ../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root --poi chhh`` (see ``--help`` for other options. Note that with ``--other-pois ctth=1 cgghh=2`` you can make the plot under other POI configurations. Anything unspecified is fixed at the SM expectation.)  . To instruct the code how to lookup the yields (single one or merged, depending on how it was created, see above) use ``--impl-type split_signals`` or ``--impl-type merged_yields``. Make all plots with ``make_all_acceptance_from_ws.sh``

- ``make_acceptance_from_ws_klambda.py`` does the same as above but from the parametric legacy workspace. Usage : ``python make_acceptance_from_ws_klambda.py --input ../../database/workspaces/NonResonant_Wisconsin/legacy_h027_stat_only/workspaces/WS-bbyy-non-resonant_param.root --do-yield --export klambda_yield.pkl``

- ``compare_yields_klambda_chhh.py`` make a comparison between the chhh and klambda parametrised yields. To use, first export the chhh yields (use ``--do-yield --export chhh_yield.pkl``)  with other POIs at SM, and then ``python compare_yields_klambda_chhh.py``


## Making results

All scripts to make results are in the ``results_scripts/`` folder.
Most of the methods of quickstats are taken from [this tutorial](https://gitlab.cern.ch/clcheng/bbyy_analysis_framework/-/blob/master/notebooks/T15-StatEvaluationFromWorkspace.ipynb) 

### Upper limit scan

To make the scan with quickstats: use the ``limit_scan`` command and then plot the results with ``make_EFT_limit_scan.py`` . The script ``make_all_limits_scans.sh`` lists the commands for the generation and plotting of the data.

### Likelihood scan

First you need to generate the Asimov dataset (``quickstats generate_asimov``), and then you can fit it with ``quickstats likelihood_scan`` and plot with ``make_likelihood_scan.py``.
The script ``make_all_likelihood_scans.sh`` lists the commands for the generation and plotting of the data.