# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

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
