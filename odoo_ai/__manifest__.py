# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

{
    'name': 'Odoo AI',
    'version': '12.0.0.0.1',
    'license': 'AGPL-3',
    'summary': 'Odoo AI',
    'description': 'Allows the application to leverage the capabilities of the GPT language model to generate human-like responses, providing a more natural and intuitive user experience',
    'author': 'Safyric Valve Co., Ltd.',
    'website': 'https://github.com/safyric-odoo-addons',
    'depends': [
	'base',
	'mail',
	'base_setup',
    ],
    'data': [
	'data/user_partner_data.xml',
	'security/ir.model.access.csv',
	'security/odoo_ai.xml',
	'views/odoo_ai_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
