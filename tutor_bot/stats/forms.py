from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


PERIODS = (
    ('allperiod', 'Без ограничений'),
    ('previousmonth', 'Прошлый месяц'),
    ('currentmonth', 'Текущий месяц'),
    ('previousweek', 'Прошлая неделя'),
    ('currentweek', 'Текущая неделя'),
    ('other', 'Произвольный период'),
)
YEARS = (timezone.now().year, timezone.now().year - 1)


class SelectDateForm_disabled(forms.Form):
    period = forms.ChoiceField(
        label='Выберите период',
        choices=PERIODS,
        widget=forms.Select(
            attrs={'id': 'select-date'}
        )
    )
    date_start = forms.DateField(
        label='Начало периода',
        widget=forms.SelectDateWidget(
            years=YEARS,
            attrs={
                'class': 'dateform',
                'disabled': True,
            }
        ),
        required=False
    )
    date_end = forms.DateField(
        label='Конец периода',
        widget=forms.SelectDateWidget(
            years=YEARS,
            attrs={
                'class': 'dateform',
                'disabled': True,
            }
        ),
        required=False
    )

    def clean(self):
        start = self.cleaned_data.get('date_start')
        end = self.cleaned_data.get('date_end')
        if start and end and start > end:
            self.add_error(
                'date_end',
                ('Вторая дата должна быть больше первой')
            )
            raise ValidationError('')
        if start and not end or not start and end:
            self.add_error(
                'date_end',
                ('Необходимо указать обе даты')
            )
            raise ValidationError('')
        return self.cleaned_data


class SelectDateForm(forms.Form):
    period = forms.ChoiceField(
        label='Выберите период',
        choices=PERIODS,
        widget=forms.Select(
            attrs={'id': 'select-date'}
        )
    )
    date_start = forms.DateField(
        label='Начало периода',
        widget=forms.SelectDateWidget(
            years=YEARS,
            attrs={
                'class': 'dateform',
            }
        ),
        required=False
    )
    date_end = forms.DateField(
        label='Конец периода',
        widget=forms.SelectDateWidget(
            years=YEARS,
            attrs={
                'class': 'dateform',
            }
        ),
        required=False
    )

    def clean(self):
        start = self.cleaned_data.get('date_start')
        end = self.cleaned_data.get('date_end')
        if start and end and start > end:
            self.add_error(
                'date_end',
                ('Вторая дата должна быть больше первой')
            )
            raise ValidationError('')
        if start and not end or not start and end:
            self.add_error(
                'date_end',
                ('Необходимо указать обе даты')
            )
            raise ValidationError('')
        return self.cleaned_data
