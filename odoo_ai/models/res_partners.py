# -*- coding: utf-8 -*-
# Copyright (C) 2023 - Myrrkel (https://github.com/myrrkel).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _compute_im_status(self):
        super(ResPartner, self)._compute_im_status()
        ai_bot_partner_id = self.env['ir.model.data'].xmlid_to_res_id('odoo_ai.partner_ai')
        for partner in self.filtered(lambda p: p.id == ai_bot_partner_id):
            partner.im_status = 'online'
