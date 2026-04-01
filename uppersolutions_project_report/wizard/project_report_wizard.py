import base64
from io import BytesIO

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class UpperSolutionsProjectReportWizard(models.TransientModel):
    _name = "uppersolutions.project.report.wizard"
    _description = "UpperSolutions Project Report Wizard"

    REPORT_COLUMNS = [
        _("Proyecto"),
        _("Cliente"),
        _("Nombre proyecto"),
        _("Fecha confirmación"),
        _("Fecha factura Cliente"),
        _("Fecha factura Proveedor"),
        _("Materiales"),
        _("Desplazamiento"),
        _("Dietas"),
        _("Horas"),
        _("Coste Horas / PS"),
        _("Subc"),
        _("Total presupuesto"),
        _("Materiales"),
        _("Desplazamiento"),
        _("Dietas"),
        _("Horas"),
        _("Coste h Internas"),
        _("Subc"),
        _("Total Real"),
        _("PRESUPUESTO"),
        _("FACTURADO"),
        _("DIFERENCIA"),
        _("MARGEN"),
    ]

    REPORT_GROUPS = [
        (6, 12, _("COSTE PROYECTO")),
        (13, 19, _("COSTE PROYECTO REAL")),
        (20, 23, _("V E N T A")),
    ]

    date_start = fields.Date(string="Fecha inicio", required=True)
    date_end = fields.Date(string="Fecha fin", required=True)
    file_data = fields.Binary(string="Archivo", readonly=True)
    file_name = fields.Char(string="Nombre del archivo", readonly=True)

    def _validate_dates(self):
        self.ensure_one()
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError(_("La fecha de inicio no puede ser mayor que la fecha de fin."))

    def _get_report_filename(self):
        self.ensure_one()
        return "reporte_proyectos_%s_%s.xlsx" % (
            self.date_start.strftime("%Y%m%d"),
            self.date_end.strftime("%Y%m%d"),
        )

    def _get_report_rows(self):
        self.ensure_one()
        return []

    def _generate_xlsx_content(self):
        self.ensure_one()
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet(_("Reporte de proyectos")[:31])

        header_format = workbook.add_format({
            "bold": True,
            "font_color": "#FFFFFF",
            "bg_color": "#1F4E78",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "text_wrap": True,
        })
        group_header_format = workbook.add_format({
            "bold": True,
            "font_color": "#FFFFFF",
            "bg_color": "#5B9BD5",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })
        cell_format = workbook.add_format({
            "border": 1,
        })

        worksheet.set_row(0, 30)
        worksheet.set_row(1, 24)
        worksheet.freeze_panes(2, 0)

        for col, column_name in enumerate(self.REPORT_COLUMNS):
            if col < 6:
                worksheet.merge_range(0, col, 1, col, column_name, header_format)
            else:
                worksheet.write(0, col, column_name, header_format)
            worksheet.set_column(col, col, max(len(column_name) + 4, 18))

        for start_col, end_col, group_name in self.REPORT_GROUPS:
            worksheet.merge_range(1, start_col, 1, end_col, group_name, group_header_format)

        for row_index, row_values in enumerate(self._get_report_rows(), start=2):
            for col_index, value in enumerate(row_values):
                worksheet.write(row_index, col_index, value or "", cell_format)

        workbook.close()
        output.seek(0)
        return output.read()

    def action_generate_xlsx(self):
        self.ensure_one()
        self._validate_dates()

        self.write({
            "file_data": base64.b64encode(self._generate_xlsx_content()),
            "file_name": self._get_report_filename(),
        })

        return {
            "type": "ir.actions.act_url",
            "url": (
                "/web/content/?model=%s&id=%s&field=file_data&filename_field=file_name&download=true"
                % (self._name, self.id)
            ),
            "target": "self",
        }


