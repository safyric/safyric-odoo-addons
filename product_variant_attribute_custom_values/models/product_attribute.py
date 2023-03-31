from odoo import api, fields, models

class ProductAttributeValue(models.Model):
    _name = 'product.variant.attribute.custom.value'
    
    name = fields.Char(string='Value')
    attribute_value_id = fields.Many2one('product.attribute.value', string='Attribute')
    product_id = fields.Many2one('product.product', string='Product Variant')
