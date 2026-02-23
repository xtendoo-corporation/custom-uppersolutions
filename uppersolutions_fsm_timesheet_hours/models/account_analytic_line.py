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
        if "x_studio_hora_inicio_1" in vals and "x_studio_hora_fina" in vals:
            self._compute_unit_amount_from_studio_times(vals)
        elif "x_studio_hora_inicio_1" in vals or "x_studio_hora_fina" in vals:
            for record in self:
                record_vals = dict(vals)
                if "x_studio_hora_inicio_1" not in record_vals:
                    record_vals["x_studio_hora_inicio_1"] = (
                        record.x_studio_hora_inicio_1
                    )
                if "x_studio_hora_fina" not in record_vals:
                    record_vals["x_studio_hora_fina"] = record.x_studio_hora_fina
                self._compute_unit_amount_from_studio_times(record_vals)
                if "unit_amount" in record_vals:
                    super(AccountAnalyticLine, record).write(
                        {"unit_amount": record_vals["unit_amount"]}
                    )
        return super().write(vals)

    @api.onchange("x_studio_hora_inicio_1", "x_studio_hora_fina")
    def _onchange_studio_hora_inicio_fin(self):
        for record in self:
            start = record.x_studio_hora_inicio_1
            end = record.x_studio_hora_fina
            if start and end and end > start:
                record.unit_amount = (end - start).total_seconds() / 3600.0

    attachment_number = fields.Integer(
        string="Nº Adjuntos",
        compute="_compute_attachment_number",
    )

    def _compute_attachment_number(self):
        attachment_data = self.env["ir.attachment"]._read_group(
            [("res_model", "=", self._name), ("res_id", "in", self.ids)],
            ["res_id"],
            ["__count"],
        )
        attachment_map = dict(attachment_data)
        for line in self:
            line.attachment_number = attachment_map.get(line.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env["ir.actions.act_window"]._for_xml_id("base.action_attachment")
        res["domain"] = [("res_model", "=", self._name), ("res_id", "=", self.id)]
        res["context"] = {
            "default_res_model": self._name,
            "default_res_id": self.id,
        }
        return res
