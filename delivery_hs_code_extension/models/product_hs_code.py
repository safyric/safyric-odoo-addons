from odoo import api, fields, models


class ProductHsCode(models.Model):
    _name = 'product.hs.code'
    _description = "Product HS Code"
    _order = 'name'

    name = fields.Char('HS Code', required=True)
    commodity_name = fields.Char('Commodity Name', translate=True)
    commodity_description = fields.Char('Commodity Description', translate=True)
    description = fields.Text(translate=True)
    commodity_usage = fields.Char('Commodity Usage', translate=True)
    primary_uom = fields.Many2one('uom.uom', string='Primary UOM')
    secondary_uom = fields.Many2one('uom.uom', string='Secondary UOM')
    duty = fields.Float(string='Duty (%)', digits=(16, 2))
    rebate = fields.Float(string="Rebate (%)", digits=(16, 2))
    inspection_cat = fields.Char('Inspection Category')
    gtin = fields.Char('GTIN')
    cas = fields.Char('CAS')
    parameter1 = fields.Char('Parameter 1')
    parameter2 = fields.Char('Parameter 2')
    parameter3 = fields.Char('Parameter 3')
    parameter4 = fields.Char('Parameter 4')
