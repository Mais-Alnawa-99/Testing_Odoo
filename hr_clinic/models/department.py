from odoo import models, fields


class HrSlip(models.Model):
    _inherit = 'hr.department'
    _description = 'form hr department'


    manager_id = fields.Many2one('hr.employee',domain=[('is_employee', '=', True)])