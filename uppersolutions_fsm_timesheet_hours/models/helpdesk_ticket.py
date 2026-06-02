# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from ast import literal_eval

from odoo import fields, models

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    partner_id = fields.Many2one(
        "res.partner",
        string="Cliente",
        tracking=True,
        index=True,
        domain=[("is_company", "=", True)],
    )

    service_to_third_parties = fields.Boolean(
        string="Técnico Externo",
        store=True,
    )

    user_id = fields.Many2one(
        "res.users",
        string="Asignado a",
        store=True,
    )

    estimated_date = fields.Date(
        string="Fecha Estimada",
        store=True,
    )

    #PRL Necesario
    necessary_prl = fields.Boolean(
        related="sale_order_id.necessary_prl",
        string="PRL Necesario",
        readonly=True,
    )

    def action_generate_fsm_task(self):
        action = super().action_generate_fsm_task()
        context = action.get("context", {})
        if isinstance(context, str):
            context = literal_eval(context)
        action["context"] = {
            **context,
            "copy_helpdesk_ticket_attachments_to_fsm_task": True,
        }
        return action

    def _copy_attachments_to_fsm_task(self, task):
        self.ensure_one()
        if not task:
            return

        attachments = self.env["ir.attachment"].search([
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
        ])
        for attachment in attachments:
            attachment.copy({
                "res_model": task._name,
                "res_id": task.id,
            })

