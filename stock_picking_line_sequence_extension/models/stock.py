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

    item = fields.Char('Item #')


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        res = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                           name, origin, values, group_id)
        res['item'] = values.get('item', False)
        return res
