from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    # re-defines the field to change the default
    sequence = fields.Integer('HiddenSequence',
                              default=1)

    # displays sequence on the stock moves
    sequence2 = fields.Integer('Line #',
                               help="Shows the sequence in the Stock Move.",
                               related='sequence', readonly=True, store=True)
