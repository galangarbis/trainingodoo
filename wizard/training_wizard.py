from odoo import fields, models, api, _
from odoo.exceptions import UserError

class TrainingWizard(models.TransientModel):

    _name = 'trainingodoo.wizard'
    _description = 'Training Wizard'

    def _default_sesi(self):
        return self.env['trainingodoo.session'].browse(self._context.get('active_ids'))
    
    session_id = fields.Many2one('trainingodoo.session', string='Sesi', default=_default_sesi)
    attendee_ids = fields.Many2many(comodel_name='trainingodoo.attendee', string='Peserta')
    session_ids = fields.Many2many(comodel_name='trainingodoo.session', string='Sesi', default=_default_sesi)
    
    def tambah_peserta(self):
        self.session_id.attendee_ids |= self.attendee_ids

    def tambah_banyak_peserta(self):
        for sesi in self.session_ids:
            sesi.attendee_ids |= self.attendee_ids

    def cron_expire_session(self):
        now = fields.Date.today()
        expired_ids = self.env['trainingodoo.session'].search([('end_date', '<', now), ('state', '=', 'open')])
        expired_ids.write({'state': 'done'})

    
