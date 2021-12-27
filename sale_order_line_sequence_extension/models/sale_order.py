from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sequence = fields.Integer(
        help="Gives the sequence of this line when displaying the sale order.",
        default=1,
        string="Sequence"
    )

    sequence2 = fields.Integer(
        help="Shows the sequence of this line in the sale order.",
        related='sequence',
        string="Line #",
        readonly=True,
        store=True
    )

    def _get_default_sequence(self):
        num = 0
        context = self.env.context
        if context.get('default_sequence'):
            num = self._context['default_sequence']
        if num:
            return num

    item = fields.Char(string='Item #', default=_get_default_sequence)

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self). \
            _prepare_procurement_values(group_id)
        # has ensure_one already
        if self.item:
            vals.update({
                'item': self.item,
            })
        return vals

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        res.update({'item': self.item})
        return res

class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.multi
    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['item']
        return fields
