from openai import OpenAI
import logging

from odoo import models, fields, api, _
from odoo import tools, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class OdooAi(models.Model):
    _name = 'odoo.ai'
    _description = 'Odoo AI'



    @api.model
    def _default_image(self):
        image_path = get_module_resource('odoo_ai', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    name = fields.Char('Name', required=True)
    active = fields.Boolean(
        default=True,
    )

    image = fields.Binary("Photo", default="_default_image", attachment=True)
    image_medium = fields.Binary("Medium-sized Photo", attachment=True)
    image_small = fields.Binary("Small-sized Photo", attachment=True)

    model_id = fields.Many2one(
        string="Model", required=True,
        comodel_name='ir.model'
    )

    service = fields.Selection(
        string='Service Provider',
        selection=[('openai', 'OpenAI')],
        required=True
    )

    api_key = fields.Char('API Key')
    api_base = fields.Char('API Endpoint')
    max_tokens = fields.Integer('Max Tokens', default=200)
    temperature = fields.Float('Temperature', default=1)
    top_p = fields.Float('Top P', default=1)
    top_k = fields.Float('Top K')
    frequency_penalty= fields.Float('Frequence Penalty')
    repetition_penalty = fields.Float('Repetition Penalty')
    presence_penalty = fields.Float('Presence Penalty')

    description = fields.Text()
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.user.company_id
    )

    ai_model = fields.Char(string='AI Model')


    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(OdooAi, self).create(vals)


    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(OdooAi, self).write(vals)

    def _connect_api(self):
        if self.service == 'openai':
            if self.api_key:
                api_key = self.api_key
            else:
                raise UserError(_('API Key is required.'))

            if self.api_base:
                api_base = self.api_base
            elif self.service == 'openai':
                raise UserError(_('API Base is required.'))

            client = OpenAI(base_url=api_base, api_key=api_key)
            return client

    def create_chat_completion(self, model, prompt):
        if not model:
            model = 'x'

        if self.service == 'openai':
            openai = self._connect_api()
            response = openai.chat.completions.create(
                model = model,
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=False
            )

            res = response.model_dump()['choices'][0]['message']['content']
            return res


