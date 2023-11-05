from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    purchase_clause_id = fields.Many2one('purchase.clause', string="Purchase Clause")
    content = fields.Html('Clause Content')
    dynamic_content = fields.Html(
        compute="_compute_dynamic_content",
        string="Dynamic Content",
        help="compute dynamic Content")

    # Dynamic field editor
    field_domain = fields.Char(string='Field Expression',
                               default='[["active", "=", True]]')
    default_value = fields.Char(
        string="Default Value",
        help="Optional value to use if the target field is empty.")
    copyvalue = fields.Char(
        string="Placeholder Expression",
        help="""Final placeholder expression, to be copy-pasted in the desired
         template field.""")

    @api.onchange('purchase_clause_id')
    def onchange_purchase_clause(self):
        content = self.purchase_clause_id
        if content:
            self.content = content.content
        else:
            self.content = False


    @api.onchange("field_domain", "default_value")
    def onchange_copyvalue(self):
        self.copyvalue = False
        if self.field_domain:
            string_list = self.field_domain.split(",")
            if string_list:
                field_domain = string_list[0][3:-1]
                self.copyvalue = "${{object.{} or {}}}".format(
                    field_domain,
                    self.default_value or "''")

    # compute the dynamic content for mako expression
    @api.multi
    def _compute_dynamic_content(self):
        MailTemplates = self.env["mail.template"]
        for clause in self:
            lang = (
                clause.partner_id.lang
                or "zh_CN"
            )
            content = MailTemplates.with_context(lang=lang)._render_template(
                clause.content, "purchase.order", clause.id
            )
            clause.dynamic_content = content
