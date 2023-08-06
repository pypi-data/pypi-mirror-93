#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A signup update, sets the user's email as the user_email in user.json
"""

from mitosheet.user_utils import (set_user)
import analytics
import sys
from mitosheet._version import __version__
from mitosheet.mito_analytics import (set_static_user_id)


SIGNUP_EVENT = 'signup_update'
SIGNUP_PARAMS = ['user_email']


def execute_signup_update(wsc, user_email):
    """
    The function responsible for signing in the user.
    """
    # Set the user_email in user.json
    set_user(user_email)

    # Update the STATIC_USER_ID for future logs
    set_static_user_id(user_email)

    # Identify the user with their new id to segment
    analytics.identify(user_email, {
        'location': __file__,
        'python_version': sys.version_info,
        'mito_version': __version__
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