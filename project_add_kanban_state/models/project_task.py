from odoo import fields, models


class ProjectTask(models.Model):
    """Added state in the Project Task."""

    _inherit = 'project.task'
