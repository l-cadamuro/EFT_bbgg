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

Then xml workspace description files are converted with the script ``modify_xml_cards.py``. This script uses the following input:

- xml input cards (path set in the script)
- Ai coefficient files (stored in ``coeff_files``)
- the yields per mHH bin (read from the previous step)