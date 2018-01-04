# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

try:
    from redminelib import Redmine
except ImportError:
    pass

_logger = logging.getLogger()


class RedmineUser(models.Model):
    _name = 'redmine.user'

    redmine_login = fields.Char(required=True)
    redmine_pass = fields.Char(required=True)
    projects = fields.One2many('project.project', 'id', string="Projects")
    tasks = fields.One2many('project.task', 'id', string="Tasks")
    # time_sheets = fields.One2many('hr_timesheet.AccountAnalyticLine', 'id', string="Timesheets")

    @api.model
    def create(self, vals):
        redmine = Redmine('https://pm.syntech.software', username='oleg.karpov@syntech.software', password='123456')
        for project in redmine.project.all():
            proj = self.projects.create({'name': project.name})
            tasks = redmine.issue.filter(project=project.identifier)

            for task in tasks:
                self.tasks.create({'project_id': proj.id, 'name': '{}'.format(task)})

        return super(RedmineUser, self).create(vals)

