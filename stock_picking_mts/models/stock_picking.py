# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'


    @api.multi
    def update_mts(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        for move in self.move_lines:
            if move.procure_method != 'make_to_stock':
                move.procure_method = 'make_to_stock'

