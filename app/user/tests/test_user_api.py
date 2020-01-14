from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
MY_URL = reverse('user:my')

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
        
    def test_create_token_for_user(self):
        """
        Test that a token is created for the user
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'testtest',
            
        }
        
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertAlmostEqual(res.status_code, status.HTTP_200_OK)
        
    def test_create_token_invalid_credential(self):
        """
        Test that token is not created if invalid credentials
        are given
        """
        create_user(email='test@gmail.com', password="testpass")
        payload = {
            'email': 'test@gmail.com',
            'password': 'strong'
        }
        
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_no_user(self):
        """
        Test that token is not created if user doesn't exist
        """
        payload = {
            'email': 'test@gmail.com',
            'password': 'strong'
        }
        
        res = self.client.post(TOKEN_URL, payload)
    
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_token_missing_field(self):
        """
        Test that email and password are required
        """
        res = self.client.post(TOKEN_URL, {'email': 'two', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_retrieve_user_unauthorized(self):
        """
        Test that authentication is required for users
        """ 
        res = self.client.get(MY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
class PrivateUserApiTest(TestCase):
    
    """
    Test API requests that require authentication 
    """
    
    def setUp(self):
        self.user = create_user(
            email= 'tester@gmail.com',
            name = 'tester',
            password = '654ERER'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
    def test_retrieve_profile_success(self):
        """
        Test retrieving profile for logged in user
        """"
        res = self.client.get(MY_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
        
    