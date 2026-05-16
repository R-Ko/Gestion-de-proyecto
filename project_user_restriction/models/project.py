from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = 'project.project'

    assigned_user_ids = fields.Many2many('res.users', string='Assigned users', help='Users allowed to see this project')
