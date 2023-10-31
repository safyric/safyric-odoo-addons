# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import fields, models
from odoo.exceptions import UserError
import openai

class OdooAiAzure(models.Model):
    _inherit = "odoo.ai"


    service = fields.Selection(
        selection_add = [('azure', 'Azure OpenAI')]
    )

    api_type = fields.Char('API Type')
    api_version = fields.Char('API Version')

    def _connect_api(self):
        res = super(OdooAiAzure, self)._connect_api()
        if self.service == 'azure':
            if not self.api_key:
                raise UserError(_('API Keye is not set, please set!'))
            openai.api_key = self.api_key
            if not self.api_base:
                raise UserError(_('API Base is not set, please set!'))
            openai.api_base = self.api_base
            if not self.api_version:
                raise UserError(_('API Version is not set, please set!'))
            openai.api_version = self.api_version
            api_type = self.api_type
            if not api_type:
                api_type = 'azure'
            openai.api_type = api_type
        return res

    def create_chat_completion(self, model, prompt):
        res = super(OdooAiAzure, self).create_chat_completion(model, prompt)
        if self.service == 'azure':
            if not model:
                raise UserError(_('Deployment ID or Model is required for Azure!'))
            self._connect_api()
            response = openai.ChatCompletion.create(
                deployment_id = model,
                messages = [
                    {"role": "user", "content": prompt}
                ]
            )
            result = response['choices'][0]['message']['content']
            return result
        return res
