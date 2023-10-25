from odoo import api, models, fields

class StockMove(models.Model):

    _inherit = 'stock.move'


    def fill_done_qty(self):
        for move_line in self.move_line_ids:
            if move_line.qty_done == 0 and move_line.product_uom_qty:
                move_line.update({'qty_done': move_line.product_uom_qty})
        return self.action_show_details()

    def unfill_done_qty(self):
        for move_line in self.move_line_ids:
            if not move_line.result_package_id:
                move_line.update({'qty_done': 0})
        return self.action_show_details()
