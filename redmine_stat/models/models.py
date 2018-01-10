# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
import logging

from odoo.osv import orm


_logger = logging.getLogger()


class RedmineTimeEntry(orm.Model):
    _name = 'redmine.hr.analytic.timesheet'
    _description = 'Redmine Time Entry Binding'
    _inherits = {'account.analytic.line': 'timesheet_id'}

    timesheet_id = fields.Many2one('account.analytic.line', 'Timesheet', required=True)
    redmine_id = fields.Integer('ID in Redmine', required=True)
    sync_date = fields.Datetime('Last Synchronization Date', required=True)
    updated_on_redmine = fields.Datetime('Last Update in Redmine', required=True)


    @api.model
    def create(self, vals):
        return super(RedmineTimeEntry, self).create(vals)

    def write(self, vals):
        from redminelib import Redmine
        redmine = Redmine('https://pm.syntech.software', username='oleg.karpov@syntech.software', password='123456')
        for project in redmine.project.all():
            proj_obj = self.env['project.project'].create({'name': project.name, 'allow_timesheets': True})


            tasks = []
            try:
                tasks = list(project.issues)
            except Exception:
                pass

            for task in tasks:
                task_obj = self.env['project.task'].create({'project_id': proj_obj.id, 'name': task})

                time_entrys = []
                try:
                    time_entrys = list(task.time_entries)
                except Exception:
                    pass

                for time_entry in time_entrys:
                    timesheet_obj = self.env['account.analytic.line'].create({'name': time_entry.comments, 'project_id': proj_obj.id, 'task_id': task_obj.id})
                    self.create({'timesheet_id': timesheet_obj.id, 'redmine_id': 1, 'sync_date': datetime.now(), 'updated_on_redmine': datetime.now()})

                    # # check if project exists
            # # project_obj = project_model.search([('name', '=', project.name)])
            # # if not project_obj:
            # project_model = self.pool.get('project.project')
            # proj = project_model.create(project_model, {'name': project.name})
            # _logger.info('11111', proj)


        return super(RedmineTimeEntry, self).write(vals)



