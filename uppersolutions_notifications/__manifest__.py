{
    "name": "UpperSolutions Notifications",
    "version": "19.0.1.0.0",
    "category": "Hidden",
    "summary": "Removes the 'Install Odoo' and 'Turn on notifications' prompts from the messaging menu.",
    "author": "Abraham (Xtendoo)",
    "website": "https://www.uppersolutions.com",
    "license": "AGPL-3",
    "depends": [
        "mail",
    ],
    "assets": {
        "web.assets_backend": [
            "uppersolutions_notifications/static/src/messaging_menu_patch.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
