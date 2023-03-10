# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def write(self, values):
        if self.sale_line_id:
            for line in self:
                line.sale_line_id.price_unit = self.purchase_price
        return super(PurchaseOrderLine, self).write(values)
