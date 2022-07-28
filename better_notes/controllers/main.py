from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class ShareNotes(http.Controller):

    @http.route("/note/<string:note_id>", type="http", auth="public", website=True)
    def share_note(self, note_id=None):
        if note_id:
            note = request.env["note.note"].sudo().search([
                ("identifier", "=", note_id),
                ("public", "=", True)
            ], limit=1)
            if note.id:
                return request.render("better_notes.public_note", {
                    "content": note.memo
                })
        return request.render("better_notes.public_note", {
            "content": "<h1>No note found!</h1>"
        })
