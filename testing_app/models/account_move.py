from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'account move for testing'

    test_id = fields.Many2one('stambach.test', string="Test")

    def button_open_back_test(self):
        self.ensure_one()
        if self.test_id:
           return{
                 'type': 'ir.actions.act_window',
                 'name': 'Test',
                 'res_model': 'stambach.test',
                 'view_mode': 'form',
                 'res_id': self.test_id.id,
                 'target': 'current',
           }

