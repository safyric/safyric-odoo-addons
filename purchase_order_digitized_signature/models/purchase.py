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

    seller_sign_date = fields.Datetime('Date')
    buyer_sign_date = fields.Datetime('Date')

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
            self.seller_sign_date(values, fields.Datetime.now())
        if self.buyer_signature:
            self._track_signature(values, 'buyer_signature')
            self.buyer_sign_date(values, fields.Datetime.now())
        return super(PurchaseOrder, self).write(values)
