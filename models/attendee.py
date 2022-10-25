from odoo import api, fields, models


class TrainingAttendee(models.Model):
    _name = 'trainingodoo.attendee'
    _description = "Training Peserta"
    _inherits = {"res.partner" : "partner_id"}

    partner_id = fields.Many2one('res.partner', 'Partner', required=True, ondelete='cascade')
    name = fields.Char(string='Nama', required=True, inherited = True)
    sex = fields.Selection([("male","Pria"),("female","Wanita")], string='Kelamin', required=True, help='Jenis Kelamin')
    marital = fields.Selection([("single","Belum Menikah"),("married","Menikah"),("divorced","Cerai")], string='Pernikahan', help='Status Pernikahan')
    session_ids = fields.Many2many('trainingodoo.session','session_attendee_rel','attendee_id','session_id','Sesi')