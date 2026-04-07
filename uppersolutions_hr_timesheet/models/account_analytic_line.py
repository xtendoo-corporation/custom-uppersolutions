from odoo import api, fields, models

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    display_helpdesk_ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Ticket',
        compute='_compute_display_helpdesk_ticket_id',
        readonly=True,
    )
    display_ticket_date = fields.Date(
        string='Fecha',
        compute='_compute_display_ticket_date',
        readonly=True,
    )

    @api.depends('helpdesk_ticket_id', 'task_id', 'task_id.helpdesk_ticket_id')
    def _compute_display_helpdesk_ticket_id(self):
        for line in self:
            line.display_helpdesk_ticket_id = line.helpdesk_ticket_id or line.task_id.helpdesk_ticket_id

    @api.depends(
        'date',
        'helpdesk_ticket_id.estimated_date',
        'task_id.helpdesk_ticket_id.estimated_date',
    )
    def _compute_display_ticket_date(self):
        for line in self:
            ticket = line.helpdesk_ticket_id or line.task_id.helpdesk_ticket_id
            line.display_ticket_date = ticket.estimated_date or line.date

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
