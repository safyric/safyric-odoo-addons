# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons import decimal_precision as dp

class SaleVendorPricelist(models.Model):
    _name = "sale.vendor.pricelist"
    _description = "Vendor Pricelist"

    name = fields.Char('Model Number', required=True, index=True)
    date = fields.Date('Date')
    quantity = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'), default=1)
    unit_price = fields.Float("Unit Price", digits=dp.get_precision('Product Price'))
    manufacturer = fields.Char('Manufacturer')
    description = fields.Text('Description')
    notes = fields.Text('Notes')
