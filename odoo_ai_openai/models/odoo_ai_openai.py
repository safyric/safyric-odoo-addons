# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import fields, models


class OdooAiOpenai(models.Model):
    _inherit = "odoo.ai"


    service = fields.Selection(
        selection_add = [('openai', 'OpenAI')]
    )
