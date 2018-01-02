# -*- coding: utf-8 -*-
from odoo import models, fields, api
try:
    from redminelib import Redmine
except ImportError:
    pass


class RedmineProject(models.Model):

    _name = 'redmine.project'
    # _inherit = "project.project"

    project_title = fields.Char(required=True, default='123')

    @api.one
    def sync_projects(self):
        redmine = Redmine('https://pm.syntech.software', username='oleg.karpov@syntech.software', password='123456')
        for project in redmine.project.all():
            self.create({'project_title': '123123'})
