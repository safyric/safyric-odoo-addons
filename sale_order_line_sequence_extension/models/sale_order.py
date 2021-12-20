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