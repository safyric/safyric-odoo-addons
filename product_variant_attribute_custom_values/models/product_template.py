from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        product_template = super(ProductTemplate, self).create(vals)

        # create product variant attribute custom value records for each variant with custom values
        for variant in product_template.product_variant_ids.filtered(lambda v: v.custom_value_ids):
            for custom_value in variant.custom_value_ids:
                self.env['product.variant.attribute.custom.value'].create({
                    'name': custom_value.name,
                    'attribute_value_id': custom_value.attribute_value_id.id,
                    'product_id': variant.id,
                })

        return product_template

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)

        # update product variant attribute custom value records for each variant with custom values
        for variant in self.product_variant_ids.filtered(lambda v: v.custom_value_ids):
            variant_custom_values = self.env['product.variant.attribute.custom.value'].search([
                ('product_id', '=', variant.id)
            ])

            for custom_value in variant.custom_value_ids:
                custom_value_record = variant_custom_values.filtered(lambda cv: cv.attribute_value_id == custom_value.attribute_value_id)
                if custom_value_record:
                    custom_value_record.write({
                        'name': custom_value.name,
                    })
                else:
                    self.env['product.variant.attribute.custom.value'].create({
                        'name': custom_value.name,
                        'attribute_value_id': custom_value.attribute_value_id.id,
                        'product_id': variant.id,
                    })

            # delete any product variant attribute custom value records that don't have a corresponding custom value
            variant_custom_values.filtered(lambda cv: not cv.attribute_value_id in variant.custom_value_ids.mapped('attribute_value_id')).unlink()

        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    custom_value_ids = fields.One2many('product.variant.attribute.custom.value', 'product_id', string='Custom Values')


