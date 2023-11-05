from odoo import api, fields, models


class PurchaseClause(models.Model):
    _name = "purchase.clause"
    _description = "Purchase Clauses"

    name = fields.Char(string="Name", required=True)
    content = fields.Html(string="Clause Content")
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will allow you to hide the agreement without "
        "removing it.")
    company_id = fields.Many2one('res.company', string='Company', readonly=True,  default=lambda self: self.env.user.company_id)

