# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

from odoo.osv import orm


_logger = logging.getLogger()


class RedmineTimeEntry(orm.Model):
    _name = 'redmine.hr.analytic.timesheet'
    _description = 'Redmine Time Entry Binding'
    _inherits = {'account.analytic.line': 'odoo_id'}

    _columns = {
        'odoo_id': fields.Many2one(
            'account.analytic.line', 'Timesheet', required=True,
            ondelete='cascade'
        ),
    }
