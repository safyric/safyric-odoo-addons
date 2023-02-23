from odoo import fields, models

class ProjectTaskType(models.Model):
    """Added state in the Project Task Type."""

    _inherit = 'project.task.type'

    legend_normal = fields.Char(
        'Grey Kanban Label', default=lambda s: _('New'), translate=True, required=True,
        help='Override the default value displayed for the normal state for kanban selection, when the task or issue is in that stage.')
    
    legend_inprogress = fields.Char(
        'Yellow Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
        help='Override the default value displayed for the in progress state for kanban selection, when the task or issue is in that stage.')
