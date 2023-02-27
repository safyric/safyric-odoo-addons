# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    signature = fields.Binary(
        string='Signature',
        attachment=True)

    sign_date = fields.Datetime('Date')

    @api.model
    def create(self, values):
        picking = super(Picking, self).create(values)
        if picking.signature:
            values = {'signature': picking.signature}
            picking._track_signature(values, 'signature')
        return picking

    @api.one
    def write(self, values):
        if self.signature:
            self._track_signature(values, 'signature')
            values['sign_date'] = fields.Datetime.now()
        return super(Picking, self).write(values)
