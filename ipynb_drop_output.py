#!/usr/bin/env python
import sys
import json

nb = sys.stdin.read()

json_in = json.loads(nb)
nb_metadata = json_in["metadata"]
suppress_output = True
if "git" in nb_metadata:
    if "leave_outputs" in nb_metadata["git"] and nb_metadata["git"]["leave_outputs"]:
        suppress_output = False
if not suppress_output:
    sys.stdout.write(nb)
    exit() 


ipy_version = int(json_in["nbformat"])-1 # nbformat is 1 more than actual version.

def strip_output_from_cell(cell):
    if "outputs" in cell:
        cell["outputs"] = []
    if "execution_count" in cell:
        cell["execution_count"] = None


if ipy_version == 2:
    for sheet in json_in["worksheets"]:
        for cell in sheet["cells"]:
            strip_output_from_cell(cell)
else:
    for cell in json_in["cells"]:
        strip_output_from_cell(cell)

json.dump(json_in, sys.stdout, sort_keys=True, indent=1, separators=(",",": "))
