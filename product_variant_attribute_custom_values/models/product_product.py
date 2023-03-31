from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    attribute_custom_value_ids = fields.One2many('product.variant.attribute.custom.value', 'product_id', string='Attribute Custom Values')
