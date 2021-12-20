# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sequence = fields.Integer(help="Shows the sequence of this line in the "
                              " invoice.", default=1,
                              string="original sequence")

    # shows sequence on the invoice line
    sequence2 = fields.Integer(help="Shows the sequence of this line in the "
                               " invoice.", related='sequence',
                               string="Line #", store=True)
