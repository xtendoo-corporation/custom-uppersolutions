import base64
from datetime import datetime, time, timedelta
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
        print(
            "[uppersolutions_project_report] Validando fechas del wizard %s: date_start=%s, date_end=%s"
            % (self.id, self.date_start, self.date_end)
        )
        if self.date_start and self.date_end and self.date_start > self.date_end:
            raise ValidationError(_("La fecha de inicio no puede ser mayor que la fecha de fin."))

    def _get_report_filename(self):
        self.ensure_one()
        return "reporte_proyectos_%s_%s.xlsx" % (
            self.date_start.strftime("%Y%m%d"),
            self.date_end.strftime("%Y%m%d"),
        )

    def _get_project_name_from_order(self, order):
        self.ensure_one()
        project_names = []

        if 'project_ids' in order._fields and order.project_ids:
            project_names.extend(order.project_ids.mapped('display_name'))
        elif 'project_id' in order._fields and order.project_id:
            project_names.append(order.project_id.display_name)

        unique_project_names = list(dict.fromkeys(name for name in project_names if name))

        print(
            "[uppersolutions_project_report] Pedido %s -> proyectos encontrados: %s"
            % (order.name, unique_project_names)
        )

        return ", ".join(unique_project_names)

    def _get_budget_values_from_order(self, order):
        self.ensure_one()
        materials_amount = 0.0
        travel_amount = 0.0
        diets_amount = 0.0
        hours_qty = 0.0
        subcontracting_amount = 0.0

        valid_lines = order.order_line.filtered(
            lambda line: not line.display_type and not getattr(line, "is_downpayment", False)
        )

        print(
            "[uppersolutions_project_report] Pedido %s -> analizando %s líneas válidas"
            % (order.name, len(valid_lines))
        )

        for line in valid_lines:
            category = line.product_id.categ_id
            is_hour_category = bool(category and category.is_hour_category)
            is_travel_category = bool(category and category.is_travel_category)

            print(
                "[uppersolutions_project_report] Línea %s | producto=%s | categoría=%s | subtotal=%s | qty_invoiced=%s | horas=%s | desplazamiento=%s"
                % (
                    line.id,
                    line.product_id.display_name,
                    category.display_name if category else "Sin categoría",
                    line.price_subtotal,
                    line.qty_invoiced,
                    is_hour_category,
                    is_travel_category,
                )
            )

            if is_hour_category:
                hours_qty += line.qty_invoiced or 0.0
            elif is_travel_category:
                travel_amount += line.price_subtotal or 0.0
            else:
                materials_amount += line.price_subtotal or 0.0

        hour_cost_amount = hours_qty * 45.0
        total_budget_amount = (
            materials_amount
            + travel_amount
            + diets_amount
            + hour_cost_amount
            + subcontracting_amount
        )

        budget_values = {
            "materials_amount": round(materials_amount, 2),
            "travel_amount": round(travel_amount, 2),
            "diets_amount": round(diets_amount, 2),
            "hours_qty": round(hours_qty, 2),
            "hour_cost_amount": round(hour_cost_amount, 2),
            "subcontracting_amount": round(subcontracting_amount, 2),
            "total_budget_amount": round(total_budget_amount, 2),
        }

        print(
            "[uppersolutions_project_report] Pedido %s -> resumen presupuesto: %s"
            % (order.name, budget_values)
        )

        return budget_values

    def _get_report_rows(self):
        self.ensure_one()
        date_start_dt = datetime.combine(self.date_start, time.min)
        date_end_dt = datetime.combine(self.date_end + timedelta(days=1), time.min)
        domain = [
            ("state", "in", ["sale", "done"]),
            ("date_order", ">=", fields.Datetime.to_string(date_start_dt)),
            ("date_order", "<", fields.Datetime.to_string(date_end_dt)),
        ]

        print(
            "[uppersolutions_project_report] _get_report_rows llamado para wizard %s con rango %s -> %s"
            % (self.id, self.date_start, self.date_end)
        )
        print(
            "[uppersolutions_project_report] Dominio de búsqueda de ventas: %s"
            % domain
        )

        sale_orders = self.env["sale.order"].search(domain, order="date_order asc, id asc")

        print(
            "[uppersolutions_project_report] Pedidos encontrados: %s -> %s"
            % (len(sale_orders), sale_orders.mapped("name"))
        )

        rows = []
        trailing_empty_columns = [""] * (len(self.REPORT_COLUMNS) - 13)
        for order in sale_orders:
            project_name = self._get_project_name_from_order(order)
            budget_values = self._get_budget_values_from_order(order)
            row = [
                order.name or order.client_order_ref or "",
                order.partner_id.display_name or "",
                project_name,
                order.date_order.strftime("%d/%m/%Y") if order.date_order else "",
                "",
                "",
                budget_values["materials_amount"],
                budget_values["travel_amount"],
                budget_values["diets_amount"],
                budget_values["hours_qty"],
                budget_values["hour_cost_amount"],
                budget_values["subcontracting_amount"],
                budget_values["total_budget_amount"],
                *trailing_empty_columns,
            ]
            print(
                "[uppersolutions_project_report] Fila construida para pedido %s (%s columnas): %s"
                % (order.name, len(row), row[:13])
            )
            rows.append(row)

        print(
            "[uppersolutions_project_report] Total filas construidas: %s"
            % len(rows)
        )
        return rows

    def _generate_xlsx_content(self):
        self.ensure_one()
        print(
            "[uppersolutions_project_report] Generando XLSX para wizard %s"
            % self.id
        )
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

        report_rows = self._get_report_rows()
        print(
            "[uppersolutions_project_report] Filas obtenidas para el XLSX: %s"
            % len(report_rows)
        )
        if report_rows:
            print(
                "[uppersolutions_project_report] Primera fila del reporte (%s columnas): %s"
                % (len(report_rows[0]), report_rows[0])
            )
        else:
            print(
                "[uppersolutions_project_report] No hay filas para escribir en el XLSX, solo se generarán cabeceras"
            )

        for row_index, row_values in enumerate(report_rows, start=2):
            for col_index, value in enumerate(row_values):
                worksheet.write(row_index, col_index, value or "", cell_format)

        workbook.close()
        output.seek(0)
        content = output.read()
        print(
            "[uppersolutions_project_report] XLSX generado correctamente, tamaño en bytes: %s"
            % len(content)
        )
        return content

    def action_generate_xlsx(self):
        self.ensure_one()
        print(
            "[uppersolutions_project_report] action_generate_xlsx lanzado para wizard %s"
            % self.id
        )
        self._validate_dates()

        file_content = self._generate_xlsx_content()
        file_name = self._get_report_filename()

        self.write({
            "file_data": base64.b64encode(file_content),
            "file_name": file_name,
        })

        print(
            "[uppersolutions_project_report] Archivo listo para descarga: file_name=%s, file_data_informado=%s"
            % (file_name, bool(self.file_data))
        )

        return {
            "type": "ir.actions.act_url",
            "url": (
                "/web/content/?model=%s&id=%s&field=file_data&filename_field=file_name&download=true"
                % (self._name, self.id)
            ),
            "target": "self",
        }


