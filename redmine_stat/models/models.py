# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RedmineUser(models.Model):

    _name = "redmine.user"
    redmine_login = fields.Char(string='Redmine Login', required=True)
    redmine_pass = fields.Char(string='Redmine Pass', required=True)
