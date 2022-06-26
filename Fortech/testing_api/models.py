""" Модели """
from django.contrib.auth.models import User
from django.db import models


class Questionary(models.Model):
    """ Вопросник (Набор тестов) """

    caption = models.CharField(max_length=100, verbose_name='Название вопросника')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'Вопросник'
        verbose_name_plural = 'Вопросники'
        ordering = ('-created_at',)


class Question(models.Model):
    """ Вопрос """

    questionary = models.ForeignKey(Questionary, related_name='question', on_delete=models.PROTECT)
    text = models.CharField(max_length=500, verbose_name='Текст вопроса')

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)
        self.__total_answers__ = None  # Всего ответов          NEW INSTANCE FIELD
        self.__valid_answers__ = None  # Правильных ответов     NEW INSTANCE FIELD

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('questionary_id',)


class Answer(models.Model):
    """ Ответ на вопрос """

    question = models.ForeignKey(Question, related_name='answer', on_delete=models.PROTECT)
    text = models.CharField(max_length=250, verbose_name='Текст ответа')
    is_valid = models.BooleanField(default=False, verbose_name='Правильно?')

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<Answer {self.pk}: {self.text}>'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('question_id',)


class UserAnswer(models.Model):
    """ Пользовательский ответ """

    user = models.ForeignKey(User, related_name='user', verbose_name='Пользователь', on_delete=models.CASCADE)
    questionary = models.ForeignKey(Questionary, related_name='user_questionary', verbose_name='Вопросник', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='user_answer', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Ответы пользователя'
        verbose_name_plural = 'Ответы пользователей'
        ordering = ('pk',)
