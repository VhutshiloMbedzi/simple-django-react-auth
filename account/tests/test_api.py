from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from account.models import Profile
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountAPITestCase(APITestCase):

    #Register User

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

        first_url = reverse('account:register')
        first_data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        first_response = self.client.post(first_url, first_data, format='json')

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

    #Login User

    '''Can login a registred user'''
    def test_user_login(self):

        #Register
        register_url = reverse('account:register')
        register_data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        self.client.post(register_url, register_data, format='json')

        #Login
        url = reverse('account:login')
        data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    '''Incorrect Credentials    -   Password'''
    def test_user_login_wrong_password(self):

        #Register
        register_url = reverse('account:register')
        register_data = {
            'username': 'bean',
            'password': 'boom12345'
        }
        self.client.post(register_url, register_data, format='json')

        #Login
        url = reverse('account:login')
        data = {
            'username': 'bean',
            'password': 'boom12348'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    '''Incorrect Credentials    -   Not registered'''
    def test_user_login_fail(self):

        url = reverse('account:login')
        data = {
            'username': 'bean',
            'password': 'boom12348'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)