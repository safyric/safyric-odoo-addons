# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    signature = fields.Binary(
        string='Signature',
        attachment=True)

    sign_date = fields.Datetime('Date')

    @api.model
    def create(self, values):
        invoice = super(AccountInvoice, self).create(values)
        if invoice.signature:
            values = {'signature': invoice.signature}
            invoice._track_signature(values, 'signature')
        return invoice

    @api.one
    def write(self, values):
        if self.signature:
            self._track_signature(values, 'signature')
            values['sign_date'] = fields.Datetime.now()
        return super(AccountInvoice, self).write(values)
