import mimetypes
from typing import List
import json
import re
import pandas as pd

from shiny.express import ui, input, render

MAX_SIZE = 50000

with ui.layout_columns():
    with ui.card():  
        ui.card_header("Upload data files to compare")
        ui.p("Body text")
        ui.input_file("file_", "", accept=[".csv", ".json"], multiple=True)

# can make use of for loops to iterate and 
# display multiple ui elements
#
# thinking of doing this after files are uploaded
# make 2 columns, one for each file, and display the
# fields of each file in the respective columns
#
# from here I can add the analytics and comparison
# functions to compare the fields of the files


# file_infos is a list of dicts; each dict represents one file. Example:
# [
#   {
#     'name': 'data.csv',
#     'size': 2601,
#     'type': 'text/csv',
#     'datapath': '/tmp/fileupload-1wnx_7c2/tmpga4x9mps/0.csv'
#   }
# ]
    
@render.text
def file_content():
    file_infos = input.file_()
    if not file_infos:
        return

    fields_dict = {}

    for file_info in file_infos:
        match = re.search("\.(\w+)$", file_info["name"])
        extension = match.group(1)

        if extension == "csv":
            df = pd.read_csv(file_info["datapath"])
            fields_dict[file_info["name"]] = df.columns.tolist()

        if extension == "json":
            with open(file_info["datapath"]) as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    all_keys = set()
                    for item in data:
                        all_keys.update(item.keys())
                    fields_dict[file_info["name"]] = list(all_keys)

    return fields_dict