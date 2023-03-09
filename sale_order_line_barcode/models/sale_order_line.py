from odoo import api, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    barcode = fields.Char(related='product_id.barcode', string="Barcode", store=True)
