# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Abstract base that carries out orchestrating one iteration of a reconciliation procedure."""
from .context import ContextMixin


class PlanMixin:
    """Abstract base that carries out orchestrating one iteration of a reconciliation procedure.

    Plans create lists of Actions to be executed sequentially by Schedulers.
    Schedulers will continue to create and execute lists of Actions until an empty list is returned.
    """

    def __init__(self, plan_name: str, **kwargs):
        """Initialize a Plan.

        Optionally provide additional kwargs in your constructor to inform your action plan creation.

        Args:
            plan_name (str): A name uniquely identifying this plan. Useful for logging.
            **kwargs: Provide additional arguments when implementing your Plans' constructors for configuration.

        """
        self.name = plan_name
        super().__init__(**kwargs)  # type: ignore

    def string(self):
        """Return a string representation of this Plan for logging.

        Should uniquely identify the plan.

        Returns:
            str: A string representation of this Plan suitible for logging. Defaults to self.plan_name.

        """
        return "{}".format(self.plan_name)

    # Must return an Iterable of Actions
    def create(self, context: ContextMixin):
        """Create a list of actions based on a given context.

        Schedulers use Plans to create the overall sequence of actions necessary to reconcile a Context's two states.
        This MUST return an None or an empty list when states are reconciled, or the Scheduler will go infininte.

        ContextMixin member functions, like get_state_diff, should be used here to inform plan creation.
        See ContexMixin.

        Args:
            context (ContextMixin): The context used to inform plan creation.

        Raises:
            NotImplementedError: Must be implemented to act as a Plan for a Scheduler.

        Returns:
            list(ActionMixin): The list of actions to be carried out in sequence
                               or None when context states are reconciled.
        """
        raise NotImplementedError


if __name__ == "__main__":

    class __TestPlan(PlanMixin):  # pylint: disable=invalid-name
        def __init__(self, some, data, **kwargs):
            self.some = some
            self.data = data
            super().__init__(**kwargs)

        def create(self, context):
            # Do something with the context to create
            # a list of actions that need to be taken
            if context[0]:
                return ["step 1"]
            return ["step 0", "step 1", "step 2"]

    TP = __TestPlan("Some", "Data", plan_name="My Plan")
    print(TP.create([False]))
