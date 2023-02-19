from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestIdea(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.idea1 = self.env["idea.idea"].create({
            "name": "My Idea",
            "user_id": 1
        })
        self.user = self.env["res.users"].browse([1])

    def test_idea_create(self):
        self.assertTrue(self.idea1.active)
        self.assertFalse(self.idea1.public)
        self.assertEqual(self.idea1.partner_id.id, self.user.partner_id.id)

    def test_idea_convert_project(self):
        self.assertTrue(self.idea1.active)
        self.assertFalse(self.idea1.project_id.id)
        self.assertFalse(self.idea1.project_id.active)

        self.idea1.action_convert_project()

        self.assertEqual(self.idea1.active, False)
        self.assertTrue(self.idea1.project_id.active)

    def test_idea_convert_task(self):
        self.idea1.action_convert_project()
        idea = self.env["idea.idea"].create({
            "name": "Another idea",
            "user_id": 1
        })
        
        self.assertTrue(idea.active)
        self.assertFalse(idea.task_id.id)
        with self.assertRaises(ValidationError) as e:
            idea.action_convert_task()

        idea.project_id = self.idea1.project_id
        idea.action_convert_task()

        self.assertFalse(idea.active)
        self.assertTrue(idea.task_id.active)
