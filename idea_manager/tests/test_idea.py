from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestIdea(TransactionCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.testUser = self.env["res.users"].create({
            "company_id": self.env.company.id,
            "login": "test",
            "name": "test",
            "groups_id": [4, self.env.ref("idea_manager.group_idea_manager_user").id]
        })
        self.user = self.env["res.users"].browse([1])
        self.idea1 = self.env["idea.idea"].create({
            "name": "My Idea",
            "user_id": 1
        })
        self.idea2 = self.env["idea.idea"].create({
            "name": "Test idea",
            "user_id": self.testUser.id
        })

    def test_idea_create(self):
        self.assertTrue(self.idea1.active)
        self.assertFalse(self.idea1.public)
        self.assertEqual(self.idea1.partner_id.id, self.user.partner_id.id)

    def test_idea_convert_project(self):
        self.assertTrue(self.idea1.active)
        self.assertFalse(self.idea1.project_id.id)
        self.assertFalse(self.idea1.project_id.active)

        self.idea1.action_convert_project()
        with self.assertRaises(UserError) as e:
            self.idea2.action_convert_project()

        self.assertEqual(self.idea1.active, False)
        self.assertTrue(self.idea1.project_id.active)

    def test_actions_archive_unarchive(self):
        self.assertTrue(self.idea1.active)
        self.assertTrue(self.idea2.active)

        self.idea1.action_archive()
        with self.assertRaises(UserError) as e:
            self.idea2.action_archive()
        self.idea2.with_user(self.testUser).action_archive()

        self.assertFalse(self.idea1.active)
        self.assertFalse(self.idea2.active)

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
