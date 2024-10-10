from odoo import models, fields


class DataTest(models.Model):
    _name = 'data.test'
    _description = 'data for test'

    name = fields.Char(string='Skill')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    test_fee = fields.Monetary(string='Test Fee', currency_field='currency_id')
    line=fields.One2many('test.line', 'test_id')
    creation_date = fields.Datetime("Creation Date", default=fields.Datetime.now)



    def get_data(self,patient_age):
        data=self.line.filtered(lambda d: d.age == patient_age)
        if data:
            return {
                'avg':data[0].avg,
                'diva': data[0].diva

            }
        return None

class TestLine(models.Model):
    _name = 'test.line'
    _description = 'data test line'

    age = fields.Integer(string='Age')
    avg = fields.Float(string='Average')
    diva = fields.Float(string='Deviation')
    test_id = fields.Many2one('data.test')










