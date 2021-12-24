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

    item = fields.Char('Item #')

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self).\
            _prepare_procurement_values(group_id)
        # has ensure_one already
        if self.item:
            vals.update({
                'item': self.item,
            })
        return vals

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['item']
        return fields
