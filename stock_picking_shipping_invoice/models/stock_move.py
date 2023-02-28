from odoo import api, fields, models

from odoo.addons import decimal_precision as dp


class StockMove(models.Model):
    _inherit = 'stock.move'

    price_unit = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), default=0.0)

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    price_unit = fields.Float('Unit Price', digits=dp.get_precision('Product Price'), related='move_id.price_unit')
