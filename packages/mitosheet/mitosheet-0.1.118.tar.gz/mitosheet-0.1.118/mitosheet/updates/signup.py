#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A signup update, sets the user's email as the user_email in user.json
"""

from mitosheet.user_utils import get_user_info, set_user_info
import analytics
import sys
from mitosheet._version import __version__


SIGNUP_EVENT = 'signup_update'
SIGNUP_PARAMS = ['user_email']


def execute_signup_update(wsc, user_email):
    """
    The function responsible for signing in the user.
    """
    # Set the user_email in user.json
    set_user_info(user_email=user_email)

    user_info = get_user_info()

    # Identify the user with their new email
    analytics.identify(user_info['static_user_id'], {
        'email': user_info['user_email']
    })


"""
This object wraps all the information
that is needed for a undo step!
"""
SIGNUP_UPDATE = {
    'event_type': SIGNUP_EVENT,
    'params': SIGNUP_PARAMS,
    'execute': execute_signup_update
}