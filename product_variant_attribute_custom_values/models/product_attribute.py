from odoo import api, fields, models

class ProductAttributeValue(models.Model):
    _name = 'product.variant.attribute.custom.value'
    _description = 'Product Variant Attribute Custom Value'
    
    name = fields.Char(string='Value')
    attribute_value_id = fields.Many2one('product.attribute.value', string='Attribute Value')
    product_id = fields.Many2one('product.product', string='Product Variant')

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    
    variant_custom_value_ids = fields.One2many('product.variant.attribute.custom.value', 'attribute_value_id', string='Variant Attribute Custom Values')
