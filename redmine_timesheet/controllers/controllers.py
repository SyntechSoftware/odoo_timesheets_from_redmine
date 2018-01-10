# -*- coding: utf-8 -*-
from odoo import http

# class /mnt/extra-addons/redmineStat(http.Controller):
#     @http.route('//mnt/extra-addons/redmine_timesheet//mnt/extra-addons/redmine_timesheet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/redmine_timesheet//mnt/extra-addons/redmine_timesheet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/redmine_stat.listing', {
#             'root': '//mnt/extra-addons/redmine_timesheet//mnt/extra-addons/redmine_timesheet',
#             'objects': http.request.env['/mnt/extra-addons/redmine_timesheet./mnt/extra-addons/redmine_timesheet'].search([]),
#         })

#     @http.route('//mnt/extra-addons/redmine_timesheet//mnt/extra-addons/redmine_timesheet/objects/<model("/mnt/extra-addons/redmine_timesheet./mnt/extra-addons/redmine_timesheet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/redmine_stat.object', {
#             'object': obj
#         })