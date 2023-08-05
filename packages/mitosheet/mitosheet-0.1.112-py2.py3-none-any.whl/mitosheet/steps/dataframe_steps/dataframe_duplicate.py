#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
This steps duplicates a dataframe of a given index. 
"""

DATAFRAME_DUPLICATE_EVENT = 'dataframe_duplicate_edit'
DATAFRAME_DUPLICATE_STEP_TYPE = 'dataframe_duplicate'

DATAFRAME_DUPLICATE_PARAMS = [
    'sheet_index'
]

def get_first_unused_name(df_names, dataframe_name):
    """
    Appends _1, _2, .. to df name until it finds an unused 
    dataframe name. If no append is necessary, will just return
    """
    if dataframe_name not in df_names:
        return dataframe_name

    for i in range(len(df_names) + 1):
        new_name = f'{dataframe_name}_{i + 1}'
        if new_name not in df_names:
            return new_name


def execute_dataframe_duplicate(
        wsc,
        sheet_index
    ):
    """
    Duplicates the dataframe at sheet_index.
    """
    # Create a new step and save the parameters
    wsc._create_and_checkout_new_step(DATAFRAME_DUPLICATE_STEP_TYPE)

    # Save the parameters
    wsc.curr_step['sheet_index'] = sheet_index

    # Execute the step
    df_copy = wsc.curr_step['dfs'][sheet_index].copy(deep=True)
    new_name = get_first_unused_name(wsc.curr_step['df_names'], wsc.curr_step['df_names'][sheet_index] + '_copy')
    wsc.add_df_to_curr_step(df_copy, new_name)


def transpile_dataframe_duplicate(
        widget_state_container,
        step,
        sheet_index
    ):
    """
    Transpiles the dataframe duplication to Python code
    """
    old_df_name = step['df_names'][sheet_index]
    new_df_name = step['df_names'][len(step['dfs']) - 1]

    return [f'{new_df_name} = {old_df_name}.copy(deep=True)']


DATAFRAME_DUPLICATE_STEP = {
    'step_version': 1,
    'event_type': DATAFRAME_DUPLICATE_EVENT,
    'step_type': DATAFRAME_DUPLICATE_STEP_TYPE,
    'params': DATAFRAME_DUPLICATE_PARAMS,
    'saturate': None,
    'execute': execute_dataframe_duplicate,
    'transpile': transpile_dataframe_duplicate
}