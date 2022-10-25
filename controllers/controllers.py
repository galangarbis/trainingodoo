# -*- coding: utf-8 -*-
# from odoo import http


# class Training-odoo(http.Controller):
#     @http.route('/training-odoo/training-odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training-odoo/training-odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('training-odoo.listing', {
#             'root': '/training-odoo/training-odoo',
#             'objects': http.request.env['training-odoo.training-odoo'].search([]),
#         })

#     @http.route('/training-odoo/training-odoo/objects/<model("training-odoo.training-odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training-odoo.object', {
#             'object': obj
#         })
