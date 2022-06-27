import json

from django.contrib.auth.models import User
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .. import models as APIModels, serializers as APISerializers


class SignUpTestCase(APITestCase):
    """ Класс тестирования регистрации """

    def test_sign_up(self):
        """ Регистрация пользователя test_case_user """
        data = {'username': 'test_case_user', 'email': 'test_case_user@example.com',
                'password': 'VeryStrongPWD_Approved'}
        response = self.client.post('/api/v1/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionAPIViewTestCase(APITestCase):
    """ Класс тестирования авторизация """

    def setUp(self):
        """ Создание пользователя и его токена """
        self.user = User.objects.create_user(username='salmo', password='AnotherStrongPWD')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        """ Аутентификация пользователя """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_questionary_api_view_authenticated(self):
        """ Тестирование получения доступа к Вопросникам авторизованным пользователям """
        response = self.client.get(reverse_lazy('questionary'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_questionary_api_view_un_authenticated(self):
        """ Тестирование получения доступа к Вопросникам не авторизованным пользователям """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse_lazy('questionary'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
