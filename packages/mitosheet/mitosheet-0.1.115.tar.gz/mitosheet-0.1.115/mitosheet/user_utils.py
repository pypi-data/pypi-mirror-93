#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions for getting and setting the user profile 
in user.json
"""

import os
import json

# Where all global .mito files are stored
MITO_FOLDER = os.path.expanduser("~/.mito")

# The path of the user.json file
USER_JSON_PATH = os.path.join(MITO_FOLDER, 'user.json')


def set_user(user_email=''):
    """
    Sets the user_email in user.json. 

    By default, the user_email is set to '' if an email in not provided.
    """
    if not os.path.exists(MITO_FOLDER):
        os.mkdir(MITO_FOLDER)

    with open(USER_JSON_PATH, 'w+') as f:
        user_profile = {
            'user_email': user_email
        }
        f.write(json.dumps(user_profile))



def get_user():
    """
    Returns the contents of the user.json file

    Returns NONE if no user.json file exists. 
    """
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
