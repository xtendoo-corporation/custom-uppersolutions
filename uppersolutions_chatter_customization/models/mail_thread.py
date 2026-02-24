# -*- coding: utf-8 -*-
from odoo import models, api

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def message_post(self, **kwargs):
        """
        Intercept message_post from the chatter.
        If the 'chatter_empty_recipients' context flag is set (meaning the user explicitly 
        left the recipients input empty in the UI), we skip notifying followers.
        """
        if self.env.context.get('chatter_empty_recipients'):
            kwargs['notify_skip_followers'] = True
            
        return super(MailThread, self).message_post(**kwargs)
