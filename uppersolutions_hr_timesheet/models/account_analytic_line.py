from odoo import models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def action_open_task(self):
        self.ensure_one()
        if self.task_id:
            return {
                'name': 'Task',
                'type': 'ir.actions.act_window',
                'res_model': 'project.task',
                'res_id': self.task_id.id,
                'view_mode': 'form',
                'target': 'current',
            }
