# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
import logging

from odoo.osv import orm

_logger = logging.getLogger()


class RedmineUser(orm.Model):
    _name = 'redmine.hr.analytic.user'
    _description = 'Redmine User'

    redmine_login = fields.Char('Redmine login', required=True)
    redmine_pass = fields.Char('Redmine password', required=True)
    redmine_url = fields.Char('Redmine url', required=True)


class RedmineTimeEntry(orm.Model):
    _name = 'redmine.hr.analytic.timesheet'
    _description = 'Redmine Time Entry Binding'
    _inherits = {'account.analytic.line': 'timesheet_id', 'redmine.hr.analytic.user': 'redmine_user'}

    timesheet_id = fields.Many2one('account.analytic.line', 'Timesheet', required=True, ondelete='cascade')
    redmine_id = fields.Integer('ID in Redmine', required=True)
    sync_date = fields.Datetime('Last Synchronization Date', required=True)
    updated_on_redmine = fields.Datetime('Last Update in Redmine', required=True)
    redmine_user = fields.Many2one('redmine.hr.analytic.user', 'Users', required=True, ondelete='cascade')

    @api.model
    def sync_data_from_redmine(self):
        if not self.env['redmine.hr.analytic.user'].browse(1):
            _logger.error('Redmine user is not been set')
            return

        _logger.info('Connect with Redmine')
        from redminelib import Redmine
        redmine_user = self.env['redmine.hr.analytic.user'].browse(1)

        redmine = Redmine(
            redmine_user.redmine_url, username=redmine_user.redmine_login, password=redmine_user.redmine_pass
        )

        for project in redmine.project.all():
            proj_query = [('name', '=', project.name)]
            _logger.info('Got project {} from Redmine'.format(project.name))
            _logger.info('Check if exists in odoo')
            if not self.env['project.project'].search(proj_query):
                _logger.info("Project Doesn't exists, creating project")
                proj_obj = self.env['project.project'].create({'name': project.name, 'allow_timesheets': True})
                _logger.info("Project: {} - CREATED ".format(proj_obj.name))
            else:
                proj_obj = self.env['project.project'].search(proj_query)[0]
                _logger.info("Project: {} - been find in odoo ".format(proj_obj.name))

                tasks = []
                try:
                    tasks = list(project.issues)
                except Exception:
                    pass

                for task in tasks:
                    task_title = task.__unicode__()
                    _logger.info(u'Got task {} from Redmine'.format(task_title))
                    _logger.info('Check if TASK EXISTS in odoo')
                    task_query = [('name', '=', task_title)]

                    if not self.env['project.task'].search(task_query):
                        _logger.info(u"Task: {}, Doesn't exists , creating task".format(task_title))

                        task_obj = self.env['project.task'].create({
                            'project_id': proj_obj.id,
                            'name': task_title,
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
                        _logger.info(u"Task: {} - CREATED ".format(task_obj.name))

                    else:
                        task_obj = self.env['project.task'].search(task_query)[0]
                        _logger.info(u"Task: {} - been find in odoo ".format(task_obj.name))

                        time_entrys = []
                        try:
                            time_entrys = list(task.time_entries)
                        except Exception:
                            pass

                        for time_entry in time_entrys:
                            time_entry_query = [('redmine_id', '=', time_entry.id)]
                            time_entry_name = time_entry.comments or 'no time comments'

                            _logger.info('Got time_entry {} from Redmine'.format(time_entry_name))

                            if self.search(time_entry_query):
                                if not self.env['hr.employee'].search([('name', '=', time_entry.user.name)]):
                                    employee = self.env['hr.employee'].create({'name': time_entry.user.name})
                                else:
                                    employee = self.env['hr.employee'].search([('name', '=', time_entry.user.name)])[0]

                                timesheet_obj = self.env['account.analytic.line'].create({
                                    'name': time_entry_name,
                                    'project_id': proj_obj.id,
                                    'task_id': task_obj.id,
                                    'employee_id': employee.id,
                                })

                                self.create({
                                    'timesheet_id': timesheet_obj.id,
                                    'redmine_id': time_entry.id,
                                    'sync_date': datetime.now(),
                                    'updated_on_redmine': datetime.now(),
                                    'name': time_entry_name,
                                    'create_date': time_entry.created_on,
                                    'unit_amount': time_entry.hours,
                                    'redmine_user': redmine_user.id
                                })