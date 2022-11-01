from random import randint

from odoo import api, fields, models


class TrainingCourse(models.Model):
    _name = 'trainingodoo.course'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Training Kursus'

    def get_default_color(self):
        return randint(1,11)
    
    name = fields.Char(string='Judul', required=True,tracking=True)
    description = fields.Text(string='Keterangan',tracking=True)
    user_id = fields.Many2one('res.users', string='Penanggung Jawab',tracking=True)
    session_ids = fields.One2many('trainingodoo.session', 'course_id', string='Sesi',tracking=True)
    product_ids = fields.Many2many('product.product','course_product_rel','course_id','product_id','Cendera Mata',tracking=True)
    ref = fields.Char(string="Referensi",readonly=True,default="/",tracking=True)
    level = fields.Selection([('basic', 'Dasar'),('advanced','Lanjutan')], string='Tingkatan', default='basic')
    color = fields.Integer('Warna',default=get_default_color)
    email = fields.Char(string="Email",related='user_id.login')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('trainingodoo.course')
        return super(TrainingCourse, self).create(vals)

    _sql_constraints = [
        ('nama_kursus_unik', 'unique(name)', 'Judul kursus harus unik!'),
        ('nama_keterangan_cek', 'CHECK(name != description)', 'Judul kursus dan keterangan tidak boleh sama ')
    ]

    def copy(self, default=None):
        default = dict(default or {})
        default.update(name=("%s (copy)") % (self.name or ''))
        return super(TrainingCourse, self).copy(default)

    def action_print_course(self):
        return self.env.ref('trainingodoo.report_trainingodoo_course_action').report_action(self)