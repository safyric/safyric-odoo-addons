from odoo import api, fields, models

class ProductBrand(models.Model):
    _inherit = 'product.brand'

    brand_type = fields.Selection(
       [('none', 'None'), ('own', 'Own Brand'), ('own_acquired', 'Own Acquired Brand'), ('foreign', 'Foreign Brand'), ('foreign_oem', 'Foreign OEM'), ('foreign_other', 'Foreign Other')],
       string="Brand Type"
    )
