from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def product_id_change(self):
        super(SaleOrderLine, self).product_id_change()

        if self.product_id:
            # create custom value records for product variant if they don't exist
            if self.product_id.product_tmpl_id.attribute_line_ids:
                for line in self.product_id.product_tmpl_id.attribute_line_ids:
                    attribute_value = self.product_id.attribute_value_ids.filtered(lambda v: v.attribute_id == line.attribute_id)
                    if attribute_value and attribute_value.custom_value:
                        if not self.product_id.custom_value_ids.filtered(lambda cv: cv.attribute_value_id == attribute_value.id):
                            self.product_id.custom_value_ids.create({
                                'name': attribute_value.custom_value,
                                'attribute_value_id': attribute_value.id,
                                'product_id': self.product_id.id,
                            })
