from odoo import models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class OdooAiBot(models.AbstractModel):
    _name = 'odoo.ai.bot'
    _description = 'Odoo AI Bot'


    def _apply_logic(self, record, values):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id('odoo_ai.partner_ai')
        if len(record) != 1 or values.get("author_id") == ai_bot_id:
            return

        if self._is_bot_pinged(values) or self._is_bot_in_private_channel(record):
            body = values.get("body", "")
            try:
                answer = self._get_answer(record, body, values)
            except:
                answer = ''
            if answer:
                message_type = 'comment'
                subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
                record = record.with_context(mail_create_nosubscribe=True).sudo()
                record.message_post(body=answer, author_id=ai_bot_id, message_type=message_type, subtype_id=subtype_id)

    def _get_answer(self, record, body, values):
        if not body:
            return
        prompt = body
        service = self.env['odoo.ai'].sudo().search([('service', '=', 'llama2')], limit=1)
        model = service.ai_model
        if not model:
            model = 'x'
        res = service.create_chat_completion(model, prompt)
        if res:
            return res

    def _is_bot_pinged(self, values):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id("odoo_ai.partner_ai")
        return (4, ai_bot_id) in values.get('partner_ids', [])


    def _is_bot_in_private_channel(self, record):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id("odoo_ai.partner_ai")
        if record._name == 'mail.channel' and record.channel_type == 'chat':
            return ai_bot_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False
