from odoo import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _message_post_after_hook(self, message, values, model_description=False, mail_auto_delete=True):
        self.env['odoo.ai.bot']._apply_logic(self, values)
        return super(MailThread, self)._message_post_after_hook(message, values, model_description=model_description, mail_auto_delete=mail_auto_delete)
