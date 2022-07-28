from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
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
    is_destroyed = fields.Boolean(
        string="Destroy?",
        help="Destroy this note after viewed once/twice/... or after a specific timestamp."
    )
    destroy_method = fields.Selection(
        string="Method of Destruction",
        selection=[
            ("once", "After viewed once"),
            ("x", "After viewed x times"),
            ("time", "After a specific timestamp")
        ],
        default="once"
    )
    destroy_max_count = fields.Integer(
        string="Destroy after (views)",
        help="View count after the note gets deleted."
    )
    public_views = fields.Integer()
    destroy_timestamp = fields.Datetime(
        string="Time of Destruction"
    )

    # FIXME: Throws error on fresh installation
    # duplicate key value violates unique constraint "note_note_identifier_unique"
    # DETAIL:  Key (identifier)=() already exists.
    # _sql_constraints = [
    #     ("identifier_unique", "unique(identifier)", "This identifier already exists.")
    # ]

    @api.model
    def create(self, vals):
        # Take care of password secured notes
        if vals["is_secured"]:
            if not vals["new_password"] or vals["new_password"].strip() == "":
                raise UserError(_("Please enter a password."))
        # Take care of note destruction
        if vals["is_destroyed"]:
            if  vals["destroy_method"] == "x" and vals["destroy_max_count"] <= 1:
                raise UserError(_("Please enter a max count above 1 if 'After viewed x times' is selected."))
            elif vals["destroy_method"] == "time" and datetime.strptime(vals["destroy_timestamp"], "%Y-%m-%d %H:%M:%S") < fields.Datetime.now():
                raise UserError(_("Please make sure the TIMESTAMP OF DESTRUCTION is not in past."))
        return super().create(vals)

    def write(self, vals):
        # Take care of password secured notes
        if "is_secured" in vals and vals["is_secured"]:
            if "new_password" not in vals or vals["new_password"].strip() == "":
                raise UserError(_("Please enter a password."))
        # Take care of note destruction
        if "is_destroyed" in vals and vals["is_destroyed"]:
            dm = vals["destroy_method"] if "destroy_method" in vals else self.destroy_method
            if dm == "x" and "destroy_max_count" in vals and vals["destroy_max_count"] <= 1:
                raise UserError(_("Please enter a max count above 1 if 'After viewed x times' is selected."))
            elif dm == "time" and "destroy_timestamp" in vals and datetime.strptime(vals["destroy_timestamp"], "%Y-%m-%d %H:%M:%S") < fields.Datetime.now():
                raise UserError(_("Please make sure the TIMESTAMP OF DESTRUCTION is not in past."))
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

    """Delete all notes with destroy mode set to timestamp and destory date in past"""
    @api.model
    def _vacuum_notes(self):
        notes = self.env["note.note"].search([
            ("is_destroyed", "=", True),
            ("destroy_method", "=", "time"),
            ("destroy_timestamp", "<", datetime.now())
        ])
        notes.unlink()
