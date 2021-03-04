from django.test import TestCase

from account.models import Profile

import tempfile

from django.contrib.auth import get_user_model

User = get_user_model()

class AccountTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="juan",
            password="boom12345"
        )

        self.other_user = User.objects.create_user(
            username="bean",
            password="boom12345"
        )

    ''' Profile should be created when a user was created,
        During set up
    '''
    def test_profile_created(self):
        profiles = Profile.objects.all()

        #since we created 2 users, we should have 2 profiles
        self.assertEqual(profiles.count(), 2)

    ''' User deletion, should also delete the profile '''
    def test_delete_user_deletes_profile(self):
        self.user.delete()

        profiles = Profile.objects.all()
        self.assertEqual(profiles.count(), 1)

    ''' Profile should have the User's username '''
    def test_profile_username(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.name, self.user.username)

    #update tests

    def test_profile_update_without_image(self):
        Profile.objects.filter(user=self.user).update(name='Mike', bio="Just a new user.")
        profile = Profile.objects.get(user=self.user)

        self.assertEqual(profile.name, "Mike")
        self.assertEqual(profile.bio, "Just a new user.")
        self.assertFalse(profile.image)

    def test_profile_update_with_image(self):
        temp_image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        
        Profile.objects.filter(user=self.user).update(image=temp_image)
        profile = Profile.objects.get(user=self.user)

        self.assertTrue(profile.image)