# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectFlowWiz(models.TransientModel):
    _name = "project.bonsu.wiz"

    task_id = fields.Many2one('project.task', string="Task")
    bonus_offer = fields.Integer(string="Bonus Points")

    def approve_task(self):
        done_stage = self.env['project.task.type'].search([('name', '=ilike', 'Done')], limit=1)
        if done_stage:
            self.task_id.stage_id = done_stage.id
            self.task_id.task_bonus = self.bonus_offer

        return True
