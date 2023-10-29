import openai
from odoo import models, _
import logging

_logger = logging.getLogger(__name__)


class MailBot(models.AbstractModel):
    _name = 'mail.ai.bot'
    _description = 'Mail AI Bot'


    def _apply_logic(self, record, values):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id('openai_integration.partner_ai')
        if len(record) != 1 or values.get("author_id") == ai_bot_id:
            return

        if self._is_bot_pinged(values) or self._is_bot_in_private_channel(record):
            body = values.get("body", "")
            try:
                answer = self._get_answer(record, body, values)
            except openai.error.InvalidRequestError as err:
                answer = ''
                _logger.error(err)
            if answer:
                message_type = 'comment'
                subtype_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
                record = record.with_context(mail_create_nosubscribe=True).sudo()
                record.message_post(body=answer, author_id=ai_bot_id, message_type=message_type, subtype_id=subtype_id)

    def _get_answer(self, record, body, values):
        if not body:
            return
        openai.api_key = self.env['ir.config_parameter'].sudo().get_param('openai_integration.openai_api_key')
        openai.api_base = self.env['ir.config_parameter'].sudo().get_param('openai_integration.openai_api_base')
        response = openai.ChatCompletion.create(
            model="x",
            messages = [
               {"role": "user", "content": body}
            ]
        )
        res = response['choices'][0]['message']['content']
        if res:
            return res

    def _is_bot_pinged(self, values):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id("openai_integration.partner_ai")
        return (4, ai_bot_id) in values.get('partner_ids', [])


    def _is_bot_in_private_channel(self, record):
        ai_bot_id = self.env['ir.model.data'].xmlid_to_res_id("openai_integration.partner_ai")
        if record._name == 'mail.channel' and record.channel_type == 'chat':
            return ai_bot_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False
