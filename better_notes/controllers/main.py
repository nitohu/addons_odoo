from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class ShareNotes(http.Controller):

    @http.route("/note/<string:note_id>", type="http", auth="public", website=True)
    def share_note(self, note_id=None):
        _logger.info(f"Note ID: {note_id}")
        if note_id:
            note = request.env["note.note"].search([
                ("identifier", "=", note_id),
                ("public", "=", True)
            ])
            if note.id:
                return note.memo
        return "<h1>No note found!</h1>"
