# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def write(self, values):
        if self.sale_line_id:
            for line in self:
                price_untaxed = self.price_unit - self.price_tax
                line.sale_line_id.purchase_price = price_untaxed
                line.product_id.standard_price = price_untaxed
        return super(PurchaseOrderLine, self).write(values)
