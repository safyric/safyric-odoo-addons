# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Line Sequence Extension",
    "summary": "Propagates SO line sequence to invoices and stock picking.",
    "version": "12.0.1.0.0",
    "author": "Safyric Co., Ltd.",
    "category": "Sales",
    "website": "https://github.com/safyric/safyric-odoo-addons",
    "license": "AGPL-3",
    'data': [
        'views/report_saleorder.xml'
    ],
    "depends": [
        "sale_order_line_sequence",
        "purchase_order_line_sequence_extension",
    ],
    "installable": True,
}
