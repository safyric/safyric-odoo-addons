from odoo import api, fields, models


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

    @api.depends("length", "width", "height")
    def _compute_volume(self):
        for pack in self:
            pack.volume = (pack.length * pack.width * pack.height) / 1000.0 ** 3
