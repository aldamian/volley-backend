from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', 'testpassword', 'Admin', 'test', 'test',)
        self.assertEqual(str(super_user), 'testuser@super.com')
        self.assertEqual(super_user.role, 'Admin')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
