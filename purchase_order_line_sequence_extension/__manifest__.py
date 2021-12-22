{
    'name': 'Purchase Order Line Sequence Extension',
    'summary': 'Adds sequence to PO lines and propagates it to'
               'Invoice lines and Stock Moves',
    'version': '12.0.1.0.0',
    'category': 'Purchase Management',
    'author': "Safyric Co., Ltd.",
    'website': 'https://github.com/safyric/safyric-odoo-addons',
    'depends': [
        'purchase_order_line_sequence',
    ],
    'data': [
      'views/report_purchaseorder.xml',
      'views/report_purchasequotation.xml',
      'views/purchase_order_view.xml',
    ],
    'installable': True,
    'license': "AGPL-3",
}
