# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    necessary_prl = fields.Boolean(
        string="PRL Necesario",
        readonly=True,
        store=True,
    )