from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)


class IdeaTags(models.Model):
    _name = "idea.tag"

    name = fields.Char(
        string="Tag Name",
        required=True,
    )
    color = fields.Integer(
        name="Color",
    )

    def _get_current_user(self):
        return self.env.user

    user_id = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=_get_current_user,
        required=True
    )
