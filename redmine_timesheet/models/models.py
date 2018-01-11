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
    def sync_data_from_redmine(self):
        from redminelib import Redmine
        redmine = Redmine('https://pm.syntech.software', username='oleg.karpov@syntech.software', password='123456')
        for project in redmine.project.all():
            if self.env['project.project'].search([('name', '!=', project.name)]):
                proj_obj = self.env['project.project'].create({'name': project.name, 'allow_timesheets': True})

                tasks = []
                try:
                    tasks = list(project.issues)
                except Exception:
                    pass

                for task in tasks:
                    if self.env['project.task'].search([('name', '!=', str(task)), ('project_id', '!=', project.id)]):

                        task_obj = self.env['project.task'].create({
                            'project_id': proj_obj.id,
                            'name': str(task),
                            'description': task.description,
                            # 'priority': task.priority,
                            'create_date': task.created_on,
                            # 'date_start': task.start_date,
                            # 'date_end': task.start_end,
                            # 'date_deadline': task.due_date,
                            # 'date_last_stage_update': task.updated_on,
                            'progress': task.done_ratio,
                            # 'status': task.status,
                        })

                        time_entrys = []
                        try:
                            time_entrys = list(task.time_entries)
                        except Exception:
                            pass

                        for time_entry in time_entrys:
                            if self.search([('redmine_id', '!=', time_entry.id)]):

                                time_entry_name = time_entry.comments or str(time_entry)
                                timesheet_obj = self.env['account.analytic.line'].create({
                                    'name': time_entry_name,
                                    'project_id': proj_obj.id,
                                    'task_id': task_obj.id
                                })

                                self.create({
                                    'timesheet_id': timesheet_obj.id,
                                    'redmine_id': time_entry.id,
                                    'sync_date': datetime.now(),
                                    'updated_on_redmine': datetime.now(),
                                    'name': time_entry.comments,
                                    'create_date': time_entry.created_on,
                                    'amount': time_entry.hours,
                                })
