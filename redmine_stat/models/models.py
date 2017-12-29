# -*- coding: utf-8 -*-
from odoo import models, fields, api


class RedmineUser(models.Model):

    _name = 'redmine.user'

    redmine_login = fields.Char(string='Redmine Login', required=True)
    redmine_pass = fields.Char(string='Redmine Pass', required=True)


class RedmineProject(models.Model):

    _name = 'redmine.project'
    # _inherit = "project.project"

    project_title = fields.Char(required=True, default='Click on generate name!')


    @api.one
    def get_project_from_redmine(self):
        from redminelib import Redmine
        redmine = Redmine('https://pm.syntech.software', username='oleg.karpov@syntech.software', password='123456')
        for project in redmine.project.all():
            self.create({'project_title': project.name})
