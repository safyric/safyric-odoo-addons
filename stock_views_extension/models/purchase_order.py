from odoo import fields, models

class PurchaseOrdreLine(models.Model):
    _inherit = 'purchase.order.line'

    def name_get(self):
      result = []
      for rec in self:
          result.append((rec.id, product_id))

      return result
