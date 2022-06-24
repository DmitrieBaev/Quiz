from datetime import datetime
from django.test import TestCase

from testing_api.models import Answer, Question, Questionary


class QuestionaryModelTest(TestCase):
    """ Класс для тестирования модели с Вопросниками """

    @classmethod
    def setUp(cls):
        Questionary.objects.create(caption='Тестируемый вопросник')

    def test_questionary_string_representation(self):
        """ Правильное строковое представление модели Вопросник """
        qR = Questionary.objects.filter(caption='Тестируемый вопросник')
        self.assertEquals('Тестируемый вопросник', str(qR[0]))

    def test_questionary_caption_max_length(self):
        """ Правильная длина поля caption модели Вопросник """
        qR = Questionary.objects.filter(caption='Тестируемый вопросник')
        self.assertEquals(qR[0]._meta.get_field('caption').max_length, 100)

    def test_questionary_caption_label(self):
        """ Правильное отображение метки поля caption модели Вопросник """
        qR = Questionary.objects.filter(caption='Тестируемый вопросник')
        self.assertEquals(qR[0]._meta.get_field('caption').verbose_name,
                          'Название вопросника')

    def test_questionary_created_at_label(self):
        """ Правильное отображение метки поля created_at модели Вопросник """
        qR = Questionary.objects.filter(caption='Тестируемый вопросник')
        self.assertEquals(qR[0]._meta.get_field('created_at').verbose_name,
                          'Дата создания')


class QuestionModelTest(TestCase):
    """ Класс для тестирования модели с Вопросами в Вопроснике """

    @classmethod
    def setUp(cls):
        qR = Questionary.objects.create(caption='Тестируемый вопросник')
        Question.objects.create(questionary=qR, text='Тестируемый вопрос в вопроснике')

    def test_question_string_representation(self):
        """ Правильное строковое представление модели Вопрос """
        q = Question.objects.filter(text='Тестируемый вопрос в вопроснике')
        self.assertEquals('Тестируемый вопрос в вопроснике', str(q[0]))

    def test_question_text_max_length(self):
        """ Правильная длина поля text модели Вопрос """
        q = Question.objects.filter(text='Тестируемый вопрос в вопроснике')
        self.assertEquals(q[0]._meta.get_field('text').max_length, 500)

    def test_question_text_label(self):
        """ Правильное отображение метки поля text модели Вопрос """
        q = Question.objects.filter(text='Тестируемый вопрос в вопроснике')
        self.assertEquals(q[0]._meta.get_field('text').verbose_name,
                          'Текст вопроса')


class AnswerModelTest(TestCase):
    """ Класс для тестирования модели Ответ на Вопрос """

    @classmethod
    def setUp(cls):
        qR = Questionary.objects.create(caption='Тестируемый вопросник')
        q = Question.objects.create(questionary=qR, text='Тестируемый вопрос в вопроснике')
        Answer.objects.create(question=q, text='CORRECT Тестируемый ответ в вопросе', is_valid=True)
        Answer.objects.create(question=q, text='INCORRECT Тестируемый ответ в вопросе')

    def test_correct_answer_string_representation(self):
        """ Правильное строковое представление модели Ответ для КОРРЕКТНОГО варианта """
        a = Answer.objects.filter(text='CORRECT Тестируемый ответ в вопросе')
        self.assertEquals('CORRECT Тестируемый ответ в вопросе', str(a[0]))

    def test_incorrect_answer_string_representation(self):
        """ Правильное строковое представление модели Вопрос для НЕКОРРЕКТНОГО варианта """
        a = Answer.objects.filter(text='INCORRECT Тестируемый ответ в вопросе')
        self.assertEquals('INCORRECT Тестируемый ответ в вопросе', str(a[0]))

    def test_correct_answer_handle(self):
        """ Правильная обработка КОРРЕКТНОГО варианта Ответ`а """
        a = Answer.objects.filter(text='CORRECT Тестируемый ответ в вопросе')
        self.assertTrue(a[0].is_valid)

    def test_incorrect_answer_handle(self):
        """ Правильная обработка НЕКОРРЕКТНОГО варианта Ответ`а """
        a = Answer.objects.filter(text='INCORRECT Тестируемый ответ в вопросе')
        self.assertFalse(a[0].is_valid)

    def test_answer_text_label(self):
        """ Правильное отображение метки поля text модели Ответ """
        a = Answer.objects.filter(text='CORRECT Тестируемый ответ в вопросе')
        self.assertEquals(a[0]._meta.get_field('text').verbose_name,
                          'Правильно?')

    def test_answer_text_max_length(self):
        """ Правильное отображение метки поля text модели Ответ """
        a = Answer.objects.filter(text='CORRECT Тестируемый ответ в вопросе')
        self.assertEquals(a[0]._meta.get_field('text').max_length, 250)
