from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя'}),
            'email': forms.TextInput(attrs={'placeholder': 'Почта'}),
            'password': forms.TextInput(attrs={'placeholder': 'Пароль'}),
            'repeat_password': forms.TextInput(attrs={'placeholder': 'Повторите пароль'}),
        }

    def clean_repeat_password(self):
        cd = self.cleaned_data
        if cd['password'] == cd['repeat_password']:
            return cd['repeat_password']
        raise forms.ValidationError('Неправильный пароль')
