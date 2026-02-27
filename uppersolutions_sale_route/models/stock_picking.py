from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    related_picking_ids = fields.Many2many(
        'stock.picking',
        'stock_picking_related_rel',
        'picking_id',
        'related_picking_id',
        compute='_compute_related_picking_ids',
        string='Traslados Relacionados',
    )
    related_picking_count = fields.Integer(
        compute='_compute_related_picking_ids',
        string='Traslados Relacionados',
    )

    @api.depends('origin', 'move_ids.move_dest_ids.picking_id', 'move_ids.move_orig_ids.picking_id')
    def _compute_related_picking_ids(self):
        for picking in self:
            # Strategy 1: Use move chaining (move_dest_ids + move_orig_ids)
            related = picking.move_ids.mapped('move_dest_ids.picking_id')
            related |= picking.move_ids.mapped('move_orig_ids.picking_id')
            related = related.filtered(lambda p: p.id != picking.id)

            # Strategy 2: Fallback using origin (same sale order)
            if not related and picking.origin:
                related = self.search([
                    ('origin', '=', picking.origin),
                    ('id', '!=', picking.id),
                ])

            picking.related_picking_ids = related
            picking.related_picking_count = len(related)

    def action_view_related_pickings(self):
        self.ensure_one()
        pickings = self.related_picking_ids
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = pickings.id
        else:
            action['domain'] = [('id', '=', False)]
        return action
