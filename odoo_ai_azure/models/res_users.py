import requests
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _init_messaging(self):
        if self.sel_groups_1_9_10 == 1:
            self._init_ai_bot()
        return super(ResUsers, self)._init_messaging()

    def _init_ai_azure_bot(self):
        self.ensure_one()
        ai_bot_partner_id = self.env['ir.model.data'].xmlid_to_res_id('odoo_ai_azure.partner_ai')
        channel_info = self.env['mail.channel'].channel_get([ai_bot_partner_id, self.partner_id.id])
        channel = self.env['mail.channel'].browse(channel_info['id'])
        return channel


    def _compute_im_status(self):
        super(ResUsers, self)._compute_im_status()
        service = self.env['odoo.ai'].sudo().search([('service', '=', 'azure')], limit=1)
        ai_bot_user_id = self.env['ir.model.data'].xmlid_to_res_id('odoo_ai_azure.user_ai')
        for user in self.filtered(lambda u: u.id == ai_bot_user_id):
            user.im_status = 'online'
