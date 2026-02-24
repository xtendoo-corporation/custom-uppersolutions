{
    'name': 'UpperSolutions Chatter Customization',
    'version': '19.0.1.0.0',
    'category': 'Discuss',
    'summary': 'Clears default followers from the chatter recipients list.',
    'description': 'This module patches the RecipientsInput component in the mail app to start with an empty recipients list by default when opening the composer.',
    'author': 'Abraham (Xtendoo)',
    'depends': ['mail'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'uppersolutions_chatter_customization/static/src/recipients_input_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
