# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Schedulers execute Plans on a given Context.

Logging:
    See config.logging.

    Message: No message is logged, fields are provided through the logging module's Extra dict.
    "Extra" keys:
        run_id: a UUID to correlate Plan execution runs.
        type: "Plan" or "Action". Plans can create multiple action lists per execution run. Actions done are logged.
        description: Message context. Plan Name or Action.string().

"""

import uuid
import logging

from typing import List

from .mixins.plan import PlanMixin
from .mixins.context import ContextMixin
from .mixins.action import ActionMixin

# from .config.logging import logging_preprocessors

logger = logging.getLogger(__name__)


class Scheduler:
    """Schedulers execute Plans on a given Context.

    Plans are executed until they return an empty list or None from Plan.create.
    """

    def __init__(self, name: str, plans: List[PlanMixin] = None):
        """Doesn't do anything special, might collect Plans in the future. Not sure.

        Args:
            name (str): NYI
            plans (List[PlanMixin], optional): NYI, schedulers might collect Plans. Not sure. Defaults to [].
        """
        self.name = name
        self.plans = plans
        self.run_id = ""

    # Execute a given plan with context
    def execute(self, plan: PlanMixin, context: ContextMixin):
        """Execute a given plan with context.

        Plans are executed until they return an empty list or None from Plan.create.
        This means that your Plan MUST eventually produce an empty list or None.
        There are no safety guarentees here, this will go infinite if you let it.

        Args:
            plan (PlanMixin): The plan to execute. See plan.create(context).
            context (ContextMixin): The context to provide to plan.create for building our list of Actions to do.

        Logging:
            Logs each plan iteration, using Plan.name for "description".
        """
        # step_count = 0
        self.run_id = str(uuid.uuid1())
        steps = plan.create(context)
        while steps:
            # step_count += 1
            logger.info(
                "",
                extra={"run_id": self.run_id, "type": "plan", "description": plan.name},
            )
            self.react(context, steps)
            steps = plan.create(context)

    # Recursively execute Actions (which may return further actions, requiring the recursion)
    def react(self, context: ContextMixin, steps: List[ActionMixin]):
        """Recurively do Actions (which may return further actiosn, requiring the recursion).

        Args:
            context (ContextMixin): The Context to pass to Action.do
            steps (List[ActionMixin]): The Actions being done.

        Logging:
            Logs each step, using Action.string() for "description".
        """
        for step in steps:
            logger.info(
                "",
                extra={
                    "run_id": self.run_id,
                    "type": "action",
                    "description": step.string(),
                },
            )
            result = step.do(context)
            if result:
                self.react(context, result)
