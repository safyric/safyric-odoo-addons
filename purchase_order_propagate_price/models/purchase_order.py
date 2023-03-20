# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def write(self, values):
        for line in self:
            if line.sale_line_id:
                price_untaxed = self.price_unit - self.price_tax
                line.sale_line_id.purchase_price = price_untaxed
                line.product_id.standard_price = price_untaxed
        return super(PurchaseOrderLine, self).write(values)
