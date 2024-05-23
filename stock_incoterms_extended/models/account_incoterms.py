from odoo import api, fields, models
from odoo.osv import expression

class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'


    edition = fields.Char(string="Incoterms Edition")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.code,rec.edition)))

        return result


    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        recs = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(recs).name_get()
