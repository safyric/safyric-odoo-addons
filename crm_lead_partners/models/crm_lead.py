from odoo import api, fields, models

class Lead(models.Model):
    _inherit = "crm.lead"
    
    project_name = fields.Char(string='Project Name', translate=True)
    epc_id = fields.Many2one('res.partner', string='EPC',
                             help="EPC of the project/opportunity")
    enduser_id = fields.Many2one('res.partner', string='End-User', 
                                 help="End User of the project/opportunity")
