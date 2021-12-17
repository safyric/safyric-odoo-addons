from odoo import api, fields, models
from datetime import datetime

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.multi
    def _compute_amount_in_words(self):
        for rec in self:
            rec.amount_words = str(rec.currency_id.amount_to_text(rec.amount_total)) + ' only'

    amount_words = fields.Char(string="Amount In Words:", compute='_compute_amount_in_words')
