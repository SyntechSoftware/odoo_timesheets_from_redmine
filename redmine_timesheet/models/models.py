# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api, _
import logging

from odoo.exceptions import UserError
from odoo.osv import orm

_logger = logging.getLogger()


class RedmineTimeEntry(orm.Model):
    _name = 'redmine.hr.analytic.timesheet'
    _description = 'Redmine Time Entry Binding'
    _inherits = {'account.analytic.line': 'timesheet_id'}

    timesheet_id = fields.Many2one('account.analytic.line', 'Timesheet', required=True, ondelete='cascade')
    redmine_id = fields.Integer('ID in Redmine', required=True)
    sync_date = fields.Datetime('Last Synchronization Date', required=True)
    updated_on_redmine = fields.Datetime('Last Update in Redmine', required=True)


    @api.model
    def sync_data_from_redmine(self, api_key=None, url=None):
        try:
            from redminelib import Redmine
        except ImportError:
            raise UserError(_('Missing python dependency (python-redmine), check https://python-redmine.com/'))

        if any([api_key, url]):
            redmine = Redmine(url, key=api_key)
        else:
            params = self.env['ir.config_parameter'].sudo()
            if not any([params.get_param('redmine_timesheet.redmine_api_key'),
                        params.get_param('redmine_timesheet.redmine_url')]):
                raise UserError(_('Please set redmine api credentials in module settings'))

            redmine = Redmine(params.get_param('redmine_timesheet.redmine_url'),
                              key=params.get_param('redmine_timesheet.redmine_api_key'))
        try:
            redmine.auth()
        except Exception as e:
            raise UserError(_(e))

        _logger.info('Connect with Redmine')

        for project in list(redmine.project.all()):
            proj_obj = self._get_or_create_project(project)
            _logger.info("Project: {} - been find in odoo ".format(proj_obj.name))

            for task in self._get_tasks_from_project(project):
                task_obj = self._get_or_create_task(task, proj_obj)
                _logger.info(u"Task: {} - been find in odoo ".format(task_obj.name))

                for time_entry in self._get_time_entrys_from_task(task):
                    self._get_or_create_timesheet(task_obj, time_entry, proj_obj)

    def _get_tasks_from_project(self, project):
        tasks = []
        try:
            tasks = list(project.issues)
        except Exception:
            pass
        return tasks

    def _get_time_entrys_from_task(self, task):
        time_entrys = []
        try:
            time_entrys = list(task.time_entries)
        except Exception:
            pass
        return time_entrys

    def _get_or_create_timesheet(self, task_obj, time_entry, proj_obj):
        time_entry_query = [('redmine_id', '=', time_entry.id)]
        time_entry_name = time_entry.comments or 'no time comments'

        _logger.info('Got time_entry {} from Redmine'.format(time_entry_name))

        if not self.search(time_entry_query):
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
            })

    def _get_or_create_task(self, task, proj_obj):
        task_title = task.subject
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

        return task_obj

    def _get_or_create_project(self, project):
        proj_query = [('name', '=', project.name)]
        _logger.info('Got project {} from Redmine'.format(project.name))
        _logger.info('Check if exists in odoo')
        if not self.env['project.project'].search(proj_query):
            _logger.info("Project Doesn't exists, creating project")
            proj_obj = self.env['project.project'].create({'name': project.name, 'allow_timesheets': True})
            _logger.info("Project: {} - CREATED ".format(proj_obj.name))
        else:
            proj_obj = self.env['project.project'].search(proj_query)[0]

        return proj_obj
