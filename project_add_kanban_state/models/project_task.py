from odoo import api, fields, models, _


class ProjectTask(models.Model):
    """Added state in the Project Task."""

    _inherit = 'project.task'

    legend_inprogress = fields.Char(related='stage_id.legend_inprogress', string='Kanban Ongoing Explanation', readonly=True, related_sudo=False)

    kanban_state = fields.Selection(selection_add=[('inprogress', 'Yellow')])
    
    @api.depends('stage_id', 'kanban_state')
    def _compute_kanban_state_label(self):
        res = super(ProjectTask, sself)._compute_kanban_state_label()
        for task in self:
            if task.kanban_state == 'inprogress':
                task.kanban_state_label = task.legend_inprogress
        return res
