from odoo import models, fields, api
import hashlib


class NoteNote(models.Model):
    _inherit = "note.note"

    identifier = fields.Char(
        string="Public identifier",
        compute="_compute_public_identifier",
        store=True
    )
    public = fields.Boolean(
        string="Share note publically",
        default=False
    )

    @api.depends("public")
    def _compute_public_identifier(self):
        for r in self:
            if r.public:
                # Use md5 sind the hash is shorter and we don't worry about too much security at this point
                r.identifier = hashlib.md5(r.name.encode()).hexdigest()
            else:
                r.identifier = ""
