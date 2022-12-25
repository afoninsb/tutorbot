from django import forms

from content.models import Category, Task


class CategoryForm(forms.ModelForm):
    """Форма создания иредактирования категории."""
    class Meta:
        model = Category
        fields = ('name', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TaskForm(forms.ModelForm):
    """Форма создания задания."""
    class Meta:
        model = Task
        fields = ('title', 'text', 'answer', 'difficulty', 'img')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'img': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'img': 'Загрузите изображение .jpg, .png',
        }
