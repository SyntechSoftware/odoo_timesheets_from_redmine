# -*- coding: utf-8 -*-
import logging

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.osv import orm
from redminelib import Redmine
from redminelib.exceptions import ForbiddenError, AuthError
from redminelib.packages.requests.exceptions import MissingSchema

_logger = logging.getLogger()


class RedmineTimeEntry(orm.Model):
    _name = 'redmine.hr.analytic.timesheet'
    _description = 'Redmine Time Entry Binding'
    _inherits = {'account.analytic.line': 'timesheet_id'}

    timesheet_id = fields.Many2one('account.analytic.line', 'Timesheet', required=True, ondelete='cascade')
    redmine_id = fields.Integer('ID in Redmine', required=True)
    sync_date = fields.Datetime('Last Synchronization Date', required=True)

    def __init_redmine_obj(self):
        """
        Return redmine credentials.
        """
        api_settings = self.env['ir.config_parameter'].sudo()
        credentials = {
            'url': api_settings.get_param('redmine_timesheet.url', default=''),
            'key': api_settings.get_param('redmine_timesheet.api_key', default='')
        }
        if not all(credentials.values()):
            raise UserError(_('Please set redmine api credentials'))
        try:
            self.redmine = Redmine(**credentials)
            self.redmine.auth()
        except (MissingSchema, AuthError) as e:
            raise UserError(e.message)

    @api.model
    def sync_data_from_redmine(self):
        self.__init_redmine_obj()

        try:
            _logger.info('Connect with Redmine')
            projects = self.redmine.project.all()
        except Exception as e:
            raise UserError(_(e.message))

        for project in projects:
            proj_obj = self.get_or_create_project(project)

            for task in self.get_project_tasks(project):
                task_obj = self.get_or_create_task(task, proj_obj)

                for time_entry in self.get_task_timesheets(task):
                    self.get_or_create_timesheet(proj_obj, task_obj, time_entry)

    def get_or_create_project(self, project):
        """
        Return created or exists project from 'project.project'.
        """
        _logger.info('Getting project {}'.format(project.name))

        proj_query = [('name', '=', project.name)]
        if self.env['project.project'].search(proj_query):
            proj_obj = self.env['project.project'].search(proj_query)[0]
            _logger.info(u"Project: {} - has been find in Projects.".format(proj_obj.name))
        else:
            proj_obj = self.env['project.project'].create({'name': project.name, 'allow_timesheets': True})
            _logger.info(u"Project: {} - CREATED ".format(proj_obj.name))

        return proj_obj

    def get_project_tasks(self, project):
        tasks = []
        try:
            tasks = list(project.issues)
        except ForbiddenError:
            _logger.error(
                u'ForbiddenError, for "{}" project tasks'.format(project.name)
            )
        return tasks

    def get_or_create_task(self, task, project):
        task_title = task.subject
        task_query = [('name', '=', task_title)]
        task_qs = self.env['project.task'].search(task_query)

        if task_qs.exists():
            task_obj = task_qs[0]
            _logger.info(u"Task: {} - has been find in Tasks ".format(task_obj.name))
        else:
            task_obj = self.env['project.task'].create({
                'project_id': project.id,
                'name': task_title,
                'description': task.description,
                'create_date': task.created_on,
                'progress': task.done_ratio,
            })

        return task_obj

    def get_task_timesheets(self, task):
        time_entries = []

        try:
            time_entries = list(task.time_entries)
        except ForbiddenError:
            _logger.error(
                u'ForbiddenError, for {} tasks timesheets'.format(task.subject)
            )

        return time_entries

    def get_or_create_timesheet(self, project, task, time_entry):
        """
        Get all tasks timesheets.
        """

        time_entry_query = [('redmine_id', '=', time_entry.id)]
        description = time_entry.comments
        if not self.search(time_entry_query).exists():
            user, account = self.get_user_and_account(time_entry.user.id)
            timesheet = self.env['account.analytic.line'].create({
                'user_id': user.id,  # res.user
                'name': description,  # description
                'date': time_entry.created_on,  #
                'account_id': account.id,  # xz
                'project_id': project.id,
                'task_id': task.id,
                'unit_amount': time_entry.hours
            })
            self.create({
                'timesheet_id': timesheet.id,
                'redmine_id': time_entry.id,
                'sync_date': datetime.now(),
            })

    def get_user_and_account(self, user_id):
        try:
            company = self.env['res.company'].search([])[0]
        except IndexError:
            _logger.error("You must create a company!")
            raise UserError("You must create a company!")

        redmine_user = self.redmine.user.get(user_id)
        user_mail = getattr(redmine_user, 'mail', '')
        user_name = ' '.join([redmine_user.firstname, redmine_user.lastname])
        user_login = user_mail if user_mail else user_name
        user_exists = self.env['res.users'].search([('login', '=', user_login)])
        if user_exists.exists():
            user = user_exists[0]
        else:
            data = {
                'company_id': company.id,
                'login': user_login,
                'name': ' '.join([redmine_user.firstname, redmine_user.lastname]),
            }
            if user_mail:
                data['email'] = user_mail
            _logger.info("Creating a new user {}".format(' '.join([redmine_user.firstname, redmine_user.lastname])))
            user = self.env['res.users'].create(data)
        account = self.get_or_create_account(user, company.id)
        return user, account

    def get_or_create_account(self, user, company_id):
        """
        Create user from redmine.
        """
        account = self.env['account.analytic.account'].search([('name', '=', user.name)])
        if account.exists():
            account = account[0]
        else:
            _logger.info("Creating a new account")
            account = self.env['account.analytic.account'].create({
                'name': user.name,
                'company_id': company_id
            })
        return account

