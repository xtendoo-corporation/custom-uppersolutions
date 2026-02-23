# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "FSM Timesheet - Cálculo de Tiempo y Adjuntos",
    "version": "19.0.1.0.0",
    "summary": "Calcula automáticamente el tiempo dedicado (Time Spent) "
    "a partir de los campos Hora Inicio y Hora Fin, y permite adjuntar "
    "archivos en los partes de horas de Servicio de Campo.",
    "author": "UpperSolutions",
    "license": "AGPL-3",
    "category": "Field Service",
    "depends": [
        "industry_fsm",
        "hr_timesheet",
    ],
    "data": [
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
