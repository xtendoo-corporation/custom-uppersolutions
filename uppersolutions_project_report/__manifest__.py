{
    "name": "UpperSolutions Project Report",
    "version": "19.0.1.0.0",
    "category": "Sales/Reporting",
    "summary": "Wizard para exportar el reporte de proyectos a Excel desde Ventas.",
    "author": "UpperSolutions",
    "website": "https://www.uppersolutions.com",
    "license": "LGPL-3",
    "external_dependencies": {
        "python": ["xlsxwriter"],
    },
    "depends": [
        "account",
        "hr_timesheet",
        "product",
        "sale_timesheet",
        "sale_management",
        "project",
        "sale_project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_invoice_report_views.xml",
        "views/product_category_views.xml",
        "views/project_report_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}


