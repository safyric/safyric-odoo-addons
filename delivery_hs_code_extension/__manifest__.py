# Copyright 2009 NetAndCo (<http://www.netandco.net>).
# Copyright 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# Copyright 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# Copyright 2016 Serpent Consulting Services Pvt. Ltd.
# Copyright 2018 Daniel Campos <danielcampos@avanzosc.es>
# Copyright 2018 Tecnativa - David Vidal
# Copyright 2019 Giovanni - GSLabIt
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Delivery HS Code Extension',
    'version': '12.0.2.0.1',
    'development_status': "Mature",
    'category': 'Product',
    'summary': "Delivery HS Code Extension",
    'author': 'Safyric Valve Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'license': 'AGPL-3',
    'depends': [
        'delivery_hs_code',
	'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_hs_code.xml',
	'views/product_brand.xml',
	'reports/report_customs_declaration.xml',
    ],
    'installable': True
}
