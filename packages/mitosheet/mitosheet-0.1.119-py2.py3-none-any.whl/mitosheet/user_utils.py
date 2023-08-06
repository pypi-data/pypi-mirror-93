#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions for getting and setting the user profile 
in user.json
"""

from copy import deepcopy
import os
import json

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The path of the user.json file
USER_JSON_PATH = os.path.join(MITO_FOLDER, 'user.json')

def get_user_info():
    """
    Returns the contents of the user.json file

    Returns NONE if no user.json file exists. 
    """
    # If we're in a Github Action, we just always return the same
    # results, so that we don't generate millions of fake users
    if 'CI' in os.environ and os.environ['CI'] is not None:
        return {
            'static_user_id': 'github_action',
            'user_email': 'github@action.com'
        }


    if not os.path.exists(MITO_FOLDER):
        return None

    if not os.path.exists(USER_JSON_PATH):
        return None
    
    with open(USER_JSON_PATH) as f:
        try:
            # We try and read the file as JSON
            return json.load(f)
        except: 
            return None


def set_user_info(
        static_user_id=None,
        user_email=None
    ):
    """
    Updates the user.json file with the newly passed static_user_id and 
    user_email. 

    If no user.json currently exists, will create one. If one already exists,
    will only update the fields that are not None.

    By default, the user_email is set to '' if an email in not provided.
    """
    # If we're in a Github Action, we don't really change anything!
    if 'CI' in os.environ and os.environ['CI'] is not None:
        return

    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    prev_user_info = get_user_info()
    # If it exists, update what we have already
    if prev_user_info is not None:
        new_user_info = deepcopy(prev_user_info)
        if static_user_id is not None:
            new_user_info['static_user_id'] = static_user_id
        if user_email is not None:
            new_user_info['user_email'] = user_email
    # Otherwise, create a new object
    else:
        new_user_info = {
            'static_user_id': static_user_id,
            'user_email': user_email
        }

    # Finially, write it to the file
    with open(USER_JSON_PATH, 'w+') as f:
        f.write(json.dumps(new_user_info))



