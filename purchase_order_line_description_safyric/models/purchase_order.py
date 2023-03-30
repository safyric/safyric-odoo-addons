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
        product = self.product_id

        if product and product.description_purchase:
            return product.display_name + "\n" + self._get_purchase_order_line_multiline_description_variants().strip(', ') + product.description_purchase
        elif product:
            return product.display_name + "\n" + self._get_purchase_order_line_multiline_description_variants().strip(', ')


    def _get_purchase_order_line_multiline_description_variants(self):
        name = ""
        product_attribute_with_is_custom = []
        product_attribute_custom_ids = []
        
        if self.sale_line_id:
            product_attribute_with_is_custom += self.sale_line_id.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')
            product_attribute_custom_ids += self.sale_line_id.product_custom_attribute_value_ids.with_context(lang=self.order_id.partner_id.lang or self.env.lang)

        # attribute_value_with_variants
        for pav in self.product_id.attribute_value_ids.with_context(lang=self.order_id.partner_id.lang or self.env.lang).filtered(
            lambda pav: pav.attribute_id not in product_attribute_with_is_custom and pav.code and pav.code != "0" and pav.code !="00" and pav.code !="000"
        ):
            attribute_id = pav.attribute_id.with_context(lang=self.order_id.partner_id.lang or self.env.lang)
            name += attribute_id.name + ': ' + pav.name + "\n"
            
        # attribute_value is_custom
        if product_attribute_custom_ids:
            for pac in product_attribute_custom_ids:
                name += pac.attribute_value_id.attribute_id.name + ': ' + pac.custom_value + "\n"

        return name
    
    @api.onchange('sale_line_id')
    def onchange_sale_line_id(self):
        line = self.new({
            'product_id': self.product_id,
            'sale_line_id': self.sale_line_id,
            'order_id': self.order_id
        })
        line.onchange_product_id()
        self.name = line.name
    
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    @api.multi
    def recalculate_names(self):
        for line in self.mapped('order_line').filtered('product_id'):
            # we make this to isolate changed values:
            line2 = self.env['purchase.order.line'].new({
                'product_id': line.product_id,
                'sale_line_id': line.sale_line_id,
                'order_id': line.order_id
            })
            line2.onchange_product_id()
            line.name = line2.name
