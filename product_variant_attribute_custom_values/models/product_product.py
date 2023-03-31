from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    attribute_custom_value_ids = fields.One2many('product.attribute.custom.value', 'product_id', string='Attribute Custom Values')

    
    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        if vals.get('attribute_custom_value_ids'):
            self.env['product.attribute.custom.value'].create({
                'product_id': res.id,
                'name': vals['name'],
                'attribute_id': vals['attribute_custom_value_ids']['attribute_id'],
            })
        return res
