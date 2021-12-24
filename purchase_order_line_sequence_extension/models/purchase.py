from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sequence = fields.Integer('Hidden Sequence',
                          help="Gives the sequence of the line when "
                               "displaying the purchase order.",
                          default=1)

    sequence2 = fields.Integer('Line #',
                               help="Displays the sequence of the line in "
                                    "the purchase order.",
                               related='sequence', readonly=True)
    
    def _get_default_sequence(self):
        num = self._context['default_sequence']
        if num:
            return num

    item = fields.Char(string='Item #', default=_get_default_sequence)

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for move, line in zip(res, self):
            move.update(item=line.item)
        return res
