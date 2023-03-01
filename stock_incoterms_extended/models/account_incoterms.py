from odoo import fields, models

class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    def name_get(self):
      result = []
      for rec in self:
          result.append((rec.id, '%s - %s' % (rec.code,rec.product_id.display_name)))

      return result
