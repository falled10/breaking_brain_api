from datetime import timedelta

from django.utils import timezone
from mixer.backend.django import mixer
from rest_framework.test import APITestCase
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken

from authentication.models import User


class BaseAPITest(APITestCase):

    def create(self, email='test@mail.com', username='testuser', password='qwerty123456'):
        user = User.objects.create_user(email=email, username=username, password=password)
        user.last_login_date = timezone.now()
        user.is_active = True
        user.save()

        return user

    def create_and_login(self, email='test@mail.com', username='testuser', password='qwerty123456'):
        user = self.create(email=email, username=username, password=password)
        self.authorize(user)
        return user

    def authorize(self, user, **additional_headers):
        tok = generate_token()
        token = mixer.blend(AccessToken, user=user, expires=timezone.now() + timedelta(hours=1), token=tok)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}",
            **additional_headers
        )

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
