from odoo import models, fields, api
from stdnum.exceptions import ValidationError
from datetime import date


class Test(models.Model):
    _name = 'stambach.test'

    _description = 'stambach test'

    name = fields.Many2one('res.partner', string='Patient Name', domain=[('state_patient', '=', True)])
    invoice_id = fields.Many2one('account.move')
    patient_age = fields.Integer(related='name.age', string='Age', store=True)
    data_test_id = fields.Many2one('data.test', string='Skill Type')
    currency_id = fields.Many2one(related='data_test_id.currency_id',store=True)
    price = fields.Monetary(related='data_test_id.test_fee', currency_field='currency_id',store=True)
    price_with_symbol = fields.Char(string="Price", compute='_compute_price_with_symbol')
    amount_paid = fields.Integer()
    avg = fields.Float(compute='_compute_data', readonly=True, store=True)
    diva = fields.Float(compute='_compute_data', reaonly=True, store=True)
    row_score = fields.Integer(string='Row_Degree', store=True)
    result = fields.Float(compute='_compute_result', string='Result', readonly=True, store=True)
    level_result = fields.Text(compute='_compute_level', string='Level_result', readonly=True, store=True)
    date_today = fields.Date(string="Today Date", default=fields.Date.today, readonly=1)

    @api.depends('patient_age', 'data_test_id')
    def _compute_data(self):
        for record in self:
            if record.patient_age and record.data_test_id:
                test_data = record.data_test_id.get_data(record.patient_age)
                if test_data:
                    record.avg = test_data['avg']
                    record.diva = test_data['diva']

                else:
                    raise models.ValidationError("no level for this  age until now ")

    @api.depends('row_score', 'avg', 'diva')
    def _compute_result(self):
        for record in self:
            if record.row_score and record.diva != 0:
                record.result = (record.row_score - record.avg) / record.diva
            else:
                record.result = 0

    @api.depends('result')
    def _compute_level(self):
        for record in self:
            if record.result:
                if -2 <= record.result <= -1:
                    record.level_result = "Difficulty limits"
                elif -3 <= record.result <= -2:
                    record.level_result = "Above Average"
                elif 2 <= record.result <= 3:
                    record.level_result = "Disorder"
                elif -1 <= record.result <= 1:
                    record.level_result = "Within Average"
                else:
                    record.level_result = "No level for this skill"
            else:
                record.level_result = "you must match test type age data with patient age"

    def action_recompute_result(self):
        for record in self:
            if record.patient_age and record.data_test_id:
                test_data = record.data_test_id.get_data(record.patient_age)
                if test_data:
                    record.avg = test_data['avg']
                    record.diva = test_data['diva']

                else:
                    raise models.ValidationError("no level for this  age until now ")
                record.row_score = 0
                record._compute_result()
                record._compute_level()
            else:
                raise models.ValidationError("Patient age or test type is missing.")


    def create_invoice(self):
        for record in self:
            if record.data_test_id:
                invoice = self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'test_id':record.id,
                    'partner_id': record.name.id,
                    'invoice_date': fields.Date.today(),
                    'invoice_line_ids': [(0, 0, {
                        'name': record.data_test_id.name,
                        'price_unit': record.data_test_id.test_fee,
                    })]
                })
                record.invoice_id = invoice.id
                invoice.action_post()
                if record.amount_paid:
                    payment = self.env['account.payment'].create({
                        'partner_id': record.name.id,
                        'amount': record.amount_paid,
                        'payment_type': 'inbound',
                        'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
                    })
                    payment.action_post()

                    if payment.line_ids:
                        invoice.js_assign_outstanding_line(payment.line_ids[0].id)
                    else:
                        raise ValidationError("No outstanding payment lines found.")


                    return invoice


    def save(self):
        for record in self:
            record.create_invoice()

    def button_open_invoice_entry(self):
        self.ensure_one()
        if self.invoice_id:
           return{
                 'type':'ir.actions.act_window',
                 'name':'Invoice',
                 'res_model':'account.move',
                 'view_mode':'form',
                 'res_id':self.invoice_id.id,
                 'target':'current',
        }

    @api.depends('price', 'currency_id')
    def _compute_price_with_symbol(self):
        for record in self:
            currency_symbol = record.currency_id.symbol if record.currency_id else ''
            record.price_with_symbol = "{} {}".format(currency_symbol, record.price if record.price else 0.0)