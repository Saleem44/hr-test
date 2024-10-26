# -*- coding: utf-8 -*-

from datetime import datetime, date

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning

import logging
_logger = logging.getLogger(__name__)


class Task(models.Model):
    _inherit = 'project.task'

    start_date = fields.Datetime(string="Start Date")
    actaul_end_date = fields.Datetime(string="Actual End Date")
    task_weight = fields.Integer(string="Weight", default=10)
    task_bonus = fields.Integer(string="Bonus Points")
    approve_reject_visibility = fields.Boolean(string="Approve Visibility", compute='_compute_task_approve_visibility')

    def start_task(self):
        self.start_date = fields.Datetime.now()
        inprogress = self.env['project.task.type'].search(['|', ('name', '=ilike', 'In Progress'), ('name', '=ilike', 'InProgress')], limit=1)
        if inprogress:
            self.stage_id = inprogress.id
    
        return True

    def submit_task(self):
        self.actaul_end_date = fields.Datetime.now()
        done_stage = self.env['project.task.type'].search(['|', ('name', '=ilike', 'Pending Approval'), ('name', '=ilike', 'PendingApproval')], limit=1)
        if done_stage:
            self.stage_id = done_stage.id

        return True
    
    def cancel_task(self):
        cancel_stage = self.env['project.task.type'].search(['|', ('name', '=ilike', 'Cancel'), ('name', '=ilike', 'Cancelled')], limit=1)
        if cancel_stage:
            self.stage_id = cancel_stage.id

        return True

    def _compute_task_approve_visibility(self):
        for rec in self:
            approve_reject_visibility = False
            if rec.stage_id.name in ('PendingApproval', 'Pending Approval'):
                approve_reject_visibility = True
            
            rec.approve_reject_visibility = approve_reject_visibility

    def approve_task(self):
        target = self.user_ids[0].employee_id.task_target
        if target:
            complted_month_tasks = self.user_ids[0].employee_id.monthly_completed_task_count()

            if complted_month_tasks > target:
                # Ask for Bonus
                return {
                    'name': _('Bonus'),
                    'type': 'ir.actions.act_window',
                    'res_model': 'project.bonsu.wiz',
                    'view_id': self.env.ref('custom_core_changes.proj_offer_bonus_wiz', False).id,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'context': {'default_task_id': self.id},
                    'target': 'new',
                }
    
        done_stage = self.env['project.task.type'].search([('name', '=ilike', 'Done')], limit=1)
        if done_stage:
            self.stage_id = done_stage.id

        return True

    def reject_task(self):
        self.actaul_end_date = False
        inprogress = self.env['project.task.type'].search(['|', ('name', '=ilike', 'In Progress'), ('name', '=ilike', 'InProgress')], limit=1)
        if inprogress:
            self.stage_id = inprogress.id

        return False
