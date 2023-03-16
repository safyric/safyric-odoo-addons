from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    barcode = fields.Char(related='product_id.barcode', string="Barcode", store=True)
