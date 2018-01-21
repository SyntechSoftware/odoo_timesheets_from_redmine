from odoo import api, fields, models, _


class RedmineApiSettings(models.TransientModel):
    _name = 'redmine.timesheets.config.settings'
    _inherit = 'res.config.settings'

    url = fields.Char(string=_('Redmine base URL'), required=True)
    api_key = fields.Char(string='Redmine API KEY', required=True)

    @api.model
    def get_default_api_credentials(self, *args):
        return {
            'url': self.env['ir.config_parameter'].sudo().get_param('redmine_timesheet.url', default=''),
            'api_key': self.env['ir.config_parameter'].sudo().get_param('redmine_timesheet.api_key', default=''),
        }

    @api.one
    def set_api_credentials(self):
        self.env['ir.config_parameter'].sudo().set_param('redmine_timesheet.url', self.url, groups=['base.group_system'])
        self.env['ir.config_parameter'].sudo().set_param('redmine_timesheet.api_key', self.api_key, groups=['base.group_system'])