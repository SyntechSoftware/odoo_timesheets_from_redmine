# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

import requests

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    redmine_api_key = fields.Char(
        # related='website_id.twitter_api_key',
        string='Redmine API Key',
        help='Redmine API key you can get it from redmine url/my/account')
    redmine_url = fields.Char(
        # related='website_id.twitter_api_secret',
        string='Redmine site url',
        help='Root url of your redmine site')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            redmine_api_key=self.env['ir.config_parameter'].sudo().get_param('redmine_timesheet.redmine_api_key'),
            redmine_url=self.env['ir.config_parameter'].sudo().get_param('redmine_timesheet.redmine_url')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('redmine_timesheet.redmine_url', self.redmine_url)
        self.env['ir.config_parameter'].sudo().set_param('redmine_timesheet.redmine_api_key', self.redmine_api_key)

    @api.model
    def create(self, vals):
        RedmineConfig = super(ResConfigSettings, self).create(vals)
        if vals.get('redmine_api_key') or vals.get('redmine_url'):
            RedmineConfig._check_redmine_authorization(vals)

        self.env['redmine.hr.analytic.timesheet'].sync_data_from_redmine(api_key=vals.get('redmine_api_key'),
                                                                         url=vals.get('redmine_url'))
        return RedmineConfig

    @api.multi
    def write(self, vals):
        RedmineConfig = super(ResConfigSettings, self).write(vals)
        if vals.get('redmine_api_key') or vals.get('redmine_url'):
            self._check_redmine_authorization(vals)
        return RedmineConfig

    def _check_redmine_authorization(self, vals):
        _logger.info(self.env['ir.config_parameter'].sudo().get_param('redmine_timesheet.redmine_url'))
        try:
            from redminelib import Redmine
        except ImportError:
            raise UserError(_('Missing python dependency, check https://python-redmine.com/'))

        redmine = Redmine(vals.get('redmine_url'), key=vals.get('redmine_api_key'))

        try:
            redmine.auth()
        except Exception as e:
            raise UserError(_(e))

