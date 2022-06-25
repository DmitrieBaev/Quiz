""" Сериализаторы """

from rest_framework import serializers

from .models import Questionary, Question, Answer, UserAnswer


class QuestionarySerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Вопросниками """

    class Meta:
        model = Questionary
        fields = ('pk', 'caption',)


class AnswerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Ответами """

    class Meta:
        model = Answer
        fields = ('pk', 'text', 'is_valid')


class QuestionSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Вопросами """

    # Сериализация внешнего ключа с Ответ`ами. Использует строковое представление модели.
    answer = AnswerSerializer(many=True, read_only=True)
    # Cериализация внешнего ключа с Вопросник`ами. Будет повторяться для каждого вопроса.
    # В случае, когда выводится только один вопрос на страницу - это может быть допустимо,
    # Когда на странице нужно выводить несколько вопросов - имеет смысл перекинуть
    #   # всю сериализацию внешних ключей в Questionary
    questionary = QuestionarySerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('questionary', 'text', 'answer')


class UserAnswerSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели с Ответами Пользователей """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # В скрытое поле помещается объект текущего пользователя

    class Meta:
        model = UserAnswer
        fields = ('answer',)

# class RandomQuestionSerializer(serializers.ModelSerializer):
#     # answer = serializers.StringRelatedField(many=True)
#     answer = AnswerSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Question
#         fields = ('questionary', 'text', 'answer')
