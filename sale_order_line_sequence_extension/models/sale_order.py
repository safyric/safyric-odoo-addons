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
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id=False)
        for line in self:
            res.update({
                'item': line.item,
            })
        return res

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                           name, origin, values, group_id)
        res['item'] = values.get('item', False)
        return res
