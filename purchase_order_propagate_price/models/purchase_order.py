# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def write(self, values):
        for line in self:
            price_untaxed = 0.0
            if line.product_qty > 0 and line.price_unit > 0:
                price_untaxed = line.price_subtotal / line.product_qty
                line.product_id.standard_price = price_untaxed
            if line.sale_line_id:
                line.sale_line_id.purchase_price = price_untaxed
        return super(PurchaseOrderLine, self).write(values)
