from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UserTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123!')
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)
        # Authenticate the client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_user_list(self):
        """Test API list view"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-list')
        response = self.client.get(url, {}, True)

        self.assertEqual(response.status_code, 200)

    def test_get_user_detail(self):
        """Test API detail view"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, {}, True)

        self.assertEqual(response.status_code, 200)

    def test_get_user_list_loggedout(self):
        """Test API list view when not authanticated"""
        self.client.logout()
        url = reverse('user-list')
        response = self.client.get(url, {}, True)

        self.assertEqual(response.status_code, 401)

    def test_get_user_detail_loggedout(self):
        """Test API detail view when not authanticated"""
        self.client.logout()
        url = reverse('user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, {}, True)

        self.assertEqual(response.status_code, 401)

    def test_create_user(self):
        """Test API user create"""
        url = reverse('user-list')
        response = self.client.post(url, {}, follow=True, format='json')

        self.assertEqual(response.status_code, 200)


class MessageTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123!')
        # Create a token for the test user
        self.token = Token.objects.create(user=self.user)
        # Authenticate the client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_all_messages(self):
        """Test API message list view"""
        self.client.force_authenticate(user=self.user)
        url = reverse('message-list')
        response = self.client.get(url, {}, True)

        self.assertEqual(response.status_code, 200)

    def test_create_message(self):
        """Test API create message when authanticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('message-list')
        response = self.client.post(url, {}, follow=True, format='json')

        self.assertEqual(response.status_code, 200)

    def test_create_message_loggedout(self):
        """Test API create message when not authanticated"""
        self.client.logout()

        url = reverse('message-list')
        response = self.client.post(url, {}, follow=True, format='json')

        self.assertEqual(response.status_code, 401)

    def test_get_unread_messages_by_user_staff_authenticated(self):
    # Create a staff user for testing unread message by user api
        staff_user = User.objects.create_user(username='staffuser', password='testpassword', is_staff=True)
        self.client.force_authenticate(user=staff_user)

        url = reverse('message-get_unread_message_by_user')  + f'?user_id={staff_user.id}'
        response = self.client.get(url, {}, follow=True)

        self.assertEqual(response.status_code, 200)

