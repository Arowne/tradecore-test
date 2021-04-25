from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User


class AccountTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.access_token = None

        user = User.objects.create_user(
            last_name="Lastname",
            first_name="Firstname",
            email="exemple@exemple.com",
            username="exemple@exemple.com",
            password='password1234'
        )

    def test_valid_login_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_valid_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple3@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_valid_missing_value(self):

        url = '/token'
        data = {'username': '', 'password': ''}
        response = self.client.post(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)       
        
    def test_create_valid_value(self):

        url = '/user/'
        data = {
                'last_name': "Lastname",
                'first_name': "Firstname",
                'email': "test@exemple.com",
                'username': "test@exemple.com",
                'password': "password1234",
                'confirm_password': "password1234",
            }
        response = self.client.post(url, data, format='json')
        
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_value(self):

        url = '/user/'
        data = {
                'last_name': "1Lastname",
                'first_name': "1Firstname",
                'email': "exemple@exemple.com",
                'password': "password123",
                'confirm_password': "",
            }
        
        response = self.client.post(url, data, format='json')
        
        data = response.json()
        
        self.assertTrue(True, data['errors']['first_name'])
        self.assertTrue(True, data['errors']['last_name'])
        self.assertTrue(True, data['errors']['email'])
        self.assertTrue(True, data['errors']['password'])
        self.assertTrue(True, data['errors']['confirm_password'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_missing_value(self):

        url = '/user/'
        data = {
                'last_name': "",
                'first_name': "",
                'email': "",
                'password': "",
                'confirm_password': "",
            }
        
        response = self.client.post(url, data, format='json')
        
        data = response.json()
        
        self.assertTrue(True, data['errors']['first_name'])
        self.assertTrue(True, data['errors']['last_name'])
        self.assertTrue(True, data['errors']['email'])
        self.assertTrue(True, data['errors']['password'])
        self.assertTrue(True, data['errors']['confirm_password'])
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_read_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        response = self.client.get(url, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_read_missing_token_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        
        url = '/user/'
        
        response = self.client.get(url, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        data = {
                'last_name': "Lastname",
                'first_name': "Firstname",
                'pseudo': 'pseudo',
                'email': "test@exemple.com",
                'password': "password1234",
            }
        
        response = self.client.put(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_missing_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        data = {
                'last_name': "",
                'first_name': "",
                'pseudo': '',
                'email': "",
                'password': "",
            }
        
        response = self.client.put(url, data, format='json')
        data = response.json()
        
        self.assertTrue(True, data['errors']['last_name'])
        self.assertTrue(True, data['errors']['first_name'])
        self.assertTrue(True, data['errors']['pseudo'])
        self.assertTrue(True, data['errors']['email'])
        self.assertTrue(True, data['errors']['password'])
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        data = {
                'last_name': "1Lastname",
                'first_name': "1Firstname",
                'pseudo': "",
                'email': "email",
                'password': "ksjksjd",
            }
        
        response = self.client.put(url, data, format='json')
        data = response.json()
        
        self.assertTrue(True, data['errors']['last_name'])
        self.assertTrue(True, data['errors']['first_name'])
        self.assertTrue(True, data['errors']['pseudo'])
        self.assertTrue(True, data['errors']['email'])
        self.assertTrue(True, data['errors']['password'])
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
           
    def test_delete_invalid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        data = {
                'password': "password123",
            }
        
        response = self.client.delete(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_missing_token_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        
        url = '/user/'
        
        data = {
                'password': "password123",
            }
        
        response = self.client.delete(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_zeta_delete_valid_value(self):

        url = '/token'
        data = {'username': 'exemple@exemple.com', 'password': 'password1234'}
        response = self.client.post(url, data, format='json')
        data = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        
        url = '/user/'
        
        data = {
                'password': "password1234",
            }
        
        response = self.client.delete(url, data, format='json')
        data = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)