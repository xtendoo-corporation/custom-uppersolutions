{
    "name": "UpperSolutions No Odoo Brand",
    "version": "19.0.1.0.0",
    "category": "Reporting",
    "summary": "Removes the 'Connect your software' Odoo brand from Sale and Purchase reports.",
    "author": "Abraham (Xtendoo)",
    "website": "https://www.uppersolutions.com",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "purchase",
    ],
    "data": [
        "views/sale_report_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
