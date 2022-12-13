from django import forms
from django.core.exceptions import ValidationError

from bots.models import Bot


class BotPass(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('password', )
        labels = {'password': 'Пароль', }
        widgets = {
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('token', 'login', 'name')
        help_texts = {
            'login': ('то, что начинается со знака @.'
                      'Обязательно заканчивается словом bot'),
        }
        widgets = {
            'token': forms.TextInput(attrs={'class': 'form-control'}),
            'login': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_login(self):
        data = self.cleaned_data['login']
        if data[0] != '@' or data[-3:].lower() != 'bot':
            raise ValidationError(
                'Логин бота должен начинаться со знака @ '
                'и заканчиваться словом bot'
            )
        return data

    def clean_token(self):
        data = self.cleaned_data['token']
        if (':' not in data or len(data) < 45
           or not data.split(':')[0].isnumeric()):
            raise ValidationError('Не верный формат токена')
        return data


class BotFormEdit(forms.ModelForm):
    class Meta:
        model = Bot
        fields = (
            'name',
            'tz',
            'is_show_wrong_right',
            'is_show_answer',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tz': forms.Select(),
            'is_show_wrong_right': forms.CheckboxInput(),
            'is_show_answer': forms.CheckboxInput(),
        }

    def clean(self):
        is_show_wrong_right = self.cleaned_data['is_show_wrong_right']
        is_show_answer = self.cleaned_data['is_show_answer']
        if is_show_answer and not is_show_wrong_right:
            self.add_error(
                'is_show_wrong_right',
                ('При показе "Правильного ответа" необходимо включить '
                 '"Показывать Правильно/Неправильно')
            )
            raise ValidationError('')
        return self.cleaned_data


class BotSchedule(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('days', 'hours')
        help_texts = {
            'days': ('Выберите один из вариантов'),
            'hours': ('Укажите часы запуска без минут через пробел. '
                      'Например, чтобы запускать бота в 8, 14 и 20 ч, '
                      'напишите так: 8 14 20'),
        }
        widgets = {
            'days': forms.RadioSelect(),
            'hours': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_hours(self):
        data = self.cleaned_data['hours']
        hours = data.split()
        for count, hour in enumerate(hours):
            if not hour.isdigit() or int(hour) > 24:
                raise ValidationError(
                    'Должны быть только целые числа от 0 до 24 и пробел.')
            # if len(hour) == 1:
            #     hours[count] = f'0{hour}'
        return ' '.join(hours)
