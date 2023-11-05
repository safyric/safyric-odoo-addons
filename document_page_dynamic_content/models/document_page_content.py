from odoo import api, fields, models


class AgreementClause(models.Model):
    _name = "document.page.content"
    _description = "Document Page Content"
    _order = "sequence"

    name = fields.Char(string="Name", required=True)
    title = fields.Char(
        string="Title",
        help="The title is displayed on the PDF." "The name is not.")
    sequence = fields.Integer(string="Sequence")
    document_page_id = fields.Many2one(
        "document.page",
        string="Document",
        ondelete="cascade")
    content = fields.Html(string="Document Content")
    dynamic_content = fields.Html(
        compute="_compute_dynamic_content",
        string="Dynamic Content",
        help="compute dynamic Content")
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will allow you to hide the document without "
        "removing it.")

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
        for content in self:
            lang =  "en_US"
            content = MailTemplates.with_context(lang=lang)._render_template(
                content.content, "document.page.content", content.id
            )
            content.dynamic_content = content
