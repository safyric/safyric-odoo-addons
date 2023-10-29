# -*- coding: utf-8 -*-
# Copyright (c) 2020-Present InTechual Solutions. (<https://intechualsolutions.com/>)

{
    'name': 'OpenAI Integration',
    'version': '12.0.1.0.1',
    'license': 'AGPL-3',
    'summary': 'Odoo OpenAI Integration',
    'description': 'Allows the application to leverage the capabilities of the GPT language model to generate human-like responses, providing a more natural and intuitive user experience',
    'author': 'Safyric Valve Co., Ltd.',
    'website': 'https://github.com/safyric-odoo-addons',
    'depends': [
	'base',
	'base_setup',
	'mail'],
    'data': [
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {
	'python': [
	    'openai'
	]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
