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
    keep_output = False
    if "cell_type" in cell and cell["cell_type"]=="code":
        if cell["source"] and cell["source"][0]=="#__keep_output__\n": # First line flag to indicate to keep this output (for not empty cells)
            keep_output = True
    if "outputs" in cell and not keep_output:
        cell["outputs"] = []
    if "execution_count" in cell: # The execution_count is always removed (if filtering is "activated")
        cell["execution_count"] = None
    if "metadata" in cell and "ExecuteTime" in cell["metadata"]: # The ExecuteTime comes from the extension ExecuteTime
        cell["metadata"]["ExecuteTime"] = None


if ipy_version == 2:
    for sheet in json_in["worksheets"]:
        for cell in sheet["cells"]:
            strip_output_from_cell(cell)
else:
    for cell in json_in["cells"]:
        strip_output_from_cell(cell)

json.dump(json_in, sys.stdout, sort_keys=True, indent=1, separators=(",",": "))
