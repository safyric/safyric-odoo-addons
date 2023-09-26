import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class ResUsersSignatures(models.Model):
    _name = 'res.users.signatures'
    _description = 'Users Signatures'


    name = fields.Char('Name', required=True)
    digital_signature = fields.Binary('Digital Signature')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)

class ResUsers(models.Model):
    _inherit = 'res.users'

    signature_ids = fields.One2many('res.users.signatures', 'user_id', string='Signatures')
