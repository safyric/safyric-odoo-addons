from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dms_ids = fields.One2many('dms.file', 'purchase_id', string='Attachments')
