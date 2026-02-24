{
    "name": "UpperSolutions Sale Route",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Adds a Route field to the Sale Order header and propagates it to all order lines.",
    "description": "This module allows setting a global route for the entire Sales Order, which will automatically update the route for all lines within it.",
    "author": "Abraham (Xtendoo)",
    "depends": ["sale_stock"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
