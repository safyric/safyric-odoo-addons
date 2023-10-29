# -*- coding: utf-8 -*-
# Copyright (C) 2023 - Myrrkel (https://github.com/myrrkel).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import requests
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _check_url(self, url):
        try:
            get = requests.get(url, timeout=1)
            if get.status_code:
                return True
            else:
                return False
        except Exception as e:
            return False


    def _compute_im_status(self):
        super(ResPartner, self)._compute_im_status()
        ai_bot_user_id = self.env['ir.model.data'].xmlid_to_res_id('openai_integration.partner_ai')
        url = self.env['ir.config_parameter'].sudo().get_param('openai_integration.openai_api_base')
        if url:
            status = self._check_url(url)
        if status:
            for user in self.filtered(lambda u: u.id == ai_bot_user_id):
                user.im_status = 'online'
