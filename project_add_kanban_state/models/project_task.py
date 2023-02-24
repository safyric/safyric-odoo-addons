from odoo import api, fields, models, _


class ProjectTask(models.Model):
    """Added state in the Project Task."""

    _inherit = 'project.task'

    legend_in_progress = fields.Char(related='stage_id.legend_in_progress', string='Kanban Ongoing Explanation', readonly=True, related_sudo=False)

    kanban_state = fields.Selection(selection_add=[('in_progress', 'Grey')])
    
    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        res = super(ProjectTask, self)._compute_kanban_state_label()
        for task in self:
            if task.kanban_state == 'in_progress':
                task.kanban_state_label = task.legend_in_progress
        return res
