# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('price_unit')
    def onchange_price_unit(self):
        if self.sale_line_id:
            for so in self:
                so.sale_line_id.price_unit = self.purchase_price
            
