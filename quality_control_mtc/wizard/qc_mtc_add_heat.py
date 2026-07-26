from odoo import api, models, fields

class QcAddHeat(models.TransientModel):
    _name = 'qc.mtc.add.heat'
    _description = 'Add Heat Code to MTC'

    def _get_mtc_id(self):
        return self.env['qc.mtc'].browse(self.env.context['active_id'])

    mtc_id = fields.Many2one('qc.mtc', string='MTC', default=_get_mtc_id)

    lot_ids = fields.Many2many('stock.production.lot', string='Lot/Serial Numbers', domain="[('mtc_id', '=', mtc_id)]")
    mtc_line_id = fields.Many2one('qc.mtc.line', string='MTC Line', required=True)
    part_ids = fields.Many2many('qc.mtc.part', string='Part Name', required=True)


    def add_heat(self):
        obj_id = self.env['qc.mtc'].browse(self.env.context['active_id'])

        result = []
        if self.lot_ids:
            lot_ids = self.lot_ids
        else:
            lot_ids = self.env['stock.production.lot'].search([('mtc_id', '=', self.mtc_id.id)])

        for part in self.part_ids:
            result.append((0,0, {'name': self.mtc_line_id.name, 'lot_ids': lot_ids, 'mtc_line_id': self.mtc_line_id.id, 'part_id': part.id, 'mtc_id': obj_id.id}))

        obj_id.mtc_heat_ids = result
        for line in obj_id.mtc_heat_ids:
            line._onchange_lot_ids()
