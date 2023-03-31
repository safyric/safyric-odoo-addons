from odoo import api, fields, models

class ProductAttributeValue(models.Model):
    _name = 'product.attribute.custom.value'
    
    name = fields.Char(string='Value')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    product_id = fields.Many2one('product.product', string='Product Variant')
