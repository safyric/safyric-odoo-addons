from odoo import api, fields, models


class DocumentPage(models.Model):
    _inherit = 'document.page'


    content_ids = fields.One2many('document.page.content', 'document_page_id', string="Content")
