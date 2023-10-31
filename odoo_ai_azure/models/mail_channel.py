# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import models, _


class MailChannel(models.Model):
    _inherit = 'mail.channel'

    def execute_command_clear_ai_chat(self, **kwargs):
        super(MailChannel, self).execute_command_clear_ai_chat(**kwargs)
        partner = self.env.user.partner_id
        key = kwargs['body']
        if key.lower().strip() == '/clear':
            ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id('odoo_ai_azure.partner_ai')
            ai_chat_member_ids = {ai_bot_id, partner.id}
            if ai_chat_member_ids == set(self.channel_member_ids.mapped('partner_id.id')):
                self.env['bus.bus'].sendone(self.env.user.partner_id, 'mail.message/delete',
                                             {'message_ids': self.message_ids.ids})
                self.message_ids.unlink()
