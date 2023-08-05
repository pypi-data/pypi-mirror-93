#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A simple import, which allows you to import dataframes with the given file_names

NOTE: special care needs to be taken when upgrading this step, as it is used (e.g in the 
api in special ways). Not sure exactly how, but be careful + test it thoroughly.
"""
import pandas as pd
import json
from mitosheet.utils import get_header_renames, make_valid_header

SIMPLE_IMPORT_EVENT = 'simple_import_edit'
SIMPLE_IMPORT_STEP_TYPE = 'simple_import'

SIMPLE_IMPORT_PARAMS = [
    'file_names', # list of strings
]

def file_name_to_df_name(file_name: str):
    # We abuse the fact that all valid mito headers are valid dataframe names...
    # doh.
    return make_valid_header(file_name)

def get_dataframe_names(file_names, existing_df_names):
    """
    Helper function for taking a list of file names and turning them into valid
    names for dataframes.

    NOTE:
    1. If there are duplicates, appends onto the end of them to deduplicate.
    2. Avoids overwriting existing df names.
    """
    new_names_inital = [file_name_to_df_name(file_name) for file_name in file_names]

    final_names = []

    # Keep appending names till we get one that doesn't overlap
    for name in new_names_inital:
        curr_name = name
        count = 0
        while curr_name in final_names or curr_name in existing_df_names:
            curr_name = f'{name}_{count}'
            count += 1
        
        final_names.append(curr_name)
    
    return final_names


def execute_simple_import(
        wsc,
        file_names
    ):
    """
    Imports the files with the given file names into the sheet
    """
    # Create a new step
    wsc._create_and_checkout_new_step(SIMPLE_IMPORT_STEP_TYPE)

    column_header_renames = dict()
    for file_name, df_name in zip(file_names, get_dataframe_names(file_names, wsc.curr_step['df_names'])):
        # TODO: catch this error in a good way
        df = pd.read_csv(file_name)
        renames = get_header_renames(df.keys())
        if len(renames) > 0:
            # Save that we did these renames
            column_header_renames[df_name] = renames
            # Actually perform any renames we need to
            df.rename(columns=renames, inplace=True)

        wsc.add_df_to_curr_step(df, df_name=df_name)
    
    # Save the renames that have occured in the step, for transpilation reasons
    wsc.curr_step['column_header_renames'] = column_header_renames


def transpile_simple_import(
        widget_state_container,
        step,
        file_names
    ):
    """
    Transpiles a sort step to Python code. 
    """

    code = ['import pandas as pd']
    for file_name, df_name in zip(file_names, step['df_names'][len(step['df_names']) - len(file_names):]):

        code.append(
            f'{df_name} = pd.read_csv(\'{file_name}\')'
        )
        # If we had to rename columns, mark that as well
        if df_name in step['column_header_renames']:
            renames = step['column_header_renames'][df_name]
            code.append(
                f'{df_name}.rename(columns={json.dumps(renames)}, inplace=True)'
            )

    return code


SIMPLE_IMPORT_STEP = {
    'step_version': 1,
    'event_type': SIMPLE_IMPORT_EVENT,
    'step_type': SIMPLE_IMPORT_STEP_TYPE,
    'params': SIMPLE_IMPORT_PARAMS,
    'saturate': None,
    'execute': execute_simple_import,
    'transpile': transpile_simple_import
}