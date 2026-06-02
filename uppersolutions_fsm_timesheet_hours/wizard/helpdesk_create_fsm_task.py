# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class HelpdeskCreateFsmTask(models.TransientModel):
    _inherit = "helpdesk.create.fsm.task"

    def action_generate_task(self):
        task = super().action_generate_task()
        if self.env.context.get("copy_helpdesk_ticket_attachments_to_fsm_task"):
            self.helpdesk_ticket_id._copy_attachments_to_fsm_task(task)
        return task

