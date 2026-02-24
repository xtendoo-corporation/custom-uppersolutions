from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    route_id = fields.Many2one(
        'stock.route',
        string='Ruta',
        domain=[('sale_selectable', '=', True)],
        ondelete='restrict',
        help="The route chosen here will be applied to all order lines."
    )

    @api.onchange('route_id')
    def _onchange_route_id(self):
        for order in self:
            if order.route_id:
                for line in order.order_line:
                    line.route_ids = [(6, 0, [order.route_id.id])]
            else:
                for line in order.order_line:
                    line.route_ids = [(5, 0, 0)]
