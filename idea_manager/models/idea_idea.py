from odoo import models, fields, _
from odoo.exceptions import ValidationError


class IdeaIdea(models.Model):
    _name = "idea.idea"
    _inherit = ["mail.thread"]
    _order = "sequence, id"

    active = fields.Boolean(
        default=True
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
    )
    name = fields.Char(
        string="Title",
        required=True,
        tracking=True
    )
    public = fields.Boolean(
        string="Share Publically",
        default=False,
        tracking=True
    )
    description = fields.Html(
        string="Description"
    )
    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="idea.tag",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="idea.category",
        tracking=True
    )
    project_id = fields.Many2one(
        string="Project",
        description="Project linked to the idea",
        comodel_name="project.project",
        tracking=True
    )
    task_id = fields.Many2one(
        string="Linked Task",
        description="Created task from idea",
        comodel_name="project.task",
        tracking=True
    )

    def _get_current_user(self):
        return self.env.user

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=_get_current_user,
        required=True,
    )

    def action_convert_project(self):
        self.ensure_one()
        rec = {
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id.id
        }
        project = self.env["project.project"].create(rec)
        self.project_id = project.id
        self.active = False
        return {
            "name": project.name,
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "view_mode": "form",
            "res_id": project.id
        }

    def action_convert_task(self):
        self.ensure_one()
        rec = {
            "name": self.name,
            "description": self.description,
            "user_ids": [self.user_id.id],
        }
        if not self.project_id:
            # TODO: Open Dialog where user can choose a project
            raise ValidationError(_("Please link this idea to a Project."))
        rec["project_id"] = self.project_id.id
        task = self.env["project.task"].create(rec)
        self.task_id = task
        self.active = False
        return {
            "name": task.name,
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "form",
            "res_id": task.id
        }
