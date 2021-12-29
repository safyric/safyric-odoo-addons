{
    'name': 'Delivery Product Weight',
    'summary': 'Add weight manually in picking line.',
    'author': 'Safyric Co., Ltd.',
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'license': 'AGPL-3',
    'category': 'Delivery',
    'version': '12.0.1.0.0',
    'depends': [
        'stock',
        'delivery',
    ],
    'data': [
        'views/delivery_view.xml',
        'views/stock_picking.xml',
        'views/product_packaging.xml',
        'report/report_deliveryslip.xml'
    ],
}
