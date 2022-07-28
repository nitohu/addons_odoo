from odoo import http
from odoo.http import request
import hashlib
import logging

_logger = logging.getLogger(__name__)


class ShareNotes(http.Controller):

    def _build_data(self, note):
        return {
            "content": note.memo,
            "is_secured": note.is_secured,
            "authorized": False
        }

    def _authorize(self, passwd, note):
        h = hashlib.sha256(passwd.encode()).hexdigest()
        if h == note.password:
            return True
        return False

    @http.route("/note/<string:note_id>", type="http", auth="public", website=True)
    def share_note(self, note_id=None):
        if note_id:
            note = request.env["note.note"].sudo().search([
                ("identifier", "=", note_id),
                ("public", "=", True)
            ], limit=1)
            if note.id:
                data = self._build_data(note)
                if request.httprequest.method == "POST":
                    passwd = request.httprequest.form.get("password", False)
                    # Authorize
                    if passwd and self._authorize(passwd, note):
                        data["authorized"] = True
                return request.render("better_notes.public_note", data)
        return request.render("better_notes.public_note", {
            "content": "<h1>No note found!</h1>"
        })
