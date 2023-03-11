from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    @api.depends('product_id', 'purchase_price', 'product_uom_qty', 'price_unit', 'price_subtotal')
    def _product_margin(self):
        for line in self:
            currency = line.order_id.pricelist_id.currency_id
            currency_rate = line.order_id.currency_rate
            price = line.purchase_price * currency_rate
            line.margin = currency.round(line.price_subtotal - (price * line.product_uom_qty))
