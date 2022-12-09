WSname="../SMEFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"
python make_acceptance_from_ws.py --input ${WSname} --poi cdp --impl-type merged_yields --smeft
python make_acceptance_from_ws.py --input ${WSname} --poi cp  --impl-type merged_yields --smeft
python make_acceptance_from_ws.py --input ${WSname} --poi ctp --impl-type merged_yields --smeft
python make_acceptance_from_ws.py --input ${WSname} --poi ctG --impl-type merged_yields --smeft
python make_acceptance_from_ws.py --input ${WSname} --poi cpg --impl-type merged_yields --smeft