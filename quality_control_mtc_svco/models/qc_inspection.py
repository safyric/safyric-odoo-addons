from odoo import api, fields, models
from odoo.osv import expression


class QcInspection(models.Model):
    _inherit = 'qc.inspection'

    material_id = fields.Many2one('qc.mtc.material', string='Material')
    heat_code = fields.Char('Heat Code')
    inspection_type = fields.Selection(selection_add=[('material', 'Material')])

    _sql_constraints = [('unique_heat_code', 'unique(heat_code)', 'Heat code already exists!')]

    def name_get(self):
        res = []
        for rec in self:
            if (rec.inspection_type == 'material'):
                res.append((rec.id, '%s - %s' % (rec.name, rec.heat_code or '')))
            else:
                res.append((rec.id, '%s' % rec.name))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            domain = ['|', ('name', operator, name), ('heat_code', operator, name)]
        recs = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(recs).name_get()

