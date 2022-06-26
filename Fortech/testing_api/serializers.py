""" Сериализаторы """

from rest_framework import serializers

from .models import Questionary, Question, Answer, UserAnswer


class AnswerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Ответами """

    class Meta:
        model = Answer
        fields = ('pk', 'text', 'is_valid')


class QuestionSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Вопросами """

    # Сериализация внешнего ключа с Ответ`ами. Использует строковое представление модели.
    answer = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('questionary', 'text', 'answer')  # 'questionary', ...


class QuestionarySerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Вопросниками """

    question = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Questionary
        fields = ('pk', 'caption', 'question')


class UserAnswerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с ответами пользователей """

    # Сериализация внешнего ключа с текущим пользователем.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # Сериализация внешнего ключа с текущим вопросником.
    questionary = serializers.PrimaryKeyRelatedField(read_only=True)
    # Сериализация внешнего ключа с ответом.
    answer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('user', 'questionary', 'answer')
