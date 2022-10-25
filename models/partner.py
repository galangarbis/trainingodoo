from odoo import api, fields, models


class TrainingPartner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string='Instruktur')
    session_ids = fields.One2many('trainingodoo.session', 'partner_id', string='Daftar Mengajar Sesi', readonly=True)