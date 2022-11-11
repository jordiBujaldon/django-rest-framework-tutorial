from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    def test_superuser_content(self):
        CustomUser.objects.create_superuser(email='user@user.com', user_name='user', first_name='', password='1234')
        superuser = CustomUser.objects.get(id=1)
        # Asserts
        self.assertEqual(f'{superuser.email}', 'user@user.com')
        self.assertEqual(f'{superuser.user_name}', 'user')
        self.assertEqual(f'{superuser.first_name}', '')
        self.assertTrue(superuser.is_superuser)

    def test_fail_superuser_content(self):
        # is_staff error
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='user@user.com', user_name='user', first_name='',
                                                password='1234', is_staff=False)
        # is_superuser error
        with self.assertRaises(ValueError):
            CustomUser.objects.create_superuser(email='user@user.com', user_name='user', first_name='',
                                                password='1234', is_superuser=False)

    def test_user_email_not_provided(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', user_name='user', first_name='', password='1234', is_staff=False)
