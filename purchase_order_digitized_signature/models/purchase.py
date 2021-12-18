# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    seller_signature = fields.Binary(
        string='Seller acceptance',
        attachment=True)

    buyer_signature = fields.Binary(
        string='Buyer signature',
        attachment=True)
    
    @api.model
    def create(self, values):
        purchase = super(PurchaseOrder, self).create(values)
        if purchase.seller_signature:
            values = {'seller_signature': purchase.seller_signature}
            purchase._track_signature(values, 'seller_signature')
        if purchase.buyer_signature:
            values = {'buyer_signature': purchase.buyer_signature}
            purchase._track_signature(values, 'buyer_signature')
        return purchase

    @api.multi
    def write(self, values):
        if self.seller_signature:
            self._track_signature(values, 'seller_signature')
        if self.buyer_signature:
            self._track_signature(values, 'buyer_signature')
        return super(PurchaseOrder, self).write(values)
