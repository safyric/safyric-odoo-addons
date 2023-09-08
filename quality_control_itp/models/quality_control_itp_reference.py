from odoo import api, fields, models

class QcItpRef(models.Model):
    _name = 'qc.itp.ref'
    _description = 'Reference Documents'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)


class QcItpVerifyDoc(models.Model):
    _name = 'qc.itp.verify.doc'
    _description = 'Verifying Documents'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)


class QcItpAccCriteria(models.Model):
    _name = 'qc.itp.acc.criteria'
    _description = 'Acceptance Criteria'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)



class QcItpRecords(models.Model):
    _name = 'qc.itp.records'
    _description = 'Records'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)



class QcItpInspLevel(models.Model):
    _name = 'qc.itp.insp.level'
    _description = 'Inspection Level'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    frequency = fields.Char('Frequency')
    sequence = fields.Integer('Sequence', default=1)

    @api.multi
    def name_get(self):
        result = []

        for rec in self:
            if rec.frequency:
                result.append((rec.id, '%s - %s' % (rec.name, rec.frequency)))
            else:
                result.append((rec.id, '%s' % (rec.name)))

        return result


class QcItpProc(models.Model):
    _name = 'qc.itp.proc'
    _description = 'Process Category'
    _order = 'sequence,id desc'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=1)

