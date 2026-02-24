from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _process_auto_invoice(self, invoice):
        """
        Override to prevent automatic posting of recurring invoices.
        By default, Odoo calls invoice.action_post() here. 
        We simply return to leave the invoice in a draft state.
        """
        return
