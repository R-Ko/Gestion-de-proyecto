from odoo import models, fields, api


class WizardChangePassword(models.TransientModel):
    _name = 'wizard.change.password'
    _description = 'Wizard to change user passwords'

    user_id = fields.Many2one('res.users', string='Usuario', required=True)
    new_password = fields.Char(string='Nueva contraseña', required=True)

    def action_change_password(self):
        self.ensure_one()
        user = self.user_id
        # set password using Odoo's method
        user.sudo().write({'password': self.new_password})
        return {'type': 'ir.actions.act_window_close'}
