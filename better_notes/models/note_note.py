from odoo import models, fields, api
import hashlib


class NoteNote(models.Model):
    _inherit = "note.note"

    identifier = fields.Char(
        string="Public identifier",
        compute="_compute_public_identifier",
        store=True
    )
    href = fields.Char(
        string="Link",
        compute="_compute_public_identifier",
        store=True
    )
    public = fields.Boolean(
        string="Share note publically",
        default=False
    )

    _sql_constraints = [
        ("identifier_unique", "unique(identifier)", "This identifier already exists.")
    ]

    @api.depends("public")
    def _compute_public_identifier(self):
        for r in self:
            if r.public:
                # Use md5 sind the hash is shorter and we don't worry about too much security at this point
                r.identifier = hashlib.md5((r.name + str(r.create_date)).encode()).hexdigest()
                r.href = self.env["ir.config_parameter"].get_param("web.base.url", "http://example.com/")
                if not r.href.endswith("/"):
                    r.href += "/"
                r.href += "note/" + r.identifier
            else:
                r.identifier = ""
                r.href = ""
