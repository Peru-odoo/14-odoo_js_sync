# Copyright 2020 Ivan Yelizariev <https://twitter.com/yelizariev>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import api, fields, models


class SyncTriggerAutomation(models.Model):

    _name = "sync.trigger.automation"
    _inherit = ["sync.trigger.mixin", "sync.trigger.mixin.actions"]
    _description = "DB Trigger"
    _sync_handler = "handle_db"
    _default_name = "DB Trigger"

    automation_id = fields.Many2one(
        "base.automation", delegate=True, required=True, ondelete="cascade"
    )

    def start(self, records):
        if self.active:
            self.sync_task_id.start(self, args=(records,))

    def get_code(self):
        return (
            """
env["sync.trigger.automation"].browse(%s).sudo().start(records)
"""
            % self.id
        )

    def name_get(self):
        result = []
        for r in self:
            result.append((r.id, r.trigger_name))
        return result

    @api.onchange("model_id")
    def onchange_model_id(self):
        self.model_name = self.model_id.model

    @api.onchange("trigger")
    def onchange_trigger(self):
        if self.trigger in ["on_create", "on_create_or_write", "on_unlink"]:
            self.filter_pre_domain = (
                self.trg_date_id
            ) = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger in ["on_write", "on_create_or_write"]:
            self.trg_date_id = self.trg_date_range = self.trg_date_range_type = False
        elif self.trigger == "on_time":
            self.filter_pre_domain = False

    @api.model
    def create(self, vals):
        vals.setdefault("name", '%s %s: %s %s' % (self.sync_task_id.project_id.name, self._default_name, self.sync_task_id.name, vals.get('trigger_name', self.trigger_name)))
        return super(SyncTriggerAutomation, self).create(vals)

    def write(self, vals):
        for record in self:
            vals['name'] = '%s %s: %s %s' % (self.sync_task_id.project_id.name, self._default_name, self.sync_task_id.name, vals.get('trigger_name', record.trigger_name))
            super(SyncTriggerAutomation, record).write(vals)
        return True

    def unlink(self):
        for record in self:
            related_automation = record.automation_id
            if super(SyncTriggerAutomation, record).unlink() and related_automation:
                related_automation.unlink()
        return True