from odoo import models, fields

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    employee_ids = fields.Many2many('hr.employee', string='Employee' ,domain=[('is_employee', '=', True)])
    employee=fields.Boolean()