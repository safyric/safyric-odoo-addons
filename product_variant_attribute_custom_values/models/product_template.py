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

    
    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if vals.get('attribute_line_ids'):
            for attribute_line in vals['attribute_line_ids']:
                for value in attribute_line[2]['value_ids']:
                    if value[2].get('custom_value'):
                        self.env['product.variant.attribute.custom.value'].create({
                            'product_id': res.product_variant_id.id,
                            'name': value[2]['custom_value'],
                            'attribute_value_id': value[2]['id'],
                        })
        return res
    
    
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if vals.get('attribute_line_ids'):
            for template in self:
                for attribute_line in vals['attribute_line_ids']:
                    for value in attribute_line[2]['value_ids']:
                        if value[2].get('custom_value'):
                            existing_custom_value = template.product_variant_id.attribute_custom_value_ids.filtered(lambda r: r.attribute_value_id == value[2]['id'])
                            if existing_custom_value:
                                existing_custom_value.write({'name': value[2]['custom_value']})
                            else:
                                self.env['product.variant.attribute.custom.value'].create({
                                    'product_id': template.product_variant_id.id,
                                    'name': value[2]['custom_value'],
                                    'attribute_value_id': value[2]['id'],
                                })
        return res
