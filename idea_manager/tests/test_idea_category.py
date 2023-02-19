from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestIdea(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.category1 = self.env["idea.category"].create({
            "name": "First Category",
            "user_id": 1
        })

    def test_idea_count(self):
        idea1 = self.env["idea.idea"].create({
            "name": "First Idea",
            "user_id": 1,
            "category_id": self.category1.id
        })
        idea2 = self.env["idea.idea"].create({
            "name": "Second Idea",
            "user_id": 1,
            "category_id": self.category1.id
        })
        idea3 = self.env["idea.idea"].create({
            "name": "Third Idea",
            "user_id": 1
        })

        self.assertEqual(self.category1.idea_count, 2)

        idea3.category_id = self.category1

        self.assertEqual(self.category1.idea_count, 3)
