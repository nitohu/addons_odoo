from odoo import models, fields, api


class IdeaCategory(models.Model):
    _name = "idea.category"
    _order = "sequence, id"

    active = fields.Boolean(
        default=True,
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    short_desc = fields.Char(
        string="Short Description",
    )
    idea_ids = fields.One2many(
        string="Ideas",
        comodel_name="idea.idea",
        inverse_name="category_id",
    )
    idea_count = fields.Integer(
        string="Number of ideas",
        compute="_get_idea_count",
    )

    def _get_default_user(self):
        return self.env.user

    user_id = fields.Many2one(
        comodel_name="res.users",
        default=_get_default_user,
        required=True
    )

    @api.depends("idea_ids")
    def _get_idea_count(self):
        for r in self:
            r.idea_count = len(r.idea_ids)
