# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    openai_api_key = fields.Char(string="API Key", help="Provide the API key here", config_parameter="openai_integration.openai_api_key")
    openai_api_base = fields.Char(string="API Base", help="Provide the API base", config_parameter="openai_integration.openai_api_base")
