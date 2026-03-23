from odoo import models
from odoo.fields import Domain
from odoo.tools.misc import unquote

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def _domain_sale_line_id(self):
        domain = super()._domain_sale_line_id()
        # Add constraint to only allow elements of the sales order corresponding to that project
        # In JS `sale_order_id` will have the ticket's sale_order_id, which is computed from project_id.sale_order_id
        domain = Domain.AND([
            domain,
            [('order_id', '=', unquote('sale_order_id'))]
        ])
        return domain
