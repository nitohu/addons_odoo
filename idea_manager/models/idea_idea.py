from odoo import models, fields


class IdeaIdea(models.Model):
    _name = "idea.idea"

    active = fields.Boolean(
        default=True
    )
    name = fields.Char(
        string="Title",
        required=True,
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
        comodel_name="idea.category"
    )
    project_id = fields.Many2one(
        string="Project",
        description="Project linked to the idea",
        comodel_name="project.project",
    )

    def _get_current_user(self):
        return self.env.user

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=_get_current_user,
        required=True,
    )

