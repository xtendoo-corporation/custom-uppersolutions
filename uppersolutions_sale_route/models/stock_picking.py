from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    next_picking_id = fields.Many2one(
        'stock.picking',
        compute='_compute_chain_picking_ids',
        string='Siguiente Traslado',
    )
    prev_picking_id = fields.Many2one(
        'stock.picking',
        compute='_compute_chain_picking_ids',
        string='Traslado Anterior',
    )
    has_next_picking = fields.Boolean(
        compute='_compute_chain_picking_ids',
    )
    has_prev_picking = fields.Boolean(
        compute='_compute_chain_picking_ids',
    )

    @api.depends(
        'origin', 'location_id', 'location_dest_id',
        'move_ids.move_dest_ids.picking_id',
        'move_ids.move_orig_ids.picking_id',
    )
    def _compute_chain_picking_ids(self):
        for picking in self:
            next_picking = self.env['stock.picking']
            prev_picking = self.env['stock.picking']

            # Strategy 1: move chaining (works with make_to_order)
            next_from_moves = picking.move_ids.mapped('move_dest_ids.picking_id').filtered(
                lambda p: p.id != picking.id
            )
            prev_from_moves = picking.move_ids.mapped('move_orig_ids.picking_id').filtered(
                lambda p: p.id != picking.id
            )
            if next_from_moves:
                next_picking = next_from_moves[:1]
            if prev_from_moves:
                prev_picking = prev_from_moves[:1]

            # Strategy 2: location chain with same origin
            if not next_picking and not prev_picking and picking.origin:
                siblings = self.search([
                    ('origin', '=', picking.origin),
                    ('id', '!=', picking.id),
                ])
                # Next: sibling whose source location == current destination location
                for sib in siblings:
                    if sib.location_id == picking.location_dest_id:
                        next_picking = sib
                        break
                # Prev: sibling whose destination location == current source location
                for sib in siblings:
                    if sib.location_dest_id == picking.location_id:
                        prev_picking = sib
                        break

            picking.next_picking_id = next_picking
            picking.prev_picking_id = prev_picking
            picking.has_next_picking = bool(next_picking)
            picking.has_prev_picking = bool(prev_picking)

    def action_view_next_picking(self):
        self.ensure_one()
        if self.next_picking_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'res_id': self.next_picking_id.id,
                'view_mode': 'form',
                'views': [(self.env.ref('stock.view_picking_form').id, 'form')],
            }

    def action_view_prev_picking(self):
        self.ensure_one()
        if self.prev_picking_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'res_id': self.prev_picking_id.id,
                'view_mode': 'form',
                'views': [(self.env.ref('stock.view_picking_form').id, 'form')],
            }
