from odoo import models, fields, api, _
from odoo.exceptions import UserError
import hashlib
import logging
_logger = logging.getLogger(__name__)


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
    is_secured = fields.Boolean(
        string="Secure with password",
        help="Secure your public note with a password.",
        default=False
    )
    password = fields.Char()
    new_password = fields.Char(
        compute="_reset_new_password",
        inverse="_encrypt_password"
    )

    # FIXME: Throws error on fresh installation
    # duplicate key value violates unique constraint "note_note_identifier_unique"
    # DETAIL:  Key (identifier)=() already exists.
    # _sql_constraints = [
    #     ("identifier_unique", "unique(identifier)", "This identifier already exists.")
    # ]

    @api.model
    def create(self, vals):
        if vals["is_secured"]:
            if not vals["new_password"] or vals["new_password"].strip() == "":
                raise UserError(_("Please enter a password."))
        return super().create(vals)

    def write(self, vals):
        if "is_secured" in vals and vals["is_secured"]:
            if "new_password" not in vals or vals["new_password"].strip() == "":
                raise UserError(_("Please enter a password."))
        return super().write(vals)

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

    def _reset_new_password(self):
        for r in self:
            r.new_password = ""

    @api.depends("new_password")
    def _encrypt_password(self):
        for r in self:
            if r.new_password:
                r.password = hashlib.sha256(r.new_password.encode()).hexdigest()
                r.new_password = ""
