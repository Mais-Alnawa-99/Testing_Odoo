from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'form hr employees'


    payslip_ids = fields.One2many('hr.payslip' , 'employee_id' , string='PaySlip')
    leave_ids = fields.Many2many('hr.leave', 'employee_ids', string='TimeOff',domain=[('employee', '=', True)])
    is_employee = fields.Boolean()
    parent_id = fields.Many2one('hr.employee' ,domain=[('is_employee', '=', True)])
    employee_type = fields.Selection([
        ('employee', 'Employee'),
        ('contractor' , 'Doctor'),
        ('freelance', 'Nirse'),
        ('student', 'Manager'),

    ])
    work_location=fields.Text()