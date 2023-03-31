from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    variant_attribute_custom_values = fields.One2many('product.variant.attribute.custom.value', compute='_compute_variant_attribute_custom_values', string='Variant Attribute Custom Values')
    
    @api.depends('product_variant_ids.attribute_custom_value_ids')
    def _compute_variant_attribute_custom_values(self):
        for template in self:
            template.variant_attribute_custom_values = self.env['product.variant.attribute.custom.value']
            for variant in template.product_variant_ids:
                template.variant_attribute_custom_values |= variant.attribute_custom_value_ids

