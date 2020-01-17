from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='test1@gmail.com', password='testpass12'):
    """
    Creates sample user
    """
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    
    def test_create_user_with_email_successful(self):
        """
        Testing creation of a new user with Email address
        """
        name = 'Test'
        email = 'test123@users.com'
        password = 'Pass1234'
        user = get_user_model().objects.create_user(
            email= email,
            name = name,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertTrue(user.check_password(password))
        
    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized
        """
        email = 'test123@users.com'
        user = get_user_model().objects.create_user(email, 'test')
        
        self.assertEqual(user.email, email.lower())
        
    def test_new_user_invalid_email(self):
        
        """
        Tests for Valid Email address
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
            
    
    def test_create_new_super_user(self):
        """
        Test create super user
        """
        user = get_user_model().objects.create_superuser(
            'test123@users.com',
            'Pass1234'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    def test_tag_str(self):
        """
        Test the tag string representation
        """
        tag = models.Tag.objects.create(
            user= sample_user(),
            name= 'Vegan'
        )
        
        self.assertEqual(str(tag), tag.name)
        
    