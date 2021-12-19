from odoo import api, fields, models

class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    name = fields.Char(translate=True)
