# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale order line description",
    "version": "12.0.1.0.0",
    "category": "Sales Management",
    "author": "Safyric Co., Ltd.",
    "website": "https://github.com/OCA/sale-workflow/",
    "license": "AGPL-3",
    "depends": [
        "sale",
        "product",
        "stock",
    ],
    "data": [
        'views/product_attribute_view.xml',
        'views/sale_views.xml',
    ],
    "installable": True,
}
