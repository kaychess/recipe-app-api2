from django.test import TestCase
# it's recommended to use get_user_model rather to user model directly
# for flexibility of changing user model later in settings.
from django.contrib.auth import get_user_model


class TestUserModel (TestCase):
    ''' Test if, Can we create a User '''

    def test_create_user_with_email_successfully(self):
        # need NOT be a valid email or password.
        email = 'test@menuroma.com'
        password = 'ABC@123'

        # Creates a user using the configured user model.
        # Note : object with data is created, but not saved yet.
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        ''' Test the email for a new user is normalized '''
        email = 'test@MENUROMA.COM'
        password = 'ABC@123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid(self):
        ''' Test creating user with no email raises error '''
        # Anything that runs in 'with' block has to raise a value error
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password='ABC@123')

    def test_create_new_super_user(self):
        ''' Test creating new super user '''
        # need NOT be a valid email or password.
        email = 'superUser@menuroma.com'
        password = 'ABC@123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
