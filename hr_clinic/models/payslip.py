from odoo import models, fields


class HrSlip(models.Model):
    _inherit = 'hr.payslip'
    _description = 'form hr payslip'


    employee_id = fields.Many2one('hr.employee',domain=[('is_employee', '=', True)])