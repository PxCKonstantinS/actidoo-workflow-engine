# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 ActiDoo GmbH

"""TestFlowDemoExpenseCreate — creates a DemoExpense record from a user form.

Reference example for the workflow-data feature: a user enters expense data
(including a receipt upload); a service task persists it as the first version of
a DemoExpense row (``action="CREATE"``).
"""

import json

from actidoo_wfe.wf.service_task_helper import ServiceTaskHelper

DATA_MODELS = ["DemoExpense"]


def service_demo_persist_create(sth: ServiceTaskHelper):
    """Persist the entered data as a new DemoExpense record (first version).

    Plain ORM: ``id``/``created_at`` come from column defaults and the
    ``before_flush`` versioning hook assigns ``version=1`` / ``is_current=True``.
    Only the provenance (``workflow_instance_id``) and ``action`` are set here.
    """
    DemoExpense = sth.get_model("DemoExpense")
    receipt = sth.task_data.get("receipt")
    sth.db.add(
        DemoExpense(
            workflow_instance_id=sth.workflow_instance_id,
            action="CREATE",
            title=sth.task_data.get("title"),
            amount=sth.task_data.get("amount"),
            category=sth.task_data.get("category"),
            status="open",
            receipt=json.dumps(receipt) if receipt else None,
        )
    )
    sth.db.flush()


__all__ = ["DATA_MODELS", "service_demo_persist_create"]
