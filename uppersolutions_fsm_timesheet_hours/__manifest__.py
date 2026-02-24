# Copyright 2026 UpperSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "FSM Timesheet - Cálculo de Tiempo y Adjuntos",
    "version": "19.0.1.0.0",
    "summary": "Calcula automáticamente el tiempo dedicado (Time Spent) "
    "a partir de los campos Hora Inicio y Hora Fin, y permite adjuntar "
    "archivos en los partes de horas de Servicio de Campo.",
    "author": "Abraham (Xtendoo)",
    "license": "AGPL-3",
    "category": "Field Service",
    "depends": [
        "industry_fsm",
        "hr_timesheet",
        "helpdesk_timesheet",
    ],
    "data": [
        "views/project_task_form_view_uppersolutions_inherit.xml",
        "views/helpdesk_ticket_form.xml",
        #"views/account_analytic_line_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            #"uppersolutions_fsm_timesheet_hours/static/src/scss/fsm_timesheet.scss",
        ],
    },
    "installable": True,
    "auto_install": False,
}
