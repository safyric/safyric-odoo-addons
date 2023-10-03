from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dms_ids = fields.One2many('dms.file', 'sale_id', string='Attachments')
