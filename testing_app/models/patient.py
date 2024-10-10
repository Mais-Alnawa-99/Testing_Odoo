from datetime import date

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Patient(models.Model):
    _inherit = 'res.partner'
    _description = 'form patient'

    name = fields.Char(string='Patient Name', required=True)
    age = fields.Integer(string="Age", compute='_compute_age', readonly=1, store=True)
    date_birthday = fields.Date(string="Date of Birth")
    state_patient= fields.Boolean()
    date_today = fields.Date(string="Today Date", default=fields.Date.today)
    test_ids = fields.One2many('stambach.test', 'name', string="Patient Tests")
    invoice_ids = fields.One2many('account.move', 'partner_id', string='Invoices')
    payment_ids = fields.One2many('account.payment', 'partner_id', string="Payments")



    @api.depends('date_birthday')
    def _compute_age(self):
        for rec in self:
            if rec.date_birthday:
                today = datetime.today().date()
                difference = relativedelta(today, rec.date_birthday)
                years = difference.years
                if difference.months > 7:
                    years += 1
                rec.age = years
            else:
                rec.age = 0

