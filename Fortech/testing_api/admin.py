""" Настройки приложения для админки """

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

import nested_admin

from .models import Questionary, Question, Answer


#region INLINE-BLOCK
class AnswerInlineFormSet(BaseInlineFormSet):
    """ Определение FormSet инлайна ответов для вопроса """

    def clean(self):
        """ Переопределяем валидацию """
        super(AnswerInlineFormSet, self).clean()
        total, valid = 0, 0
        for form in self.forms:
            if not form.is_valid():
                return  # Есть другие ошибки

            # Форма прошла валидацию + Нет помеченных на удаление записей
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                total += 1
                valid += 1 if form.cleaned_data['is_valid'] else 0

        self.instance.__total_answer__ = total
        self.instance.__valid_answer__ = valid

        # Кастомные валидаторы:
        if self.instance.__total_answer__ is not None and self.instance.__total_answer__ < 2:
            raise ValidationError('Минимум 2 ответа на вопрос!')
        if self.instance.__valid_answer__ is not None and self.instance.__valid_answer__ < 1:
            raise ValidationError('Минимум 1 ПРАВИЛЬНЫЙ ответ на вопрос!')
        if self.instance.__valid_answer__ is not None and self.instance.__valid_answer__ == self.instance.__total_answer__:
            raise ValidationError('Все варианты ответов НЕ могут быть ПРАВИЛЬНЫМИ!')


class AnswerInlineModel(nested_admin.NestedTabularInline):
    """ Описание параметров инлайна """
    model = Answer
    formset = AnswerInlineFormSet
    # list_display = ('text', 'is_valid')
    # list_editable = ('text', 'is_valid')
    extra = 2  # Первоначальное количество записей


class QuestionInlineFormSet(BaseInlineFormSet):
    """ Определение FormSet инлайна ответов для вопроса """
    pass


class QuestionInlineModel(nested_admin.NestedTabularInline):
    model = Question
    # formset = QuestionInlineFormSet
    # fields = ('questionary', 'text')
    # list_display = ('text',)
    inlines = (AnswerInlineModel,)
    extra = 0
#endregion


@admin.register(Questionary)
class QuestionaryAdmin(nested_admin.NestedModelAdmin):
    list_display = ('pk', 'caption', 'created_at')
    list_display_links = ('pk', 'caption')
    inlines = (QuestionInlineModel,)


# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ('questionary', 'text')
#     list_display = ('text',)
#     inlines = (AnswerInlineModel,)


# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ('question', 'text', 'is_valid')
