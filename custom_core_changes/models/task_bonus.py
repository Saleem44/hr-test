# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class TaskBonus(models.Model):
    _name = 'project.task.bonus'

    bonus = fields.Float(string="Bonus")
    performamce = fields.Integer(string="Performance")
    bonus_year = fields.Integer(string="Year")
    bonus_month = fields.Integer(string="Month")
    bonus_month_char = fields.Char(string="Month Name")
    # task_id = fields.Many2one('project.task', string="Task")
    employee_id = fields.Many2one('hr.employee', string="Employee")
