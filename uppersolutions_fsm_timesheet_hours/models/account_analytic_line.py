# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.model
    def _compute_unit_amount_from_studio_times(self, vals):
        """Calculate unit_amount (Time Spent) from Studio start/end time fields.

        If x_studio_hora_inicio_1 (Hora Inicio) and x_studio_hora_fina (Hora Fin)
        are both provided, compute unit_amount as the difference in hours.
        """
        start = vals.get("x_studio_hora_inicio_1")
        end = vals.get("x_studio_hora_fina")
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
        # If both times are being set in this write, compute unit_amount directly
        if "x_studio_hora_inicio_1" in vals and "x_studio_hora_fina" in vals:
            self._compute_unit_amount_from_studio_times(vals)
        elif "x_studio_hora_inicio_1" in vals or "x_studio_hora_fina" in vals:
            # Only one of the two fields changed: compute per record
            for record in self:
                record_vals = dict(vals)
                # Fill in the missing field from the existing record value
                if "x_studio_hora_inicio_1" not in record_vals:
                    record_vals["x_studio_hora_inicio_1"] = (
                        record.x_studio_hora_inicio_1
                    )
                if "x_studio_hora_fina" not in record_vals:
                    record_vals["x_studio_hora_fina"] = record.x_studio_hora_fina
                self._compute_unit_amount_from_studio_times(record_vals)
                # Only update unit_amount if it was computed
                if "unit_amount" in record_vals:
                    super(AccountAnalyticLine, record).write(
                        {"unit_amount": record_vals["unit_amount"]}
                    )
        return super().write(vals)

    @api.onchange("x_studio_hora_inicio_1", "x_studio_hora_fina")
    def _onchange_studio_hora_inicio_fin(self):
        """Recalculate unit_amount when start or end time changes in the UI."""
        for record in self:
            start = record.x_studio_hora_inicio_1
            end = record.x_studio_hora_fina
            if start and end and end > start:
                record.unit_amount = (end - start).total_seconds() / 3600.0
            elif not end or not start:
                # Don't reset if only one is set
                pass
