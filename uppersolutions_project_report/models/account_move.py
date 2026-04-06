from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_hour_category_invoice_lines(self):
        self.ensure_one()
        return self.invoice_line_ids.filtered(
            lambda line:
                not line.display_type
                and line.product_id
                and line.product_id.categ_id
                and line.product_id.categ_id.is_hour_category
        )

    def _has_hour_category_invoice_lines(self):
        self.ensure_one()
        return bool(self._get_hour_category_invoice_lines())

    def _get_hour_parts_timesheets(self):
        self.ensure_one()
        hour_sale_lines = self._get_hour_category_invoice_lines().mapped("sale_line_ids")
        timesheets = self.env["account.analytic.line"]

        if "timesheet_ids" in self._fields:
            timesheets = self.timesheet_ids.filtered(lambda timesheet: timesheet.so_line in hour_sale_lines)
        elif hour_sale_lines:
            timesheets = self.env["account.analytic.line"].search([
                ("timesheet_invoice_id", "=", self.id),
                ("so_line", "in", hour_sale_lines.ids),
            ])

        return timesheets.sorted(lambda timesheet: (timesheet.date or fields.Date.today(), timesheet.id))

    def _get_hour_part_ticket_name(self, timesheet):
        timesheet.ensure_one()
        if "helpdesk_ticket_id" in timesheet._fields and timesheet.helpdesk_ticket_id:
            return timesheet.helpdesk_ticket_id.display_name
        if timesheet.task_id and "helpdesk_ticket_id" in timesheet.task_id._fields and timesheet.task_id.helpdesk_ticket_id:
            return timesheet.task_id.helpdesk_ticket_id.display_name
        return ""

    def _get_invoice_hour_parts_data(self):
        self.ensure_one()
        hour_parts = []
        for timesheet in self._get_hour_parts_timesheets():
            hour_parts.append({
                "date": timesheet.date.strftime("%d/%m/%Y") if timesheet.date else "",
                "description": timesheet.name or "",
                "ticket": self._get_hour_part_ticket_name(timesheet),
                "duration": round(timesheet.unit_amount or 0.0, 2),
            })
        return hour_parts

