from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    profile_bio = fields.Text(string='Bio')
    avatar_url = fields.Char(string='Avatar URL')
    favorite_color = fields.Char(string='Favorite color')
