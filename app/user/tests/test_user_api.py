from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**param):
    return get_user_model().objects.create_user(**param)



class PublicUserApiTests(TestCase):
    """
    Test  users API (public)
    """
    def setup(self):
        self.client = APIClient()
        
    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        """
        payload = {
            'email': 'tester@gmail.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_paasword(payload['password']))
        self.assertNotIn('password', res.data)
        
    def test_user_exists(self):
        """
        Test for already existing user
        """
        payload = {
            'email': 'tester@gmail.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        create_user(**payload)
        
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters
        """
        payload = {
            'email': 'tester@gmail.com',
            'password': 'test',
            'name': 'Test2 name'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        
        self.assertFalse(user_exists)
        
        