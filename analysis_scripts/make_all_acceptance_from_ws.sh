WSname="../EFT_workspaces/workspace/WS-bbyy-non-resonant_non_param.root"
python make_acceptance_from_ws.py --input ${WSname} --poi chhh  --impl-type merged_yields
python make_acceptance_from_ws.py --input ${WSname} --poi cgghh --impl-type merged_yields
python make_acceptance_from_ws.py --input ${WSname} --poi ctthh --impl-type merged_yields
python make_acceptance_from_ws.py --input ${WSname} --poi ctth  --impl-type merged_yields
python make_acceptance_from_ws.py --input ${WSname} --poi cggh  --impl-type merged_yields