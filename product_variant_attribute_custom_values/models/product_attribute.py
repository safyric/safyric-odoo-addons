from odoo import api, fields, models

class ProductVariantAttributeCustomValue(models.Model):
    _name = 'product.variant.attribute.custom.value'
    _description = 'Product Variant Attribute Custom Value'

    name = fields.Char(string='Value')
    attribute_value_id = fields.Many2one('product.attribute.value', string='Attribute Value', required=True)
    product_id = fields.Many2one('product.product', string='Product Variant', required=True)
