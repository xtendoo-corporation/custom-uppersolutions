# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models
from odoo.tools import float_round


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    _TIME_ROUNDING_MINUTES = 15
    _TIME_ROUNDING_HOURS = _TIME_ROUNDING_MINUTES / 60

    # -------------------------------------------------------
    # Cálculo de Time Spent desde campos Studio hora inicio/fin
    # -------------------------------------------------------

    @api.model
    def _round_datetime_to_quarter(self, value):
        dt_value = fields.Datetime.to_datetime(value)
        if not dt_value:
            return False
        day_start = dt_value.replace(hour=0, minute=0, second=0, microsecond=0)
        total_seconds = (dt_value - day_start).total_seconds()
        rounding_seconds = self._TIME_ROUNDING_MINUTES * 60
        rounded_steps = int((total_seconds + (rounding_seconds / 2)) // rounding_seconds)
        return day_start + timedelta(seconds=rounded_steps * rounding_seconds)

    @api.model
    def _round_unit_amount_to_quarter(self, unit_amount):
        if unit_amount in (False, None):
            return unit_amount
        return float_round(
            unit_amount,
            precision_rounding=self._TIME_ROUNDING_HOURS,
            rounding_method="HALF-UP",
        )

    @api.model
    def _get_resolved_datetime_value(self, vals, field_name, record=None):
        if field_name in vals:
            return fields.Datetime.to_datetime(vals[field_name]) if vals[field_name] else False
        return record[field_name] if record else False

    @api.model
    def _get_resolved_float_value(self, vals, field_name, record=None):
        if field_name in vals:
            return vals[field_name]
        return record[field_name] if record else False

    @api.model
    def _normalize_quarter_hour_values(self, vals, record=None):
        values = dict(vals)

        for field_name in ("start_hour", "final_hour"):
            if values.get(field_name):
                values[field_name] = fields.Datetime.to_string(
                    self._round_datetime_to_quarter(values[field_name])
                )

        if "unit_amount" in values:
            values["unit_amount"] = self._round_unit_amount_to_quarter(values["unit_amount"])

        start = self._get_resolved_datetime_value(values, "start_hour", record=record)
        end = self._get_resolved_datetime_value(values, "final_hour", record=record)
        unit_amount = self._get_resolved_float_value(values, "unit_amount", record=record)

        if start and end and ("start_hour" in values or "final_hour" in values):
            if end >= start:
                values["unit_amount"] = self._round_unit_amount_to_quarter(
                    (end - start).total_seconds() / 3600.0
                )
            return values

        if "unit_amount" in values and unit_amount not in (False, None):
            if start:
                values["final_hour"] = fields.Datetime.to_string(
                    self._round_datetime_to_quarter(start + timedelta(hours=unit_amount))
                )
            elif end:
                values["start_hour"] = fields.Datetime.to_string(
                    self._round_datetime_to_quarter(end - timedelta(hours=unit_amount))
                )
            return values

        if "start_hour" in values and start and unit_amount not in (False, None) and not end:
            values["final_hour"] = fields.Datetime.to_string(
                self._round_datetime_to_quarter(start + timedelta(hours=unit_amount))
            )
        elif "final_hour" in values and end and unit_amount not in (False, None) and not start:
            values["start_hour"] = fields.Datetime.to_string(
                self._round_datetime_to_quarter(end - timedelta(hours=unit_amount))
            )

        return values

    @api.model_create_multi
    def create(self, vals_list):
        normalized_vals_list = [self._normalize_quarter_hour_values(vals) for vals in vals_list]
        return super().create(normalized_vals_list)

    def write(self, vals):
        tracked_fields = {"start_hour", "final_hour", "unit_amount"}
        if not tracked_fields.intersection(vals):
            return super().write(vals)

        if len(self) == 1:
            return super().write(self._normalize_quarter_hour_values(vals, record=self))

        for record in self:
            super(AccountAnalyticLine, record).write(
                self._normalize_quarter_hour_values(vals, record=record)
            )
        return True

    def _apply_quarter_hour_onchange(self, vals):
        for record in self:
            normalized_vals = record._normalize_quarter_hour_values(vals, record=record)
            for field_name, value in normalized_vals.items():
                if field_name in ("start_hour", "final_hour") and value:
                    record[field_name] = fields.Datetime.to_datetime(value)
                else:
                    record[field_name] = value

    @api.onchange("start_hour", "final_hour")
    def _onchange_studio_hora_inicio_fin(self):
        for record in self:
            record._apply_quarter_hour_onchange(
                {
                    "start_hour": record.start_hour,
                    "final_hour": record.final_hour,
                }
            )

    @api.onchange("unit_amount")
    def _onchange_unit_amount_quarter_rounding(self):
        for record in self:
            record._apply_quarter_hour_onchange({"unit_amount": record.unit_amount})

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
