from django import forms

from content.models import Category, Task


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text', 'answer', 'img')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'img': 'Загрузите изображение .jpg, .png',
        }