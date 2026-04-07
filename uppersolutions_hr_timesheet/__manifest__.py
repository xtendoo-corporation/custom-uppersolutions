{
    'name': 'Uppersolutions HR Timesheet',
    'version': '19.0.1.0.0',
    'description': 'Makes task viewable from timesheet list',
    'author': 'Uppersolutions',
    'depends': ['hr_timesheet', 'helpdesk', 'helpdesk_sale_timesheet', 'helpdesk_fsm'],
    'data': [
        'views/hr_timesheet_views.xml',
        'views/helpdesk_ticket_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
