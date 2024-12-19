# -*- coding: utf-8 -*-
# from odoo import http


# class PlaygroundManagement(http.Controller):
#     @http.route('/playground_management/playground_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/playground_management/playground_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('playground_management.listing', {
#             'root': '/playground_management/playground_management',
#             'objects': http.request.env['playground_management.playground_management'].search([]),
#         })

#     @http.route('/playground_management/playground_management/objects/<model("playground_management.playground_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('playground_management.object', {
#             'object': obj
#         })
