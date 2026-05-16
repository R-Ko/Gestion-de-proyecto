from odoo import models, fields, api, SUPERUSER_ID
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = 'res.users'

    profile_bio = fields.Text(string='Bio')
    avatar_url = fields.Char(string='Avatar URL')
    favorite_color = fields.Char(string='Favorite color')

    allowed_project_ids = fields.Many2many(
        'project.project',
        'res_users_allowed_project_rel',
        'user_id',
        'project_id',
        string='Allowed Projects',
        help='Projects this user is allowed to see'
    )

    @api.model
    def create(self, vals):
        # Only administrators (settings group / superuser) can create new users
        if self.env.uid != SUPERUSER_ID and not self.env.user.has_group('base.group_system'):
            raise AccessError('Only administrators can create users')
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        # Prevent non-admins from changing allowed_project_ids or creating users
        restricted_fields = {'allowed_project_ids'}
        if vals and any(f in vals for f in restricted_fields):
            if self.env.uid != SUPERUSER_ID and not self.env.user.has_group('base.group_system'):
                raise AccessError('Only administrators can change user project permissions')
        return super(ResUsers, self).write(vals)
