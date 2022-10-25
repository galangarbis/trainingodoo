from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TrainingSession(models.Model):
    _name = 'trainingodoo.session'
    _description = 'Training Sesi'

    @api.depends('seats','attendee_ids')
    def compute_taken_seats(self):
        for sesi in self:
            sesi.taken_seats = 0
            if sesi.seats and sesi.attendee_ids :
                sesi.taken_seats = 100 * len(sesi.attendee_ids) / sesi.seats

    def default_partner_id(self):
        instruktur = self.env['res.partner'].search(['|',('instructor','=',True),('category_id.name','ilike','Pengajar')], limit=1)
        return instruktur
    
    @api.depends('start_date','duration')
    def get_end_date(self):
        for sesi in self:
            if not sesi.start_date:
                sesi.end_date = sesi.start_date
                continue

            start = fields.Date.from_string(sesi.start_date)
            sesi.end_date = start + timedelta(days=sesi.duration)
    
    def set_end_date(self):
        for sesi in self:
            if not(sesi.start_date and sesi.end_date):
                continue

            start_date = fields.Datetime.from_string(sesi.start_date)
            end_date = fields.Datetime.from_string(sesi.end_date)
            sesi.duration = (end_date - start_date).days + 1
    
    course_id = fields.Many2one('trainingodoo.course', string='Judul Kursus', required=True, ondelete='cascade', readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char(string='Nama', required=True, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date(string='Tanggal',default=fields.Date.context_today, readonly=True, states={'draft': [('readonly', False)]})
    duration = fields.Float(string='Durasi',help='Jumlah Hari Training',default = 3, readonly=True, states={'draft': [('readonly', False)]})
    seats = fields.Integer(string='Kursi', help='Jumlah Kuota Kursi',default = 10, readonly=True, states={'draft': [('readonly', False)]})
    partner_id = fields.Many2one('res.partner', string='Instruktur', domain=['|',('instructor','=','True'),('category_id.name','ilike','Pengajar')], default=default_partner_id, readonly=True, states={'draft': [('readonly', False)]})
    attendee_ids = fields.Many2many( 
        comodel_name='trainingodoo.attendee', 
        relation='session_attendee_rel',
        column1='session_id',
        column2='attendee_id',
        string='Peserta', 
        readonly=True, 
        states={'draft': [('readonly', False)]}
    )
    taken_seats = fields.Float(string="Kursi Terisi", compute="compute_taken_seats")
    end_date = fields.Date(String="Tanggal Selesai",compute="get_end_date",inverse="set_end_date",store=True, readonly=True, states={'draft': [('readonly', False)]})
    attendees_count = fields.Integer(string="Jumlah Peserta",compute="get_attendees_count",store=True)
    color = fields.Integer(string='Color Index',default=0)
    level = fields.Selection(string='Tingkatan', related='course_id.level')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('done', 'Done')], string='Status', default='draft')
    
    def action_confirm(self):
        self.write({'state': 'open'})
      
    def action_cancel(self):
        self.write({'state': 'draft'})
      
    def action_close(self):
        self.write({'state': 'done'})
    

    @api.depends('attendee_ids')
    def get_attendees_count(self):
        for sesi in self:
            sesi.attendees_count = len(sesi.attendee_ids)

    @api.constrains('seats','attendee_ids')
    def check_seats_and_attendees(self):
        for r in self:
            if r.seats < len(r.attendee_ids):
                raise ValidationError("Jumlah peserta melebihi kuota yang disediakan")
    
    @api.onchange('duration')
    def verify_valid_duration(self):
        if self.duration <= 0:
            self.duration = 1
            return {'warning' : {'title' : 'Perhatian', 'message' : 'Durasi Hari Training Tidak Boleh 0 atau Negatif'}}
        
    def cron_expire_session(self):
        now = fields.Date.today()
        expired_ids = self.search([('end_date', '<', now), ('state', '=', 'open')])
        expired_ids.write({'state': 'done'})
