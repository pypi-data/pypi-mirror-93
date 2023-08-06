# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Module-level exceptions."""


class ReconcileException(Exception):
    """Base class for exceptions in this module."""


class ContextMissingStateException(ReconcileException):
    """Exception raised in the event that a Context tries to access non-existent Current or Desired states."""

    def __init__(self, context_name: str, missing_state: str):
        """Exception raised in the event that a Context tries to access non-existent Current or Desired states.

        Args:
            context_name (str): Which context is raising the error
            missing_state (str): Which state is triggering the error
        """
        self.context_name = context_name
        self.missing_state = missing_state
        super().__init__()
