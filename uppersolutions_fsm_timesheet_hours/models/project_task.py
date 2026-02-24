# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    service_for_or_the_third_parties = fields.Boolean(
        related="helpdesk_ticket_id.service_to_third_parties",
        readonly=True
    )

    ticket_manager = fields.Many2one(
        related="helpdesk_ticket_id.user_id",
        string="Gestor del Ticket",
        readonly=True
    )

    original_ticket = fields.Many2one(
        related="helpdesk_ticket_id",
        string="Ticket Original",
        readonly=True,
    )

    intervention_date = fields.Date(
        related="helpdesk_ticket_id.estimated_date",
        string="Fecha de Intervención",
        readonly=True,
    )
