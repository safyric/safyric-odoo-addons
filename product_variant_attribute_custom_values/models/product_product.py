from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    attribute_custom_value_ids = fields.One2many('product.variant.attribute.custom.value', 'product_id', string='Attribute Custom Values')

    
    @api.model
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        if vals.get('attribute_custom_value_ids'):
            self.env['product.variant.attribute.custom.value'].create({
                'product_id': res.id,
                'name': vals['name'],
                'attribute_id': vals['attribute_custom_value_ids']['attribute_id'],
            })
        return res

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if vals.get('attribute_custom_value_ids'):
            for product in self:
                existing_values = product.attribute_custom_value_ids.filtered(lambda r: r.attribute_id == vals['attribute_custom_value_ids']['attribute_id'])
                if existing_values:
                    existing_values.write({'name': vals['name']})
                else:
                    self.env['product.variant.attribute.custom.value'].create({
                        'product_id': product.id,
                        'name': vals['name'],
                        'attribute_id': vals['attribute_custom_value_ids']['attribute_id'],
                    })
        return res
