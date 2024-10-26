# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    bonus_ids = fields.One2many('project.task.bonus', 'employee_id', string="Bonus")
    task_target = fields.Integer(string="Task Target")
    current_month_percentage = fields.Char(string="Month %", compute='_compute_emp_progress')
    avg_year_percentage = fields.Char(string="Year Average %", compute='_compute_emp_progress')


    def create(self, vals):
        dept_id = vals.get('department_id')
        if vals.get('task_target') == 0 and dept_id:
            dept_obj = self.env['hr.department'].browse(dept_obj)
            vals['task_target'] = dept_obj.task_target

        return super().create(vals)

    @api.onchange('department_id')
    def onchange_department_id(self):
        if self.department_id and self.task_target == 0:
            self.task_target = self.department_id.task_target

    def monthly_completed_task_count(self):
        current_month = datetime.now().replace(day=1, hour=0, minute=0)
        # current_year = datetime.now().replace(month=1, day=1, hour=0, minute=0)
        complted_month_tasks = self.env['project.task'].sudo().search_count([
            ('actaul_end_date', '>=', current_month), ('user_ids', 'in', [self.user_id.id])])

        return complted_month_tasks

    def _compute_emp_progress(self):
        for rec in self:
            current_month_percentage = 0
            avg_year_percentage = 0
            taget = rec.task_target or rec.department_id.task_target
            if taget:
                complted_month_tasks = rec.monthly_completed_task_count()
                current_month_percentage = (complted_month_tasks/taget) * 100
                performamce = rec.bonus_ids.filtered(lambda obj: obj.bonus_year == datetime.now().year).mapped('performamce')
                if performamce:
                    avg_year_percentage = sum(performamce)/len(performamce)


            rec.current_month_percentage = current_month_percentage
            rec.avg_year_percentage = avg_year_percentage

    @api.model
    def _cron_assign_past_month_bonus(self):
        all_employee = self.search([])
        today = datetime.now()
        first_day_of_current_month  = today.replace(day=1, hour=0, minute=0)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        for emp in all_employee:
            complted_bonus_tasks = self.env['project.task'].sudo().search_count([
                ('actaul_end_date', '>=', first_day_of_previous_month), 
                ('actaul_end_date', '<=', last_day_of_previous_month),
                ('task_bonus', '>', 0),
                ('user_ids', 'in', [emp.user_id.id])])

            bonus_vals = {
                'bonus_year': last_day_of_previous_month.year,
                'bonus_month': last_day_of_previous_month.month,
                'bonus_month_char': last_day_of_previous_month.strftime('%B'),
                'employee_id': emp.id,
                'bonus': 0,
                'performamce': 100,
            }
            if complted_bonus_tasks:
                total_bonus = sum(complted_bonus_tasks.mapped('task_bonus'))
                bonus_vals['bonus'] = total_bonus
                bonus_vals['performamce'] += total_bonus

            self.env['project.task.bonus'].create(bonus_vals)


class Department(models.Model):
    _inherit = 'hr.department'

    task_target = fields.Integer(string="Task Target", default=10)
