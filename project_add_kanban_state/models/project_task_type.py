from odoo import fields, models

class ProjectTaskType(models.Model):
    """Added state in the Project Task Type."""

    _inherit = 'project.task.type'
