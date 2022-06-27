import json

from django.contrib.auth.models import User
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .. import models as APIModels


class SignUpTestCase(APITestCase):
    """ Класс тестирования регистрации """

    def test_sign_up(self):
        """ Регистрация пользователя test_case_user """
        data = {'username': 'test_case_user', 'email': 'test_case_user@example.com',
                'password': 'VeryStrongPWD_Approved'}
        response = self.client.post('/api/v1/auth/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class QuestionaryTestCase(APITestCase):
    """ Класс тестирования Вопросников """

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


class QuestionWithAnswersTestCase(APITestCase):
    """ Класс тестирования Вопросов с Ответами  """

    def setUp(self):
        """ Подготовка данных """

        # Создание пользователя и его токена
        self.user = User.objects.create_user(username='salmo', password='AnotherStrongPWD')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')  # Аутентификация пользователя

        # Создание Вопросника
        self.questionary = APIModels.Questionary.objects.create(caption='Валюта разных стран')

        # Создание Вопроса к Вопроснику
        self.question = APIModels.Question.objects.create(questionary=self.questionary,
                                                          text='В какой стране появились самые первые бумажные деньги?')

        # Создание Ответов на Вопрос
        self.answer_1 = APIModels.Answer.objects.create(question=self.question, text='В Китае', is_valid=True)
        self.answer_2 = APIModels.Answer.objects.create(question=self.question, text='В Швейцарии', is_valid=False)

    def test_question_api_view_authenticated_with_expected_data(self):
        """ Тестирование корректного получения доступа к Вопросу авторизованным пользователям """
        response = self.client.get(reverse_lazy('question', kwargs={'questionary_id': self.questionary.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Доступ получен
        self.assertEqual(response.data['next'], None,
                         '[!] Ожидалась одна страница, получено несколько.')  # Только одна страница
        self.assertEqual(response.data['results'][0]['questionary'],
                         self.questionary.pk,
                         '[!] Ожидаемая запись из вопросника не соответствует созданной.')
        self.assertEqual(response.data['results'][0]['text'], self.question.text,
                         '[!] Получен отличный от ожидаемого текст вопроса.')  # Корректный текст вопроса
        # Тестирование ответов:
        self.assertEqual(response.data['results'][0]['answer'][0]['text'], self.answer_1.text,
                         '[!] Получен отличный от ожидаемого текст 1-го ответа.')  # Корректный текст 1-го ответа
        self.assertEqual(response.data['results'][0]['answer'][0]['is_valid'], self.answer_1.is_valid,
                         '[!] Ожидалось, что 2-й ответ коректный, а полученный результат не удовлетворяет ожидания.')  # 1-й ответ - корректный
        self.assertEqual(response.data['results'][0]['answer'][1]['text'], self.answer_2.text,
                         '[!] Получен отличный от ожидаемого текст 1-го ответа.')  # Корректный текст 2-го ответа
        self.assertEqual(response.data['results'][0]['answer'][1]['is_valid'], self.answer_2.is_valid,
                         '[!] Ожидалось, что 2-й ответ коректный, а полученный результат не удовлетворяет ожидания.')  # 2-й ответ - корректный

    def test_question_api_view_un_authenticated(self):
        """ Тестирование получения доступа к Вопросу не авторизованным пользователям """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse_lazy('question', kwargs={'questionary_id': self.questionary.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserAnswerTestCase(APITestCase):
    """ Класс тестирования сохранения и получения Пользовательских ответов """

    def setUp(self):
        """ Подготовка данных """

        # Создание пользователя и его токена
        self.user = User.objects.create_user(username='salmo', password='AnotherStrongPWD')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')  # Аутентификация пользователя

        # Создание Вопросника
        self.questionary = APIModels.Questionary.objects.create(caption='Валюта разных стран')

        # Создание Вопроса к Вопроснику
        self.question = APIModels.Question.objects.create(questionary=self.questionary, text='Национальная валюта Венгрии')

        # Создание Ответов на Вопрос
        self.answer_1 = APIModels.Answer.objects.create(question=self.question, text='Евро', is_valid=False)
        self.answer_2 = APIModels.Answer.objects.create(question=self.question, text='Форинт', is_valid=True)
        self.answer_3 = APIModels.Answer.objects.create(question=self.question, text='Франк', is_valid=False)

    def test_trying_to_pass_quiz(self):
        """ Тестирование корректного сохранения пользовательского ответа """
        response = self.client.post(reverse_lazy('user-answer'),
                                    {'questionary': self.questionary.pk, 'answer': self.answer_1.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Сохранено
        self.assertEqual(json.loads(response.content),
                         {'questionary': self.questionary.pk, 'answer': self.answer_1.pk},
                         '[!] Ожидалось, что сохранение пройдет успешно, но полученные значения не соответствуют сохраненным')  # Сохранено

    def test_trying_to_access_quiz_page_unauthorized(self):
        """ Тестирование сохранения пользовательского ответа не авторизованным пользователем """
        self.client.force_authenticate(user=None)
        response = self.client.post(reverse_lazy('user-answer'),
                                    {'questionary': self.questionary, 'answer': self.answer_1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_trying_to_receive_quiz_results(self):
        """ Тестирование корректного получения пользовательских ответов """

        # Сохраняем ответ, прежде чем получить о нем информацию
        response = self.client.post(reverse_lazy('user-answer'),
                                    {'questionary': self.questionary.pk, 'answer': self.answer_2.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Сохранено
        # Сохранено успешно
        # Получаем результат назад
        response = self.client.get(reverse_lazy('user-answer-result', kwargs={'questionary_id': self.questionary.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Доступ получен
        # Проверяем полученные значения
        self.assertEqual(response.data[0]['answer']['text'], self.answer_2.text,
                         '[!] Получен отличный от ожидаемого и сохраненного текст ответа.')
        self.assertTrue(response.data[0]['answer']['is_valid'], '[!] Ожидалось, что ответ будет корректным.')  # is_valid=true

    def test_trying_to_receive_quiz_results_unauthorized(self):
        """ Тестирование получения доступа к результатам не авторизованным пользователем """
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse_lazy('user-answer-result', kwargs={'questionary_id': self.questionary.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
