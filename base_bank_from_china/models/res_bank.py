from odoo import fields, models


class ResBank(models.Model):
    _inherit = 'res.bank'

    cnaps_code = fields.Char(string="CNAPS Code", help="银行联行号是一个地区银行的唯一识别标志。")
