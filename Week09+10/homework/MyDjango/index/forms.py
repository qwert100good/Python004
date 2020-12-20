from django import forms
from django.forms import widgets


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名'
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        widget=forms.PasswordInput
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=12,
        required=True,
        error_messages={'required': '用户名不能为空', 'invalid': '输入数据不规范'},
    )
    pwd = forms.CharField(
        label='密码',
        min_length=8,
        required=True,
        widget=forms.PasswordInput
    )
    confirm_pwd = forms.CharField(
        label='确认密码',
        min_length=8,
        required=True,
        widget=forms.PasswordInput
    )

    def clean(self):
        if self.cleaned_data['confirm_pwd'] == self.cleaned_data['pwd']:
            print(self.cleaned_data['confirm_pwd'])
            print(self.cleaned_data['pwd'])
            return self.cleaned_data
        else:
            self.add_error('confirm_pwd', '密码不一致')
            return self.cleaned_data
