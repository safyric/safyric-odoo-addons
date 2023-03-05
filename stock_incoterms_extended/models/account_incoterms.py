from odoo import fields, models

class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    
    edition = fields.Char(string="Incoterms Edition")
    
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.code,rec.edition)))
            
        return result

