from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    idea_ids = fields.One2many(
        string="Linked Ideas",
        comodel_name="idea.idea",
        inverse_name="project_id",
    )
