# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)
import os
import qianfan
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class OdooAiBaidu(models.Model):
    _inherit = "odoo.ai"


    service = fields.Selection(
        selection_add = [('baidu', 'Baidu ERNIE')]
    )

    access_key = fields.Char('Access Key')
    secret_key = fields.Char('Secret Key')

    def _connect_api(self):
        res = super(OdooAiBaidu, self)._connect_api()
        if self.service == 'baidu':
            if not self.access_key:
                raise UserError(_('Access Key is not set, please set!'))
            os.environ["QIANFAN_ACCESS_KEY"] = self.access_key
            if not self.secret_key:
                raise UserError(_('Secret Key is not set, please set!'))
            os.environ["QIANFAN_SECRET_KEY"] = self.secret_key
        return res

    def create_chat_completion(self, model, prompt):
        res = super(OdooAiBaidu, self).create_chat_completion(model, prompt)
        if self.service == 'baidu':
            if not model:
                raise UserError(_('Model is required for Baidu ERNIE!'))
            self._connect_api()
            chat_comp = qianfan.ChatCompletion(model=model)
            response = chat_comp.do(
                messages = [
                    {"role": "user", "content": prompt}
                ]
            )
            result = response['result']
            return result
        return res

