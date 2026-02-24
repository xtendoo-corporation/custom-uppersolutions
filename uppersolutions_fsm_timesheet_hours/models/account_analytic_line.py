# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # -------------------------------------------------------
    # Cálculo de Time Spent desde campos Studio hora inicio/fin
    # -------------------------------------------------------

    @api.model
    def _compute_unit_amount_from_studio_times(self, vals):
        """Compute unit_amount from x_studio_hora_inicio_1 and x_studio_hora_fina."""
        start = vals.get("x_studio_hora_inicio_1")
        end = vals.get("final_hour")
        if start and end:
            start_dt = fields.Datetime.to_datetime(start)
            end_dt = fields.Datetime.to_datetime(end)
            if start_dt and end_dt and end_dt > start_dt:
                vals["unit_amount"] = (end_dt - start_dt).total_seconds() / 3600.0
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._compute_unit_amount_from_studio_times(vals)
        return super().create(vals_list)

    def write(self, vals):
        if "start_hour" in vals and "final_hour" in vals:
            self._compute_unit_amount_from_studio_times(vals)
        elif "start_hour" in vals or "final_hour" in vals:
            for record in self:
                record_vals = dict(vals)
                if "start_hour" not in record_vals:
                    record_vals["start_hour"] = (
                        record.start_hour
                    )
                if "final_hour" not in record_vals:
                    record_vals["final_hour"] = record.final_hour
                self._compute_unit_amount_from_studio_times(record_vals)
                if "unit_amount" in record_vals:
                    super(AccountAnalyticLine, record).write(
                        {"unit_amount": record_vals["unit_amount"]}
                    )
        return super().write(vals)

    @api.onchange("start_hour", "final_hour")
    def _onchange_studio_hora_inicio_fin(self):
        for record in self:
            start = record.start_hour
            end = record.final_hour
            if start and end and end > start:
                record.unit_amount = (end - start).total_seconds() / 3600.0

    attachment_number = fields.Integer(
        string="Nº Adjuntos",
        compute="_compute_attachment_number",
    )

    attachment_ids = fields.Many2many(
        comodel_name="ir.attachment",
        relation="account_analytic_line_attachment_rel",
        column1="line_id",
        column2="attachment_id",
        string="Adjuntos",
    )

    @api.depends("attachment_ids")
    def _compute_attachment_number(self):
        for line in self:
            line.attachment_number = len(line.attachment_ids)




    # -------------------------------------------------------
    # Campos de studio y funcionamiento pasado a odoo normal
    # -------------------------------------------------------
    start_hour = fields.Datetime(
        string="Hora Inicio",
    )

    final_hour = fields.Datetime(
        string="Hora Fin",
    )
