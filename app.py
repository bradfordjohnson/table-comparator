from shiny.ui import page_navbar
from functools import partial
from shiny.express import ui, input, render
from helpers import get_similar_fields
import mimetypes
from typing import List
from fuzzywuzzy import fuzz
from itertools import combinations
import pandas as pd
import json
import re


MAX_SIZE = 50000

ui.page_opts(
    title="Table Comparator",
    page_fn=partial(page_navbar, id="page"),
)

with ui.nav_panel("Field Similarity"):
    with ui.layout_columns():
        with ui.card():
            ui.card_header("Upload data files to compare")
            ui.p("Body text")
            (ui.input_slider("field_slider", "Max similar fields to return", 1, 5, 2),)
            ui.input_file("file_", "Upload datasets", accept=[
                ".csv", ".json"], multiple=True)

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
            match = re.search("\\.(\\w+)$", file_info["name"])
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
        if len(fields_dict) == 1:
            return "Please upload more than one dataset at a time"

        return get_similar_fields(fields_dict, input.field_slider())
