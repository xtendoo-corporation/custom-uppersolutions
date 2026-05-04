# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

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
