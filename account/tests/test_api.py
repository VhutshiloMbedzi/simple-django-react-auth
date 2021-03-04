from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from account.models import Profile
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountAPITestCase(APITestCase):

    '''Can register a new user'''
    def test_user_registration(self):
        url = reverse('account:register')
        data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(username='bean')
        self.assertTrue(new_user)

    '''Duplicating a username should be a bad request'''
    def test_duplicate_username_fail(self):

        url = reverse('account:register')
        data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        first_response = self.client.post(url, data, format='json')

        url = reverse('account:register')
        data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    '''Password with len lower than 5 should be a bad request'''
    def test_password_too_small_fail(self):
        url = reverse('account:register')
        data = {
            'username': 'juan',
            'password': 'boom'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    '''Profile should be created for the new user'''
    def test_profile_created(self):
        url = reverse('account:register')
        data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        profile = Profile.objects.get(name='bean')
        self.assertTrue(profile)