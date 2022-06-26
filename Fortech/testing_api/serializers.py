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

    # Cериализация внешнего ключа с Вопросник`ами. Будет повторяться для каждого вопроса.
    # В случае, когда выводится только один вопрос на страницу - это может быть допустимо,
    # Когда на странице нужно выводить несколько вопросов - имеет смысл перекинуть
    #   # всю сериализацию внешних ключей в Questionary
    # questionary = QuestionarySerializer(read_only=True)

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
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    questionary = serializers.PrimaryKeyRelatedField(read_only=True)
    answer = serializers.PrimaryKeyRelatedField(read_only=True)
    # answer = AnswerSerializer(many=True, read_only=True)
    # answer = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # answer = serializers.PrimaryKeyRelatedField(source='unit', queryset=Unit.objects.all())

    class Meta:
        model = UserAnswer
        fields = ('user', 'questionary', 'answer')


    # class UserAnswerSerializer(serializers.ModelSerializer):
    #     def validate(self, data):
    #         errors = {}
    #
    #         # Обязательные поля
    #         required_fields = ['user', 'questionary', 'answers']
    #         for field in required_fields:
    #             if field not in data:
    #                 errors[field] = 'Обязательное поле.'
    #
    #         if errors:
    #             raise serializers.ValidationError(errors)
    #
    #         return data
    #
    #     def create(self, validated_data):
    #         user_answer = UserAnswer.objects.create(
    #             user=validated_data['user'],
    #             questionary=validated_data['questionary'],  # Скрытое поле с идентификатором Вопросника
    #             answer=validated_data['answer']
    #         )
    #
    #         return user_answer

    # class Meta:
    #     model = UserAnswer
    #     fields = ('pk', 'user', 'questionary', 'answer')

# class UserAnswerListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         answer = [Answer(**answer) for answer in validated_data]
#         return Answer.objects.bulk_create(answer)


# class UserAnswerSerializer(serializers.ModelSerializer):
#     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         list_serializer_class = UserAnswerListSerializer
#         model = Answer
#         fields = ('user', 'answer',)

# class UserAnswerListSerializer(serializers.ListSerializer):
#     @classmethod
#     def many_init(cls, *args, **kwargs):
#         # Instantiate the child serializer.
#         kwargs['child'] = cls()
#         # Instantiate the parent list serializer.
#         return UserAnswerListSerializer(*args, **kwargs)
#
#     def create(self, validated_data):
#         user_answer = [UserAnswer(**answer) for answer in validated_data]
#         print(f'<SERIALIZER>Ответы пользователя в LIST_SERIALIZER: {user_answer}')
#         return UserAnswer.objects.bulk_create(user_answer)
#
#
# class UserAnswerSerializer(serializers.ModelSerializer):
#     """ Сериализатор для модели с Ответами Пользователей """
#     user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
#     # user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # В скрытое поле помещается объект текущего пользователя
#     answer = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#
#     # def create(self, validated_data):
#     #     print(validated_data)
#     #     return UserAnswer.objects.create(**validated_data)
#
#     class Meta:
#         model = UserAnswer
#         list_serializer_class = UserAnswerListSerializer
#         fields = ('user', 'answer')

# class RandomQuestionSerializer(serializers.ModelSerializer):
#     # answer = serializers.StringRelatedField(many=True)
#     answer = AnswerSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Question
#         fields = ('questionary', 'text', 'answer')
