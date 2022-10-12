from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    volume = fields.Float(
        "Volume (m³)",
        digits=(8, 4),
        compute="_compute_volume",
        readonly=True,
        store=False,
        help="volume in cubic meters",
    )

    weight = fields.Float(
        'Package Weight', digits=dp.get_precision('Stock Weight'),
        help="Weight of the packaging. The unit of measure can be changed in the general settings")
    
    @api.depends("length", "width", "height")
    def _compute_volume(self):
        for pack in self:
            pack.volume = (pack.length * pack.width * pack.height) / 1000.0 ** 3
