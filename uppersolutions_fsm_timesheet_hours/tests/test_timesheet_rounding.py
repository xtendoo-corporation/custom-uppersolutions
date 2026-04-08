from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestTimesheetQuarterHourRounding(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({
            "name": "Proyecto redondeo cuartos",
            "allow_timesheets": True,
        })
        cls.employee = cls.env["hr.employee"].create({
            "name": "Empleado redondeo cuartos",
            "company_id": cls.env.company.id,
        })

    def test_create_rounds_datetimes_and_duration(self):
        line = self.env["account.analytic.line"].create({
            "name": "Parte redondeado",
            "project_id": self.project.id,
            "employee_id": self.employee.id,
            "start_hour": "2026-04-08 10:08:00",
            "final_hour": "2026-04-08 11:53:00",
        })

        self.assertEqual(
            line.start_hour,
            fields.Datetime.to_datetime("2026-04-08 10:15:00"),
        )
        self.assertEqual(
            line.final_hour,
            fields.Datetime.to_datetime("2026-04-08 12:00:00"),
        )
        self.assertEqual(line.unit_amount, 1.75)

    def test_write_rounds_unit_amount_and_recomputes_final_hour(self):
        line = self.env["account.analytic.line"].create({
            "name": "Parte editable",
            "project_id": self.project.id,
            "employee_id": self.employee.id,
            "start_hour": "2026-04-08 10:00:00",
            "final_hour": "2026-04-08 10:30:00",
        })

        line.write({"unit_amount": 0.95})

        self.assertEqual(line.unit_amount, 1.0)
        self.assertEqual(
            line.final_hour,
            fields.Datetime.to_datetime("2026-04-08 11:00:00"),
        )

    def test_onchange_rounds_unit_amount_to_next_quarter_in_form(self):
        line = self.env["account.analytic.line"].new({
            "project_id": self.project.id,
            "employee_id": self.employee.id,
            "start_hour": fields.Datetime.to_datetime("2026-04-08 09:00:00"),
            "unit_amount": 0.95,
        })

        line._onchange_unit_amount_quarter_rounding()

        self.assertEqual(line.unit_amount, 1.0)
        self.assertEqual(
            line.final_hour,
            fields.Datetime.to_datetime("2026-04-08 10:00:00"),
        )


