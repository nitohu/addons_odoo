from odoo import http
from odoo.http import request
from datetime import datetime
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

    def _check_deletion(self, note):
        if not note.is_destroyed:
            return
        # No need to check for time here, since it will be removed by cron
        if note.destroy_method == "once":
            note.unlink()
        elif note.destroy_method == "x":
            note.public_views += 1
            if note.public_views >= note.destroy_max_count:
                note.unlink()

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
                        # Prevent notes with timestamp deletion from being opened if cron didn't ran yet
                        if note.is_destroyed and note.destroy_method == "time" and note.destroy_timestamp < datetime.now():
                            data["authorized"] = False
                        self._check_deletion(note)
                return request.render("better_notes.public_note", data)
        return request.render("better_notes.note_not_found")
