from odoo import api, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"


    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(PurchaseOrderLine, self).onchange_product_id()
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang
        )

        self.name = self.get_purchase_order_line_multiline_description_purchase(product)

        return res

    def get_purchase_order_line_multiline_description_purchase(self, product):
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang
        )

        if product and product.description_purchase:
            return product.display_name + "\n" + self._get_purchase_order_line_multiline_description_variants().strip(', ') + product.description_purchase
        elif product:
            return product.display_name + "\n" + self._get_purchase_order_line_multiline_description_variants().strip(', ')


    def _get_purchase_order_line_multiline_description_variants(self):
        name = ""

        # attribute_value_with_variants
        for pav in self.product_id.attribute_value_ids.with_context(lang=self.order_id.partner_id.lang or self.env.lang):
            attribute_id = pav.attribute_id.with_context(lang=self.order_id.partner_id.lang or self.env.lang)
            name += attribute_id.name + ': ' + pav.name + "\n"

        return name
    
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.multi
    def recalculate_names(self):
        for line in self.mapped('order_line').filtered('product_id'):
            # we make this to isolate changed values:
            line2 = self.env['purchase.order.line'].new({
                'product_id': line.product_id,
            })
            line2.onchange_product_id()
            line.name = line2.name
        return True
