# -*- coding: utf-8 -*-
from odoo import http

# class /mnt/extra-addons/redmineStat(http.Controller):
#     @http.route('//mnt/extra-addons/redmine_stat//mnt/extra-addons/redmine_stat/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/redmine_stat//mnt/extra-addons/redmine_stat/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/redmine_stat.listing', {
#             'root': '//mnt/extra-addons/redmine_stat//mnt/extra-addons/redmine_stat',
#             'objects': http.request.env['/mnt/extra-addons/redmine_stat./mnt/extra-addons/redmine_stat'].search([]),
#         })

#     @http.route('//mnt/extra-addons/redmine_stat//mnt/extra-addons/redmine_stat/objects/<model("/mnt/extra-addons/redmine_stat./mnt/extra-addons/redmine_stat"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/redmine_stat.object', {
#             'object': obj
#         })