Odoo Redmine Timesheets
---------------
The app allows transferring and synchronization objects from Redmine (project, issue, time entry) to Odoo (project,
task, employee, timesheet). The synchronization is set up by cron tasks.

A Simple User Interface
----------------------
1. Install app Redmine Timesheet.

2. Go to menu item Configuration --> Settings or Settings --> General Settings --> Redmine Timesheets
    - Set Redmine API Key
    - Set Redmine URL
    - Validate API Key and URL

3. Click Save and projects, tasks, timesheets, employees will be populated in odoo if doesn't exists.

4. Also cron task will be activated, and once in a day new data from redmine will be synced and populated in odoo.
